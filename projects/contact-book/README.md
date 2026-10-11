# Contact Book

Build a tiny in-memory address book. The [interactive lesson](https://pythonlessonlab.com/lessons/project-contact-book/) and [video walkthrough](https://youtu.be/bBvf1IgZLY8) show why an exact dictionary lookup raises `KeyError` when the searched name has different capitalization or surrounding spaces. Both saving and finding a contact use `strip().casefold()` for a consistent key.

## Run the demo

From the repository root:

```sh
python projects/contact-book/contact_book.py
```

Expected output:

```text
ada.new@example.com
Contacts: 2
Missing: Not found
```

The demo adds Ada and Grace, updates Ada's email by adding her name again with different capitalization, and checks an absent name. The email addresses are fictional. No contact information leaves your computer; the dictionary disappears when the program exits.

## Try it yourself

1. Change the searched Ada name to uppercase and add spaces. The lookup should still work.
2. Add a third person and print their email.
3. Search for an absent person. Check the result before indexing `['email']`.
4. Run the tests:

   ```sh
   python -m unittest discover -s projects/contact-book -p "test_*.py"
   ```

The name is the lookup key in this small project. Two different people with the same normalized name would collide, so a larger address book should use separate stable IDs and define how ambiguous name searches work. This version does not save contacts to disk and is not intended for real private contact data.
