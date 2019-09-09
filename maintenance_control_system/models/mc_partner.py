# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _


class McPartner(models.Model):
    """
    Class that represent customer and supplier.
    """
    _description = 'Partner'
    _name = "mc.partner"

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
    date = fields.Date(string='Creation Date',
                       required=True,
                       index=True,
                       default=_get_default_date)
    email = fields.Char(string='Email',
                        required=True)
    image = fields.Binary("Image",
                          attachment=True,
                          help="This field holds the image used as avatar for this contact, limited to 1024x1024px")
    name = fields.Char(index=True,
                       required=True)
    phone = fields.Char(string='Phone',
                        required=True)
    active = fields.Boolean(default=True)
    supplier = fields.Boolean(string='Is a Vendor',
                              default=lambda self: self.env.context.get('supplier') or False)
    type = fields.Selection([('internal', 'Internal'),
                             ('external', 'External')],
                            string='Type')

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Name must be unique!'),
    ]

    @api.model
    def create(self, vals):
        """
        Generate the code.
        :param vals:
        :return:
        """
        if vals['supplier']:
            vals['code'] = self.env['ir.sequence'].next_by_code('mc.supplier.sequence')
        else:
            vals['code'] = self.env['ir.sequence'].next_by_code('mc.customer.sequence')
        return super(McPartner, self).create(vals)


