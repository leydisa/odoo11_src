# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _


class McMaintenance(models.Model):
    """
    Maintenance.
    """
    _description = 'Maintenance'
    _inherit = ['doc.state']
    _name = 'mc.maintenance'
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

    line_ids = fields.One2many('mc.maintenance.line', 'maintenance_id',
                               string='Lines')
    partner_id = fields.Many2one('mc.partner',
                                 string='Customer',
                                 required=True,
                                 domain="[('supplier', '=', supplier)]")
    supplier = fields.Boolean(string='Is a Vendor',
                              default=lambda self: self.env.context.get('supplier') or False)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.contract_id = False

    @api.one
    def action_finalized(self):
        """
        Generate the code.
        :return:
        """
        if self.supplier:
            self.code = self.env['ir.sequence'].next_by_code('mc.maintenance.received.sequence')
        else:
            self.code = self.env['ir.sequence'].next_by_code('mc.maintenance.provided.sequence')
        return super(McMaintenance, self).action_finalized()


class McMaintenanceLine(models.Model):
    """
    Class Maintenance Line.
    """
    _description = 'Maintenance Line'
    _name = "mc.maintenance.line"

    maintenance_id = fields.Many2one('mc.maintenance',
                                     ondelete='restrict')
    equipment_id = fields.Many2one('mc.equipment',
                                   required=True)
    qty = fields.Integer(string='Quantity')
    total_cuc = fields.Float(string='Current Price(CUC)',
                             related='equipment_id.total_cuc',
                             readonly=True)
    total_cup = fields.Float(string='Current Price(CUP)',
                             related='equipment_id.total_cup',
                             readonly=True)

