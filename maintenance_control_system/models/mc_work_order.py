# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _


class McWorkOrder(models.Model):
    """
    Class that represent customer and supplier.
    """
    _description = 'Work Order'
    _name = "mc.work.order"

    def _get_default_date(self):
        """
        :return: to the date of the day
        """
        year = fields.Date.from_string(fields.Date.today()).strftime('%Y')
        return '{}-01-01'.format(year)

    code = fields.Char(string='Code',
                       required=True,
                       readonly=True,
                       default=_('New'))
    date = fields.Date(string='Creation Date',
                       required=True,
                       index=True,
                       default=_get_default_date)
    partner_id = fields.Many2one('mc.partner',
                                string='Customer',
                                domain="[('supplier', '=', False)]")


    @api.model
    def create(self, vals):
        """
        Generate the code.
        :param vals:
        :return:
        """
        vals['code'] = self.env['ir.sequence'].next_by_code('mc.work.order.sequence')
        return super(McWorkOrder, self).create(vals)


