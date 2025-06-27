/** @odoo-module **/

import { jsonrpc } from "@web/core/network/rpc_service";
import { url } from '@web/core/utils/urls';
import { useService } from '@web/core/utils/hooks';
import { Component, onWillUnmount, onMounted, useState } from '@odoo/owl';

export class AppsBar extends Component {
    static template = 'muk_web_appsbar.AppsBar';

    setup() {
        this.companyService = useService('company');
        this.appMenuService = useService('app_menu');

        if (this.companyService.currentCompany.has_appsbar_image) {
            this.sidebarImageUrl = url('/web/image', {
                model: 'res.company',
                field: 'appbar_image',
                id: this.companyService.currentCompany.id,
            });
        }

        // Initialize the state with apps and an extra property for unread messages
        this.state = useState({
            apps: this.appMenuService.getAppsMenuItems(),
       
        });

        onMounted(async () => {
            await this.fetchActivityCounts();
        });

        const renderAfterMenuChange = () => {
            this.render();
        };
        this.env.bus.addEventListener('MENUS:APP-CHANGED', renderAfterMenuChange);
        onWillUnmount(() => {
            this.env.bus.removeEventListener('MENUS:APP-CHANGED', renderAfterMenuChange);
        });
    }

    async fetchActivityCounts() {
        try {
            // Fetch counts for various apps including messages
            const counts = await jsonrpc('/app_activity/counts', {});
            console.log("Fetched activity counts:", counts);

            // Define a mapping between app.xmlid and the model names returned by the controller.
            const modelMapping = {
                'custom_helpdesk.menu_helpdesk_root': 'helpdesk.ticket',
                'hr_policy.hr_policy_root_menu': 'hr.policy',
                'custom_approval.menu_custom_approvals_root': 'approval.request',
                'hr_holidays.menu_hr_holidays_root': 'hr.leave',
                'MOM.menu_mom_root': 'mom.action.plan',
                'daily_report.menu_daily_report_root': 'employee.report',
                'crm.crm_menu_root': 'crm.lead',
                'project.menu_main_pm': 'project.task',
                'mail.menu_root_discuss': 'mail.message_unread',

                // Assume your messaging app uses this xmlid and count key:
            };

            // Update the apps with their corresponding activity count.
            const updatedApps = this.state.apps.map(app => {
                const modelName = modelMapping[app.xmlid] || undefined;
                console.log(`Mapping for app ${app.name} (xmlid: ${app.xmlid}):`, modelName);
                return {
                    ...app,
                    activityCount: modelName ? (counts[modelName] || 0) : 0,
                };
            });

            // Optionally, if you want a dedicated unread count property for messages:
            const mailUnreadCount = counts['mail.channel'] || 0;

            // Update the reactive state with the new data.
            this.state.apps = updatedApps;
        } catch (error) {
            console.error("Error fetching activity counts:", error);
        }
    }
}
