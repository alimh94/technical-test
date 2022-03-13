# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _

class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'
    _description = "Adding Tax Amount to Invoice Lines"

    tax_amount = fields.Monetary(string='Total Amount', compute='_compute_tax_amount', store=True, readonly=True,
                                      currency_field='currency_id')


    @api.depends('price_subtotal', 'price_total')
    def _compute_tax_amount(self):
        for record in self:
            record.tax_amount = record.price_total - record.price_subtotal