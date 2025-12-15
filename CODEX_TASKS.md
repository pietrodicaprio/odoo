# CODEX_TASKS — BlackShip Sale (Odoo 18)

Read `CODEX_RULES.md` first and follow it strictly.

Assumed addon path: `addons/blackship_sale/`

---

## TASK 01 — Scaffold addon `blackship_sale` + i18n base

### Goal
Create an installable Odoo 18 addon skeleton with translation scaffolding.

### Scope
Allowed:
- Create everything under `addons/blackship_sale/`
Forbidden:
- Any changes outside `addons/blackship_sale/`

### Deliverables
- `addons/blackship_sale/__init__.py`
- `addons/blackship_sale/__manifest__.py`
- `addons/blackship_sale/models/__init__.py`
- `addons/blackship_sale/views/`
- `addons/blackship_sale/security/ir.model.access.csv`
- `addons/blackship_sale/report/`
- `addons/blackship_sale/static/src/scss/`
- `addons/blackship_sale/i18n/blackship_sale.pot`
- `addons/blackship_sale/i18n/it.po`
- `addons/blackship_sale/README.md`

### DoD
- Manifest:
  - name: `BlackShip Sales`
  - version: `18.0.1.0.0`
  - depends: `crm`, `sale`, `contacts`, `account`
  - application: true
  - license: `LGPL-3`
- i18n files exist with valid headers (it.po).
- README includes i18n export/import commands (generic).

### Verification
- Module installs without errors (basic).

---

## TASK 02 — Model `blackship.stage` + views + configuration menu

### Goal
Add configurable BlackShip stages.

### Scope
Allowed:
- `addons/blackship_sale/models/*`
- `addons/blackship_sale/views/*`
- `addons/blackship_sale/security/*`
- `addons/blackship_sale/__manifest__.py`

### Deliverables
- `models/blackship_stage.py`
- `views/blackship_stage_views.xml`
- `views/blackship_menus.xml`
- Update `security/ir.model.access.csv`
- Update `__manifest__.py` data list

### Spec
Model `blackship.stage` fields:
- `name = fields.Char(required=True, translate=True)`
- `sequence = fields.Integer(default=10, index=True)`
- `probability = fields.Float()`
- `is_gate = fields.Boolean()`
- `required_fields = fields.Json(help=...)`
- `sla_hours = fields.Integer()`

Menu:
- Under CRM or Sales → Configuration → BlackShip Stages

Access:
- `base.group_user`: read/write/create = 1, unlink = 0

### DoD
- Views load.
- Menu visible.
- All UI strings extractable for i18n.

### Verification
- Open menu and create/edit stage.

---

## TASK 03 — Extend `crm.lead`: BlackShip fields + compute `gate_ok`

### Goal
Add BlackShip fields to lead and compute gate completeness.

### Scope
Allowed:
- `models/crm_lead.py`
- `views/crm_lead_views.xml`
- `models/__init__.py`
- `__manifest__.py` (if new xml added)

### Deliverables
- New/updated `models/crm_lead.py`
- Update `views/crm_lead_views.xml`

### Spec
Add fields:
- `blackship_stage_id = fields.Many2one("blackship.stage", string="BlackShip Stage", tracking=True)`
- `risk_score = fields.Integer(string="Risk Score")`
- `discovery_notes = fields.Html(string="Discovery Notes")`
- `solution_brief = fields.Html(string="Solution Brief")`
- `gate_ok = fields.Boolean(string="Gate OK", compute="_compute_gate_ok", store=False)`

Compute `_compute_gate_ok`:
- If no stage => True
- Else:
  - read `required_fields` dict
  - for each key with truthy value:
    - if field does not exist on model => gate_ok False
    - if field exists but value is falsy/empty => gate_ok False

UI:
- Add tab/section "BlackShip" to lead form including fields.
- Show an alert when `gate_ok` is False.

### DoD
- No user-facing strings in Python without `_()`.
- No side effects; just compute.

### Verification
- Create stage with required_fields = {"discovery_notes": true}
- On lead, gate_ok should flip based on discovery_notes content.

---

## TASK 04 — Checklist model `blackship.checklist.item` + lead integration

### Goal
Support per-lead checklist items (mandatory/optional).

### Scope
Allowed:
- `models/blackship_checklist.py`
- `models/crm_lead.py` (extend)
- `views/crm_lead_views.xml`
- `security/ir.model.access.csv`

### Deliverables
- `models/blackship_checklist.py`
- Extend lead with One2many:
  - `blackship_checklist_ids = fields.One2many("blackship.checklist.item", "lead_id", string="BlackShip Checklist")`
- Lead view: editable tree for checklist (name, mandatory, is_done, stage_id, sequence)

### Spec
Model fields:
- `lead_id` (Many2one crm.lead, required, ondelete=cascade, index)
- `stage_id` (Many2one blackship.stage, index)
- `name` (Char, required, translate=True)
- `is_done` (Boolean default False)
- `mandatory` (Boolean default True)
- `sequence` (Integer default 10)

Access:
- base.group_user: read/write/create=1 unlink=0

### DoD
- Checklist is editable inside lead.
- All UI strings extractable.

### Verification
- Create checklist rows and toggle done.

---

## TASK 05 — Gate blocking on stage change (requirements + checklist)

### Goal
Prevent moving into a gate stage unless requirements/checklist are satisfied.

### Scope
Allowed:
- `models/crm_lead.py`

### Deliverables
- Override `write()` (and handle `create()` if stage set at creation)
- Block when:
  - new stage has `is_gate=True` AND
  - gate_ok for that target stage is False OR
  - mandatory checklist for that stage is not all done

### Spec decisions (document in short comments)
- Checklist filtering:
  - Only items where `stage_id == new_stage` AND `mandatory=True` must be done.
  - If no items exist, checklist condition passes.

Error message:
- Translatable `_()`
- Mentions missing required fields (max 5) and incomplete checklist items (max 5).

### DoD
- Does not affect non-BlackShip leads.
- Works for multi-record write.
- No hardcoded user-facing strings.

### Verification
- Create gate stage requiring discovery_notes + checklist item mandatory; try moving stage.

---

## TASK 06 — CRM kanban badges (BlackShip + Gate incomplete)

### Goal
Show BlackShip hints in CRM kanban.

### Scope
Allowed:
- `views/crm_lead_kanban.xml` (new) OR extend existing view file
- `__manifest__.py` include

### Deliverables
- Inherit CRM kanban view (robust xpath)
- If blackship_stage_id present => badge `BlackShip: <stage>`
- If gate_ok false => badge `Gate incompleto`

### DoD
- Minimal layout impact.
- Strings extractable.

### Verification
- Open pipeline and see badges.

---

## TASK 07 — Wizard “Crea Proposta BlackShip” (lead → sale.order)

### Goal
Create quotations from leads via a guided wizard.

### Scope
Allowed:
- `wizard/create_proposal.py`
- `wizard/__init__.py`
- `views/create_proposal_wizard_views.xml`
- `views/crm_lead_views.xml`
- `__manifest__.py`

### Deliverables
- Transient model `blackship.create_proposal_wizard`
- Button on lead form to open wizard
- Wizard action creates `sale.order`:
  - partner_id required
  - link to lead via `opportunity_id` if available
  - set `is_blackship=True` (ensure field exists by TASK 08; if not yet, create now or guard)

### DoD
- All error strings in `_()`.
- No extra dependencies.

### Verification
- From lead: create quotation and open it.

---

## TASK 08 — sale.order: `is_blackship`, `quote_version`, “Crea revisione”

### Goal
Support BlackShip quotation versioning.

### Scope
Allowed:
- `models/sale_order.py`
- `views/sale_order_views.xml`
- `models/__init__.py`
- `__manifest__.py`

### Deliverables
- Fields:
  - `is_blackship` (Boolean default False)
  - `quote_version` (Integer default 1)
- Method `action_blackship_new_revision()`:
  - copy() order
  - increment quote_version
  - return action to open new record
- UI:
  - show fields in a dedicated group (only visible when is_blackship)
  - button “Crea revisione” only when is_blackship

### DoD
- Translatable labels/messages.

### Verification
- Create revision; version increments.

---

## TASK 09 — Approvals: block confirmation for discount threshold

### Goal
Governance: require approval if discount too high.

### Scope
Allowed:
- `models/blackship_approval.py`
- `models/sale_order.py`
- `views/sale_order_views.xml`
- `security/ir.model.access.csv`
- `__manifest__.py`

### Deliverables
- Model `blackship.approval` with:
  - sale_id, requested_by, status (pending/approved/rejected), comment
- sale.order:
  - One2many approvals
  - Override `action_confirm()`:
    - If is_blackship AND any order_line.discount > DISCOUNT_THRESHOLD (e.g. 20.0)
    - If no approved approval exists -> create pending approval and raise UserError
- UI:
  - Tab "Approvals" with list
  - Approve/Reject buttons restricted to `sales_team.group_sale_manager` (groups on buttons)

### DoD
- Errors translatable `_()`.
- Does not affect non-blackship orders.

### Verification
- Set discount > threshold; try confirm; must block and create approval.

---

## TASK 10 — QWeb PDF report “Offerta BlackShip” + SCSS assets

### Goal
Provide a dedicated PDF quotation for BlackShip.

### Scope
Allowed:
- `report/blackship_quote_report.xml`
- `static/src/scss/report.scss`
- `__manifest__.py`

### Deliverables
- Report action & template for sale.order
- Title: “Offerta BlackShip v<quote_version>”
- Use `web.report_assets_common` to include SCSS
- No absolute URLs, no external assets required

### DoD
- Strings extractable for i18n.
- Report renders.

### Verification
- Print report for a blackship quotation.

---

## TASK 11 — Seed data: default stages

### Goal
Provide initial stage configuration.

### Scope
Allowed:
- `data/blackship_stage_data.xml`
- `__manifest__.py`

### Deliverables
- Create stages:
  - Intake, Qualify, Discovery, Solutioning, Proposal, Negotiation, Commit, Won, Lost
- For a couple of stages set `required_fields` ONLY using fields that exist (e.g. discovery_notes, solution_brief)

### DoD
- Data loads and stages appear in config list.

### Verification
- Update module and see stages.

---

## TASK 12 — i18n completion: update POT + Italian PO + README

### Goal
Ensure translations cover UI and errors.

### Scope
Allowed:
- `i18n/blackship_sale.pot`
- `i18n/it.po`
- `README.md`

### Deliverables
- POT includes all extractable strings
- it.po includes Italian translations for:
  - menus/views labels
  - wizard labels
  - gate blocking errors
  - approval blocking errors
  - report headings

### DoD
- No new user-facing strings left untranslated in it.po (for the module scope).

### Verification
- Load Italian language and confirm UI strings show in Italian.

---

## TASK 13 — Guardrail script: i18n presence + basic anti-hardcode check

### Goal
Prevent regressions in translations and user-facing errors.

### Scope
Allowed:
- `scripts/check_i18n.sh` OR `scripts/check_i18n.py`
- `README.md`

### Deliverables
Script checks:
1) `i18n/blackship_sale.pot` exists
2) `i18n/it.po` exists
3) best-effort grep:
   - detect `UserError("` or `ValidationError("` without `_(` in `models/` and `wizard/`

### DoD
- Script exits non-zero on failures.
- README documents how to run it.

### Verification
- Run script locally; should pass after previous tasks.

---
