# pandas is used to create and work with DataFrames
import pandas as pd

# Faker is used to generate fake data
from faker import Faker

# random is used to generate random values
import random

# sys is used to read command-line arguments
import sys

# os is used to create folders and work with the operating system
import os

# datetime is used for date/time operations
# timedelta is used to add/subtract time
from datetime import datetime, timedelta


# Create a Faker object
# NOTE: Faker is not actually used in this code currently
fake = Faker()


# ============================================================
# FUNCTION 1: Generate daily orders
# ============================================================

def generate_daily_orders(
    target_date,              # Date for which we generate orders
    batch_label,              # AM or PM
    num_customers=300,        # Default: 300 customers
    num_products=80,          # Default: 80 products
    num_stores=4,             # Default: 4 stores
    num_orders=75             # Default: 75 orders
):
    """
    Generates one batch of orders.
    """

    # Set a fixed random seed.
    # Same date + same batch will generate the same random data.
    random.seed(f"{target_date}-{batch_label}")

    # Create an empty list.
    # We will store every order dictionary inside this list.
    orders = []

    # Loop from 1 to num_orders.
    # If num_orders = 75, this runs 75 times.
    for i in range(1, num_orders + 1):

        # Create a random time for the order.
        #
        # datetime.combine()
        # combines the target date with midnight (00:00:00).
        #
        # random.randint(0, 23)
        # generates a random hour.
        #
        # random.randint(0, 59)
        # generates a random minute.
        #
        # timedelta()
        # adds the random hours and minutes.
        order_time = (
            datetime.combine(
                target_date,
                datetime.min.time()
            )
            + timedelta(
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
        )

        # Create one order as a dictionary.
        #
        # Dictionary format:
        # "column_name": value
        #
        # Then append() adds this dictionary to the orders list.
        orders.append({

            # Create order ID.
            #
            # strftime("%Y%m%d")
            # converts date 2026-09-17 → 20260917
            #
            # {i:04d}
            # converts 1 → 0001
            "order_id": (
                f"{target_date.strftime('%Y%m%d')}"
                f"-{batch_label}-"
                f"{i:04d}"
            ),

            # Generate random customer ID from 1 to 300
            "customer_id": random.randint(1, num_customers),

            # Generate random product ID from 1 to 80
            "product_id": random.randint(1, num_products),

            # Generate random store ID from 1 to 4
            "store_id": random.randint(1, num_stores),

            # Store the randomly generated order timestamp
            "order_timestamp": order_time,

            # Generate quantity between 1 and 4
            "quantity": random.randint(1, 4),

            # Select an order status randomly.
            #
            # Completed  → 85% chance
            # Cancelled  → 10% chance
            # Returned   → 5% chance
            #
            # random.choices() returns a list.
            # [0] takes the first item from that list.
            "order_status": random.choices(
                ["Completed", "Cancelled", "Returned"],
                weights=[0.85, 0.1, 0.05]
            )[0]
        })

    # Convert the list of dictionaries into a Pandas DataFrame.
    #
    # Example:
    #
    # [
    #   {"order_id": "001", "customer_id": 10},
    #   {"order_id": "002", "customer_id": 20}
    # ]
    #
    # becomes:
    #
    # order_id | customer_id
    # ---------|------------
    # 001      | 10
    # 002      | 20
    return pd.DataFrame(orders)


# ============================================================
# FUNCTION 2: Generate daily website/app sessions
# ============================================================

def generate_daily_sessions(
    target_date,              # Date for the sessions
    batch_label,              # AM or PM
    num_customers=300,        # Default: 300 customers
    num_sessions=200          # Default: 200 sessions
):
    """
    Generates one batch of website/app session activity.
    """

    # Different seed from the orders function
    # because we are generating session data.
    random.seed(f"{target_date}-{batch_label}-sessions")

    # Empty list to store session records
    sessions = []

    # List of possible devices
    devices = ["Mobile", "Desktop", "Tablet"]

    # Run the loop 200 times by default
    for i in range(1, num_sessions + 1):

        # Generate a random timestamp during the target date
        session_time = (
            datetime.combine(
                target_date,
                datetime.min.time()
            )
            + timedelta(
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
        )

        # Create one session dictionary
        sessions.append({

            # Example:
            # 20260917-AM-S00001
            #
            # {i:05d} means:
            # 1 → 00001
            # 25 → 00025
            "session_id": (
                f"{target_date.strftime('%Y%m%d')}"
                f"-{batch_label}-"
                f"S{i:05d}"
            ),

            # Create a list containing:
            #
            # None
            # 1
            # 2
            # 3
            # ...
            # 300
            #
            # None represents an anonymous user.
            #
            # random.choice() selects one value randomly.
            "customer_id": random.choice(
                [None] + list(range(1, num_customers + 1))
            ),

            # Store session timestamp
            "session_timestamp": session_time,

            # Randomly select Mobile/Desktop/Tablet
            "device_type": random.choice(devices),

            # Random number of pages viewed
            # between 1 and 15
            "pages_viewed": random.randint(1, 15),

            # Random session duration
            # between 10 seconds and 1800 seconds
            "session_duration_seconds": random.randint(10, 1800)
        })

    # Convert session list into a Pandas DataFrame
    return pd.DataFrame(sessions)


# ============================================================
# MAIN PROGRAM
# ============================================================

# This condition means:
#
# "Run the following code only when this file
# is executed directly."
#
# Example:
# python generate_daily_data.py
#
# If another Python file imports this file,
# this section will not automatically run.
if __name__ == "__main__":

    # --------------------------------------------------------
    # GET DATE FROM COMMAND LINE
    # --------------------------------------------------------

    # sys.argv contains values passed when running the script.
    #
    # Example:
    #
    # python generate_daily_data.py 2026-09-17 AM
    #
    # sys.argv[0] = generate_daily_data.py
    # sys.argv[1] = 2026-09-17
    # sys.argv[2] = AM

    # Check whether the user provided a date
    if len(sys.argv) > 1:

        # Convert string "2026-09-17"
        # into a Python date object.
        target_date = datetime.strptime(
            sys.argv[1],
            "%Y-%m-%d"
        ).date()

    else:

        # If no date was provided,
        # use today's date.
        target_date = datetime.today().date()


    # --------------------------------------------------------
    # GET AM / PM BATCH LABEL
    # --------------------------------------------------------

    # Check whether the user provided AM or PM
    if len(sys.argv) > 2:

        # .upper() converts:
        #
        # "am" → "AM"
        # "pm" → "PM"
        batch_label = sys.argv[2].upper()

    else:

        # If AM/PM wasn't provided,
        # automatically determine it from current time.
        #
        # Before 12 → AM
        # 12 or later → PM
        batch_label = (
            "AM"
            if datetime.now().hour < 12
            else "PM"
        )


    # Convert date into string.
    #
    # Example:
    # 2026-09-17
    #
    # becomes:
    # "2026-09-17"
    date_str = target_date.strftime("%Y-%m-%d")


    # --------------------------------------------------------
    # GENERATE ORDERS
    # --------------------------------------------------------

    # Call the generate_daily_orders() function.
    #
    # Since we don't provide the optional parameters,
    # Python uses their default values:
    #
    # num_customers = 300
    # num_products = 80
    # num_stores = 4
    # num_orders = 75

    orders_df = generate_daily_orders(
        target_date,
        batch_label
    )


    # --------------------------------------------------------
    # GENERATE SESSIONS
    # --------------------------------------------------------

    # Call the session generation function.
    #
    # Default:
    # num_customers = 300
    # num_sessions = 200

    sessions_df = generate_daily_sessions(
        target_date,
        batch_label
    )


    # --------------------------------------------------------
    # CREATE FOLDER PATHS
    # --------------------------------------------------------

    # Create the orders folder path.
    #
    # Example:
    # data/raw/orders/2026-09-17

    orders_dir = f"data/raw/orders/{date_str}"


    # Create the sessions folder path.
    #
    # Example:
    # data/raw/sessions/2026-09-17

    sessions_dir = f"data/raw/sessions/{date_str}"


    # --------------------------------------------------------
    # CREATE DIRECTORIES
    # --------------------------------------------------------

    # Create orders directory.
    #
    # exist_ok=True means:
    # If the folder already exists,
    # don't throw an error.

    os.makedirs(
        orders_dir,
        exist_ok=True
    )


    # Create sessions directory
    os.makedirs(
        sessions_dir,
        exist_ok=True
    )


    # --------------------------------------------------------
    # SAVE ORDERS AS CSV
    # --------------------------------------------------------

    # Convert orders DataFrame into a CSV file.
    #
    # Example output:
    #
    # data/raw/orders/2026-09-17/
    # orders_2026-09-17_AM.csv
    #
    # index=False means:
    # Don't add Pandas' index column to the CSV.

    orders_df.to_csv(
        f"{orders_dir}/orders_{date_str}_{batch_label}.csv",
        index=False
    )


    # --------------------------------------------------------
    # SAVE SESSIONS AS CSV
    # --------------------------------------------------------

    # Save sessions DataFrame as CSV.

    sessions_df.to_csv(
        f"{sessions_dir}/sessions_{date_str}_{batch_label}.csv",
        index=False
    )


    # --------------------------------------------------------
    # PRINT FINAL MESSAGE
    # --------------------------------------------------------

    # len(orders_df)
    # tells us how many rows/orders were generated.
    #
    # len(sessions_df)
    # tells us how many sessions were generated.

    print(
        f"[{batch_label}] Generated "
        f"{len(orders_df)} orders and "
        f"{len(sessions_df)} sessions "
        f"for {date_str}"
    )