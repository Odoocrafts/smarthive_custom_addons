from odoo import models, fields, api
from odoo.exceptions import UserError

COLORS_LIST = [
    ('0', "No color"),
    ('1', "Red"),
    ('2', "Orange"),
    ('3', "Yellow"),
    ('4', "Cyan"),
    ('5', "Purple"),
    ('6', "Almond"),
    ('7', "Teal"),
    ('8', "Blue"),
    ('9', "Raspberry"),
    ('10', "Green"),
    ('11', "Violet"),
]


class CrmLead(models.Model):
    _inherit = "crm.lead"
    stage_color = fields.Char(string="Stage Color", related="stage_id.color", store=True)
    color = fields.Integer(string="Color", compute="_compute_ribbon_color", readonly=False, store=True)

    @api.depends('stage_id', 'stage_id.color_select')
    def _compute_ribbon_color(self):
        for record in self:
            if record.stage_id:
                record.color = record.stage_id.color_select or '0'
                record.color = int(record.color)

class CrmStage(models.Model):
    _inherit = 'crm.stage'

    color = fields.Char(string="Kanban Background Color", help="Custom color for Kanban cards in this stage")
    color_select = fields.Selection(selection=COLORS_LIST, string="Kanban Ribbon Color")