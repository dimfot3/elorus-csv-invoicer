
import requests
import time
import logging
import random


def get_all_contacts(contacts_url, headers, test_run):
    """ Retrieve all contacts by iterating over pages (if pagination is used). """
    contacts = []
    if test_run: return contacts
    url = contacts_url
    while url:
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            logging.error(f"Failed to fetch contacts: {resp.status_code} {resp.text}")
            break
        data = resp.json()
        contacts.extend(data.get('results', []))
        url = data.get('next')  # Assuming standard REST pagination
    return contacts

def find_contact_id(email, contacts_cache=None):
    """ Lookup existing contact ID in provided contacts list. """
    email_norm = email.strip().lower()
    for c in contacts_cache or []:
        for e in c.get('email', []):
            if e.get('email', '').strip().lower() == email_norm:
                return c.get('id')
    return None

def create_contact(name, email, default_taxes, contacts_url, headers):
    payload = {
        "first_name": name,
        "is_client": True,
        "client_type": "4",
        "default_currency_code": "EUR",
        "default_language": "el",
        "email": [{"email": email, "primary": True}],
        "default_taxes": default_taxes
    }
    resp = requests.post(contacts_url, headers=headers, json=payload)
    if resp.status_code == 201:
        return resp.json().get('id')
    logging.error(f"Contact creation failed ({name}, {email}): {resp.status_code} {resp.text}")
    return None

def get_or_create_contact_id(name, email, contacts_cache, theme_id, default_taxes, contacts_url, headers, test_run):
    if test_run: return str(random.randint(10000000000, 999999999999))
    contact_id = find_contact_id(email, contacts_cache)
    if contact_id:
        return contact_id
    for attempt in range(3):
        contact_id = create_contact(name, email, theme_id, default_taxes, contacts_url, headers)
        if contact_id:
            return contact_id
        time.sleep(1)
    logging.error(f"Failed to get/create contact for {name} <{email}> after 3 attempts")
    return None