import os
from dotenv import load_dotenv
from azure.storage.filedatalake import DataLakeServiceClient

load_dotenv()
print("DEBUG:", os.getenv("AZURE_STORAGE_CONNECTION_STRING"))

def get_service_client():
    connection_string=os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    return DataLakeServiceClient.from_connection_string(connection_string)

def upload_file(local_path,container_name,remote_path):
    """
    Uploads a single local file to a specific path inside the Data Lake container.
    """
    service_client = get_service_client()
    file_system_client = service_client.get_file_system_client(file_system=container_name)

    directory_path = os.path.dirname(remote_path)
    file_name = os.path.basename(remote_path)

    directory_client = file_system_client.get_directory_client(directory_path)
    directory_client.create_directory()  # safe to call even if it already exists

    file_client = directory_client.get_file_client(file_name)

    with open(local_path, "rb") as f:
        data = f.read()
        file_client.upload_data(data, overwrite=True)

    print(f"Uploaded {local_path} -> {container_name}/{remote_path}")

def upload_folder(local_folder, container_name, remote_base_path):
    """
    Uploads every file inside a local folder (recursively) to the Data Lake,
    preserving the folder structure.
    """
    for root, dirs, files in os.walk(local_folder):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_folder)
            remote_path = os.path.join(remote_base_path, relative_path).replace("\\", "/")
            upload_file(local_path, container_name, remote_path)


if __name__ == "__main__":
    container = "raw"

    # Upload dimension files (customers, products, stores) - flat, no date folder
    upload_file("data/raw/customers.csv", container, "customers/customers.csv")
    upload_file("data/raw/products.csv", container, "products/products.csv")
    upload_file("data/raw/stores.csv", container, "stores/stores.csv")

    # Upload all orders and sessions (recursively, preserving date-partitioned folders)
    upload_folder("data/raw/orders", container, "orders")
    upload_folder("data/raw/sessions", container, "sessions")

    print("All files uploaded successfully.")


