# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):

    _inherit = 'account.move'
    _description = "Override create function to create payment"

    @api.model
    def action_post(self):
        self._post(soft=False)
        payment_term_id = self.env['account.payment.term'].search([('name', '=', 'Immediate Payment')], limit=1)
        for record in self:
            if record.invoice_payment_term_id == payment_term_id:
                for record in self:
                    journal_id = self.env['account.journal'].search([('name', '=', 'Cash')], limit=1).id
                    if journal_id:
                        payment_info= {
                        'partner_id': record.partner_id.id,
                        'payment_type': 'inbound',
                        'partner_type': 'customer',
                        'amount': record.amount_residual,
                        'ref': record.name,
                        'journal_id': journal_id,
                         }
                        return self.env['account.payment'].create(payment_info)
                    else:
                        raise UserError(_("There is no payment method created for cash payout please create it."))
