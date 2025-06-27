from odoo import fields, models, api

class CrmStageRequiredField(models.Model):
    _name = 'crm.stage.required.field'
    _description = 'Required Fields for CRM Stage'
    
    stage_id = fields.Many2one('crm.stage', string='Stage', required=True, ondelete='cascade')
    field_id = fields.Many2one('ir.model.fields', string='Field', required=True, 
                               domain=[('model', '=', 'crm.lead'), 
                                       ('ttype', 'not in', ['binary', 'boolean', 'one2many', 'many2many'])],
                               ondelete='cascade',
                               help="The field that will be required in this stage")
    field_name = fields.Char(related='field_id.name', string='Field Name', readonly=True, store=True)
    field_description = fields.Char(related='field_id.field_description', string='Field Label', readonly=True)
    
    _sql_constraints = [
        ('unique_field_per_stage', 'unique(stage_id, field_id)', 'This field is already required for this stage!')
    ]
