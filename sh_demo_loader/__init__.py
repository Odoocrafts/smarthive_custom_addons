# -*- coding: utf-8 -*-
# Part of SmartHive. See LICENSE file for full copyright and licensing details.

from . import models
import logging
import random
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

def post_init_hook(cr, registry):
    """Run after module installation"""
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        _logger.info("Running post-init hook for SmartHive Demo Loader...")
        
        # Create users for employees if they don't exist
        create_employee_users(env)
        
        # Update team members with correct users
        update_team_members(env)
        
        # Randomize some lead dates and trigger country detection
        randomize_lead_data(env)
        
        _logger.info("SmartHive Demo Loader post-init hook completed.")


def create_employee_users(env):
    """Create users for the employees"""
    try:
        # Get employees
        afsal = env.ref('sh_demo_loader.employee_afsal')
        neha = env.ref('sh_demo_loader.employee_neha')
        arjun = env.ref('sh_demo_loader.employee_arjun')
        
        # Create users if they don't already exist
        users = []
        if not afsal.user_id:
            afsal_user = env['res.users'].create({
                'name': afsal.name,
                'login': 'afsal.rahman@noventis.edu.in',
                'email': 'afsal.rahman@noventis.edu.in',
                'password': 'demo123',
                'groups_id': [(6, 0, [
                    env.ref('base.group_user').id, 
                    env.ref('sales_team.group_sale_salesman').id
                ])]
            })
            afsal.user_id = afsal_user.id
            users.append(afsal_user)
        
        if not neha.user_id:
            neha_user = env['res.users'].create({
                'name': neha.name,
                'login': 'neha.sharma@noventis.edu.in',
                'email': 'neha.sharma@noventis.edu.in',
                'password': 'demo123',
                'groups_id': [(6, 0, [
                    env.ref('base.group_user').id, 
                    env.ref('sales_team.group_sale_salesman').id
                ])]
            })
            neha.user_id = neha_user.id
            users.append(neha_user)
        
        if not arjun.user_id:
            arjun_user = env['res.users'].create({
                'name': arjun.name,
                'login': 'arjun.nair@noventis.edu.in',
                'email': 'arjun.nair@noventis.edu.in',
                'password': 'demo123',
                'groups_id': [(6, 0, [
                    env.ref('base.group_user').id, 
                    env.ref('sales_team.group_sale_salesman_all_leads').id,
                    env.ref('sales_team.group_sale_manager').id
                ])]
            })
            arjun.user_id = arjun_user.id
            users.append(arjun_user)
            
        return users
    except Exception as e:
        _logger.error(f"Error creating employee users: {e}")
        return []


def update_team_members(env):
    """Update team members with correct users"""
    try:
        # Update team members with correct users
        afsal = env.ref('sh_demo_loader.employee_afsal')
        neha = env.ref('sh_demo_loader.employee_neha')
        arjun = env.ref('sh_demo_loader.employee_arjun')
        
        if afsal.user_id:
            env.ref('sh_demo_loader.team_member_afsal').write({'user_id': afsal.user_id.id})
        
        if neha.user_id:
            env.ref('sh_demo_loader.team_member_neha').write({'user_id': neha.user_id.id})
        
        if arjun.user_id:
            env.ref('sh_demo_loader.team_member_arjun').write({'user_id': arjun.user_id.id})
    except Exception as e:
        _logger.error(f"Error updating team members: {e}")


def randomize_lead_data(env):
    """Randomize lead creation dates and trigger country detection"""
    try:
        leads = env['crm.lead'].search([])
        
        for lead in leads:
            # Randomize create date within the last 30 days
            days_ago = random.randint(1, 30)
            from datetime import datetime, timedelta
            create_date = datetime.now() - timedelta(days=days_ago)
            lead.write({'create_date': create_date})
            
            # Assign user based on team
            if lead.team_id == env.ref('sh_demo_loader.team_kozhikode'):
                lead.user_id = env.ref('sh_demo_loader.employee_afsal').user_id.id
            elif lead.team_id == env.ref('sh_demo_loader.team_ernakulam'):
                lead.user_id = env.ref('sh_demo_loader.employee_neha').user_id.id
            
            # Create a log note
            if random.random() > 0.5:  # 50% chance to add a note
                note_templates = [
                    "Contacted via phone. Lead sounded interested in our programs.",
                    "Sent brochure via email. Waiting for response.",
                    "Lead requested fee structure details.",
                    "Scheduled campus visit for next week.",
                    "Lead has concerns about hostel facilities.",
                    "Lead inquired about placement opportunities.",
                    "Lead referred by an existing student.",
                    "Lead's parent called for additional information."
                ]
                lead.message_post(body=random.choice(note_templates))
            
            # Create a sale order for confirmed lead (Jacob - BCA Program)
            if lead.id == env.ref('sh_demo_loader.lead_jacob').id and hasattr(lead, 'action_create_sale_order'):
                try:
                    # Add dummy bank and aadhaar details required for sale order creation
                    lead.write({
                        'aadhaar_no': '1234 5678 9012',
                        'bank_account_name': 'Jacob Thomas',
                        'bank_account_no': '1234567890123456',
                        'bank_ifsc_code': 'SBIN0001234',
                        'bank_name': 'State Bank of India',
                        'relation_with_bank_acc_holder': 'self'
                    })
                    
                    # Create and link a partner if needed
                    if not lead.partner_id:
                        partner = env['res.partner'].create({
                            'name': lead.partner_name,
                            'email': lead.email_from,
                            'phone': lead.phone,
                        })
                        lead.partner_id = partner.id
                        
                    # Try to create sale order
                    lead.action_create_sale_order()
                except Exception as e:
                    _logger.warning(f"Could not create sale order for demo lead: {e}")
            
            # Trigger country detection from phone number if the module is installed
            if hasattr(env, 'ref') and env.ref('crm_country_detect.model_tiju_phone_country', False):
                if hasattr(lead, '_compute_possible_country'):
                    lead._compute_possible_country()
                
    except Exception as e:
        _logger.error(f"Error randomizing lead data: {e}")
