#!env python

from manage_google_group import delete_group
import argparse, random, string

def randomword(length=6):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def parse_args():
    parser = argparse.ArgumentParser(
            description="email for the google group remove. IT IS IRREVERSIBLE. CAN'T BE UNDONE"
    )
    parser.add_argument('group_email', metavar='group_email', type=str,
           help='email of the group to remove')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    group_email = ""

    if args.group_email is not None:
        group_email = args.group_email

    rw = randomword()

    print("\n\n")
    rd = input(f"Please, type {rw} in capital letters to proceed:")

    if rw.upper() == rd:
        print("removing...")
        delete_group(group_email)
    else:
        print("... nothing done")



