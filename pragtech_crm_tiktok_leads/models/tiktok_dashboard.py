from odoo import fields, models, _

class TikTokSocailDashboard(models.Model):
    _name = "tiktok.socail.dashboard"
    _description = "TikTok Dashboard"

    name = fields.Char()

