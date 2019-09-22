# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


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
    @api.depends('material_ids')
    def _compute_coste(self):
        """
        Calculate the current coste of the material.
        :return:
        """
        self.coste_cuc = sum([x.coste_cuc * x.factor for x in self.material_ids])
        self.coste_cup = sum([x.coste_cup * x.factor for x in self.material_ids])

    @api.constrains('material_ids')
    def _check_data(self):
        """
        It is checked that at least one of the 2 costs must be greater than 0.
        :return:
        """
        if not (self.coste_cuc > 0 or self.coste_cup > 0):
            raise ValidationError(_('The price must be greater than 0.'))

    date = fields.Date(string='Date',
                       required=True,
                       default=_get_default_date)
    description = fields.Text(string="Description")
    name = fields.Char(string='Name',
                       required=True)
    material_ids = fields.One2many('mc.equipment.material', 'equipment_id',
                                   string='Material Expenditure Per Equipment')
    coste_cuc = fields.Float(string='CUC',
                             compute=_compute_coste,
                             store=True)
    coste_cup = fields.Float(string='CUP',
                             compute=_compute_coste,
                             store=True)


class McEquipmentMaterial(models.Model):
    """
    Class that represent material expenditure per equipment.
    """
    _description = 'Material expenditure per equipment'
    _name = "mc.equipment.material"

    @api.one
    @api.depends('factor_ids')
    def _compute_current_factor(self):
        """
        Calculate the current coste of the material.
        :return:
        """
        if len(self.factor_ids) > 0:
            self.factor_id = self.factor_ids.sorted(key='date')[-1]
        else:
            self.factor_id = False

    equipment_id = fields.Many2one('mc.equipment',
                                   ondelete='cascade')
    factor = fields.Float(string='Factor',
                          related='factor_id.factor',
                          readonly=True)
    factor_id = fields.Many2one('mc.equipment.material.factor',
                                 string='Trace Factor',
                                compute=_compute_current_factor,
                                store=True)
    factor_ids = fields.One2many('mc.equipment.material.factor', 'parent_id',
                                 string='Factor Trace',
                                 required=True)
    material_id = fields.Many2one('mc.material',
                                  string='Material',
                                  required=True,
                                  ondelete='restrict')
    coste_cuc = fields.Float(string='CUC',
                             related='material_id.coste_cuc')
    coste_cup = fields.Float(string='CUP',
                             related='material_id.coste_cup')
    user_id = fields.Many2one('res.users',
                              string='User',
                              readonly=True,
                              default=lambda self: self.env.user.id)

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
    parent_id = fields.Many2one('mc.equipment.material',
                                ondelete='cascade')
    factor = fields.Float(string='Factor')
    observation = fields.Text('Observation',
                              required=True)
    user_id = fields.Many2one('res.users',
                              string='User',
                              readonly=True,
                              default=lambda self: self.env.user.id)

    _sql_constraints = [
        ('date_uniq', 'unique (parent_id, date)',
         'Repeated date.!')
    ]