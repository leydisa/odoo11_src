# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


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

    @api.constrains('maintenance_id', 'line_ids')
    def _check_data(self):
        """
        Check that it cannot be saved without the detail of the lines.
        :return:
        """
        if len(self.line_ids) == 0:
            raise ValidationError(_('Missing work order detail.'))

    code = fields.Char(string='Code',
                       required=True,
                       readonly=True,
                       default=_('New'))
    contract_id = fields.Many2one('mc.contract',
                                  string='Contract',
                                  related='maintenance_id.contract_id',
                                  readonly=True,
                                  store=True)
    date = fields.Date(string='Creation Date',
                       required=True,
                       index=True,
                       default=_get_default_date)
    file = fields.Binary(string='Document')
    filename = fields.Char('File Name')
    line_ids = fields.One2many('mc.work.order.line', 'workorder_id',
                               required=True,
                               string='Lines')
    partner_id = fields.Many2one('mc.partner',
                                 string='Customer',
                                 related='maintenance_id.partner_id',
                                 readonly=True,
                                 store=True)
    maintenance_id = fields.Many2one('mc.maintenance',
                                     string='Maintenance',
                                     required=True,
                                     domain="[('supplier', '=', False), "
                                            "('type', '=', 'external'), "
                                            "('workorder_id', '=', False)]")
    user_id = fields.Many2one('res.users',
                              string='Created by',
                              readonly=True,
                              default=lambda self: self.env.user.id)

    @api.one
    def action_finalized(self):
        """
        Assign the work order to maintenance.
        Generate the code.
        :return:
        """
        # Assign the work order to maintenance.
        maintenance = self.env['mc.maintenance'].browse(self.maintenance_id.id)
        if maintenance.workorder_id:
            raise ValidationError(_('The maintenance already has an assigned work order.'))
        else:
            maintenance.write({'workorder_id': self.id})
        # Generate the code.
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
    inventory_no = fields.Char(string='Inventory No.',
                               required=True)
    local = fields.Text(string='Local',
                        required=True)
    observation = fields.Text('Observation')
    serial_no = fields.Text(string='Serial No.',
                            required=True)
    workorder_id = fields.Many2one('mc.work.order',
                                   ondelete='cascade')
