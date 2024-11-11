import argparse
import json

import requests

environments = {
    "local": "http://localhost:8000",
    #"dev": "https://apppoc-dev.up.railway.app",
    #"prod": "https://simpleapp-production.up.railway.app"
}

client_creds = { # Update with your credentials
    "client_id": "",
    "client_secret": ""
}

def populate_database(base_json_file, base_uuid, num_items=20, base_host="http://localhost:8000", endpoint_url="/2/footprints/create-product-footprint/"):
    with open(base_json_file, 'r') as f:
        base_item = json.load(f)

    auth_response = requests.post(
        f"{base_host}/auth/token",
        data={
            "grant_type": "",
            "scope": "",
            "client_id": client_creds["client_id"],
            "client_secret": client_creds["client_secret"]
        },
    )
    auth_response.raise_for_status()

    access_token = auth_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    for i in range(1, num_items+1):
        item = base_item.copy()  # Shallow copy might suffice
        item['id'] = f"{base_uuid[:-2]}{i:02d}"

        response = requests.post(f"{base_host}{endpoint_url}", json=item, headers=headers)
        response.raise_for_status()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Populate a database with test data")
    parser.add_argument("--base_json", default="valid_test_product_footprint.json", help="Path to the base JSON file")
    parser.add_argument("--base_uuid", default="3fa85f64-5717-4562-b3fc-2c963f66afa6", help="Base UUID for generating items")
    parser.add_argument("--num_items", type=int, default=20, help="Number of items to create")
    parser.add_argument("--endpoint", default="/2/footprints/create-product-footprint/", help="API endpoint for item creation")
    parser.add_argument("--base_host", default=environments["local"], help="Base host URL for the API (e.g., http://localhost:8000)")

    args = parser.parse_args()

    populate_database(
        base_json_file=args.base_json,
        base_uuid=args.base_uuid,
        num_items=args.num_items,
        endpoint_url=args.endpoint,
        base_host=args.base_host
    )
