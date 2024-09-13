import os
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Set the scopes you need
SCOPES = ['https://www.googleapis.com/auth/admin.directory.group']

# Path to the credentials file you downloaded from Google Cloud
CLIENT_SECRET_FILE = 'client_secret_apps.googleusercontent.com.json'

def get_credentials():
    creds = None
    # Check if we already have valid credentials
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid credentials, do the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def create_group(group_email, group_name, group_description):
    # Get credentials and create the Admin SDK service
    creds = get_credentials()
    service = build('admin', 'directory_v1', credentials=creds)

    # Define the new group to be created
    group_body = {
        "email": group_email,
        "name": group_name,
        "description": group_description
    }

    # Call the Admin SDK Directory API to create the group
    try:
        group = service.groups().insert(body=group_body).execute()
        print(f'Group created: {group["name"]} ({group["email"]})')
        return group
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

def list_groups(customer_id='my_customer'):
    """Lists all Google Groups for the current customer."""
    creds = get_credentials()
    service = build('admin', 'directory_v1', credentials=creds)

    try:
        # Use the Admin SDK to list groups
        results = service.groups().list(customer=customer_id).execute()
        groups = results.get('groups', [])

        if not groups:
            print('No groups found.')
        else:
            print('Groups:')
            for group in groups:
                print(f"{group['email']} \"{group['name']}\"")
    except Exception as e:
        print(f'An error occurred: {e}')


def list_group_members(group_email):
    """Lists all members of a given Google Group."""
    creds = get_credentials()
    service = build('admin', 'directory_v1', credentials=creds)

    try:
        # Use the Admin SDK to list members
        results = service.members().list(groupKey=group_email).execute()
        members = results.get('members', [])

        if not members:
            print(f'No members found in the group: {group_email}.')
        else:
            print(f'Members of group {group_email}:')
            for member in members:
                print(f"{member['email']} {member['role']}")
    except Exception as e:
        print(f'An error occurred: {e}')


def add_member_to_group(group_email, member_email, role='MEMBER'):
    """Adds a new member to the given Google Group."""
    creds = get_credentials()
    service = build('admin', 'directory_v1', credentials=creds)

    # Define the new member to be added
    member_body = {
        'email': member_email,
        'role': role  # MEMBER, MANAGER, or OWNER
    }

    try:
        # Use the Admin SDK to insert a new member to the group
        result = service.members().insert(groupKey=group_email, body=member_body).execute()
        print(f"Member {result['email']} added to group {group_email} as {result['role']}.")
    except Exception as e:
        print(f'An error occurred: {e}')

def remove_member_from_group(group_email, member_email):
    """Removes a member from the given Google Group."""
    creds = get_credentials()
    service = build('admin', 'directory_v1', credentials=creds)

    try:
        # Use the Admin SDK to remove the member from the group
        service.members().delete(groupKey=group_email, memberKey=member_email).execute()
        print(f'Member {member_email} removed from group {group_email}.')
    except Exception as e:
        print(f'An error occurred while removing {member_email}: {e}')

def delete_group(group_email):
    """Deletes a Google Group using the Admin SDK."""
    creds = get_credentials()
    service = build('admin', 'directory_v1', credentials=creds)

    try:
        # Use the Admin SDK to delete the group
        service.groups().delete(groupKey=group_email).execute()
        print(f"Group {group_email} has been deleted.")
    except Exception as e:
        print(f'An error occurred: {e}')

