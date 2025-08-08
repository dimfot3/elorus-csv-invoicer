import logging
from decimal import Decimal
from datetime import date
import requests
import json


def create_invoice(contact_id, title, money, number, document_type_id, tax_id, invoice_url, headers, test_run):
    amount = Decimal(money).quantize(Decimal('0.00'))
    payload = {
        'client': contact_id,
        'documenttype': document_type_id,
        'date': str(date.today()),
        'currency_code': 'EUR',
        'mydata_document_type': '11.2',
        'items': [{
            'title': title,
            'quantity': 1,
            'unit_value': str(amount),
            'unit_discount': 0,
            'unit_discount_mode': 'amount',
            'unit_total': str(amount),
            'item_net': str(amount),
            'taxes': [{
                'tax': tax_id,
                'auto_calculate': True,
                'auto_calculate_vat': True,
                'amount': '0.00',
                'vat_amount': '0.00'
            }],
            'accounts': [{
                'mydata_classification': 'income',
                'mydata_classification_category': 'category1_3',
                'mydata_classification_type': 'E3_561_003',
                'amount': str(amount)
            }],
            'vat_exempted_195': False,
            'vat_exemption_category': 15
        }],
        'taxes': [{
            'tax': tax_id,
            'amount': '0',
            'auto_calculate': True,
            'applied_on_lines': True,
            'taxable': str(amount)
        }],
        'paid_on_receipt': str(amount),
        'payment_method': '7',
        'total': str(amount),
        'net': str(amount),
        'draft': False,
        'sequence_flat': 'A',
        'number': number,
        'calculator_mode': 'initial'
    }
    if test_run:
        logging.info(f"[TEST RUN] Would create invoice #{number} for client {contact_id}")
        logging.debug(f"Payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        return True

    resp = requests.post(invoice_url, headers=headers, json=payload)
    if resp.status_code == 201:
        logging.info(f"Invoice #{number} created for contact {contact_id}")
        return True
    logging.error(f"Invoice creation failed for invoice #{number}, contact {contact_id}: {resp.status_code} {resp.text}")
    return False