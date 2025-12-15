# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    blackship_discount_threshold = fields.Float(
        string="BlackShip Discount Threshold", help="Maximum allowed discount percentage before approval is required."
    )


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    blackship_discount_threshold = fields.Float(related="company_id.blackship_discount_threshold", readonly=False)
