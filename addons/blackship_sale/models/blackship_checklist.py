# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, fields, models
from odoo.exceptions import UserError


class BlackShipChecklistItem(models.Model):
    _name = "blackship.checklist.item"
    _description = "BlackShip Checklist Item"
    _order = "sequence, id"

    lead_id = fields.Many2one("crm.lead", string="Lead", required=True, ondelete="cascade")
    stage_id = fields.Many2one("blackship.stage", string="Stage")
    name = fields.Char(string="Name", required=True, translate=True)
    is_done = fields.Boolean(string="Done")
    mandatory = fields.Boolean(string="Mandatory", default=True)
    sequence = fields.Integer(string="Sequence", default=10)

    def unlink(self):
        raise UserError(_("Deleting checklist items is not allowed."))


class CrmLead(models.Model):
    _inherit = "crm.lead"

    blackship_checklist_ids = fields.One2many(
        "blackship.checklist.item",
        "lead_id",
        string="BlackShip Checklist",
    )
