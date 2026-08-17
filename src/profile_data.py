import pandas as pd

pipeline = pd.read_csv("data/raw/sales_pipeline.csv")

print("Dataset shape:")
print(pipeline.shape)

print("\nColumns:")
print(pipeline.columns.tolist())

print("\nFirst 5 rows:")
print(pipeline.head())

print("\nData types:")
print(pipeline.dtypes)

print("\nMissing values:")
print(pipeline.isnull().sum())

print("\nDeal stages:")
print(pipeline["deal_stage"].value_counts())

# Step 2

dictionary = pd.read_csv("data/raw/data_dictionary.csv")

print("\nData Dictionary:")
print(dictionary.to_string(index=False))

# Are missing close dates and values expected because the deals haven't closed? we'll examine whether the missing values are actually associated with open deals.

print("\nDeal stage vs missing close date:")

print(
    pipeline.groupby("deal_stage")["close_date"]
    .apply(lambda x: x.isna().sum())
)

# 

print("\nDeal stage vs missing close value:")

print(
    pipeline.groupby("deal_stage")["close_value"]
    .apply(lambda x: x.isna().sum())
)

# Now we'll know whether missing engagement dates are concentrated in particular stages.

print("\nDeal stage vs missing engage date:")

print(
    pipeline.groupby("deal_stage")["engage_date"]
    .apply(lambda x: x.isna().sum())
)

# We also need:
# deal duration distribution
# average/median deal value
# sales-agent performance
# product distribution
# account relationships
# date range

# This will help us create realistic synthetic behaviour based on the actual datase

# Convert dates
pipeline["engage_date"] = pd.to_datetime(pipeline["engage_date"])
pipeline["close_date"] = pd.to_datetime(pipeline["close_date"])

# Closed deals only
closed_deals = pipeline[pipeline["deal_stage"].isin(["Won", "Lost"])].copy()

# Deal duration
closed_deals["deal_duration_days"] = (
    closed_deals["close_date"] - closed_deals["engage_date"]
).dt.days

print("\nClosed deals:")
print(len(closed_deals))

print("\nWin rate among closed deals:")
print(
    (closed_deals["deal_stage"] == "Won").mean() * 100
)

print("\nDeal duration statistics:")
print(
    closed_deals["deal_duration_days"].describe()
)

print("\nClose value statistics:")
print(
    closed_deals["close_value"].describe()
)

print("\nDeals by sales agent:")
print(
    pipeline["sales_agent"].value_counts().head(10)
)

print("\nDeals by product:")
print(
    pipeline["product"].value_counts()
)