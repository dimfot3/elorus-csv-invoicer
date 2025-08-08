# Elorus CSV Invoice Importer

A Python tool to batch import invoices into Elorus from CSV files. Automatically matches or creates contacts, applies Greek VAT rates, supports test mode, and logs errors for easy review and retry. Designed for fast and simple CSV-based invoicing.

---

## Features

- Imports contacts & invoices from CSV  
- Handles new and existing contacts  
- Logs skipped/failed rows  
- Resume mode for interrupted runs  
- Supports various Greek VAT & document types  

---

## Quick Start

1. **Clone the repository**
2. **Edit `config.yaml`**  
   - Add your Elorus API key and organization ID.
   - Choose the correct document and tax IDs (see below).
3. **Prepare your `info.csv`:**
   - Required columns: `name`, `email`, `title`, `money`
   - Example:
     ```
     name,email,title,money
     John Doe,john@example.com,Consulting,120.00
     ```
     - The above can be exported from xls files that many platforms keep like Stripes
4. **Run the script:**
   ```bash
   python main.py
   ```
   - For testing (no real API calls), use `test_run: True` in `config.yaml`.
   - For real invoices, set `test_run: False` (use with caution!).

---

## Configuration Example

```yaml
api_key: "your_api_key_here"
org_id: "your_org_id_here"
document_type_id: "3288935716926522758"  # Service Receipt
tax_id: "3288935716884580213"            # VAT 0% (exempt)
tax_category_id: "3288941048683825015"   # VAT exemption
starting_invoice_number: 241
csv_file: "info.csv"
test_run: True
resume: True
skip_log_file: "skipped_rows.txt"
```

---

## VAT & Tax IDs (Greece)

| Description            | ID                |
|------------------------|-------------------|
| Standard VAT (24%)     | 3288935716884580210 |
| Reduced VAT (13%)      | 3288935716884580211 |
| Reduced VAT (6%)       | 3288935716884580212 |
| VAT 0% (exempt)        | 3288935716884580213 |
| Withholding tax (20%)  | 3288935716884580214 |
| VAT exemption category | 3288941048683825015 |

---

## Document Type IDs

| ID                  | Greek                             | English                | Default | Description                         |
|---------------------|-----------------------------------|------------------------|---------|-------------------------------------|
| 3288935716926522761 | Απλοποιημένο τιμολόγιο            | Simplified Invoice     | No      | Simplified invoicing                |
| 3288935716926522758 | Απόδειξη παροχής υπηρεσιών        | Service Receipt        | No      | Receipt for services                |
| 3288935716926522759 | Στοιχείο αυτοπαράδοσης            | Self-Delivery Document | No      | Internal delivery records           |
| 3288935716926522760 | Στοιχείο ιδιοχρησιμοποίησης        | Self-Usage Document    | No      | For internal/personal use           |
| 3288935716926522756 | Τιμολόγιο                         | Invoice                | Yes     | Standard invoice (default)          |
| 3288935716926522757 | Τιμολόγιο παροχής υπηρεσιών       | Service Invoice        | No      | Invoice for services                |
| 3288935716926522763 | Απόδειξη επιστροφής               | Return Receipt         | No      | Receipt for returns                 |
| 3288935716926522762 | Πιστωτικό τιμολόγιο               | Credit Invoice         | Yes     | Credit invoice                      |
| 3288935716926522767 | Προσφορά                          | Quote                  | Yes     | Quote                               |
| 3288935716926522764 | Τιμολόγιο (Alt)                   | Invoice (Alt)          | Yes     | Invoice variant                     |
| 3288935716926522765 | Τιμολόγιο παροχής υπηρεσιών (Alt) | Service Invoice (Alt)  | No      | Service invoice variant             |
| 3288935716926522766 | Πιστωτικό τιμολόγιο (Alt)         | Credit Invoice (Alt)   | Yes     | Credit invoice variant              |

---

## Logging & Error Handling

- All logs are saved to `logs/app.log` (rotates automatically).  
- Skipped/problem rows go to `skipped_rows.txt` for review or retry.  
- To resume from skipped rows, set `resume: True` in your config.  

---

## FAQ

**Q: Will it create real invoices?**  
A: Only if `test_run` is `False`. In test mode, nothing is sent to Elorus.

**Q: What if something goes wrong?**  
A: Check `logs/app.log` and `skipped_rows.txt` for error details.

---

## License

MIT License. See [LICENSE](LICENSE).

---

**Questions?**  
Open an issue or contact the maintainer.
