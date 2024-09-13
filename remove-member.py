#!env python

from manage_google_group import remove_member_from_group
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
            description='Remove an user email from a google group'
    )
    parser.add_argument('--user-email', type=str, nargs=1, required=True,
         help='user email to be removed from the group')

    parser.add_argument('--group-email', type=str, nargs=1, required=True,
           help='email of the group where we want to remove the user')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    group_email = ""
    user_email = ""
    role = "MEMBER"

    if args.group_email is not None:
        group_email = args.group_email[0]

    if args.user_email:
        user_email = args.user_email[0]

    remove_member_from_group(group_email, user_email) 
