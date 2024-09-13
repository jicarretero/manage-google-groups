#!env python

from manage_google_group import list_group_members
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
            description='email for the google group to query users'
    )
    parser.add_argument('group_email', metavar='group_email', type=str,
           help='email of the group whose users we want to list')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.group_email is not None:
        list_group_members(args.group_email)


