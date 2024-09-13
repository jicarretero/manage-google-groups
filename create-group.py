#!env python

from manage_google_group import create_group
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
            description='Create a new google group with mail, description and name'
    )
    parser.add_argument('--name', type=str, nargs=1, required=True,
         help='name of the group to be created')
    parser.add_argument('--description', type=str, nargs=1,
         help='name of the group to be created')

    parser.add_argument('--email', type=str, nargs=1, required=True,
           help='email of the group whose users we want to list')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    mail=""
    name=""
    description=""

    if args.email is not None:
        mail = args.email[0]

    if args.name:
        name = args.name[0]

    if args.description:
        description = args.description[0]

    create_group(mail, name, description)
