# controllers/app_activity_counter.py
from odoo import http,fields
from odoo.http import request

class AppActivityCounter(http.Controller):
    _name = "app.activity.counter"

    @http.route('/app_activity/counts', type='json', auth='user')
    def get_activity_counts(self):
        activity_data = {}
        try:

            # Count of activities grouped by res_model (mail.activity)
            activities = request.env["mail.activity"].read_group(
                domain=[("user_id", "=", request.env.user.id)],
                fields=["res_model"],
                groupby=["res_model"]
            )

            for act in activities:
                model_name = act.get("res_model")
                count = act.get("res_model_count", 0)
                if model_name and count > 0:
                    activity_data[model_name] = count
            # approval module
            helpdesk_count = request.env['helpdesk.ticket'].sudo().search_count([
                ('state','=','submitted'),
                ('category_id.team_id.member_ids', 'in', request.uid)
            ])
            activity_data['helpdesk.ticket'] = helpdesk_count
            approval_count = request.env['approval.request'].sudo().search_count([
                ('state', '=', 'submitted'),
                ('approver_ids.approver_id', '=', request.uid),  # User is an approver
                ('approved_by_ids', 'not in', request.uid)  # User has NOT approved
            ])

            activity_data['approval.request'] = approval_count

            # Additionally, for example, fetch count of submitted daily work reports
            daily_report_count = request.env['employee.report'].sudo().search_count([
                ('name.parent_id.user_id', '=', request.uid),
                ('state', '=', 'submitted'),
                ('date','=', fields.Date.today())
            ])
            activity_data['employee.report'] = daily_report_count

            #MoM Count
            employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.uid)], limit=1)
            mom_count = 0  # Default value in case no employee is found

            if employee:
                mom_count = request.env['mom.action.plan'].sudo().search_count([
                    ('responsible_id', '=', employee.id),
                    ('state','!=','completed')
                ])
            activity_data['mom.action.plan'] = mom_count

            #Task Count
            task_count = request.env['project.task'].sudo().search_count([
                ('user_ids', 'in', [request.uid]),
                ('state', '=', '01_in_progress')
            ])
            activity_data['project.task'] = task_count

            # Discus Count
            partner = request.env.user.partner_id
            unread_count = request.env['discuss.channel.member'].search([('partner_id', '=', partner.id)]).mapped(
                'message_unread_counter')

            total_unread = sum(unread_count) if unread_count else 0
            activity_data['mail.message_unread'] = total_unread


            # You can add counts for other models similarly:
            # e.g., For a custom model 'custom.model'
            # custom_count = request.env['custom.model'].sudo().search_count([])
            # activity_data['custom.model'] = custom_count

            print("Activity counts: %s", activity_data)
        except Exception as e:
            print("Error in get_activity_counts: %s", e)
            activity_data["error"] = str(e)
        return activity_data
