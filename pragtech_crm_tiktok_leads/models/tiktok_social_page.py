# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SocialPageTikTok(models.Model):
    _name = 'tiktok.social.page'
    _description = 'TikTok Pages'
    _rec_name = 'name'

    name = fields.Char('Page Name')
    tiktok_page_id = fields.Char('TikTok Page ID')
    tik_advertiser_id = fields.Char('TikTok Advertiser ID')


