# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


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

    @api.model
    def _default_current_labor_coste(self):
        """
        Calculate the current price of labor.
        :return:
        """
        labor = self.env['mc.labor'].search([], limit=1, order='date desc')
        if len(labor) == 0:
            raise ValidationError(_('Define the cost of labor.'))
        else:
            return labor

    @api.one
    @api.depends('line_ids', 'labor_hours', 'labor_days')
    def _compute_coste(self):
        """
        Calculate the current price of the material.
        :return:
        """
        self.coste_cuc = sum([x.qty * x.equipment_id.coste_cuc for x in self.line_ids])
        self.coste_cuc += self.labor_days * self.labor_hours * self.labor_id.coste_cuc
        self.coste_cup = sum([x.qty * x.equipment_id.coste_cup for x in self.line_ids])
        self.coste_cup += self.labor_days * self.labor_hours * self.labor_id.coste_cup
        self.mt = self.coste_cuc + self.coste_cup

    @api.constrains('datetime_start', 'datetime_stop')
    def _check_data(self):
        if (fields.Datetime.from_string(self.datetime_start) >= fields.Datetime.from_string(self.datetime_stop)):
            raise ValidationError(_('Contract start date must be less than contract end date.'))

    code = fields.Char(string='Code',
                       required=True,
                       readonly=True,
                       default=_('New'))
    date = fields.Date(string='Creation Date',
                       required=True,
                       index=True,
                       default=_get_default_date)
    datetime_start = fields.Datetime(string="",
                                     required=True)
    datetime_stop = fields.Datetime(string="",
                                    required=True)
    partner_id = fields.Many2one('mc.partner')
    contract_id = fields.Many2one('mc.contract',
                                  string='Contract',
                                  domain="[('partner_id', '=', partner_id), "
                                         "('state', '=', 'finalized')]")
    province_id = fields.Many2one(string='Province',
                                  related='partner_id.province_id',
                                  readonly=True)
    entity_id = fields.Many2one('mc.partner',
                                string='Entidad',
                                domain="[('supplier', '=', False), "
                                       "('type', '=', 'internal')]")
    supplier = fields.Boolean(string='Is a Vendor',
                              default=lambda self: self.env.context.get('supplier') or False)
    type = fields.Selection([('internal', 'Internal'),
                             ('external', 'External')],
                            string='Type',
                            default=lambda self: self.env.context.get('type') or False)
    observation = fields.Text('Observation',
                              required=True)
    invoice = fields.Binary(string='Invoice')
    invoice_filename = fields.Char('Invoice')
    line_ids = fields.One2many('mc.maintenance.line', 'maintenance_id',
                               string='Lines')
    coste_cuc = fields.Float(string='CUC',
                             compute=_compute_coste,
                             store=True)
    coste_cup = fields.Float(string='CUP',
                             compute=_compute_coste,
                             store=True)
    mt = fields.Float(string='MT',
                      compute=_compute_coste,
                      store=True)
    workorder_id = fields.Many2one('mc.work.order',
                                   'Work Order',
                                   readonly=True)
    labor_id = fields.Many2one('mc.labor',
                               string="Labor",
                               default=_default_current_labor_coste,
                               ondelete='restrict')
    labor_days = fields.Float('Worked Days',
                              required=True)
    labor_hours = fields.Float('Hours Worked per Day',
                               required=True)

    _sql_constraints = [
        ('labor_days_zero', 'CHECK (labor_days)', 'The labor days must be greater than 0.'),
        ('labor_hours_zero', 'CHECK (labor_hours)', 'The labor hours must be greater than 0.'),
    ]

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
            self.code = self.env['ir.sequence'].next_by_code('mc.%s.maintenance.provided.sequence' % self.type)
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
    coste_cuc = fields.Float(string='CUC)',
                             related='equipment_id.coste_cuc',
                             readonly=True)
    coste_cup = fields.Float(string='CUP',
                             related='equipment_id.coste_cup',
                             readonly=True)

    _sql_constraints = [
        ('name_ref_uniq', 'unique (name, product_id)', 'The combination of serial number and product must be unique !'),
    ]