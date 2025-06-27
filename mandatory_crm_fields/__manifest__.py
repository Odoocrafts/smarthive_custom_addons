{
    'name': 'CRM Required Fields by Stage',
    'version': '1.1',
    'category': 'Sales/CRM',
    'summary': 'Make fields required based on CRM stage',
    'description': """
        This module allows users to configure which fields are required in each CRM stage,
        without needing code changes.
    """,
    'depends': ['crm', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_stage_views.xml',
        'views/crm_lead_views.xml',
        'views/crm_stage_required_field_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
