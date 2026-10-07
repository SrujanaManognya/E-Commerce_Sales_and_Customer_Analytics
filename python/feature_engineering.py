import pandas as pd
import data_cleaning

# Delivery Features
def create_delivery_features(orders):
    orders = orders.copy()

    orders["delivery_days"] = (
                                      orders["order_delivered_customer_date"]
                                      - orders["order_purchase_timestamp"]
                              ).dt.total_seconds() / 86400

    orders["estimated_delivery_days"] = (
                                                orders["order_estimated_delivery_date"]
                                                - orders["order_purchase_timestamp"]
                                        ).dt.total_seconds() / 86400

    orders["delivery_delay_days"] = (
                                            orders["order_delivered_customer_date"]
                                            - orders["order_estimated_delivery_date"]
                                    ).dt.total_seconds() / 86400

    return orders

# Delivery Status
def create_delivery_status(orders):
    orders = orders.copy()

    orders["delivery_status"] = "Not Delivered"

    delivered = orders["delivery_days"].notna()

    orders.loc[
        delivered & (orders["delivery_delay_days"] < 0),
        "delivery_status"
    ] = "Early"

    orders.loc[
        delivered & (orders["delivery_delay_days"] == 0),
        "delivery_status"
    ] = "On Time"

    orders.loc[
        delivered & (orders["delivery_delay_days"] > 0),
        "delivery_status"
    ] = "Delayed"

    return orders

# Order Financials
def create_order_financials(order_items):

    financials = (
        order_items
        .groupby("order_id")
        .agg(
            order_revenue=("price", "sum"),
            freight_cost=("freight_value", "sum"),
            item_count=("order_item_id", "count")
        )
        .reset_index()
    )

    financials["total_order_value"] = (
            financials["order_revenue"]
            + financials["freight_cost"]
    )

    return financials

# Review Summary
def create_review_summary(reviews):

    review_summary = (
        reviews
        .groupby("order_id")
        .agg(
            review_score=("review_score", "mean")
        )
        .reset_index()
    )

    return review_summary

# Payment Summary
def create_payment_summary(payments):

    payment_summary = (
        payments
        .groupby("order_id")
        .agg(
            payment_value=("payment_value", "sum"),
            payment_installments=("payment_installments", "max")
        )
        .reset_index()
    )

    return payment_summary

# Product Summary
def create_product_summary(order_items, products):

    items_products = order_items.merge(
        products[
            ["product_id", "product_category"]
        ],
        on="product_id",
        how="left"
    )
    product_summary = (
        items_products
        .groupby("order_id")
        .agg(
            unique_products=("product_id", "nunique"),
            product_categories=(
                "product_category",
                lambda x: ", ".join(
                    x.dropna().unique()
                )
            )
        )
        .reset_index()
    )
    return product_summary

# Analytical Order-Level Table
def create_analytical_table(
        orders,
        customers,
        financials,
        payment_summary,
        review_summary,
        product_summary
):

    df = orders.merge(
        customers,
        on="customer_id",
        how="left"
    )

    df = df.merge(
        financials,
        on="order_id",
        how="left"
    )

    df = df.merge(
        payment_summary,
        on="order_id",
        how="left"
    )

    df = df.merge(
        review_summary,
        on="order_id",
        how="left"
    )

    df = df.merge(
        product_summary,
        on="order_id",
        how="left"
    )

    return df


# MAIN EXECUTION

if __name__ == "__main__":

    print("\nLoading datasets...")
    datasets = data_cleaning.load_data()

    # Get individual DataFrames from dictionary
    orders = datasets["orders"]
    order_items = datasets["order_items"]
    payments = datasets["payments"]
    reviews = datasets["reviews"]
    products = datasets["products"]
    customers = datasets["customers"]
    sellers = datasets["sellers"]
    translation = datasets["translation"]
    geolocation = datasets["geolocation"]

    print("Datasets loaded successfully.")

    # Timestamp Conversion
    data_cleaning.timestamp_conversion(datasets)

    # Translate Product Categories
    datasets["products"] = data_cleaning.translate_categories(
        datasets["products"],
        datasets["translation"]
    )

    products = datasets["products"]

    # Order Status Flags
    orders = data_cleaning.create_order_status_flags(
        orders
    )

    # Delivery Features
    orders = create_delivery_features(orders)

    # Delivery Status
    orders = create_delivery_status(orders)

    # Financial Summary
    financials = create_order_financials(
        order_items
    )

    # Review Summary
    review_summary = create_review_summary(
        reviews
    )

    # Payment Summary
    payment_summary = create_payment_summary(
        payments
    )

    # Product Summary
    product_summary = create_product_summary(
        order_items,
        products
    )

    # Create Analytical Table
    analytical_df = create_analytical_table(
        orders,
        customers,
        financials,
        payment_summary,
        review_summary,
        product_summary
    )

    # Validation
    print("\n")
    print("=" * 60)
    print("ANALYTICAL ORDER-LEVEL TABLE")
    print("=" * 60)

    print("\nRows:", analytical_df.shape[0])

    print(
        "Unique Orders:",
        analytical_df["order_id"].nunique()
    )

    print(
        "Duplicate Order IDs:",
        analytical_df["order_id"].duplicated().sum()
    )

    print("\nColumns:")
    for column in analytical_df.columns:
        print("-", column)

    print("\nFirst 5 Rows:")
    print(analytical_df.head())

    # Missing Values in Analytical Table
    print("\nMissing Values:")
    print(
        analytical_df.isnull()
        .sum()
        .sort_values(ascending=False)
        .head(15)
    )

    # Delivery Status Summary
    print("\nDelivery Status:")
    print(
        analytical_df["delivery_status"]
        .value_counts()
    )

    # Export
    output_path = (
        "Data/processed/analytical_order_level.csv"
    )

    analytical_df.to_csv(
        output_path,
        index=False
    )

    print("\n" + "=" * 60)
    print("SUCCESS")
    print("=" * 60)
    print(
        f"Analytical table exported to: {output_path}"
    )