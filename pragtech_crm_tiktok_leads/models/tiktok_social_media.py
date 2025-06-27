# -*- coding: utf-8 -*-

import requests

from odoo import _, models, fields
from odoo.exceptions import UserError
from werkzeug.urls import url_encode, url_join


class SocialMediaTikTok(models.Model):

    _name = 'tiktok.pragtech.social.media'
    _description = 'TikTok Social Pages'
    _rec_name = 'tiktok_media_name'

    _TIKTOK_ENDPOINT = 'https://api.linkedin.com/v2/'

    tiktok_media_name = fields.Char('Name', readonly=True, required=True, translate=True)
    tiktok_media_description = fields.Char('Description', readonly=True)
    tiktok_media_image = fields.Binary('Image', readonly=True)
    # linkedin_account_ids = fields.One2many('linkedin.pragtech.social.account', 'instagram_social_media_id', string="Facebook Accounts")
    tiktok_media_link_accounts = fields.Boolean('link Your accounts ?', default=True, readonly=True, required=True, )
    tiktok_media_type = fields.Selection([('tiktok', 'TikTok')], string='Media Type', required=True, default='tiktok')

    def pragtech_action_tiktok_add_account(self):
        self.ensure_one()
        # print("pragtech_action_tiktok_add_account=============",self)

        tiktok_app_id = self.env['ir.config_parameter'].sudo().get_param('pragtech_crm_tiktok_leads.tiktok_app_id')
        tiktok_rid = self.env['ir.config_parameter'].sudo().get_param('pragtech_crm_tiktok_leads.rid')
        tiktok_client_secret = self.env['ir.config_parameter'].sudo().get_param('pragtech_crm_tiktok_leads.tiktok_client_secret')
        if tiktok_app_id and tiktok_client_secret:
            return self._add_tiktok_accounts_from_configuration(tiktok_app_id,tiktok_rid)
        else:
            raise UserError(_(" You are Missing some credentials."))

    def _add_tiktok_accounts_from_configuration(self, tiktok_app_id,tiktok_rid):
        get_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        split_base_url = get_base_url.split(':')[0]
        if split_base_url == 'http':
            get_base_url = get_base_url.replace("http", "https")
        else:
            pass
        params = {
            'app_id': tiktok_app_id,
            'state': 'your_custom_params',
            'redirect_uri': url_join(get_base_url, "/social_tiktok_leads/callback"),
            'rid': tiktok_rid

        }


        return {
            'type': 'ir.actions.act_url',
            'url': 'https://ads.tiktok.com/marketing_api/auth?%s' % url_encode(params),
            'target': 'new'
        }

