# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _


class Test(models.Model):
    _name = 'test'

    code = fields.Char('Code', required=True)
    name = fields.Char('Name', required=True)



