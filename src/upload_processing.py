"""Validate and process session-uploaded CRM CSV files."""

from __future__ import annotations

from io import BytesIO
from typing import BinaryIO

import pandas as pd

try:
    from .feature_engineering import build_feature_dataset
except ImportError:
    from feature_engineering import build_feature_dataset


PIPELINE_COLUMNS = {
    "opportunity_id", "sales_agent", "product", "account", "deal_stage",
    "engage_date", "close_date", "close_value",
}
BEHAVIOURAL_COLUMNS = {
    "email_history.csv": {
        "email_id", "opportunity_id", "sales_agent", "sent_at", "responded_at",
        "response_time_hours", "email_type", "response_status",
    },
    "crm_activities.csv": {
        "activity_id", "opportunity_id", "sales_agent", "activity_date",
        "activity_type", "activity_outcome",
    },
    "stage_history.csv": {
        "transition_id", "opportunity_id", "sales_agent", "from_stage", "to_stage",
        "changed_at", "days_in_previous_stage",
    },
}
BEHAVIOURAL_KEYS = {
    "email_history.csv": "email_id",
    "crm_activities.csv": "activity_id",
    "stage_history.csv": "transition_id",
}
DATE_COLUMNS = {
    "sales_pipeline.csv": ["engage_date", "close_date"],
    "email_history.csv": ["sent_at", "responded_at"],
    "crm_activities.csv": ["activity_date"],
    "stage_history.csv": ["changed_at"],
}


def _empty_frame(filename: str) -> pd.DataFrame:
    columns = PIPELINE_COLUMNS if filename == "sales_pipeline.csv" else BEHAVIOURAL_COLUMNS[filename]
    return pd.DataFrame(columns=sorted(columns))


def _read_csv(uploaded_file: BinaryIO, filename: str) -> tuple[pd.DataFrame, list[str]]:
    actual_name = getattr(uploaded_file, "name", filename)
    if actual_name.rsplit("/", 1)[-1] != filename:
        return _empty_frame(filename), [f"Expected {filename}, but received {actual_name}."]
    if not filename.lower().endswith(".csv"):
        return _empty_frame(filename), [f"{filename}: only CSV files are supported."]
    try:
        content = uploaded_file.getvalue()
        if not content.strip():
            return _empty_frame(filename), [f"{filename}: the uploaded file is empty."]
        frame = pd.read_csv(BytesIO(content))
    except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError) as error:
        return _empty_frame(filename), [f"{filename}: could not read the CSV ({error})."]
    if frame.empty:
        return frame, [f"{filename}: the uploaded dataset contains no rows."]
    return frame, []


def _standardise(frame: pd.DataFrame, filename: str) -> pd.DataFrame:
    frame = frame.copy()
    for column in frame.select_dtypes(include="object").columns:
        frame[column] = frame[column].str.strip()
    for column in DATE_COLUMNS[filename]:
        frame[column] = pd.to_datetime(frame[column], errors="coerce")
    return frame


def validate_uploaded_frames(frames: dict[str, pd.DataFrame]) -> list[str]:
    """Return user-facing validation errors without changing uploaded frames."""
    errors: list[str] = []
    pipeline = frames["sales_pipeline.csv"]
    missing = sorted(PIPELINE_COLUMNS - set(pipeline.columns))
    if missing:
        errors.append(f"sales_pipeline.csv is missing required columns: {', '.join(missing)}")
        return errors

    if pipeline.empty:
        errors.append("sales_pipeline.csv: the uploaded dataset contains no rows.")
        return errors

    required_values = ["opportunity_id", "sales_agent", "product", "deal_stage"]
    missing_values = pipeline[required_values].isna().any(axis=1).sum()
    if missing_values:
        errors.append(f"sales_pipeline.csv: {missing_values} rows are missing required values.")
    duplicate_count = int(pipeline["opportunity_id"].duplicated().sum())
    if duplicate_count:
        errors.append(f"sales_pipeline.csv: {duplicate_count} duplicate opportunity_id values found.")

    allowed_stages = {"Prospecting", "Engaging", "Won", "Lost"}
    invalid_stages = sorted(set(pipeline["deal_stage"].dropna()) - allowed_stages)
    if invalid_stages:
        errors.append(f"sales_pipeline.csv: invalid deal stages: {', '.join(invalid_stages)}")

    raw_close_values = pipeline["close_value"]
    numeric_close_values = pd.to_numeric(raw_close_values, errors="coerce")
    invalid_close_values = int((raw_close_values.notna() & numeric_close_values.isna()).sum())
    if invalid_close_values:
        errors.append(f"sales_pipeline.csv: {invalid_close_values} close_value values are not numeric.")

    standardised_pipeline = _standardise(pipeline, "sales_pipeline.csv")
    for column in DATE_COLUMNS["sales_pipeline.csv"]:
        invalid_dates = int((pipeline[column].notna() & standardised_pipeline[column].isna()).sum())
        if invalid_dates:
            errors.append(f"sales_pipeline.csv: {invalid_dates} invalid {column} values.")

    reversed_dates = int((standardised_pipeline["close_date"] < standardised_pipeline["engage_date"]).sum())
    if reversed_dates:
        errors.append(f"sales_pipeline.csv: {reversed_dates} opportunities close before they engage.")

    closed = pipeline["deal_stage"].isin(["Won", "Lost"])
    closed_missing = int(pipeline.loc[closed, ["engage_date", "close_date", "close_value"]].isna().any(axis=1).sum())
    if closed_missing:
        errors.append(f"sales_pipeline.csv: {closed_missing} closed opportunities lack required close information.")

    pipeline_ids = set(pipeline["opportunity_id"].dropna())
    for filename, frame in frames.items():
        if filename == "sales_pipeline.csv" or frame.empty:
            continue
        required = BEHAVIOURAL_COLUMNS[filename]
        missing = sorted(required - set(frame.columns))
        if missing:
            errors.append(f"{filename} is missing required columns: {', '.join(missing)}")
            continue
        key = BEHAVIOURAL_KEYS[filename]
        duplicate_count = int(frame[key].duplicated().sum())
        if duplicate_count:
            errors.append(f"{filename}: {duplicate_count} duplicate {key} values found.")
        orphan_count = int((~frame["opportunity_id"].isin(pipeline_ids)).sum())
        if orphan_count:
            errors.append(f"{filename}: {orphan_count} rows reference unknown opportunity_id values.")
        standardised = _standardise(frame, filename)
        for column in DATE_COLUMNS[filename]:
            invalid_dates = int((frame[column].notna() & standardised[column].isna()).sum())
            if invalid_dates:
                errors.append(f"{filename}: {invalid_dates} invalid {column} values.")
        numeric_column = {
            "email_history.csv": "response_time_hours",
            "stage_history.csv": "days_in_previous_stage",
        }.get(filename)
        if numeric_column:
            numeric_values = pd.to_numeric(frame[numeric_column], errors="coerce")
            invalid_numeric = int((frame[numeric_column].notna() & numeric_values.isna()).sum())
            if invalid_numeric:
                errors.append(f"{filename}: {invalid_numeric} {numeric_column} values are not numeric.")

    return errors


def process_uploaded_dataset(uploaded_files: dict[str, BinaryIO]) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    """Read, validate, standardize, and feature-engineer uploaded files in memory."""
    filenames = ["sales_pipeline.csv", *BEHAVIOURAL_COLUMNS]
    frames: dict[str, pd.DataFrame] = {}
    errors: list[str] = []
    for filename in filenames:
        if filename in uploaded_files:
            frame, file_errors = _read_csv(uploaded_files[filename], filename)
            errors.extend(file_errors)
            frames[filename] = frame
        elif filename == "sales_pipeline.csv":
            errors.append("sales_pipeline.csv must be uploaded.")
        else:
            frames[filename] = _empty_frame(filename)

    errors.extend(validate_uploaded_frames(frames))
    if errors:
        raise ValueError("\n".join(dict.fromkeys(errors)))

    standardised = {
        filename: _standardise(frame, filename)
        for filename, frame in frames.items()
    }
    standardised["sales_pipeline.csv"]["close_value"] = pd.to_numeric(
        standardised["sales_pipeline.csv"]["close_value"], errors="coerce"
    )
    datasets = {
        "pipeline": standardised["sales_pipeline.csv"],
        "emails": standardised["email_history.csv"],
        "activities": standardised["crm_activities.csv"],
        "stages": standardised["stage_history.csv"],
    }
    return build_feature_dataset(datasets), frames
