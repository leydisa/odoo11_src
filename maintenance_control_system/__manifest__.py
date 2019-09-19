# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Maintenance Control System',
    'version': '1.0',
    'summary': 'Maintenance Control System',
    'description': "",
    'website': 'https://www.example.com',
    'depends': [],
    'category': 'maintenance_control_system',
    'sequence': 13,
    'demo': [
    ],
    'data': [
        'data/data.xml',
        'data/sequence.xml',

        'security/security.xml',

        'report/report.xml',
        'report/rp_work_order.xml',

        'views/mc_nomenclator.xml',
        'views/mc_partner.xml',
        'views/mc_contract.xml',
        'views/mc_material.xml',
        'views/mc_equipement.xml',
        'views/mc_labor.xml',
        'views/mc_budget.xml',
        'views/mc_work_order.xml',
        'views/mc_maintenance.xml',
        'views/maintenance_control.xml',
    ],
    'qweb': [
    ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': True,
}
