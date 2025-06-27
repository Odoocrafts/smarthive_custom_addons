from odoo import models,fields,api, SUPERUSER_ID
import logging
import random

_logger = logging.getLogger("Voxbay Debug")
class VoxbayCallData(models.Model):
    _name = "voxbay.call.data.record"
    name = fields.Char(string="Name", compute="_compute_name", store=True)
    @api.depends('call_type', 'call_date', 'call_uuid', 'called_number', 'caller_number')
    def _compute_name(self):
        for record in self:
            record.name = f"[{(record.call_type or '')}] "
            if record.call_date:
                record.name += f'{record.call_date} - '
            if record.call_uuid:
                record.name += f'{record.call_uuid}'

    call_uuid = fields.Char(string="Call UUID")
    call_type = fields.Selection(string="Call Type", selection=[('incoming', 'Incoming Call'), ('outgoing', 'Outgoing Call')])
    event_status = fields.Selection(string="Event Status", selection=[('agent_received_call', 'Agent Received Call'), ('agent_answered_call', 'Agent Accepted Call'), ('agent_initiated_call', 'Agent Initiated Call'), ('call_ended', 'Call Ended')])
    total_call_duration = fields.Integer(string="Duration",)
    call_date = fields.Datetime(string="Call Date")
    call_status = fields.Selection(string="Call Status", selection=[('Connected', 'Connected'), ('Not Connected', 'Not Connected'), ('Cancel', 'Cancel'), ('NOANSWER', 'No Answer'), ('BUSY', 'BUSY'), ('CONGESTION', 'Congestion'), ('CHANUNAVAIL', 'Channel Unavailable'), ('FAILED', 'Failed')])

    called_number = fields.Char(string="Called Number") # Customer Number (Outgoing Calls), Operator Number (Incoming Calls)
    caller_number = fields.Char(string="Caller Number") # Customer Number (Incoming Calls), Operator Number (Outgoing Calls)
    agent_number = fields.Char(string="Number of Agent") #AgentNumber

    recording_url = fields.Char(string="Recording")
    
    call_start_time = fields.Datetime(string="Start Time")
    call_end_time = fields.Datetime(string="End Time")
    dtmf = fields.Char(string="DTMF Sequence")
    transferred_number = fields.Char("Transferred Number")

    extension_number = fields.Char(string="Extension Number") #Not present in data received by voxbay api
    destination_number = fields.Char(string="Destination Number") #Not present in data received by voxbay api
    caller_id = fields.Char(string="Caller ID") #Not present in data received by voxbay api
    conversation_duration = fields.Integer("Conversation Duration")

    operator_employee_id = fields.Many2one('hr.employee', string="Operator Employee", compute="_compute_operator_employee_id", store=True, readonly=False)

    lead_id = fields.Many2one('crm.lead', string="Lead")
    @api.depends('agent_number')
    def _compute_operator_employee_id(self):
        for record in self:
            if record.agent_number:
                operator_employee = self.env['hr.employee'].sudo().search([('agent_number','=',record.agent_number)], limit=1)
                if operator_employee:
                    record.operator_employee_id = operator_employee[0].id
                    continue
            record.operator_employee_id = False

    @api.model_create_multi
    def create(self, vals):
        res = super().create(vals)
        return res
    
    def write(self, vals):
        res = super().write(vals)
        for record in self:
            if record.lead_id:
                # record._compute_operator_employee_id()
                # Set current user in env variable as either the user of the employee who made the call or the SUPERUSER
                self = self.with_user(record.operator_employee_id.user_id or self.sudo().browse(SUPERUSER_ID))
                # Update the user_id field of Lead with the actual user who made the call, instead of the SUPERUSER
                if (self.env.user.id != SUPERUSER_ID):
                    record.lead_id.write({'user_id': self.env.user.id})
        return res

    # Function to create a new lead from call record or assign new lead to call record
    def create_update_lead(self):
        for record in self:
            lead = False
            if record.call_type == 'incoming':
                lead = self.env['crm.lead'].sudo().search([('phone','like',record.caller_number), ('phone','!=',False)], limit=1)
                contact_number = record.caller_number
            elif record.call_type == 'outgoing':
                lead = self.env['crm.lead'].sudo().search([('phone','like',record.called_number), ('phone','!=',False)], limit=1)
                contact_number = record.called_number
            if lead:
                record.lead_id = lead[0].id
            else:
                sales_team = False
                lead_user = record.operator_employee_id.user_id or self.sudo().browse(SUPERUSER_ID)
                self = self.with_user(lead_user)

                lead_data = {
                    'name': f'[{record.call_type.upper()}] {contact_number}',
                    'phone': contact_number,
                    'type': 'lead',
                    'source_id': 82,
                    'user_id': lead_user.id
                }

                if lead_user.id == SUPERUSER_ID:
                    sales_teams = self.env['crm.team'].sudo().search([])
                    if sales_teams:
                        random_choice = random.choice(range(len(sales_teams)))
                        sales_team = sales_teams[random_choice]
                else:
                    sales_team = lead_user.sale_team_id

                if sales_team:
                    lead_data.update({'team_id': sales_team.id, 'user_id': False})

                _logger.error(f'lead_data, {lead_data}')
                record.lead_id = self.env['crm.lead'].sudo().create(lead_data).id

            # Ensure the sales team is assigned correctly when the call ends and the salesperson is changed
            if record.lead_id and not record.lead_id.team_id:
                if record.lead_id.user_id and record.lead_id.user_id.sale_team_id:
                    record.lead_id.write({'team_id': record.lead_id.user_id.sale_team_id.id})
                else:
                    sales_teams = self.env['crm.team'].sudo().search([])
                    if sales_teams:
                        random_choice = random.choice(range(len(sales_teams)))
                        sales_team = sales_teams[random_choice]
                        record.lead_id.write({'team_id': sales_team.id})

            _logger.error(f"Created or Updated Lead with Number: {record.lead_id.phone}")