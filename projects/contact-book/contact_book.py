"""Keep a tiny contact book in memory.

Companion project: https://pythonlessonlab.com/lessons/project-contact-book/
"""


def normalized_name(name):
    """Make one lookup key for names that differ only by case or edge spaces."""
    key = name.strip().casefold()
    if not key:
        raise ValueError("Contact name cannot be blank")
    return key


def add_contact(book, name, email):
    """Add a contact, or replace the record with the same normalized name."""
    key = normalized_name(name)
    clean_email = email.strip()
    if not clean_email:
        raise ValueError("Contact email cannot be blank")
    book[key] = {"name": name.strip(), "email": clean_email}


def find_contact(book, name):
    """Return a contact record, or None if the normalized name is absent."""
    return book.get(normalized_name(name))


def main():
    book = {}
    add_contact(book, "Ada Lovelace", "ada@example.com")
    add_contact(book, "Grace Hopper", "grace@example.com")
    add_contact(book, " ada LOVELACE ", "ada.new@example.com")

    found = find_contact(book, " ADA lovelace ")
    print(found["email"] if found else "Not found")
    print(f"Contacts: {len(book)}")

    missing = find_contact(book, "Unknown Person")
    print(f"Missing: {missing['email'] if missing else 'Not found'}")


if __name__ == "__main__":
    main()
