# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _


class McContract(models.Model):
    """
    Class that represent Contracts.
    """
    _description = 'Contract'
    _name = "mc.contract"

    def _get_default_date(self):
        """
        :return: to the date of the day
        """
        year = fields.Date.from_string(fields.Date.today()).strftime('%Y')
        return '{}-01-01'.format(year)

    code = fields.Char(string='Code',
                       required=True)
    date = fields.Date(string='Creation Date',
                       required=True,
                       index=True,
                       default=_get_default_date)
    description = fields.Text('Description',
                              required=True)
    expiration_date = fields.Date(string='Expiration Date')
    file = fields.Binary(string="Documento",
                         required=True)
    filename = fields.Char('File Name',
                           required=True)
    partner_id = fields.Many2one('mc.partner',
                                 string='Customer',
                                 required=True,
                                 domain="[('supplier', '=', False)]")

