{
    'name': 'SmartHive Demo Loader',
    'version': '17.0.1.0.0',
    'category': 'Sales/CRM',
    'summary': 'Loads demo data for SmartHive CRM educational institute setup',
    'description': """
        This module provides demo data for a fictional educational institution 
        (Noventis Institute of Technology) including company branding, CRM pipeline 
        stages, sales teams, employees, and demo leads with realistic data.
    """,
    'author': 'SmartHive',
    'website': 'https://www.smarthive.io',
    'depends': ['base', 'crm', 'hr', 'crm_country_detect'],
    'data': [
        'security/ir.model.access.csv',
        'data/res_company.xml',
        'data/crm_stages.xml',
        'data/crm_teams.xml',
        'data/hr_employee.xml',
        'data/crm_leads.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
