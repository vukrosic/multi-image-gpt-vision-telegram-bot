import logging
import os

import requests

# Get Airtable credentials
def get_airtable_credentials():
    airtable_api_key = os.getenv("AIRTABLE_API_KEY")
    airtable_base_id = os.getenv("AIRTABLE_BASE_ID")
    airtable_table_id = os.getenv("AIRTABLE_TABLE_ID")
    return airtable_api_key, airtable_base_id, airtable_table_id

# Get Airtable record by user ID
async def get_airtable_record(user_id):
    airtable_api_key, airtable_base_id, airtable_table_id = get_airtable_credentials()

    # Airtable API endpoint
    airtable_url = f'https://api.airtable.com/v0/{airtable_base_id}/{airtable_table_id}'

    # Headers for the API request
    headers = {
        'Authorization': f'Bearer {airtable_api_key}',
        'Content-Type': 'application/json',
    }

    # Query parameters to filter records by Telegram User ID
    params = {
        'filterByFormula': f"{{Telegram User ID}} = '{user_id}'",
        'maxRecords': 1  # Assuming there is only one record per user
    }

    # Perform the GET request to list records
    list_response = requests.get(airtable_url, headers=headers, params=params)

    if list_response.status_code == 200:
        records = list_response.json().get('records', [])
        return records
    else:
        print(f"Error listing records. Status Code: {list_response.status_code}")
        return None

# Update Airtable record with available budget
async def update_airtable_available_budget(user_id, user_name, available_budget):
    records = await get_airtable_record(user_id)
    airtable_api_key, airtable_base_id, airtable_table_id = get_airtable_credentials()

    if records:
        # Use the ID of the first record (assuming only one record per user)
        record_id = records[0]['id']
        logging.info(f'available_budget for {user_name}: {available_budget}')
        # Fields to be updated
        record_fields = {
            "Available Budget": float(available_budget)
        }

        # Airtable API endpoint
        airtable_url = f'https://api.airtable.com/v0/{airtable_base_id}/{airtable_table_id}'

        # Headers for the PATCH request
        headers = {
            'Authorization': f'Bearer {airtable_api_key}',
            'Content-Type': 'application/json',
        }

        # Payload for the PATCH request
        payload = {
            "records": [
                {
                    "id": record_id,
                    "fields": record_fields
                }
            ]
        }

        # Perform the PATCH request
        update_response = requests.patch(airtable_url, headers=headers, json=payload)

        if update_response.status_code == 200:
            print(f"Record for user {user_name} (ID: {user_id}) updated successfully.")
        else:
            print(f"Error updating record for user {user_name} (ID: {user_id}). Status Code: {update_response.status_code}")
    else:
        print(f"No record found for user {user_name} (ID: {user_id}).")


async def modify_airtable_budget(user_id, user_name, amount_to_modify, operation):
    """
    Modify the available budget for a user in Airtable.

    Parameters:
    - user_id (str): The unique identifier for the user.
    - user_name (str): The name of the user.
    - amount_to_modify (float): The amount by which to modify the budget.
    - operation (str): The operation to perform ('add' or 'subtract').

    Usage:
    - To increase the budget: modify_airtable_budget(user_id, user_name, amount_to_increase, 'add')
    - To decrease the budget: modify_airtable_budget(user_id, user_name, amount_to_decrease, 'subtract')
    """
    records = await get_airtable_record(user_id)

    if records:
        existing_budget = records[0].get('fields', {}).get('Available Budget', 0.0)

        if operation == 'add':
            new_budget = existing_budget + amount_to_modify
        elif operation == 'subtract':
            new_budget = existing_budget - amount_to_modify
        else:
            print("Invalid operation. Use 'add' or 'subtract'.")
            return

        await update_airtable_available_budget(user_id, user_name, new_budget)
    else:
        print(f"No record found for user {user_name} (ID: {user_id}).")

