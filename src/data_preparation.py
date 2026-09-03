"""Prepare and validate the CRM datasets before feature engineering.

The source CSV files deliberately contain some missing values.  This module
standardises fields without inventing values, records data-quality findings,
and writes clean copies for downstream analytical steps.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


RAW_DATA = Path("data/raw")
OUTPUT_DATA = Path("data/processed/cleaned")
REPORT_PATH = Path("data/processed/data_quality_report.json")

DATASETS = {
    "pipeline": {
        "file": "sales_pipeline.csv",
        "required": {
            "opportunity_id", "sales_agent", "product", "account", "deal_stage",
            "engage_date", "close_date", "close_value",
        },
        "date_columns": ["engage_date", "close_date"],
    },
    "emails": {
        "file": "email_history.csv",
        "required": {
            "email_id", "opportunity_id", "sales_agent", "sent_at", "responded_at",
            "response_time_hours", "email_type", "response_status",
        },
        "date_columns": ["sent_at", "responded_at"],
    },
    "activities": {
        "file": "crm_activities.csv",
        "required": {
            "activity_id", "opportunity_id", "sales_agent", "activity_date",
            "activity_type", "activity_outcome",
        },
        "date_columns": ["activity_date"],
    },
    "stages": {
        "file": "stage_history.csv",
        "required": {
            "transition_id", "opportunity_id", "sales_agent", "from_stage", "to_stage",
            "changed_at", "days_in_previous_stage",
        },
        "date_columns": ["changed_at"],
    },
}


def load_and_standardise(raw_data: Path = RAW_DATA) -> dict[str, pd.DataFrame]:
    """Load raw CSVs, trim text fields, and safely parse date fields."""
    datasets: dict[str, pd.DataFrame] = {}

    for name, config in DATASETS.items():
        path = raw_data / config["file"]
        frame = pd.read_csv(path)

        missing_columns = config["required"] - set(frame.columns)
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"{path} is missing required columns: {missing}")

        for column in frame.select_dtypes(include="object").columns:
            frame[column] = frame[column].str.strip()

        for column in config["date_columns"]:
            frame[column] = pd.to_datetime(frame[column], errors="coerce")

        datasets[name] = frame

    return datasets


def _finding(name: str, status: str, detail: str) -> dict[str, str]:
    return {"check": name, "status": status, "detail": detail}


def validate_datasets(datasets: dict[str, pd.DataFrame]) -> list[dict[str, str]]:
    """Return explicit pass/warning/fail checks for analytical data quality."""
    pipeline = datasets["pipeline"]
    emails = datasets["emails"]
    activities = datasets["activities"]
    stages = datasets["stages"]
    findings: list[dict[str, str]] = []

    primary_keys = {
        "pipeline": "opportunity_id",
        "emails": "email_id",
        "activities": "activity_id",
        "stages": "transition_id",
    }
    for dataset_name, key in primary_keys.items():
        duplicate_count = int(datasets[dataset_name][key].duplicated().sum())
        findings.append(_finding(
            f"unique_{key}",
            "pass" if duplicate_count == 0 else "fail",
            f"{duplicate_count} duplicate values in {dataset_name}",
        ))

    allowed_stages = {"Prospecting", "Engaging", "Won", "Lost"}
    unexpected_stages = sorted(set(pipeline["deal_stage"].dropna()) - allowed_stages)
    findings.append(_finding(
        "valid_deal_stages",
        "pass" if not unexpected_stages else "fail",
        "All deal stages are recognised." if not unexpected_stages else
        f"Unexpected stages: {', '.join(unexpected_stages)}",
    ))

    closed = pipeline["deal_stage"].isin(["Won", "Lost"])
    closed_missing = int(pipeline.loc[closed, ["engage_date", "close_date", "close_value"]].isna().any(axis=1).sum())
    findings.append(_finding(
        "closed_deal_completeness",
        "pass" if closed_missing == 0 else "fail",
        f"{closed_missing} closed opportunities lack an engagement date, close date, or close value.",
    ))

    open_with_close_data = int(pipeline.loc[~closed, ["close_date", "close_value"]].notna().any(axis=1).sum())
    findings.append(_finding(
        "open_deal_close_fields",
        "pass" if open_with_close_data == 0 else "warning",
        f"{open_with_close_data} open opportunities contain a close date or close value.",
    ))

    invalid_duration = int((pipeline["close_date"] < pipeline["engage_date"]).sum())
    findings.append(_finding(
        "chronological_pipeline_dates",
        "pass" if invalid_duration == 0 else "fail",
        f"{invalid_duration} opportunities close before they engage.",
    ))

    response_mismatch = int(((emails["response_status"] == "Responded") & emails["responded_at"].isna()).sum())
    response_mismatch += int(((emails["response_status"] == "Responded") & emails["response_time_hours"].isna()).sum())
    findings.append(_finding(
        "responded_email_completeness",
        "pass" if response_mismatch == 0 else "fail",
        f"{response_mismatch} required response values are missing for responded emails.",
    ))

    invalid_email_dates = int((emails["responded_at"] < emails["sent_at"]).sum())
    findings.append(_finding(
        "chronological_email_dates",
        "pass" if invalid_email_dates == 0 else "fail",
        f"{invalid_email_dates} emails have a response before the send time.",
    ))

    pipeline_ids = set(pipeline["opportunity_id"])
    for dataset_name, frame in {"emails": emails, "activities": activities, "stages": stages}.items():
        orphan_count = int((~frame["opportunity_id"].isin(pipeline_ids)).sum())
        findings.append(_finding(
            f"{dataset_name}_opportunity_relationship",
            "pass" if orphan_count == 0 else "fail",
            f"{orphan_count} {dataset_name} rows do not match a pipeline opportunity.",
        ))

    activity_before_engagement = activities.merge(
        pipeline[["opportunity_id", "engage_date"]], on="opportunity_id", how="left"
    )
    invalid_activity_dates = int((activity_before_engagement["activity_date"] < activity_before_engagement["engage_date"]).sum())
    findings.append(_finding(
        "chronological_activity_dates",
        "pass" if invalid_activity_dates == 0 else "warning",
        f"{invalid_activity_dates} activities occur before their opportunity engagement date.",
    ))

    return findings


def build_report(datasets: dict[str, pd.DataFrame], findings: list[dict[str, str]]) -> dict:
    return {
        "dataset_summary": {
            name: {
                "rows": len(frame),
                "columns": len(frame.columns),
                "missing_values": {column: int(value) for column, value in frame.isna().sum().items()},
            }
            for name, frame in datasets.items()
        },
        "findings": findings,
        "summary": {
            "passed": sum(item["status"] == "pass" for item in findings),
            "warnings": sum(item["status"] == "warning" for item in findings),
            "failed": sum(item["status"] == "fail" for item in findings),
        },
    }


def write_cleaned_data(datasets: dict[str, pd.DataFrame], output_data: Path = OUTPUT_DATA) -> None:
    output_data.mkdir(parents=True, exist_ok=True)
    for name, frame in datasets.items():
        frame.to_csv(output_data / DATASETS[name]["file"], index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare and validate DealMakers source data.")
    parser.add_argument("--check-only", action="store_true", help="Validate data without writing cleaned CSV files.")
    args = parser.parse_args()

    datasets = load_and_standardise()
    findings = validate_datasets(datasets)
    report = build_report(datasets, findings)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    if not args.check_only:
        write_cleaned_data(datasets)

    for item in findings:
        print(f"[{item['status'].upper()}] {item['check']}: {item['detail']}")
    print(f"\nQuality report: {REPORT_PATH}")
    if not args.check_only:
        print(f"Cleaned data: {OUTPUT_DATA}")

    if report["summary"]["failed"]:
        raise SystemExit("Data quality validation failed. See the report for details.")


if __name__ == "__main__":
    main()
