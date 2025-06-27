from odoo import http
from odoo.http import request
import logging
import json
import traceback
_logger = logging.getLogger("Voxbay Debug: ")


class VoxbayApi(http.Controller):

    '''
        *****Incoming Call API******
    '''
    # Event 1: Incoming call landed on server
    @http.route(
        '/voxbay/api/incoming_landed',
        type='json', auth='none', methods=["POST"], csrf=False)
    def incoming_landed(self, *args, **post):
        try:
            post_data: dict = request.httprequest.json
            _logger.info(f"API Incoming Landed Called with data: {post_data}")
            data = {
                'called_number': post_data['calledNumber'],
                'caller_number': post_data['callerNumber'],
                'call_uuid': post_data['CallUUID'],
                'event_status': 'agent_received_call',
                'call_type': 'incoming',
            }
            call_record = request.env['voxbay.call.data.record'].sudo().create(data)
            call_record.create_update_lead()
            return json.dumps({'status': 'success',})

        except Exception as e:
            _logger.error("Exception Occurred")
            _logger.error(traceback.format_exc())
            _logger.error(post_data)
        return json.dumps({'status': 'failed',})
    
    #Event 2: Call answered by an agent
    @http.route(
        '/voxbay/api/incoming_answered',
        type='json', auth='none', methods=["POST"], csrf=False)
    def incoming_answered(self, *args, **post):
        try:
            post_data: dict = request.httprequest.json
            _logger.info(f"API Incoming Answered Called with data: {post_data}")

            data =  {
                    'called_number': post_data['calledNumber'],
                    'caller_number': post_data['callerNumber'],
                    'call_uuid': post_data['CallUUID'],
                    'call_type': 'incoming',
                    'agent_number': post_data['AgentNumber'],
                    'event_status': 'agent_answered_call',
                }

            call_record = request.env['voxbay.call.data.record'].sudo().search([('call_uuid','=',post_data['CallUUID'])])
            if call_record:
                call_record.write(data)
            else:
                call_record = request.env['voxbay.call.data.record'].sudo().create(data)
            call_record.create_update_lead()
                # _logger.error(f"Record with CallUUID {post_data['CallUUID']} Doesn't Exist")
            return json.dumps({'status': 'success',})

        except Exception as e:
            _logger.error("Exception Occurred")
            _logger.error(traceback.format_exc())
            _logger.error(post_data)

        return json.dumps({'status': 'failed',})
    
    #Event 3: When a call is disconnected
    @http.route(
        '/voxbay/api/incoming_disconnected',
        type='json', auth='none', methods=["POST"], csrf=False)
    def incoming_disconnected(self, *args, **post):
        try:
            post_data: dict = request.httprequest.json
            _logger.info(f"API Incoming Disconnected Called with data: {post_data}")

            data =  {
                    'called_number': post_data['calledNumber'],
                    'caller_number': post_data['callerNumber'],
                    'call_uuid': post_data['CallUUID'],
                    'call_type': 'incoming',
                    'agent_number': post_data['AgentNumber'],
                    'event_status': 'call_ended',
                }
            
            call_record = request.env['voxbay.call.data.record'].sudo().search([('call_uuid','=',post_data['CallUUID'])])        
            if call_record:
                call_record.write(data)     
            else:
                call_record = request.env['voxbay.call.data.record'].sudo().create(data)
            call_record.create_update_lead()
            # Ensure the sales team is assigned correctly
            if call_record.lead_id and not call_record.lead_id.team_id:
                if call_record.lead_id.user_id and call_record.lead_id.user_id.sale_team_id:
                    call_record.lead_id.write({'team_id': call_record.lead_id.user_id.sale_team_id.id})
                else:
                    sales_teams = request.env['crm.team'].sudo().search([])
                    if sales_teams:
                        random_choice = random.choice(range(len(sales_teams)))
                        sales_team = sales_teams[random_choice]
                        call_record.lead_id.write({'team_id': sales_team.id})
            return json.dumps({'status': 'success',})

                # _logger.error(f"Record with CallUUID {post_data['CallUUID']} Doesn't Exist")   
        except Exception as e:
            _logger.error("Exception Occurred")
            _logger.error(traceback.format_exc())
            _logger.error(post_data)

        return json.dumps({'status': 'failed',})

    
    # Event 4: CDR push at the end of the call
    @http.route(
        '/voxbay/api/incoming_cdr_push',
        type='json', auth='none', methods=["POST"], csrf=False)
    def incoming_cdr_push(self, *args, **post):
        try:
            post_data: dict = request.httprequest.json
            _logger.info(f"API Incoming CDR Push Called with data: {post_data}")

            data =  {
                    'called_number': post_data['calledNumber'],
                    'caller_number': post_data['callerNumber'],
                    'call_uuid': post_data['CallUUID'],
                    'call_type': 'incoming',
                    'agent_number': post_data['AgentNumber'],
                    'total_call_duration': post_data['totalCallDuration'],   # Total call duration
                    'call_date': post_data['callDate'],                      # Date and time of the call
                    'call_status': post_data['callStatus'],                  # Status of the call
                    'recording_url': post_data['recording_URL'],             # Recording URL
                    'call_start_time': post_data['callStartTime'],
                    'call_end_time': post_data['callEndTime'],
                    'conversation_duration': post_data['conversationDuration'],  # Conversation duration
                    'dtmf': post_data['dtmf'],                              # DTMF input sequence
                    'transferred_number': post_data['transferredNumber'],    # Transferred number
                    'event_status': 'call_ended',  
                }

            call_record = request.env['voxbay.call.data.record'].sudo().search([('call_uuid','=',post_data['CallUUID'])])
            if call_record:
                call_record.write(data)
            else:
                call_record = request.env['voxbay.call.data.record'].sudo().create(data)
            call_record.create_update_lead()
            # Ensure the sales team is assigned correctly
            if call_record.lead_id and not call_record.lead_id.team_id:
                if call_record.lead_id.user_id and call_record.lead_id.user_id.sale_team_id:
                    call_record.lead_id.write({'team_id': call_record.lead_id.user_id.sale_team_id.id})
                else:
                    sales_teams = request.env['crm.team'].sudo().search([])
                    if sales_teams:
                        random_choice = random.choice(range(len(sales_teams)))
                        sales_team = sales_teams[random_choice]
                        call_record.lead_id.write({'team_id': sales_team.id})
            return json.dumps({'status': 'success',})


        except Exception as e:
            _logger.error("Exception Occurred")
            _logger.error(traceback.format_exc())
            _logger.error(post_data)

        return json.dumps({'status': 'failed',})
    
    '''
        *****Outgoing Call API******
    '''

    # Event 1: when an outgoing call initiated
    @http.route(
        '/voxbay/api/outgoing_initiated',
        type='json', auth='none', methods=["POST"], csrf=False)
    def outgoing_initiated(self, *args, **post):
        try:
            post_data: dict = request.httprequest.json
            _logger.info(f"API Outgoing Initiated Called with data: {post_data}")

            data = {
                'caller_number': post_data['callerNumber'],
                'called_number': post_data['calledNumber'],
                # 'caller_id': post_data['callerId'],
                'agent_number': post_data.get('AgentNumber',False),
                'call_uuid': post_data['CallUUID'],
                'event_status': 'agent_initiated_call',
                'call_type': 'outgoing',                
            }

            call_record = request.env['voxbay.call.data.record'].sudo().create(data)
            call_record.create_update_lead()
            return json.dumps({'status': 'success',})

        except Exception as e:
            _logger.error("Exception Occurred")
            _logger.error(traceback.format_exc())
            _logger.error(post_data)

        return json.dumps({'status': 'failed',})
    
    # Event 2: CDR push at the end of the call
    @http.route(
        '/voxbay/api/outgoing_cdr_push',
        type='json', auth='none', methods=["POST"], csrf=False)
    def outgoing_cdr_push(self, **post):
        try:
            post_data: dict = request.httprequest.json
            _logger.info(f"API Outgoing CDR Push Called with data: {post_data}")

            data = {
                'caller_number': post_data['callerNumber'],
                'called_number': post_data['calledNumber'],
                # 'caller_id': post_data['callerId'],
                'call_uuid': post_data['CallUUID'],
                'call_type': 'outgoing',     

                'agent_number': post_data['AgentNumber'],
                # 'caller_id': post_data['callerid'],
                'call_start_time': post_data['callStartTime'],
                'call_end_time': post_data['callEndTime'],
                'total_call_duration': post_data['totalCallDuration'],
                'conversation_duration': post_data['conversationDuration'],
                'dtmf': post_data['dtmf'],
                'call_status': post_data['callStatus'],
                'call_date': post_data['callDate'],
                'recording_url': post_data['recording_URL'],
                'event_status': 'call_ended',           
            }

            call_record = request.env['voxbay.call.data.record'].sudo().search([('call_uuid','=',post_data['CallUUID'])])
            if call_record:
                call_record.write(data)   
            else:
                call_record = request.env['voxbay.call.data.record'].sudo().create(data)
            call_record.create_update_lead()
            # Ensure the sales team is assigned correctly
            if call_record.lead_id and not call_record.lead_id.team_id:
                if call_record.lead_id.user_id and call_record.lead_id.user_id.sale_team_id:
                    call_record.lead_id.write({'team_id': call_record.lead_id.user_id.sale_team_id.id})
                else:
                    sales_teams = request.env['crm.team'].sudo().search([])
                    if sales_teams:
                        random_choice = random.choice(range(len(sales_teams)))
                        sales_team = sales_teams[random_choice]
                        call_record.lead_id.write({'team_id': sales_team.id})
            return json.dumps({'status': 'success',})

        except Exception as e:
            _logger.error("Exception Occurred")
            _logger.error(traceback.format_exc())
            _logger.error(post_data)

        return json.dumps({'status': 'failed',})
