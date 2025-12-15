# -*- coding: utf-8 -*-
from odoo import fields, models


class BlackshipApproval(models.Model):
    _name = "blackship.approval"
    _description = "BlackShip Approval"

    sale_id = fields.Many2one("sale.order", string="Sale Order", required=True, ondelete="cascade")
    requested_by = fields.Many2one(
        "res.users", string="Requested By", required=True, default=lambda self: self.env.user
    )
    status = fields.Selection(
        [
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        string="Status",
        default="pending",
        required=True,
    )
    comment = fields.Text(string="Comment")

    def action_approve(self):
        self.write({"status": "approved"})

    def action_reject(self):
        self.write({"status": "rejected"})
