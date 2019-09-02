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
        'views/mc_partner.xml',
        'views/mc_contract.xml',
        'views/mc_nomenclator.xml',
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
