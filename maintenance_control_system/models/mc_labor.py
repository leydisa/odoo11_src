# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, api


class McLabor(models.Model):
    """
    Class that represent Labor.
    """
    _description = 'Labor Costs'
    _name = "mc.labor"

    def _get_default_date(self):
        """
        :return: to the date of the day
        """
        date = fields.Date.from_string(fields.Date.today())
        return '{}-01-01'.format(date)

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

