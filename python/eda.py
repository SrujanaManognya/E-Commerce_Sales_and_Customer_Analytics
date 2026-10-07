import pandas as pd
import os


# ==================================================
# LOAD ANALYTICAL DATA
# ==================================================

def load_analytical_data():

    file_path = "Data/processed/analytical_order_level.csv"

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"File not found: {file_path}\n"
            "Run feature_engineering.py first."
        )

    df = pd.read_csv(file_path)

    return df


# ==================================================
# DATA OVERVIEW
# ==================================================

def data_overview(df):

    print("\n" + "=" * 60)
    print("DATA OVERVIEW")
    print("=" * 60)

    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(
        df.isnull()
        .sum()
        .sort_values(ascending=False)
        .head(15)
    )


# ==================================================
# OVERALL BUSINESS KPIs
# ==================================================

def overall_kpis(df):

    print("\n" + "=" * 60)
    print("OVERALL BUSINESS KPIs")
    print("=" * 60)

    total_orders = df["order_id"].nunique()

    total_revenue = df["order_revenue"].sum()

    total_freight = df["freight_cost"].sum()

    total_order_value = df["total_order_value"].sum()

    average_order_value = (
        df["total_order_value"].mean()
    )

    average_review = (
        df["review_score"].mean()
    )

    print(f"Total Orders: {total_orders:,}")
    print(f"Total Product Revenue: {total_revenue:,.2f}")
    print(f"Total Freight Cost: {total_freight:,.2f}")
    print(f"Total Order Value: {total_order_value:,.2f}")
    print(f"Average Order Value: {average_order_value:,.2f}")
    print(f"Average Review Score: {average_review:.2f}")


# ==================================================
# ORDER STATUS ANALYSIS
# ==================================================

def order_status_analysis(df):

    print("\n" + "=" * 60)
    print("ORDER STATUS ANALYSIS")
    print("=" * 60)

    status_counts = (
        df["order_status"]
        .value_counts()
    )

    print("\nOrder Count:")
    print(status_counts)

    print("\nOrder Percentage:")

    status_percentage = (
        df["order_status"]
        .value_counts(normalize=True)
        .mul(100)
        .round(2)
    )

    print(status_percentage)


# ==================================================
# SALES ANALYSIS
# ==================================================

def sales_analysis(df):

    print("\n" + "=" * 60)
    print("SALES ANALYSIS")
    print("=" * 60)

    print("\nTop Orders by Total Value:")

    top_orders = (
        df[
            [
                "order_id",
                "order_revenue",
                "freight_cost",
                "total_order_value"
            ]
        ]
        .sort_values(
            "total_order_value",
            ascending=False
        )
        .head(10)
    )

    print(top_orders)


# ==================================================
# CUSTOMER ANALYSIS
# ==================================================

def customer_analysis(df):

    print("\n" + "=" * 60)
    print("CUSTOMER ANALYSIS")
    print("=" * 60)

    total_customers = (
        df["customer_unique_id"]
        .nunique()
    )

    print(
        f"Unique Customers: {total_customers:,}"
    )

    orders_per_customer = (
        df.groupby("customer_unique_id")
        .agg(
            total_orders=("order_id", "nunique"),
            total_spending=(
                "total_order_value",
                "sum"
            )
        )
        .sort_values(
            "total_orders",
            ascending=False
        )
    )

    print("\nTop Customers by Number of Orders:")
    print(
        orders_per_customer.head(10)
    )

    print("\nTop Customers by Spending:")
    print(
        orders_per_customer
        .sort_values(
            "total_spending",
            ascending=False
        )
        .head(10)
    )


# ==================================================
# PRODUCT CATEGORY ANALYSIS
# ==================================================

def product_category_analysis(df):

    print("\n" + "=" * 60)
    print("PRODUCT CATEGORY ANALYSIS")
    print("=" * 60)

    category_sales = (
        df[
            ["product_categories", "order_revenue"]
        ]
        .dropna()
    )

    print(
        "\nTop Product Categories "
        "by Revenue:"
    )

    print(
        category_sales
        .sort_values(
            "order_revenue",
            ascending=False
        )
        .head(20)
    )


# ==================================================
# PAYMENT ANALYSIS
# ==================================================

def payment_analysis(df):

    print("\n" + "=" * 60)
    print("PAYMENT ANALYSIS")
    print("=" * 60)

    if "payment_type" in df.columns:

        payment_counts = (
            df["payment_type"]
            .value_counts()
        )

        print("\nPayment Types:")
        print(payment_counts)

    print("\nPayment Value:")
    print(
        df["payment_value"]
        .describe()
    )

    print("\nPayment Installments:")
    print(
        df["payment_installments"]
        .describe()
    )


# ==================================================
# REVIEW ANALYSIS
# ==================================================

def review_analysis(df):

    print("\n" + "=" * 60)
    print("REVIEW ANALYSIS")
    print("=" * 60)

    print("\nReview Score Distribution:")

    print(
        df["review_score"]
        .value_counts()
        .sort_index()
    )

    print("\nAverage Review Score:")

    print(
        df["review_score"]
        .mean()
    )

    print("\nAverage Order Value by Review Score:")

    review_value = (
        df.groupby("review_score")
        ["total_order_value"]
        .mean()
        .round(2)
    )

    print(review_value)


# ==================================================
# STATE ANALYSIS
# ==================================================

def state_analysis(df):

    print("\n" + "=" * 60)
    print("CUSTOMER STATE ANALYSIS")
    print("=" * 60)

    if "customer_state" not in df.columns:
        print("customer_state column not found.")
        return

    state_analysis_df = (
        df.groupby("customer_state")
        .agg(
            orders=("order_id", "nunique"),
            revenue=(
                "total_order_value",
                "sum"
            ),
            average_order_value=(
                "total_order_value",
                "mean"
            )
        )
        .sort_values(
            "revenue",
            ascending=False
        )
    )

    print(
        state_analysis_df.head(15)
    )


# ==================================================
# DELIVERY STATUS OVERVIEW
# ==================================================

def delivery_status_analysis(df):

    print("\n" + "=" * 60)
    print("DELIVERY STATUS OVERVIEW")
    print("=" * 60)

    if "delivery_status" not in df.columns:
        print("delivery_status column not found.")
        return

    print(
        df["delivery_status"]
        .value_counts()
    )

    print("\nDelivery Status Percentage:")

    print(
        df["delivery_status"]
        .value_counts(normalize=True)
        .mul(100)
        .round(2)
    )


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    print("\nLoading analytical dataset...")

    df = load_analytical_data()

    print("Analytical dataset loaded successfully.")

    data_overview(df)

    overall_kpis(df)

    order_status_analysis(df)

    sales_analysis(df)

    customer_analysis(df)

    product_category_analysis(df)

    payment_analysis(df)

    review_analysis(df)

    state_analysis(df)

    delivery_status_analysis(df)

    print("\n" + "=" * 60)
    print("EDA COMPLETED SUCCESSFULLY")
    print("=" * 60)