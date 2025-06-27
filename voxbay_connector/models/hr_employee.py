from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger("Voxbay Debug:")
class HrEmployee(models.Model):
    _inherit = "hr.employee"

    agent_number = fields.Char(string="Voxbay Agent Number")

    voxbay_incoming_calls = fields.One2many('voxbay.call.data.record', 'operator_employee_id', string="Incoming Calls", domain=[('call_type','=','incoming')])
    voxbay_incoming_calls_count = fields.Integer(compute="_compute_voxbay_incoming_calls_count")
    @api.depends('voxbay_incoming_calls')
    def _compute_voxbay_incoming_calls_count(self):
        for record in self:
            record.voxbay_incoming_calls_count = len(record.voxbay_incoming_calls)

    voxbay_outgoing_calls = fields.One2many('voxbay.call.data.record', 'operator_employee_id', string="Outgoing Calls", domain=[('call_type','=','outgoing')])
    voxbay_outgoing_calls_count = fields.Integer(compute="_compute_voxbay_outgoing_calls_count")
    @api.depends('voxbay_outgoing_calls')
    def _compute_voxbay_outgoing_calls_count(self):
        for record in self:
            record.voxbay_outgoing_calls_count = len(record.voxbay_outgoing_calls)

    @api.onchange('agent_number')
    def onchange_agent_number(self):
        if self.agent_number:
            domain = [('agent_number','=',self.agent_number)]
            if isinstance(self.id, int):
                domain.append(('id','!=', self.id))
            employee_with_same_agent_no = self.env['hr.employee'].sudo().search(domain, limit=1)
            if employee_with_same_agent_no:
                raise ValidationError(f"This Agent Number is already assigned to {employee_with_same_agent_no[0].name}! You need to unassign this Agent Number from {employee_with_same_agent_no[0].name}, before setting it to another Employee.")
            
    def action_view_incoming_calls(self):
        return {
            'name': _("Incoming Calls"),
            'type': 'ir.actions.act_window',
            'res_model': 'voxbay.call.data.record',
            'context': {'create': False},
            'view_mode': 'list',
            'domain': [('id', 'in', self.voxbay_incoming_calls.ids)],
            'views': [(self.env.ref('voxbay_connector.voxbay_incoming_cdr_tree_view').id, 'list')],
        }
    
    def action_view_outgoing_calls(self):
        return {
            'name': _("Outgoing Calls"),
            'type': 'ir.actions.act_window',
            'res_model': 'voxbay.call.data.record',
            'context': {'create': False},
            'view_mode': 'list',
            'domain': [('id', 'in', self.voxbay_outgoing_calls.ids)],
            'views': [(self.env.ref('voxbay_connector.voxbay_outgoing_cdr_tree_view').id, 'list')],

        }