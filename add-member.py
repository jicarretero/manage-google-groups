#!env python

from manage_google_group import add_member_to_group
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
            description='Add an user email to a google group'
    )
    parser.add_argument('--user-email', type=str, nargs=1, required=True,
         help='user email to be added to the group')

    parser.add_argument('--group-email', type=str, nargs=1, required=True,
           help='email of the group where we want to add the user')

    parser.add_argument('--owner', required=False,
           action='store_true',
           help='Set the role OWNER for the user. The highest level of perminsions in the group.')

    parser.add_argument('--manager', required=False,
           action='store_true',
           help='Set the role MANAGER for the user. A higher level of perminsions in the group.')

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

    if args.owner:
        role = 'OWNER' 
    elif args.manager:
        role = 'MANAGER' 

    add_member_to_group(group_email, user_email, role) 
