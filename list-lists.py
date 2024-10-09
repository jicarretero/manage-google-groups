#!env python

from manage_google_group import list_groups

if __name__ == "__main__":
    groups = list_groups()

    if groups:
        for group in groups:
            print(f"{group['email']} \"{group['name']}\"")
    else:
        print('No group found')

  
