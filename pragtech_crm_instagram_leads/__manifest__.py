{
    'name': 'CRM Instagram Lead Integration',
    'version': '17.1',
    'category': 'Social',
    'author': 'Pragmatic TechSoft Pvt Ltd.',
    'website': 'www.pragtech.co.in',
    'summary': 'Crm odoo dashboard social media facebook instagram linkedin twitter google adwords tik tok campaigns facebook forms lead generation capture leads ad campaigns lead forms lead import dynamic dashboard Odoo CRM Social Media Lead Form Ads Campaign Integration App',
    'description': "Sync Instagram Leads with Odoo CRM",
    'depends': ['crm', 'utm', 'odoo_lead_forms_ad_integration_hub_crm'],
    'data': [
        'security/ir.model.access.csv',
        'data/instagram_socail_dashboard_data.xml',
        'views/instagram_menu_view.xml',
        'views/instagram_res_config_settings_views.xml',
        'views/instagram_social_media_view.xml',
        'views/instagram_social_account_view.xml',
        'views/crm_view.xml',
        'views/instagram_scedulars_view.xml'
    ],

    'assets': {
        'web.assets_common': [
            'pragtech_crm_instagram_leads/static/css/custome_css.css',
        ],
    },
    'images': ['static/description/pragtech_crm_instagram_leads.gif'],
    # 'images': ['static/description/end-of-year-sale-main.jpg'],
    'live_test_url': 'https://www.pragtech.co.in/company/proposal-form.html?id=103&name=crm-instagram-leads',
    'license': 'OPL-1',
    'price': 100.0,
    'currency': 'USD',
    'installable': True,
    'auto_install': False,
}
