# CRM Course Required by Stage

## Overview
This module enhances Odoo's CRM functionality by allowing administrators to configure which CRM stages require a course field to be filled in. This removes the need for code changes when business requirements change regarding mandatory fields at different sales stages.

## Features
- Configure course field requirements per CRM stage
- Validation when moving opportunities to stages that require a course
- User-friendly warnings and error messages
- Seamless integration with standard Odoo CRM workflow

## Technical Details

### Models
1. **CRM Stage Extension (`crm.stage`)**
   - Adds `course_required` boolean field to mark stages where course selection is mandatory
   - Located in `/models/crm_stage.py`

2. **CRM Lead Extension (`crm.lead`)**
   - Adds `course_id` field referencing `product.product` with service type
   - Implements validation logic for required fields based on stage configuration
   - Located in `/models/crm_lead.py`

### Views
1. **CRM Stage Form View**
   - Adds "Course Mandatory in this Stage?" checkbox to stage configuration
   - Located in `views/crm_stage_views.xml`

2. **CRM Lead Form View**
   - Displays course field in the opportunity form
   - Located in `views/crm_lead_views.xml`

## Extension Guidelines

### Adding More Mandatory Fields by Stage
To add another field that should be mandatory based on stages:

1. Add a new boolean field to `crm.stage` model to indicate if the field is mandatory:
   ```python
   new_field_required = fields.Boolean(string="New Field Mandatory in this Stage?", default=False)
   ```

2. Add the new field to the `crm.lead` model if it doesn't exist already
   ```python
   new_field_id = fields.Many2one('model.name', string='New Field')
   ```

3. Extend the `_check_course_required` method to include validation for your new field:
   ```python
   @api.constrains('stage_id', 'course_id', 'new_field_id')
   def _check_course_required(self):
       for record in self:
           if record.stage_id and record.stage_id.course_required and not record.course_id:
               raise ValidationError(_("A course must be selected for opportunities in the '%s' stage.") % record.stage_id.name)
           if record.stage_id and record.stage_id.new_field_required and not record.new_field_id:
               raise ValidationError(_("The new field must be filled for opportunities in the '%s' stage.") % record.stage_id.name)
   ```

4. Add the `onchange` handler for the new field similar to the course field
   ```python
   @api.onchange('stage_id')
   def _onchange_stage_id_for_fields_required(self):
       # Extend existing method to handle the new field
   ```

5. Update the views to show the new configuration option in the stage form and the field in the opportunity form

### Creating a Generic Field Requirement Framework
For better scalability, consider refactoring to a more generic approach:

1. Create a many2many relationship between stages and fields that should be required
2. Use a wizard or configuration screen to let administrators select which fields are required for each stage
3. Implement dynamic validation using reflection or field introspection in Odoo

## Dependencies
- CRM (`crm`)
- Product (`product`)

## Installation
1. Place the module folder in your Odoo addons directory
2. Update the module list in Odoo
3. Install the module through the Odoo interface

## License
LGPL-3
