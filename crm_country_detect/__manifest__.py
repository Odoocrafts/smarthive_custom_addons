{
    'name': 'CRM Country Detection from Phone',
    'version': '17.0.1.0.0',
    'category': 'Sales/CRM',
    'summary': 'Auto-detect country from phone number and show flag in CRM',
    'description': """
        This module enhances the CRM by automatically detecting a lead's country
        from the phone number and displaying the country flag in the kanban view.
    """,
    'author': 'Odoocrafts',
    'website': '',
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'views/crm_lead_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
    'external_dependencies': {
        'python': ['phonenumbers', 'pycountry'],
    },
}
