# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _


class McContract(models.Model):
    """
    Class that represent Contracts.
    """
    _description = 'Contract'
    _inherit = ['doc.state']
    _name = "mc.contract"
    _rec_name = 'code'

    def _get_default_date(self):
        """
        :return: to the date of the day
        """
        date = fields.Date.from_string(fields.Date.today())
        return '{}-01-01'.format(date)

    code = fields.Char(string='Code',
                       required=True,
                       readonly=True,
                       default=_('New'))
    date = fields.Date(string='Creation Date',
                       required=True,
                       index=True,
                       default=_get_default_date)
    description = fields.Text('Description',
                              required=True)
    expiration_date = fields.Date(string='Expiration Date')
    file = fields.Binary(string="Document",
                         required=True)
    filename = fields.Char('File Name',
                           required=True)
    partner_id = fields.Many2one('mc.partner',
                                 required=True)
    supplier = fields.Boolean(string='Is a Vendor',
                              default=lambda self: self.env.context.get('supplier') or False)

    @api.one
    def action_finalized(self):
        """
        Generate the code.
        :return:
        """
        self.code = self.env['ir.sequence'].next_by_code('mc.contract.sequence')
        return super(McContract, self).action_finalized()

