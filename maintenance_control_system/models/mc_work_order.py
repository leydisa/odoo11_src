# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _


class McWorkOrder(models.Model):
    """
    Class that represent Work Order.
    """
    _description = 'Work Order'
    _inherit = ['doc.state']
    _name = 'mc.work.order'
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
    contract_id = fields.Many2one('mc.contract',
                                  string='Contract',
                                  required=True,
                                  domain="[('partner_id', '=', partner_id)]")
    date = fields.Date(string='Creation Date',
                       required=True,
                       index=True,
                       default=_get_default_date)
    file = fields.Binary(string='Document')
    filename = fields.Char('File Name')
    line_ids = fields.One2many('mc.work.order.line', 'workorder_id',
                               string='Lines')
    partner_id = fields.Many2one('mc.partner',
                                 string='Customer',
                                 required=True,
                                 domain="[('supplier', '=', False)]")

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.contract_id = False

    @api.one
    def action_finalized(self):
        """
        Generate the code.
        :return:
        """
        self.code = self.env['ir.sequence'].next_by_code('mc.work.order.sequence')
        return super(McWorkOrder, self).action_finalized()


class McWorkOrderLine(models.Model):
    """
    Class that represent Work Order Line.
    """
    _description = 'Work Order Line'
    _name = "mc.work.order.line"

    equipment_id = fields.Many2one('mc.equipment',
                                   required=True)
    inventory_no = fields.Char(string='Inventory No.')
    local = fields.Text(string='Local',
                        required=True)
    observation = fields.Text('Observation')
    serial_no = fields.Text(string='Serial No.')
    workorder_id = fields.Many2one('mc.work.order',
                                   ondelete='restrict')
