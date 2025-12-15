# -*- coding: utf-8 -*-
from odoo import _, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_blackship = fields.Boolean(string="BlackShip Proposal", default=False)
    quote_version = fields.Integer(string="Quote Version", default=1)
    approval_ids = fields.One2many(
        "blackship.approval", "sale_id", string="Approvals", copy=False
    )

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

    def _blackship_requires_approval(self):
        self.ensure_one()
        threshold = self.company_id.blackship_discount_threshold
        if threshold is None:
            return False
        return any(line.discount > threshold for line in self.order_line)

    def action_confirm(self):
        for order in self:
            if (
                order.is_blackship
                and order._blackship_requires_approval()
                and not order.approval_ids.filtered(lambda approval: approval.status == "pending")
            ):
                order.env["blackship.approval"].create(
                    {
                        "sale_id": order.id,
                        "requested_by": self.env.user.id,
                        "status": "pending",
                    }
                )
                raise UserError(
                    _(
                        "This BlackShip order has discounts above the allowed threshold and requires approval before confirmation."
                    )
                )

        return super().action_confirm()
