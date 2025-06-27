# -*- coding: utf-8 -*-
import base64
import json

import requests
import werkzeug
import urllib.parse
from werkzeug.urls import url_encode, url_join
import datetime
import time

from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError
from odoo.exceptions import AccessError, MissingError, ValidationError
from werkzeug.urls import url_join


class SocialTiktokController(http.Controller):

    @http.route(['/social_tiktok_leads/callback'], type='http', auth='public')
    def tiktok_account_token_callback(self, access_token=None, is_extended_token=False, **kw_social):
        # print("\n\n\n access_token=======", access_token)
        # print("kw_social=====================",kw_social)
        if not request.env.user.has_group('odoo_lead_forms_ad_integration_hub_crm.group_social_manager'):
            raise UserError(_("Please provide access right"))
        if kw_social.get('auth_code'):
            access_token = kw_social.get('auth_code')
            # print("access_token=================")
            media = request.env.ref('pragtech_crm_tiktok_leads.tiktok_pragtech_social_media')

            try:
                self._create_tiktok_accounts(access_token, media, is_extended_token)
                return "You can Close this window now"

            except (AccessError, MissingError):
                pass


    def _create_tiktok_accounts(self, access_token, media, is_extended_token):
        extended_access_token = access_token if is_extended_token else self._get_tiktok_access_token(access_token, media)
        tiktok_url = 'https://business-api.tiktok.com/open_api/v1.2/oauth2/advertiser/get/'
        tiktok_app_id = request.env['ir.config_parameter'].sudo().get_param('pragtech_crm_tiktok_leads.tiktok_app_id')
        tiktok_client_secret = request.env['ir.config_parameter'].sudo().get_param('pragtech_crm_tiktok_leads.tiktok_client_secret')

        params = {
            'secret': tiktok_client_secret,
            'app_id': tiktok_app_id,
            'access_token': extended_access_token,
        }
        headers = {
            "Content-Type": "application/json",
        }
        json_response = requests.get(tiktok_url, headers=headers, json=params).json()
        if 'data' not in json_response:
            raise ValidationError(_('Provide a valid access token or it may access token has expired.'))
        accounts_to_create = []
        for account in json_response.get('data')['list']:
            pragtech_account_id = account['advertiser_id']
            if pragtech_account_id:
                tiktok_page_ids = self._get_tiktok_pages(extended_access_token, pragtech_account_id)
                accound_ids = request.env['tiktok.pragtech.social.account'].search([('tiktok_social_media_id', '=', int(media)),('tiktok_account_id', '=', pragtech_account_id)])
                # print("accound_ids===========",accound_ids)
                access_token = extended_access_token
                if accound_ids:
                    accound_ids.write({
                        'tiktok_access_token': access_token,
                        'tiktok_pragtech_is_media_disconnected': False
                    })
                else:
                    accounts_to_create.append({
                        'name': account.get('advertiser_name'),
                        'tiktok_social_media_id': media.id,
                        'tiktok_account_id': pragtech_account_id,
                        'tiktok_access_token': access_token,
                    })

        if accounts_to_create:
            request.env['tiktok.pragtech.social.account'].create(accounts_to_create)

    def _get_tiktok_pages(self, extended_access_token, pragtech_account_id):
        # print("\n\n _get_tiktok_pages---------------",extended_access_token, pragtech_account_id)
        start_time = request.env['ir.config_parameter'].sudo().get_param('pragtech_crm_tiktok_leads.start_time')
        end_time = request.env['ir.config_parameter'].sudo().get_param('pragtech_crm_tiktok_leads.end_time')
        tiktok_url = 'https://business-api.tiktok.com/open_api/v1.2/pages/get/'
        start_time_obj = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        start_timestamp = (time.mktime(start_time_obj.timetuple()))
        end_time_obj = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        end_timestamp = (time.mktime(end_time_obj.timetuple()))
        params = {
            'advertiser_id': pragtech_account_id,
            'update_time_range': {"start": start_timestamp, "end": end_timestamp},
        }
        headers = {
            "Access-Token":extended_access_token,
            "Content-Type": "application/json",
        }
        tiktok_page_return = []
        json_response = requests.get(tiktok_url, headers=headers, json=params).json()
        if json_response.get("data")['list']:
            # print("ifffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
            for page_info in json_response.get("data")['list']:
                # print("page_info=====================",page_info.get('title'),page_info.get('page_id'))
                page_ids = request.env['tiktok.social.page'].search([('tiktok_page_id', '=', page_info.get('page_id'))])
                if not page_ids:
                    p_id = request.env['tiktok.social.page'].create(
                        {'name':page_info.get('title'),
                         'tiktok_page_id': page_info.get('page_id'),
                         'tik_advertiser_id': pragtech_account_id
                         })
                    tiktok_page_return.append(p_id)
        return tiktok_page_return
        # print("json_response==============",json_response)


    def _get_tiktok_access_token(self, access_token, media):
        print("\n _get_linkedin_access_token=============",)
        tiktok_url = 'https://business-api.tiktok.com/open_api/v1.2/oauth2/access_token/'
        tiktok_app_id = request.env['ir.config_parameter'].sudo().get_param('pragtech_crm_tiktok_leads.tiktok_app_id')
        tiktok_client_secret = request.env['ir.config_parameter'].sudo().get_param('pragtech_crm_tiktok_leads.tiktok_client_secret')
        params = {
            'secret': tiktok_client_secret,
            'app_id': tiktok_app_id,
            'auth_code': access_token,
        }
        headers = {
            "Content-Type": "application/json",
        }
        response = requests.post(tiktok_url, headers=headers, json=params).json()
        return response.get('data')['access_token']
