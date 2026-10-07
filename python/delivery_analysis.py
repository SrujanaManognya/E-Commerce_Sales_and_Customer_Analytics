import pandas as pd
import os

# Load Analytical Data
def load_analytical_data():
    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )
    file_path = os.path.join(
        base_dir,
        "Data",
        "processed",
        "analytical_order_level.csv"
    )
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"\nAnalytical file not found:\n{file_path}\n\n"
            "Please run feature_engineering.py first."
        )
    df = pd.read_csv(file_path)
    return df

# Delivery Overview
def delivery_overview(df):
    print("\nDelivery Overview")
    print("-" * 50)
    delivered = df[
        df["delivery_days"].notna()
    ]
    total_orders = df["order_id"].nunique()
    delivered_orders = (
        delivered["order_id"].nunique()
    )
    average_delivery = (
        delivered["delivery_days"].mean()
    )
    average_estimated = (
        delivered["estimated_delivery_days"].mean()
    )
    average_delay = (
        delivered["delivery_delay_days"].mean()
    )
    print(f"Total Orders: {total_orders:,}")
    print(f"Delivered Orders: {delivered_orders:,}")
    print(
        f"Average Delivery Time: "
        f"{average_delivery:.2f} days"
    )
    print(
        f"Average Estimated Delivery Time: "
        f"{average_estimated:.2f} days"
    )
    print(
        f"Average Delivery Delay: "
        f"{average_delay:.2f} days"
    )

# Delivery Status Analysis
def delivery_status_analysis(df):
    print("\nDelivery Status Analysis")
    print("-" * 50)
    status_counts = (
        df["delivery_status"]
        .value_counts()
    )
    print("\nDelivery Status Count:")
    print(status_counts)
    print("\nDelivery Status Percentage:")
    status_percentage = (
        df["delivery_status"]
        .value_counts(normalize=True)
        .mul(100)
        .round(2)
    )
    print(status_percentage)

# Delay Analysis
def delay_analysis(df):
    print("\nDelivery Delay Analysis")
    print("-" * 50)
    delivered = df[
        df["delivery_delay_days"].notna()
    ]
    delayed = delivered[
        delivered["delivery_delay_days"] > 0
        ]
    print(
        f"Delivered Orders: "
        f"{len(delivered):,}"
    )
    print(
        f"Delayed Orders: "
        f"{len(delayed):,}"
    )
    if len(delayed) > 0:
        print(
            f"Average Delay Among Delayed Orders: "
            f"{delayed['delivery_delay_days'].mean():.2f} days"
        )
        print(
            f"Maximum Delay: "
            f"{delayed['delivery_delay_days'].max():.2f} days"
        )
        print(
            f"Minimum Delay: "
            f"{delayed['delivery_delay_days'].min():.2f} days"
        )

# Delivery Status
def delivery_performance(df):
    print("\nDelivery Performance")
    print("-" * 50)
    delivered = df[
        df["delivery_days"].notna()
    ]
    total = len(delivered)
    if total == 0:
        print("No delivered orders available.")
        return
    early = len(
        delivered[
            delivered["delivery_delay_days"] < 0
            ]
    )
    on_time = len(
        delivered[
            delivered["delivery_delay_days"] == 0
            ]
    )
    delayed = len(
        delivered[
            delivered["delivery_delay_days"] > 0
            ]
    )
    print(
        f"Early Deliveries: "
        f"{early:,} "
        f"({early / total * 100:.2f}%)"
    )
    print(
        f"On-Time Deliveries: "
        f"{on_time:,} "
        f"({on_time / total * 100:.2f}%)"
    )
    print(
        f"Delayed Deliveries: "
        f"{delayed:,} "
        f"({delayed / total * 100:.2f}%)"
    )

# Most Delayed Orders
def most_delayed_orders(df):
    print("\nTop 10 Most Delayed Orders")
    print("-" * 50)
    columns = [
        "order_id",
        "order_status",
        "delivery_days",
        "estimated_delivery_days",
        "delivery_delay_days",
        "review_score",
        "total_order_value"
    ]
    available_columns = [
        col for col in columns
        if col in df.columns
    ]
    delayed_orders = (
        df[
            df["delivery_delay_days"] > 0
            ][available_columns]
        .sort_values(
            "delivery_delay_days",
            ascending=False
        )
        .head(10)
    )
    print(delayed_orders.to_string(index=False))

# Delivery by Customer State
def delivery_by_state(df):
    print("\nDelivery Performance by Customer State")
    print("-" * 50)
    if "customer_state" not in df.columns:
        print(
            "customer_state column not found."
        )
        return
    delivered = df[
        df["delivery_days"].notna()
    ]
    state_delivery = (
        delivered
        .groupby("customer_state")
        .agg(
            orders=(
                "order_id",
                "nunique"
            ),
            average_delivery_days=(
                "delivery_days",
                "mean"
            ),
            average_delay_days=(
                "delivery_delay_days",
                "mean"
            )
        )
        .sort_values(
            "average_delay_days",
            ascending=False
        )
        .round(2)
    )
    print(
        state_delivery.to_string()
    )

# Top States by Delivery Time
def slowest_states(df):
    print("\nSlowest Customer States")
    print("-" * 50)
    if "customer_state" not in df.columns:
        print("customer_state column not found.")
        return
    delivered = df[
        df["delivery_days"].notna()
    ]
    result = (
        delivered
        .groupby("customer_state")
        .agg(
            orders=(
                "order_id",
                "nunique"
            ),
            average_delivery_days=(
                "delivery_days",
                "mean"
            )
        )
        .sort_values(
            "average_delivery_days",
            ascending=False
        )
        .head(10)
        .round(2)
    )
    print(result.to_string())

# Delivery VS Review Score
def delivery_vs_reviews(df):
    print("\nDelivery Time VS Review Score")
    print("-" * 50)
    delivered = df[
        df["delivery_days"].notna()
    ]
    result = (
        delivered
        .groupby("review_score")
        .agg(
            orders=(
                "order_id",
                "nunique"
            ),
            average_delivery_days=(
                "delivery_days",
                "mean"
            ),
            average_delay_days=(
                "delivery_delay_days",
                "mean"
            ),
            average_order_value=(
                "total_order_value",
                "mean"
            )
        )
        .round(2)
    )
    print(result.to_string())

# Delay VS Order Value
def delay_vs_order_value(df):
    print("\nDelivery Delay VS Order Value")
    print("-" * 50)
    delivered = df[
        df["delivery_delay_days"].notna()
    ].copy()
    if delivered.empty:
        print("No delivery data available.")
        return
    try:
        delivered["order_value_group"] = pd.qcut(
            delivered["total_order_value"],
            q=4,
            duplicates="drop"
        )
        result = (
            delivered
            .groupby(
                "order_value_group",
                observed=True
            )
            .agg(
                orders=(
                    "order_id",
                    "nunique"
                ),
                average_order_value=(
                    "total_order_value",
                    "mean"
                ),
                average_delay_days=(
                    "delivery_delay_days",
                    "mean"
                )
            )
            .round(2)
        )
        print(result.to_string())
    except ValueError:
        print(
            "Unable to create order-value groups."
        )

# Delivery by Order Status
def delivery_by_order_status(df):
    print("\nDelivery Performance by Order Status")
    print("-" * 50)
    result = (
        df
        .groupby("order_status")
        .agg(
            orders=(
                "order_id",
                "nunique"
            ),
            average_delivery_days=(
                "delivery_days",
                "mean"
            ),
            average_delay_days=(
                "delivery_delay_days",
                "mean"
            )
        )
        .round(2)
    )
    print(result.to_string())

# Delivery Summary
def delivery_summary(df):
    print("\nDelivery Summary")
    print("-" * 50)
    delivered = df[
        df["delivery_days"].notna()
    ]
    total = len(delivered)
    if total == 0:
        print(
            "No delivered orders available."
        )
        return
    early = len(
        delivered[
            delivered["delivery_delay_days"] < 0
            ]
    )
    on_time = len(
        delivered[
            delivered["delivery_delay_days"] == 0
            ]
    )
    delayed = len(
        delivered[
            delivered["delivery_delay_days"] > 0
            ]
    )
    print(
        f"Total Delivered: {total:,}"
    )
    print(
        f"Early: {early:,} "
        f"({early / total * 100:.2f}%)"
    )
    print(
        f"On Time: {on_time:,} "
        f"({on_time / total * 100:.2f}%)"
    )
    print(
        f"Delayed: {delayed:,} "
        f"({delayed / total * 100:.2f}%)"
    )

# Main
if __name__ == "__main__":

    print("\nLoading analytical dataset...")

    df = load_analytical_data()

    print(
        f"Loaded {len(df):,} order records."
    )

    delivery_overview(df)

    delivery_status_analysis(df)

    delay_analysis(df)

    delivery_performance(df)

    most_delayed_orders(df)

    delivery_by_state(df)

    slowest_states(df)

    delivery_vs_reviews(df)

    delay_vs_order_value(df)

    delivery_by_order_status(df)

    delivery_summary(df)

    print("\n" + "=" * 60)
    print("DELIVERY ANALYSIS COMPLETED SUCCESSFULLY")
    print("=" * 60)