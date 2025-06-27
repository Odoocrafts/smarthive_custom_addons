/** @odoo-module **/
import { StatusBarDurationField,statusBarDurationField } from "@mail/views/fields/statusbar_duration/statusbar_duration_field";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

import { Component, onWillRender, onRendered, useEffect, useExternalListener, useRef } from "@odoo/owl";

export class StatusBarDurationFieldColored extends StatusBarDurationField {

    setup(){
        super.setup()
        
        onRendered(()=>{
            console.log('this.props.record.data', this.props.record.data)
            const rootElement = $(this.rootRef.el);
            const stageColor = this.props.record.data['stage_color'];
            let selected = rootElement.find('.o_arrow_button_current')
            if (stageColor && selected) {
                selected.css('background-color', stageColor);
            }
        })
    }



    async selectItem(item) {
        const rootElement = $(this.rootRef.el);
        console.log('this.props.record.data', this.props.record.data)

        let old_selected = rootElement.find('.o_arrow_button_current')
        // Call the parent method to handle item selection
        await super.selectItem(item);
        let new_selected = rootElement.find('.o_arrow_button_current')
        // Get the stage color
        if (old_selected){
            old_selected.css('background-color', '')
        }
        // Apply the stage color if it exists and is valid
        const stageColor = this.props.record.data['stage_color'];
        if (stageColor && new_selected) {
            new_selected.css('background-color', stageColor);
        }
    }
}


export const statusBarDurationFieldColored = {
    ...statusBarDurationField,
    component: StatusBarDurationFieldColored,
}
registry.category("fields").add("statusbar_duration_colored", statusBarDurationFieldColored);
