# -*- coding: utf-8 -*-

import logging
import requests
from odoo import models, fields, api
from datetime import datetime

_logger = logging.getLogger(__name__)


class InstagramUtmAdset(models.Model):
    _name = 'utm.tiktok.adset'
    _description = 'Utm Toktok Adset'

    name = fields.Char()
    tiktok_adset_id = fields.Char()

    _sql_constraints = [
        ('tiktokadset_unique', 'unique(tiktok_adset_id)',
         'This TikTok AdSet already exists!')
    ]


class TikTokUtmMedium(models.Model):
    _inherit = 'utm.medium'

    tiktok_ad_id = fields.Char()

    _sql_constraints = [
        ('tiktok_ad_unique', 'unique(tiktok_ad_id)',
         'This TikTok Ad already exists!')
    ]


class TikTokUtmCampaign(models.Model):
    _inherit = 'utm.campaign'

    tiktok_campaign_id = fields.Char()

    _sql_constraints = [
        ('tiktok_campaign_unique', 'unique(tiktok_campaign_id)',
         'This TikTok Campaign already exists!')
    ]


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    description = fields.Html('Notes')
    tiktok_lead_id = fields.Char(readonly=True)
    tiktok_page_id = fields.Many2one('crm.tiktok.page')
    tiktok_ad_id = fields.Many2one('utm.medium', readonly=True, string='TikTok Ad')
    tiktok_campaign_id = fields.Many2one('utm.campaign', readonly=True, string='TikTok Campaign')
    tiktok_date_create = fields.Datetime(readonly=True)

    _sql_constraints = [
        ('tiktok_lead_unique', 'unique(tiktok_lead_id)',
         'This TikTok lead already exists!')
    ]


class CrmTiktokPage(models.Model):
    _name = 'crm.tiktok.page'
    _description = 'TikTok Page'

    tiktok_account = fields.Many2one('tiktok.social.page', string="TikTok pages", store=True)
    tiktok_page_id = fields.Char('TikTok Page ID')
    tik_advertiser_id = fields.Char('TikTok Advertiser ID')

    @api.onchange('tiktok_account')
    def _onchange_tiktok_account(self):
        if self.tiktok_account:
            self.tiktok_page_id = self.tiktok_account.tiktok_page_id
            self.tik_advertiser_id = self.tiktok_account.tik_advertiser_id

    def import_lead_form(self):
        # print("\n\nimport_lead_form-----------------", self)
        tiktok_url = 'https://business-api.tiktok.com/open_api/v1.2/pages/leads/mock/get/'
        tiktok_account_id = self.env['tiktok.pragtech.social.account'].search([('tiktok_account_id', '=', self.tik_advertiser_id)])
        tiktok_access_token = tiktok_account_id.tiktok_access_token
        crm_instance = self.env['crm.lead']
        params = {
            'advertiser_id': self.tik_advertiser_id,
            'page_id': self.tiktok_page_id,
        }
        headers = {
            "Access-Token": tiktok_access_token,
            "Content-Type": "application/json",
        }
        tiktok_page_return = []
        lead_data_dict = {}
        all_response_data = {}
        key_collecter_dict = {}
        json_response = requests.get(tiktok_url, headers=headers, json=params).json()
        if json_response.get('message') == 'OK':
            _logger.info("*****IMPORT  Leads!!!!!!!!!!!!!!!!!!!!!!!!!!!!!****")
            # print("json_response====================",json_response)
            if json_response.get('data')['lead_data']:
                all_response_data = dict(json_response.get('data')['lead_data']).copy()
                # print("all_response_data============", all_response_data)
                if 'name' in json_response.get('data')['lead_data'] and json_response.get('data')['lead_data']['name']:
                    key_collecter_dict['name'] = json_response.get('data')['lead_data']['name']
                    lead_data_dict['name'] = json_response.get('data')['lead_data']['name']
                    lead_data_dict['contact_name'] = json_response.get('data')['lead_data']['name']

                if 'email' in json_response.get('data')['lead_data'] and json_response.get('data')['lead_data']['email']:
                    key_collecter_dict['email'] = json_response.get('data')['lead_data']['email']
                    lead_data_dict['email_from'] = json_response.get('data')['lead_data']['email']
                if 'phone_number' in json_response.get('data')['lead_data'] and json_response.get('data')['lead_data']['phone_number']:
                    key_collecter_dict['phone_number'] = json_response.get('data')['lead_data']['phone_number']
                    lead_data_dict['phone'] = json_response.get('data')['lead_data']['phone_number']
            diff_dict_value = set(key_collecter_dict.keys()).intersection(all_response_data.keys())
            for val in diff_dict_value:
                all_response_data.pop(str(val))
            # print("diff_dict==================", diff_dict_value)
            # print("\n\n\nall_response_data============", all_response_data)
            notes = []
            if all_response_data:
                for key, value in all_response_data.items():
                    notes.append('<b>%s</b>: %s <br><br>' % (str(key), value))
            if notes:
                lead_data_dict['description'] = "\n".join(notes)
            source_id = self.env.ref('pragtech_crm_tiktok_leads.utm_source_tiktok')
            if source_id:
                lead_data_dict['source_id'] = source_id.id or source_id
            medium_id = self.env.ref('pragtech_crm_tiktok_leads.utm_medium_tiktok')
            if medium_id:
                lead_data_dict['medium_id'] = medium_id.id or medium_id
            if json_response.get('data')['meta_data']:
                if 'lead_id' in json_response.get('data')['meta_data'] and json_response.get('data')['meta_data']['lead_id']:
                    lead_data_dict['tiktok_lead_id'] = json_response.get('data')['meta_data']['lead_id']
                if 'page_id' in json_response.get('data')['meta_data'] and json_response.get('data')['meta_data']['page_id']:
                    tiktok_records = self.env['crm.tiktok.page'].search([('tiktok_page_id', '=', json_response.get('data')['meta_data']['page_id'])])
                    if tiktok_records:
                        lead_data_dict['tiktok_page_id'] = tiktok_records.id or tiktok_records
                    else:
                        tiktok_page_id = self.env['crm.lead'].create({'tiktok_page_id': json_response.get('data')['meta_data']['page_id']})
                        lead_data_dict['tiktok_page_id'] = tiktok_page_id.id

                if 'ad_id' in json_response.get('data')['meta_data'] and json_response.get('data')['meta_data']['ad_id']:
                    adset_records = self.env['utm.tiktok.adset'].search([('tiktok_page_id', '=', json_response.get('data')['meta_data']['ad_id'])])
                    if adset_records:
                        lead_data_dict['tiktok_ad_id'] = adset_records or adset_records.id
                    else:
                        tiktok_ad_id = self.env['utm.tiktok.adset'].create({
                            'tiktok_page_id': json_response.get('data')['meta_data']['ad_id'],
                            'name': json_response.get('data')['meta_data']['ad_name']})
                        lead_data_dict['tiktok_campaign_id'] = tiktok_ad_id.id or tiktok_ad_id
                if 'campaign_id' in json_response.get('data')['meta_data'] and json_response.get('data')['meta_data']['campaign_id']:
                    campaign_records = self.env['utm.campaign'].search(
                        [('tiktok_campaign_id', '=', json_response.get('data')['meta_data']['campaign_id'])])
                    if campaign_records:
                        lead_data_dict['tiktok_campaign_id'] = campaign_records.id or campaign_records
                    else:
                        tiktok_campaign_id = self.env['utm.campaign'].create({
                            'tiktok_campaign_id': json_response.get('data')['meta_data']['campaign_id'],
                            'name': json_response.get('data')['meta_data']['campaign_name']})
                        lead_data_dict['tiktok_campaign_id'] = tiktok_campaign_id.id or tiktok_campaign_id

                if 'create_time' in json_response.get('data')['meta_data'] and json_response.get('data')['meta_data']['create_time']:
                    time_stamp = int(json_response.get('data')['meta_data']['create_time'])
                    lead_data_dict['tiktok_date_create'] = datetime.utcfromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')

        if lead_data_dict:
            lead_crm_records = crm_instance.search([('tiktok_lead_id', '=', lead_data_dict.get('tiktok_lead_id'))])
            if not lead_crm_records:
                crm_instance.create(lead_data_dict)
            else:
                crm_instance.write(lead_data_dict)
