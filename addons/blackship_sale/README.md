# BlackShip Sales

BlackShip Sales is an Odoo 18 addon scaffold that depends on CRM, Sales, Contacts, and Accounting apps. The module is prepared for future customizations with translation support already configured.

## Installation

1. Copy the `blackship_sale` directory into your Odoo addons path (e.g., `./addons`).
2. Update the addon list and install **BlackShip Sales** from Apps, or install it from the command line:

```bash
./odoo-bin -d <database_name> -u blackship_sale --addons-path=addons
```

## Translation export/import

Use Odoo's built-in i18n commands to manage translations for this module.

### Export

Generate or update the translation template (POT) or locale file (PO):

```bash
./odoo-bin -d <database_name> --addons-path=addons --i18n-export=addons/blackship_sale/i18n/blackship_sale.pot --modules=blackship_sale --language=en_US
./odoo-bin -d <database_name> --addons-path=addons --i18n-export=addons/blackship_sale/i18n/it.po --modules=blackship_sale --language=it_IT
```

### Import

Load translations back into the database:

```bash
./odoo-bin -d <database_name> --addons-path=addons --i18n-import=addons/blackship_sale/i18n/it.po --language=it_IT
```

The Italian catalog translates all user-facing labels, wizard messages, gate blocking errors, approval errors, and report headings. Regenerate `blackship_sale.pot` and refresh `it.po` whenever new strings are added.

