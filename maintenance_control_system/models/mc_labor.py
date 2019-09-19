# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, api


class McLabor(models.Model):
    """
    Class that represent Labor Coste.
    """
    _description = 'Labor'
    _name = "mc.labor"

    @api.one
    @api.depends('coste_ids')
    def _compute_last_coste(self):
        """
        Calculate the current coste of the labor.
        :return:
        """
        if len(self.coste_ids) > 0:
            self.coste_id = self.coste_ids.sorted(key='date')[-1]
        else:
            self.coste_id = False

    coste_cuc = fields.Float(string='Current Coste (CUC)',
                             related='coste_id.coste_cuc',
                             readonly=True)
    coste_cup = fields.Float(string='Current Coste(CUP)',
                             related='coste_id.coste_cup',
                             readonly=True)
    coste_id = fields.Many2one('mc.labor.line',
                               string='Last Coste',
                               compute=_compute_last_coste,
                               store=True)
    coste_ids = fields.One2many('mc.labor.line', 'labor_id',
                                string='Costes',
                                required=True)


class McLaborLine(models.Model):
    """
    Class that represent Work Force Line.
    """
    _description = 'Costes of Labor'
    _name = "mc.labor.line"

    def _get_default_date(self):
        """
        :return: to the date of the day
        """
        date = fields.Date.from_string(fields.Date.today())
        return '{}-01-01'.format(date)

    labor_id = fields.Many2one('mc.labor',
                               ondelete='restrict')
    date = fields.Date(string='Date',
                       required=True,
                       default=_get_default_date)
    coste_cuc = fields.Float(string='Coste (CUC)',
                             required=True)
    coste_cup = fields.Float(string='Coste (CUP)',
                             required=True)

    _sql_constraints = [
        ('coste_zero', 'CHECK (coste_cuc > 0 and coste_cup > 0)', 'The coste must be greater than 0.'),
        ('date_unique', 'unique (date)', 'Repeated date!'),
    ]

