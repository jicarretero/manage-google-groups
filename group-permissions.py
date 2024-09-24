#!env python

from manage_google_group import get_credentials
from googleapiclient.discovery import build
import argparse
import json


valid_moderation_levels = ['MODERATE_NON_MEMBERS', 'MODERATE_ALL_MESSAGES', 'MODERATE_NEW_MEMBERS', 'MODERATE_NONE']
valid_posting_values = ['ANYONE_CAN_POST', 'ALL_IN_DOMAIN_CAN_POST', 'ALL_MANAGERS_CAN_POST', 'NONE_CAN_POST']

def parse_args():
    parser = argparse.ArgumentParser(
            description='Set group permissions for posting and moderation. By default anyone can post and it is unmoderated'
    )
    parser.add_argument('--group-email', type=str, nargs=1, required=True,
         help='group email to be modified')

    parser.add_argument('--moderation-level', type=str, nargs=1, required=True,
         help='Set the moderation level. Valid values are: MODERATE_NON_MEMBERS, MODERATE_ALL_MESSAGES, MODERATE_NEW_MEMBERS, MODERATE_NONE')

    parser.add_argument('--who-can-post', type=str, nargs=1, required=True,
         help='Set who can post messages. Valid values are: ANYONE_CAN_POST, ALL_IN_DOMAIN_CAN_POST, ALL_MANAGERS_CAN_POST, NONE_CAN_POST')

    return parser.parse_args()


def set_permissions(group_email, moderation_level, who_can_post):
    """Updates the moderation settings for external messages for the given Google Group."""
    creds = get_credentials()
    service = build('groupssettings', 'v1', credentials=creds)

    # Fetch the current group settings
    group_settings = service.groups().get(groupUniqueId=group_email).execute()

    # Update the settings to moderate external messages
    group_settings['whoCanPostMessage'] = who_can_post
    group_settings['messageModerationLevel'] = moderation_level

    try:
        # Apply the updated settings
        result = service.groups().update(groupUniqueId=group_email, body=group_settings).execute()
        print(json.dumps(result))
    except Exception as e:
        print(f'An error occurred: {e}')


if __name__ == "__main__":
    args = parse_args()

    group_email = ""
    who_can_post = ""
    moderation_level = ""

    if args.group_email is not None:
        group_email = args.group_email[0]

    if args.moderation_level:
        moderation_level= args.moderation_level[0]
        if moderation_level not in valid_moderation_levels:
            raise ValueError('--moderation-level must be one of MODERATE_NON_MEMBERS, MODERATE_ALL_MESSAGES'
                             'MODERATE_NEW_MEMBERS, MODERATE_NONE ')

    if args.who_can_post:
        who_can_post = args.who_can_post[0]
        if who_can_post not in valid_posting_values:
            raise ValueError('--who-can-post must be one of ANYONE_CAN_POST, ALL_IN_DOMAIN_CAN_POST, ALL_MANAGERS_CAN_POST, NONE_CAN_POST')

    set_permissions(group_email, moderation_level, who_can_post) 
