from . import models

def post_init_hook(env):
    """Create UTM source if it doesn't exist"""
    # Note: In Odoo 17, the post_init_hook only receives the env parameter
    source_vals = [
        {'name': 'Online SBU Referral'},
        {'name': 'Organic Media Leads'}
    ]
    
    for vals in source_vals:
        existing_source = env['utm.source'].search([('name', '=', vals['name'])], limit=1)
        if not existing_source:
            env['utm.source'].create(vals)
