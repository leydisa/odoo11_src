# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, api


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
    @api.depends('price_ids')
    def _compute_current_price(self):
        """
        Calculate the current price of the material.
        :return:
        """
        if len(self.price_ids) > 0:
            self.price_id = self.price_ids.sorted(key='date')[-1]
        else:
            self.price_id = False

    date = fields.Date(string='Date',
                       required=True,
                       default=_get_default_date)
    description = fields.Text(string="Description")
    name = fields.Char(string='Name',
                       required=True)
    price_cuc = fields.Float(string='Current Price(CUC)',
                             related='price_id.price_cuc',
                             readonly=True)
    price_cup = fields.Float(string='Current Price(CUP)',
                             related='price_id.price_cup',
                             readonly=True)
    price_id = fields.Many2one('mc.material.price.trace',
                               string='Price',
                               compute=_compute_current_price,
                               store=True)
    price_ids = fields.One2many('mc.material.price.trace', 'material_id',
                                string='Prices',
                                required=True)
    um = fields.Many2one('um',
                         string='UM',
                         required=True)


class McMaterialPriceTrace(models.Model):
    """
    Class that represent Material.
    """
    _description = 'Price of Material'
    _name = "mc.material.price.trace"

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
                                  ondelete='restrict')
    observation = fields.Text('Observation',
                              required=True)
    price_cuc = fields.Float(string='Price(CUC)',
                             required=True)
    price_cup = fields.Float(string='Price(CUP)',
                             required=True)

    _sql_constraints = [
        ('price_zero', 'CHECK (price_cuc > 0 and price_cup > 0)',
         'The price must be greater than 0.'),
        ('date_unique', 'unique (material_id, date)',
         'Repeated date!'),
    ]

