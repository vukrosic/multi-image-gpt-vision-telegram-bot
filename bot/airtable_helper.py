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
        logging.info(f'Airtable records: {records}')
        if not records:
            print("No records found for this Telegram User ID.")
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
            print(
                f"Error updating record for user {user_name} (ID: {user_id}). Status Code: {update_response.status_code}")
    else:
        print(f"No record found for user {user_name} (ID: {user_id}).")


async def add_user_to_airtable(user_id, user_name, openai_thread_id):
    airtable_api_key, airtable_base_id, airtable_table_id = get_airtable_credentials()
    # Make a request to add a new record to Airtable
    airtable_url = f'https://api.airtable.com/v0/{airtable_base_id}/{airtable_table_id}'
    headers = {
        'Authorization': f'Bearer {airtable_api_key}',
        'Content-Type': 'application/json',
    }
    print(f"Adding user {user_name} (ID: {user_id}), OpenAI Thread ID: {openai_thread_id} to Airtable...")
    data = {
        "records": [
            {
                "fields": {
                    "Telegram User ID": int(user_id),
                    "Telegram Username": user_name,
                    "OpenAI Assistants API Thread ID": openai_thread_id,
                }
            }
        ]
    }
    response = requests.post(airtable_url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"User {user_name} (ID: {user_id}) added to Airtable.")
    else:
        print(f"Error adding user {user_name} (ID: {user_id}) to Airtable. Status Code: {response.status_code}")
