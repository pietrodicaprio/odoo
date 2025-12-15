# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class BlackshipCreateProposalWizard(models.TransientModel):
    _name = "blackship.create.proposal.wizard"
    _description = "BlackShip Create Proposal Wizard"

    lead_id = fields.Many2one(
        "crm.lead",
        string="Lead",
        required=True,
        default=lambda self: self._default_lead_id(),
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        required=True,
        default=lambda self: self._default_partner_id(),
    )
    pricelist_id = fields.Many2one("product.pricelist", string="Pricelist")
    note = fields.Html(string="Note")

    @api.model
    def _default_lead_id(self):
        return self.env.context.get("default_lead_id") or self.env.context.get("active_id")

    @api.model
    def _default_partner_id(self):
        lead_id = self._default_lead_id()
        if not lead_id:
            return False
        lead = self.env["crm.lead"].browse(lead_id)
        return lead.partner_id.id

    def action_create_proposal(self):
        self.ensure_one()

        if not self.lead_id:
            raise UserError(_("Please select a lead."))

        if not self.partner_id:
            raise UserError(_("Please select a customer."))

        partner_addresses = self.partner_id.address_get(["delivery", "invoice"])
        lead_pricelist = getattr(self.lead_id, "pricelist_id", False)
        pricelist = self.pricelist_id or lead_pricelist or self.partner_id.property_product_pricelist

        order_vals = {
            "partner_id": self.partner_id.id,
            "partner_invoice_id": partner_addresses.get("invoice") or self.partner_id.id,
            "partner_shipping_id": partner_addresses.get("delivery") or self.partner_id.id,
            "pricelist_id": pricelist.id if pricelist else False,
            "opportunity_id": self.lead_id.id,
            "company_id": self.lead_id.company_id.id or self.env.company.id,
            "team_id": self.lead_id.team_id.id,
            "user_id": self.lead_id.user_id.id,
            "note": self.note,
            "is_blackship": True,
        }

        order = self.env["sale.order"].create(order_vals)

        return {
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "res_id": order.id,
            "view_mode": "form",
            "target": "current",
        }
