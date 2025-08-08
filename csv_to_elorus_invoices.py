import csv
import yaml
import logging
from decimal import Decimal
from tools.contacts import get_all_contacts, get_or_create_contact_id
from tools.loggers import setup_logging, log_skipped_row
from tools.invoice import create_invoice
import os
import json 


# Load config from YAML file
def load_config(config_file='config.yaml'):
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def load_skipped_rows(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]

def parse_row(row, idx):
    name, email, title, money = row.get('name', '').strip(), row.get('email', '').strip(), row.get('title', '').strip(), row.get('money', '').strip()
    if not all([name, email, title, money]):
        logging.warning(f"Row {idx}: missing data → {row}")
        return None
    try:
        _ = Decimal(money)
    except:
        logging.warning(f"Row {idx}: invalid money '{money}'")
        return None
    return name, email, title, money

def process_csv():
    config = load_config()
    API_KEY = config['api_key']
    ORG_ID = config['org_id']
    DOCUMENT_TYPE_ID = config['document_type_id']
    TAX_ID = config['tax_id']
    TAX_CATEGORY_ID = config['tax_category_id']
    DEFAULT_TAXES = [TAX_CATEGORY_ID]
    CSV_FILE = config['csv_file']
    TEST_RUN = config.get('test_run', False)
    SKIP_LOG_FILE = config.get('skip_log_file', 'skipped_rows.txt')
    RESUME = config.get('resume', False)
    BASE_URL = 'https://api.elorus.com/v1.2'
    CONTACTS_URL = f'{BASE_URL}/contacts/'
    INVOICES_URL = f'{BASE_URL}/invoices/'
    HEADERS = {
        'Authorization': f'Token {API_KEY}',
        'X-Elorus-Organization': ORG_ID,
        'Content-Type': 'application/json'
    }
    number = config['starting_invoice_number']
    
    rows = load_skipped_rows(SKIP_LOG_FILE) if RESUME else None
    if rows:
        logging.info("Resuming from skipped rows...")
        open(SKIP_LOG_FILE, 'w').close()  # Clear log
    else:
        with open(CSV_FILE, newline='', encoding='utf-8-sig') as f:
            rows = list(csv.DictReader(f))

    contacts_cache = get_all_contacts(CONTACTS_URL, HEADERS, TEST_RUN)
    
    for idx, row in enumerate(rows, start=1):
        parsed = parse_row(row, idx)
        if not parsed:
            log_skipped_row(row, 'parse_failed', SKIP_LOG_FILE)
            continue
        name, email, title, money = parsed
        contact_id = get_or_create_contact_id(name, email, contacts_cache, DEFAULT_TAXES, CONTACTS_URL, HEADERS, TEST_RUN)
        if not contact_id:
            log_skipped_row(row, 'contact_failed', SKIP_LOG_FILE)
            continue
        if not create_invoice(contact_id, title, money, number, DOCUMENT_TYPE_ID, TAX_ID, INVOICES_URL, HEADERS, TEST_RUN):
            log_skipped_row(row, 'invoice_failed', SKIP_LOG_FILE)
            continue
        number += 1

if __name__ == "__main__":
    setup_logging(
        log_path='logs/app.log',
        max_bytes=5 * 1024 * 1024,      # rotate after 5 MB
        backup_count=3, level=logging.INFO
    )
    logging.info("App started")
    process_csv()
    logging.info("App finished")
