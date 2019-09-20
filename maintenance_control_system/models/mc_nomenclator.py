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

    # @api.multi
    # def unlink(self):
    #     try:
    #         s = super(McProvince, self).unlink()
    #     except Exception as e:
    #         pass
    #     return s


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