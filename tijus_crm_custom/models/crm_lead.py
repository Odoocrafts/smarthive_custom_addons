from odoo import models, fields, api
from datetime import datetime

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    date_closed_editable = fields.Boolean('Allow Editing Date Closed', default=False)
    date_closed = fields.Datetime('Closed Date', readonly=True, copy=False, tracking=True)

    def set_date_closed_editable(self):
        """Method to toggle date_closed editability"""
        for record in self:
            record.date_closed_editable = not record.date_closed_editable
        return True

    def write(self, vals):
        # Override write to handle date_closed field editability
        if 'date_closed' in vals and not self.date_closed_editable:
            vals.pop('date_closed')
        return super(CrmLead, self).write(vals)

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        # Override to dynamically set readonly status
        res = super(CrmLead, self).fields_get(allfields, attributes)
        if 'date_closed' in res:
            res['date_closed']['readonly'] = False
        return res
