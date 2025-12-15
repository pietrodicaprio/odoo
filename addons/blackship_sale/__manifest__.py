# -*- coding: utf-8 -*-
{
    "name": "BlackShip Sales",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "summary": "BlackShip Sales customizations",
    "depends": ["crm", "sale", "sale_crm", "contacts", "account"],
    "data": [
        "security/ir.model.access.csv",
        "views/blackship_stage_views.xml",
        "views/blackship_checklist_views.xml",
        "views/blackship_create_proposal_wizard_views.xml",
        "views/sale_order_views.xml",
    ],
    "application": True,
    "license": "LGPL-3",
}
