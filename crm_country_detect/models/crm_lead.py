import phonenumbers
from phonenumbers import geocoder
import pycountry
from odoo import api, fields, models

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    possible_country = fields.Char(
        string='Possible Country',
        compute='_compute_possible_country',
        store=True,
        help='Country detected from phone number'
    )

    country_flag = fields.Char(
        string='Country Flag',
        compute='_compute_possible_country',
        store=True,
        help='Flag of the detected country'
    )

    @api.depends('phone')
    def _compute_possible_country(self):
        for lead in self:
            country_name = "Unknown"
            country_flag = "🏳️"
            phone = (lead.phone or '').strip()

            try:
                parsed_number = phonenumbers.parse(phone, None)
                country_code = geocoder.region_code_for_number(parsed_number)
                if country_code:
                    country = pycountry.countries.get(alpha_2=country_code.upper())
                    if country:
                        country_name = country.name
                        # Unicode flags use regional indicators A=0x1F1E6, B=0x1F1E7, ...
                        country_flag = ''.join(
                            chr(0x1F1E6 + ord(c) - ord('A')) for c in country.alpha_2
                        )
            except Exception:
                pass  # If parsing fails, fallback to Unknown

            lead.possible_country = country_name
            lead.country_flag = country_flag

    @api.model
    def update_country_detection_for_existing_leads(self, limit=500):
        """
        Update country detection for existing leads in batches
        This method is meant to be called by a scheduled action
        """
        # Get leads that have a phone number but may need country detection update
        leads = self.search([
            '|',
            ('possible_country', '=', False),
            '&',
            ('possible_country', '=', 'Unknown'),
            ('phone', '!=', False)
        ], limit=limit)
        
        if leads:
            # Force recomputation of the fields
            leads._compute_possible_country()
            return f"Updated {len(leads)} lead records with country detection"
        return "No leads to update"
