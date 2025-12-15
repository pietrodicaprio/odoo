# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_blackship = fields.Boolean(string="BlackShip Proposal", default=False)
