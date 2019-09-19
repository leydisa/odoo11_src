# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime
from odoo import fields, models, api


def _get_years():
    year_list = []
    for i in range(2018, datetime.datetime.now().year + 1):
        year_list.append((str(i), str(i)))
    return year_list

class McBudget(models.Model):
    """
    Class that represent Annual Budget.
    """
    _description = 'Annual Budget'
    _name = "mc.budget"

    def _get_default_year(self):
        """
        :return: to the current year
        """
        return str(datetime.datetime.now().year)

    year = fields.Selection(_get_years(),
                            string='Year',
                            required=True,
                            default=_get_default_year)
    maintenance_budget_provided_cuc = fields.Float("CUC",
                                                   required=True)
    maintenance_budget_provided_cup = fields.Float("CUP",
                                                   required=True)
    maintenance_budget_received_cuc = fields.Float("CUC",
                                                   required=True)
    maintenance_budget_received_cup = fields.Float("CUP",
                                                   required=True)

    _sql_constraints = [
        ('budget_zero', 'CHECK (maintenance_budget_provided_cuc > 0 and maintenance_budget_provided_cup > 0'
                        'and maintenance_budget_received_cuc > 0 and maintenance_budget_received_cup > 0)',
         'The coste must be greater than 0.'),
        ('year_unique', 'unique(year)', 'Repeated year!'),
    ]