import pandas as pd

# Loading data
def load_data():
    customers = pd.read_csv("Data/raw/olist_customers_dataset.csv")
    orders = pd.read_csv("Data/raw/olist_orders_dataset.csv")
    order_items = pd.read_csv("Data/raw/olist_order_items_dataset.csv")
    payments = pd.read_csv("Data/raw/olist_order_payments_dataset.csv")
    reviews = pd.read_csv("Data/raw/olist_order_reviews_dataset.csv")
    products = pd.read_csv("Data/raw/olist_products_dataset.csv")
    sellers = pd.read_csv("Data/raw/olist_sellers_dataset.csv")
    geolocation = pd.read_csv("Data/raw/olist_geolocation_dataset.csv")
    translation = pd.read_csv("Data/raw/product_category_name_translation.csv")

    return {
        "customers": customers,
        "orders": orders,
        "order_items": order_items,
        "payments": payments,
        "reviews": reviews,
        "products": products,
        "sellers": sellers,
        "translation": translation,
        "geolocation": geolocation
    }


# Shape & Datatypes
def inspect_data(datasets):
    for name, df in datasets.items():
        print("\n" + "=" * 50)
        print(name.upper())
        print("=" * 50)
        print("Shape:", df.shape)
        print("\nData Types:")
        print(df.dtypes)
        print("\nFirst 5 rows:")
        print(df.head())

# Duplicate IDs
def check_duplicates(datasets):
    print("\nDuplicate Check")
    print("-" * 50)
    checks = {
        "orders": ["order_id"],
        "customers": ["customer_id"],
        "products": ["product_id"],
        "sellers": ["seller_id"],
        "reviews": ["review_id"]
    }
    for table, columns in checks.items():
        df = datasets[table]
        duplicates = df.duplicated(subset=columns).sum()
        print(f"{table}: {duplicates} duplicate IDs")
    order_items = datasets["order_items"]
    duplicates = order_items.duplicated(subset=["order_id", "order_item_id"]).sum()
    print(
        f"order_items: {duplicates} duplicate "
        f"(order_id + order_item_id)"
    )

# Missing Values
def check_missing_values(datasets):
    print("\nMissing Value Check")
    print("-" * 50)
    for name, df in datasets.items():
        print(f"\n{name}")
        missing = df.isnull().sum()
        missing = missing[missing > 0].sort_values(ascending=False)
        print(missing)

# Primary/Foreign Keys
def check_relationships(
        orders,
        order_items,
        payments,
        reviews,
        products,
        customers,
        sellers
):
    print("\nPrimary Key Validation")
    print("-" * 50)
    pk_check = [
        (orders, "order_id", "orders"),
        (products, "product_id", "products"),
        (customers, "customer_id", "customers"),
        (sellers, "seller_id", "sellers"),
        (reviews, "review_id", "reviews")
    ]
    for df, pk_col, name in pk_check:
        if pk_col in df.columns:
            is_unique = df[pk_col].is_unique
            no_nulls = df[pk_col].notnull().all()
            print(
                f"{name} → {pk_col}: "
                f"Valid PK? {is_unique and no_nulls} "
                f"(Unique: {is_unique}, "
                f"No Nulls: {no_nulls})"
            )
        else:
            print(
                f"{name} → column "
                f"'{pk_col}' not found!"
            )
    print("\nForeign Key Validation")
    print("-" * 50)
    print(
        "order_items → orders:",
        order_items["order_id"]
        .isin(orders["order_id"])
        .all()
    )
    print(
        "order_items → products:",
        order_items["product_id"]
        .isin(products["product_id"])
        .all()
    )
    print(
        "order_items → sellers:",
        order_items["seller_id"]
        .isin(sellers["seller_id"])
        .all()
    )
    print(
        "payments → orders:",
        payments["order_id"]
        .isin(orders["order_id"])
        .all()
    )
    print(
        "reviews → orders:",
        reviews["order_id"]
        .isin(orders["order_id"])
        .all()
    )

# Timestamp Conversion
def timestamp_conversion(datasets):
    print("\nTimestamps Conversion")
    print("-" * 50)
    timestamp_columns = [
        "shipping_limit_date",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
    for name, df in datasets.items():
        df.columns = df.columns.str.strip()
        for col in timestamp_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
                print(
                    f"{name} → {col}: "
                    f"Converted Successfully"
                )
                print(f"Data Type: {df[col].dtype}\n")

# Translation
def translate_categories(
        products,
        translation
):
    print("\nTranslation")
    print("-"*50)
    products = products.merge(
        translation,
        on = "product_category_name",
        how = "left"
    )
    products["product_category"] = (
        products["product_category_name_english"].fillna(
            products["product_category_name"]
        )
    )
    return products

# Order Status
def analyze_order_status(orders):
    print("\nOrder Status")
    print("-"*50)
    print(orders["order_status"].value_counts())
def create_order_status_flags(orders):
    orders["is_delivered"] = (orders["order_status"] == "Delivered")
    orders["is_cancelled"] = (orders["order_status"] == "Cancelled")
    orders["is_unavailable"] = (orders["order_status"] == "Unavailable")
    return orders

def main():

    # Load all datasets
    datasets = load_data()

    # Inspect datasets
    inspect_data(datasets)

    # Check duplicates
    check_duplicates(datasets)

    # Check missing values
    check_missing_values(datasets)

    # Check Primary/Foreign Keys
    check_relationships(
        datasets["orders"],
        datasets["order_items"],
        datasets["payments"],
        datasets["reviews"],
        datasets["products"],
        datasets["customers"],
        datasets["sellers"]
    )

    # Timestamp Conversion
    timestamp_conversion(datasets)

    # Translate Product Category
    datasets["products"] = translate_categories(
        datasets["products"],
        datasets["translation"]
    )
    print(datasets["translation"])

    # Order Status
    analyze_order_status(datasets["orders"])

    # Order Status Flags
    datasets["orders"] = create_order_status_flags(datasets["orders"])



if __name__ == "__main__":
    main()