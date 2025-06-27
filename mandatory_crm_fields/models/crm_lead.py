from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    # Keep the course_id field for backward compatibility
    course_id = fields.Many2one('product.product', string='Course', 
        domain="[('type', '=', 'service')]",
        help="Select the course related to this opportunity")
        
    @api.constrains('stage_id')
    def _check_required_fields(self):
        for record in self:
            if not record.stage_id or not record.stage_id.required_field_ids:
                continue
                
            errors = []
            for required_field in record.stage_id.required_field_ids:
                field_name = required_field.field_name
                if not record[field_name]:
                    field_label = required_field.field_description or field_name
                    errors.append(field_label)
            
            if errors:
                if len(errors) == 1:
                    message = _("Field '%s' must be filled for opportunities in the '%s' stage.") % (errors[0], record.stage_id.name)
                else:
                    fields_list = ", ".join(errors)
                    message = _("Fields '%s' must be filled for opportunities in the '%s' stage.") % (fields_list, record.stage_id.name)
                raise ValidationError(message)
