# Codex Rules — BlackShip Sale (Odoo 18)

## Project context
- Target: Odoo 18
- New addon: `blackship_sale`
- Addon path (assumption): `addons/blackship_sale/`
- Mandatory deps (manifest): `crm`, `sale`, `contacts`, `account`

## Global constraints (must follow)
1) Work ONLY inside `addons/blackship_sale/` unless a task explicitly allows additional paths.
2) Do NOT refactor unrelated code. No "cleanup", no formatting sweeps, no renames outside scope.
3) Do NOT introduce JavaScript unless explicitly requested by a task (currently: never).
4) Keep changes minimal and atomic: implement only what the current TASK requires.
5) Do NOT modify Odoo core or other addons.
6) If a decision is ambiguous, prefer the simplest implementation and document it in a short comment.

## i18n (translations) rules
### Python
- Always import: `from odoo import _, api, fields, models`
- Any user-facing text MUST be wrapped in `_()`:
  - `UserError(_("..."))`
  - `ValidationError(_("..."))`
  - action names, button labels created in Python, etc.
- Do not build user-facing strings with complex concatenation.
  - Prefer `_("%s: %s") % (a, b)` if needed.

### XML views / QWeb / menus
- Use `string="..."` normally; Odoo extracts it.
- Avoid dynamic concatenation for UI text; keep text as normal strings.
- For QWeb reports, keep headings/labels as plain text nodes so they are extracted.

### Translatable fields
- For configurable names (stages, checklist item name), use `translate=True` on Char fields where appropriate.

### i18n files
- Ensure:
  - `addons/blackship_sale/i18n/blackship_sale.pot`
  - `addons/blackship_sale/i18n/it.po`
- Keep `it.po` header valid; update entries as new strings appear.

## Error messages (UX constraints)
- Errors should be:
  - concise
  - actionable (what is missing / what to do next)
  - translatable
- When listing missing items, cap at max 5 entries.

## Code style / structure
- Standard Odoo addon layout:
  - `models/`, `views/`, `wizard/`, `security/`, `report/`, `data/`, `static/`, `i18n/`
- One feature per file group is okay; avoid mega-files.

## Verification (local)
Use these as generic references (adapt to your environment/compose):
- Start Odoo with this addon mounted in addons path.
- Install module: `blackship_sale`
- Smoke:
  - open CRM → Opportunities → open a lead → tab BlackShip
  - set stage, toggle checklist items, try gate blocking
  - open/create quotation via wizard

## i18n export/import (generic Odoo CLI)
NOTE: Commands require a DB where the module is installed.

Export POT:
- `odoo-bin -d <db> -u blackship_sale --i18n-export=addons/blackship_sale/i18n/blackship_sale.pot --modules=blackship_sale --stop-after-init`

Export/Update Italian PO:
- `odoo-bin -d <db> -u blackship_sale --i18n-export=addons/blackship_sale/i18n/it.po --language=it_IT --modules=blackship_sale --stop-after-init`

Import Italian PO:
- `odoo-bin -d <db> -u blackship_sale --i18n-import=addons/blackship_sale/i18n/it.po --language=it_IT --stop-after-init`

## How Codex should respond
For each TASK:
- Modify only the allowed scope.
- Output a clean diff of files changed/added.
- If something cannot be implemented due to missing context, add a short note at the top of the diff (not as prose elsewhere).
