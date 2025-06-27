{
    'name': "Voxbay Connector",
    'author': 'Rizwaan',
    'version': "17.0.0.0",
    'sequence': "0",
    'depends': ['base','crm','hr','odoo-rest-api', 'audio_player_widget'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee.xml',
        'views/crm.xml',
        'views/call_data.xml',
    ],
    'demo': [],
    'summary': "Voxbay Connector",
    'description': "Voxbay Telphony integration plugin for Odoo",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': False
}