# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class McProvince(models.Model):
    """
    Class that represent Province.
    """
    _description = 'Province'
    _name = "mc.province"

    name = fields.Char(string='Name',
                       required=True)


class McEntity(models.Model):
    """
    Class that represent Entity.
    """
    _description = 'Entity'
    _name = "mc.entity"

    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    name = fields.Char(string='Name',
                       required=True)


class UM(models.Model):
    """
    Class that represent Unit of Measurement.
    """
    _description = 'UM'
    _name = "um"

    code = fields.Char(string='Code',
                       required=True)
    name = fields.Char(string='Name',
                       required=True)


class McMaterial(models.Model):
    """
    Class that represent Material.
    """
    _description = 'Material'
    _name = "mc.material"

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string="Description")
    price_ids = fields.One2many('mc.material.price', 'material_id',
                                string='Prices')
    um = fields.Many2one('um',
                         string='UM',
                         required=True)


class McMaterialPrice(models.Model):
    """
    Class that represent Material.
    """
    _description = 'Price of Material'
    _name = "mc.material.price"

    def _get_default_date(self):
        """
        :return: to the date of the day
        """
        year = fields.Date.from_string(fields.Date.today()).strftime('%Y')
        return '{}-01-01'.format(year)

    date = fields.Date(string='Date',
                       required=True,
                       default=_get_default_date)
    material_id = fields.Many2one('mc.material',
                                  ondelete='restrict')
    price_cuc = fields.Float(string='Price(CUC)')
    price_cup = fields.Float(string='Price(CUP)')
