# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta

import json

import requests
from odoo import models, fields, api
from werkzeug.urls import url_join
import logging

_logger = logging.getLogger(__name__)


class SocialAccountTikTok(models.Model):
    _name = 'tiktok.pragtech.social.account'
    _description = 'TikTok Account'
    _rec_name = 'name'

    tiktok_social_media_id = fields.Many2one('tiktok.pragtech.social.media', string="Social Media", required=True,
                                             readonly=True, ondelete='cascade')
    tiktok_social_media_type = fields.Selection(related='tiktok_social_media_id.tiktok_media_type')
    name = fields.Char('Advertiser Name', readonly=True)
    tiktok_pragtech_is_media_disconnected = fields.Boolean('Link with external Social Media is broken')
    tiktok_account_id = fields.Char('TikTok Advertiser ID', readonly=True)
    tiktok_access_token = fields.Char('TikTok Access Token', readonly=True)
    tiktok_page_id = fields.Many2one('tiktok.social.page', string="TikTok pages")
