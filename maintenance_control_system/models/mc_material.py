# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class McMaterial(models.Model):
    """
    Class that represent Material.
    """
    _description = 'Material'
    _name = "mc.material"

    def _get_default_date(self):
        """
        :return: to the date of the day
        """
        date = fields.Date.from_string(fields.Date.today())
        return '{}-01-01'.format(date)

    @api.one
    @api.depends('coste_ids')
    def _compute_current_coste(self):
        """
        Calculate the current price of the material.
        :return:
        """
        if len(self.coste_ids) > 0:
            self.coste_id = self.coste_ids.sorted(key='date')[-1]
        else:
            self.coste_id = False

    @api.constrains('coste_id')
    def _check_data(self):
        """
        It is checked that at least one of the 2 costs must be greater than 0.
        :return:
        """
        if not (self.coste_id.coste_cuc > 0 or self.coste_id.coste_cup > 0):
            raise ValidationError(_('The price must be greater than 0.'))

    date = fields.Date(string='Date',
                       required=True,
                       default=_get_default_date)
    description = fields.Text(string="Description")
    name = fields.Char(string='Name',
                       required=True)
    coste_cuc = fields.Float(string='CUC',
                             related='coste_id.coste_cuc',
                             readonly=True)
    coste_cup = fields.Float(string='CUP',
                             related='coste_id.coste_cup',
                             readonly=True)
    coste_id = fields.Many2one('mc.material.coste',
                               string='Price',
                               compute=_compute_current_coste,
                               ondelete='restrict',
                               store=True)
    coste_ids = fields.One2many('mc.material.coste', 'material_id',
                                string='Prices',
                                required=True)
    um = fields.Many2one('um',
                         string='UM',
                         required=True,
                         ondelete='restrict')
    user_id = fields.Many2one('res.users',
                              string='User',
                              readonly=True,
                              default=lambda self: self.env.user.id)


class McMaterialCoste(models.Model):
    """
    Class that represent Material.
    """
    _description = 'Coste of Material'
    _name = "mc.material.coste"

    def _get_default_date(self):
        """
        :return: to the date of the day
        """
        date = fields.Date.from_string(fields.Date.today())
        return '{}-01-01'.format(date)

    date = fields.Date(string='Date',
                       required=True,
                       default=_get_default_date)
    material_id = fields.Many2one('mc.material',
                                  ondelete='cascade')
    observation = fields.Text('Observation',
                              required=True)
    coste_cuc = fields.Float(string='CUC',
                             required=True)
    coste_cup = fields.Float(string='CUP',
                             required=True)
    user_id = fields.Many2one('res.users',
                              string='User',
                              readonly=True,
                              default=lambda self: self.env.user.id)

    _sql_constraints = [
        ('coste_zero', 'CHECK (coste_cuc > 0 or coste_cup > 0)',
         'The coste must be greater than 0.'),
        ('date_unique', 'unique (material_id, date)',
         'Repeated date!'),
    ]

