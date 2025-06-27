{
    'name': 'CRM Kanban Card Color Customizer',
    'version': '1.0',
    'summary': 'Set custom colors for CRM Kanban cards based on stages',
    'author': 'Muhammed Anas',
    'website': 'http://www.odoocrafts.com',
    'category': 'CRM',
    'depends': ['crm', 'mail'],
    'data': [
        'views/crm_views.xml',
    ],
    "assets": {
        "web.assets_backend": [
            'crm_custom_color/static/src/views/fields/**/*'
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}