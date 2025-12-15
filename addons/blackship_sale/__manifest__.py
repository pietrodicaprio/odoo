# -*- coding: utf-8 -*-
{
    "name": "BlackShip Sales",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "summary": "BlackShip Sales customizations",
    "depends": ["crm", "sale", "contacts", "account"],
    "data": [
        "security/ir.model.access.csv",
        "views/blackship_stage_views.xml",
        "views/blackship_checklist_views.xml",
    ],
    "application": True,
    "license": "LGPL-3",
}
