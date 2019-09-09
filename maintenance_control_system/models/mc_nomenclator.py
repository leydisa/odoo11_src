# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, api


class DocState(models.Model):
    """
    Class to represent the document states.
    """
    _description = 'Document State'
    _name = "doc.state"

    state = fields.Selection([('edition', 'In Edition'),
                              ('finalized', 'Finalized')],
                             string="Status",
                             default='edition')

    @api.one
    def action_finalized(self):
        """
        Sets document to finalized state.
        :return:
        """
        self.state = 'finalized'


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


class McEquipment(models.Model):
    """
    Class that represent hardware.
    """
    _description = 'Equipment'
    _name = "mc.equipment"

    def _get_default_date(self):
        """
        :return: to the date of the day
        """
        date = fields.Date.from_string(fields.Date.today())
        return '{}-01-01'.format(date)

    @api.one
    @api.depends('material_expense_ids')
    def _compute_total(self):
        """
        Calculate the current price of the material.
        :return:
        """
        self.total_cuc = sum([x.price_cuc * x.factor for x in self.material_expense_ids])
        self.total_cup = sum([x.price_cup * x.factor for x in self.material_expense_ids])

    date = fields.Date(string='Date',
                       required=True,
                       default=_get_default_date)
    description = fields.Text(string="Description")
    name = fields.Char(string='Name',
                       required=True)
    material_expense_ids = fields.One2many('mc.equipment.material.expense', 'equipment_id',
                                           string='Material Expenditure Per Equipment')
    total_cuc = fields.Float(string='Total (CUC)',
                             compute=_compute_total,
                             store=True)
    total_cup = fields.Float(string='Total (CUP)',
                             compute=_compute_total,
                             store=True)


class McEquipmentMaterialExpense(models.Model):
    """
    Class that represent material expenditure per equipment.
    """
    _description = 'Material expenditure per equipment'
    _name = "mc.equipment.material.expense"

    @api.one
    @api.depends('factor_ids')
    def _compute_current_factor(self):
        """
        Calculate the current price of the material.
        :return:
        """
        if len(self.factor_ids) > 0:
            self.factor_id = self.factor_ids.sorted(key='date')[-1]
        else:
            self.factor_id = False

    equipment_id = fields.Many2one('mc.equipment')
    factor = fields.Float(string='Factor',
                          related='factor_id.factor',
                          readonly=True)
    factor_id = fields.Many2one('mc.equipment.material.factor',
                                 string='Trace Factor',
                                compute=_compute_current_factor,
                                store=True)
    factor_ids = fields.One2many('mc.equipment.material.factor', 'expense_id',
                                 string='Factor Trace',
                                 required=True)
    material_id = fields.Many2one('mc.material',
                                  string='Material',
                                  required=True)
    price_cuc = fields.Float(string='Price(CUC)',
                             related='material_id.price_cuc')
    price_cup = fields.Float(string='Price(CUP)',
                             related='material_id.price_cup')

    _sql_constraints = [
        ('material_uniq', 'unique (equipment_id, material_id)',
         'A material cannot be repeated per equipment!')
    ]


class McEquipmentMaterialFactor(models.Model):
    """
    Class that represent material expenditure per equipment.
    """
    _description = 'Material factor per equipment'
    _name = "mc.equipment.material.factor"

    def _get_default_date(self):
        """
        :return: to the date of the day
        """
        date = fields.Date.from_string(fields.Date.today())
        return '{}-01-01'.format(date)

    date = fields.Date(string='Date',
                       required=True,
                       default=_get_default_date)
    expense_id = fields.Many2one('mc.equipment.material.expense',
                                 ondelete='restrict')
    factor = fields.Float(string='Factor')
    observation = fields.Text('Observation',
                              required=True)

    _sql_constraints = [
        ('date_uniq', 'unique (expense_id, date)',
         'Repeated date.!')
    ]