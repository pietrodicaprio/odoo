# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import _, fields, models
from odoo.exceptions import UserError


class BlackShipStage(models.Model):
    _name = "blackship.stage"
    _description = "BlackShip Stage"
    _order = "sequence, id"

    name = fields.Char(string="Stage Name", required=True, translate=True)
    sequence = fields.Integer(default=10, index=True)
    probability = fields.Float(string="Probability (%)", help=_("Expected probability of reaching this stage."))
    is_gate = fields.Boolean(string="Gate")
    required_fields = fields.Json(string="Required Fields", help=_("Fields required to complete this gate."))
    sla_hours = fields.Integer(string="SLA (Hours)", help=_("Target resolution time for this stage, in hours."))

    def unlink(self):
        raise UserError(_("Deleting BlackShip stages is not allowed."))
