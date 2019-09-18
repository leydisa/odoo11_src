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

    @api.one
    @api.depends('line_ids')
    def _compute_coste(self):
        """
        Calculate the current price of the material.
        :return:
        """
        self.coste_cuc = sum([x.qty * x.equipment_id.total_cuc for x in self.line_ids])
        self.coste_cup = sum([x.qty * x.equipment_id.total_cup for x in self.line_ids])

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
    observation = fields.Text('Observation',
                              required=True)
    coste_cuc = fields.Float(string='Coste (CUC)',
                             compute=_compute_coste,
                             store=True)
    coste_cup = fields.Float(string='Coste (CUP)',
                             compute=_compute_coste,
                             store=True)

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

    _sql_constraints = [
        ('name_ref_uniq', 'unique (name, product_id)', 'The combination of serial number and product must be unique !'),
    ]