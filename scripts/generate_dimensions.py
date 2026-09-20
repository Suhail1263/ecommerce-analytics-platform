import pandas as pd
from faker import Faker
import random

fake=Faker()
Faker.seed(42)
random.seed(42)

# ---- Customers ----
num_customers=300
customers=[]

for i in range(1,num_customers+1):
    customers.append({
        "customer_id":i,
        "customer_name":fake.name(),
        "email":fake.email(),
        "city":fake.city(),
        "country":"UAE" if random.random() < 0.6 else fake.country(),
        "signup_date":fake.date_between(start_date="-2y",end_date="today")
    })
pd.DataFrame(customers).to_csv("data/raw/customers.csv",index=False)
print(f"Generated {len(customers)} customers")

# ---- Products ----

categories = ["Electronics", "Fashion", "Home & Kitchen", "Beauty", "Groceries", "Sports"]
num_products = 80
products = []
for i in range(1, num_products + 1):
    products.append({
        "product_id": i,
        "product_name": fake.word().capitalize() + " " + random.choice(["Pro", "Max", "Lite", "Plus"]),
        "category": random.choice(categories),
        "unit_price": round(random.uniform(10, 800), 2)
    })
pd.DataFrame(products).to_csv("data/raw/products.csv", index=False)
print(f"Generated {len(products)} products")

# ---- Stores (fulfillment centers / warehouses) ----
warehouses = ["Dubai", "Abu Dhabi", "Sharjah", "Ajman"]
stores = []
for i, city in enumerate(warehouses, start=1):
    stores.append({
        "store_id": i,
        "store_name": f"{city} Fulfillment Center",
        "city": city,
        "country": "UAE"
    })
pd.DataFrame(stores).to_csv("data/raw/stores.csv", index=False)
print(f"Generated {len(stores)} stores")

