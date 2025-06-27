from odoo import fields, models

class CrmStage(models.Model):
    _inherit = 'crm.stage'

    required_field_ids = fields.One2many('crm.stage.required.field', 'stage_id', 
                                         string="Required Fields", 
                                         help="Fields that will be mandatory for leads in this stage")
