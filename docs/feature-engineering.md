# Behavioural Feature Engineering

## Objective

Create an opportunity-level analytical dataset by combining the original sales pipeline with simulated behavioural data.

## Source datasets

- sales_pipeline.csv
- email_history.csv
- crm_activities.csv
- stage_history.csv

## Behavioural features

### Email features

- email_count
- response_rate
- avg_response_hours
- median_response_hours

### CRM activity features

- activity_count
- unique_activity_types

### Stage features

- stage_transition_count
- total_stage_days
- avg_stage_days

### Pipeline features

- deal_duration_days
- deal_stage
- close_value
- sales_agent
- product
- account

## Output

The resulting dataset is:

data/processed/opportunity_features.csv

Each row represents one sales opportunity.