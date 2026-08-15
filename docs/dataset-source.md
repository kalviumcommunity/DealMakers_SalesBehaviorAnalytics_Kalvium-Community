# Dataset Source

## Source

Public Kaggle CRM Sales Opportunities dataset.

Dataset:
CRM Sales Opportunities

Source:
Kaggle

## Files

The dataset contains:

- `accounts.csv`
- `data_dictionary.csv`
- `products.csv`
- `sales_pipeline.csv`
- `sales_teams.csv`

## Primary Dataset

Our main analysis table is:

`sales_pipeline.csv`

It contains 8,800 sales opportunities and the following fields:

- `opportunity_id`
- `sales_agent`
- `product`
- `account`
- `deal_stage`
- `engage_date`
- `close_date`
- `close_value`

## Supporting Tables

`accounts.csv`
- Company information

`products.csv`
- Product information

`sales_teams.csv`
- Sales agent and team information

`data_dictionary.csv`
- Field descriptions and business definitions

## Relevance to Team 05

The dataset provides the foundation for analysing sales opportunities,
deal stages, sales agents, products, engagement dates, closing dates,
and deal values.

However, it does not contain detailed behavioural records such as
email response history, CRM activities, or historical stage
transitions.

These behavioural datasets may therefore be simulated and linked to
the real opportunities using `opportunity_id`, with all simulation
assumptions documented.