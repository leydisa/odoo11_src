# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime
from odoo import fields, models, api
from odoo.exceptions import ValidationError


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
    _rec_name = "year"

    def add_maintenance_provided(self, date, cuc, cup):
        """

        :param cuc:
        :param cup:
        :return:
        """
        year = fields.Datetime.from_string(date).year
        budget = self.search([('year', '=', year)], limit=1)
        if len(budget) == 0:
            raise ValidationError(_('Define the budget for the current year.'))
        else:
            budget.write({'used_provided_cuc':  budget.used_provided_cuc + cuc,
                          'percent_provided_cuc':  ((budget.used_provided_cuc + cuc) * 100)
                                                   / budget.budget_provided_cuc,
                          'used_provided_cup':  budget.used_provided_cup + cup,
                          'percent_provided_cup':  ((budget.used_provided_cup + cup) * 100)
                                                   / budget.budget_provided_cup})

    def add_maintenance_received(self, date, cuc, cup):
        """

        :param cuc:
        :param cup:
        :return:
        """
        year = fields.Datetime.from_string(date).year
        budget = self.search([('year', '=', year)], limit=1)
        if len(budget) == 0:
            raise ValidationError(_('Define the budget for the current year.'))
        else:
            budget.write({'used_received_cuc':  budget.used_received_cuc + cuc,
                          'percent_received_cuc':  ((budget.used_received_cuc + cuc) * 100)
                                                   / budget.budget_received_cuc,
                          'used_received_cup':  budget.used_received_cup + cup,
                          'percent_received_cup':  ((budget.used_received_cup + cup) * 100)
                                                   / budget.budget_received_cup})

    def _get_default_year(self):
        """
        :return: to the current year
        """
        return str(datetime.datetime.now().year)

    year = fields.Selection(_get_years(),
                            string='Year',
                            required=True,
                            default=_get_default_year)
    budget_provided_cuc = fields.Float("CUC",
                                       required=True)
    budget_provided_cup = fields.Float("CUP",
                                       required=True)
    budget_received_cuc = fields.Float("CUC",
                                       required=True)
    budget_received_cup = fields.Float("CUP",
                                       required=True)
    used_provided_cuc = fields.Float("Used",
                                     readonly=True)
    used_provided_cup = fields.Float("Used",
                                     readonly=True)
    used_received_cuc = fields.Float("Used",
                                     readonly=True)
    used_received_cup = fields.Float("Used",
                                     readonly=True)
    percent_provided_cuc = fields.Float("Percent",
                                        readonly=True)
    percent_provided_cup = fields.Float("Percent",
                                        readonly=True)
    percent_received_cuc = fields.Float("Percent",
                                        readonly=True)
    percent_received_cup = fields.Float("Percent",
                                        readonly=True)

    _sql_constraints = [
        ('budget_zero', 'CHECK (budget_provided_cuc > 0 and budget_provided_cup > 0'
                        'and budget_received_cuc > 0 and budget_received_cup > 0)',
         'The coste must be greater than 0.'),
        ('year_unique', 'unique(year)', 'Repeated year!'),
    ]