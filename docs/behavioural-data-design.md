# Behavioural Data Design

## 1. Project Context

Team 05 is building a sales behaviour analytics product.

The problem statement is:

> A B2B sales organization maintains CRM updates, email response history, and deal-stage transitions, but sales coaching remains intuition-driven because no behavioural analysis identifies patterns linked to faster deal closures.

The core analytical question is:

> Which sales behaviours are associated with faster deal closures and better deal outcomes?

---

## 2. Existing Source Dataset

The public CRM dataset provides opportunity-level sales information.

The main sales pipeline fields are:

- opportunity_id
- sales_agent
- product
- account
- deal_stage
- engage_date
- close_date
- close_value

The dataset contains the following pipeline stages:

- Prospecting
- Engaging
- Won
- Lost

The `opportunity_id` will be the primary link between the existing sales data and the synthetic behavioural data.

---

## 3. Why Synthetic Data Is Required

The public dataset does not contain detailed behavioural event history.

The project requires analysis of:

- email response behaviour
- CRM activities
- deal-stage transitions

Therefore, synthetic behavioural datasets will be generated and linked to the real opportunity records.

The original source dataset will remain unchanged.

Synthetic data will be clearly documented as simulated data.

---

# 4. Email History

File:

`data/raw/email_history.csv`

### Fields

| Field | Description |
|---|---|
| email_id | Unique identifier for an email event |
| opportunity_id | Related sales opportunity |
| sales_agent | Sales agent associated with the opportunity |
| sent_at | Date and time the email was sent |
| responded_at | Date and time of customer response |
| response_time_hours | Time between email and response |
| email_type | Type of sales email |
| response_status | Whether the customer responded |

### Example email types

- Introduction
- Follow-up
- Proposal
- Product information
- Negotiation
- Closing follow-up

### Purpose

Email history will allow analysis of:

- response rate
- average response time
- number of follow-ups
- email activity per opportunity
- relationship between response behaviour and deal outcomes

---

# 5. CRM Activities

File:

`data/raw/crm_activities.csv`

### Fields

| Field | Description |
|---|---|
| activity_id | Unique identifier for the activity |
| opportunity_id | Related sales opportunity |
| sales_agent | Sales agent associated with the opportunity |
| activity_date | Date and time of activity |
| activity_type | Type of CRM activity |
| activity_outcome | Result of the activity |

### Example activity types

- Call
- Email
- Meeting
- Demo
- Follow-up

### Example outcomes

- Connected
- No answer
- Completed
- Rescheduled
- Interested
- Not interested
- Responded

### Purpose

CRM activity data will allow analysis of:

- activity frequency
- activities per opportunity
- activity types
- activity patterns of successful deals
- relationship between sales activity and deal duration

---

# 6. Stage History

File:

`data/raw/stage_history.csv`

### Fields

| Field | Description |
|---|---|
| transition_id | Unique identifier for the transition |
| opportunity_id | Related sales opportunity |
| from_stage | Previous pipeline stage |
| to_stage | New pipeline stage |
| changed_at | Date and time of transition |
| days_in_previous_stage | Duration spent in the previous stage |

### Expected stage flow

Prospecting → Engaging → Won

or

Prospecting → Engaging → Lost

### Purpose

Stage history will allow analysis of:

- time spent in each stage
- stage conversion rates
- stage drop-offs
- deals that remain longer in a stage
- relationship between stage progression and final outcomes

---

# 7. Relationship Between the Datasets

The datasets will be connected using `opportunity_id`.

```text
sales_pipeline
      |
      | opportunity_id
      |
      +------------------+
      |                  |
      v                  v
email_history      crm_activities
      |
      |
      v
stage_history