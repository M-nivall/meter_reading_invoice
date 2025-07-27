from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'  # Extend the invoice line model

    # Add custom fields for meter reading
    previous_reading = fields.Float(string="Previous Reading", readonly=True)
    new_reading = fields.Float(string="New Reading")
    actual_usage = fields.Float(string="Actual Usage", compute='_compute_actual_usage', store=True)

    @api.depends('new_reading', 'previous_reading')
    def _compute_actual_usage(self):
        # Calculate actual usage based on readings
        for line in self:
            line.actual_usage = line.new_reading - line.previous_reading

    @api.onchange('actual_usage')
    def _onchange_actual_usage_set_quantity(self):
        # Auto-set the quantity field to match actual usage
        for line in self:
            line.quantity = line.actual_usage

    @api.model
    def create(self, vals):
        # On record creation, fetch the last new reading from previous invoice
        if 'move_id' in vals and 'new_reading' in vals:
            invoice = self.env['account.move'].browse(vals['move_id'])
            if invoice and invoice.partner_id:
                prev_invoice = self.env['account.move'].search([
                    ('partner_id', '=', invoice.partner_id.id),
                    ('move_type', '=', 'out_invoice'),
                    ('state', '=', 'posted'),
                    ('id', '!=', invoice.id),
                ], limit=1, order='date desc')
                if prev_invoice and prev_invoice.invoice_line_ids:
                    # Set the previous reading from last invoice
                    vals['previous_reading'] = prev_invoice.invoice_line_ids[-1].new_reading
        return super(AccountMoveLine, self).create(vals)
