# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import datetime

from odoo import api, fields, models, tools, SUPERUSER_ID, _


# class Partner(models.Model):
#     """
#
#     """
#     _description = 'Contact'
#     _name = "res.partner"
#
#     # def _get_default_date(self):
#     #     year = fields.Date.from_string(fields.Date.today()).strftime('%Y')
#     #     return '{}-01-01'.format(year)
#
#     code = fields.Char(string='Code',
#                        required=True)
#     date = fields.Date(index=True,
#                        # default=_get_default_date
#                        )
#     image = fields.Binary("Image",
#                           attachment=True,
#                           help="This field holds the image used as avatar for this contact, limited to 1024x1024px" )
#     name = fields.Char(index=True,
#                        required=True)
#     email = fields.Char(string='Email')
#     phone = fields.Char()
#     state = fields.Selection([('active', 'Active'),
#                               ('inactive', 'Inactive')],
#                              string='State',
#                              default='active')
#     supplier = fields.Boolean(string='Is a Vendor',
#                               default=lambda self: self.env.context.get('supplier') or False,
#                               help="Check this box if this contact is a vendor. If it's not checked, purchase "
#                                    "people will not see it when encoding a purchase order.")

    # _sql_constraints = [
    #     ('check_name', "CHECK( (type='contact' AND name IS NOT NULL) or (type!='contact') )", 'Contacts require a name.'),
    # ]

