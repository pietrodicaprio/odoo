# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_blackship = fields.Boolean(string="BlackShip Proposal", default=False)
    quote_version = fields.Integer(string="Quote Version", default=1)

    def action_blackship_new_revision(self):
        self.ensure_one()

        new_order = self.copy({"quote_version": (self.quote_version or 1) + 1})

        return {
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "res_id": new_order.id,
            "view_mode": "form",
            "target": "current",
        }
