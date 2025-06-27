# coding: utf-8

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    tiktok_own_account = fields.Boolean("Tiktok Account",
                                        config_parameter='pragtech_crm_tiktok_leads.tiktok_own_account')
    tiktok_app_id = fields.Char("TikTok App ID",
                                compute='_compute_tiktok_app_id', inverse='_inverse_tiktok_app_id')
    rid = fields.Char("TikTok R ID", compute='_compute_tiktok_r_id', inverse='_inverse_tiktok_r_id')
    tiktok_client_secret = fields.Char("TikTok App Secret",
                                       compute='_compute_tiktok_client_secret', inverse='_inverse_tiktok_client_secret')
    start_time = fields.Datetime(string='Start time', compute='_compute_start_time', inverse='_inverse_start_time')
    end_time = fields.Datetime(string='End time', compute='_compute_end_time', inverse='_inverse_end_time')

    @api.onchange('tiktok_own_account')
    def _onchange_tiktok_own_account(self):
        if not self.tiktok_own_account:
            self.tiktok_app_id = False
            self.tiktok_client_secret = False
            self.rid = False
            self.start_time = False
            self.end_time = False

    @api.depends('tiktok_own_account')
    def _compute_start_time(self):
        for record in self:
            if self.env.user.has_group('odoo_lead_forms_ad_integration_hub_crm.group_social_manager'):
                record.start_time = self.env['ir.config_parameter'].sudo().get_param(
                    'pragtech_crm_tiktok_leads.start_time')
            else:
                record.start_time = None

    def _inverse_start_time(self):
        for record in self:
            if self.env.user.has_group('odoo_lead_forms_ad_integration_hub_crm.group_social_manager'):
                self.env['ir.config_parameter'].sudo().set_param('pragtech_crm_tiktok_leads.start_time', record.start_time)

    @api.depends('tiktok_own_account')
    def _compute_end_time(self):
        for record in self:
            if self.env.user.has_group('odoo_lead_forms_ad_integration_hub_crm.group_social_manager'):
                record.end_time = self.env['ir.config_parameter'].sudo().get_param(
                    'pragtech_crm_tiktok_leads.end_time')
            else:
                record.end_time = None

    def _inverse_end_time(self):
        for record in self:
            if self.env.user.has_group('odoo_lead_forms_ad_integration_hub_crm.group_social_manager'):
                self.env['ir.config_parameter'].sudo().set_param('pragtech_crm_tiktok_leads.end_time', record.end_time)

    @api.depends('tiktok_own_account')
    def _compute_tiktok_r_id(self):
        for record in self:
            if self.env.user.has_group('odoo_lead_forms_ad_integration_hub_crm.group_social_manager'):
                record.rid = self.env['ir.config_parameter'].sudo().get_param(
                    'pragtech_crm_tiktok_leads.rid')
            else:
                record.rid = None

    def _inverse_tiktok_r_id(self):
        for record in self:
            if self.env.user.has_group('odoo_lead_forms_ad_integration_hub_crm.group_social_manager'):
                self.env['ir.config_parameter'].sudo().set_param('pragtech_crm_tiktok_leads.rid', record.rid)

    @api.depends('tiktok_own_account')
    def _compute_tiktok_app_id(self):
        for record in self:
            if self.env.user.has_group('odoo_lead_forms_ad_integration_hub_crm.group_social_manager'):
                record.tiktok_app_id = self.env['ir.config_parameter'].sudo().get_param(
                    'pragtech_crm_tiktok_leads.tiktok_app_id')
            else:
                record.tiktok_app_id = None

    def _inverse_tiktok_app_id(self):
        for record in self:
            if self.env.user.has_group('odoo_lead_forms_ad_integration_hub_crm.group_social_manager'):
                self.env['ir.config_parameter'].sudo().set_param('pragtech_crm_tiktok_leads.tiktok_app_id',
                                                                 record.tiktok_app_id)

    @api.depends('tiktok_own_account')
    def _compute_tiktok_client_secret(self):
        for record in self:
            if self.env.user.has_group('odoo_lead_forms_ad_integration_hub_crm.group_social_manager'):
                record.tiktok_client_secret = self.env['ir.config_parameter'].sudo().get_param(
                    'pragtech_crm_tiktok_leads.tiktok_client_secret')
            else:
                record.tiktok_client_secret = None

    def _inverse_tiktok_client_secret(self):
        for record in self:
            if self.env.user.has_group('odoo_lead_forms_ad_integration_hub_crm.group_social_manager'):
                self.env['ir.config_parameter'].sudo().set_param('pragtech_crm_tiktok_leads.tiktok_client_secret',
                                                                 record.tiktok_client_secret)
