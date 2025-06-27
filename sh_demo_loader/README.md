# SmartHive Demo Loader

This Odoo 17 module loads demo data for SmartHive CRM specifically configured for educational institutions.

## Overview

This module creates a complete demo setup for a fictional educational institution called "Noventis Institute of Technology". It configures:

- Company branding and configuration
- CRM pipeline stages specific to educational admissions
- Sales teams for different locations
- Employee records with proper job positions
- Demo leads with realistic data

## Features

- Complete setup in one click
- Realistic data to showcase CRM functionality
- Proper relationships between teams, employees and leads
- Phone numbers that trigger country detection
- Post-init hook to randomize dates and assign users

## Installation

1. Install the module through the Odoo apps interface
2. The module will automatically set up all demo data
3. No additional configuration is needed

## Technical Details

The module creates:

1. Company details for Noventis Institute of Technology
2. 7 CRM stages: New Enquiry, Contacted, Details Shared, Follow-up Scheduled, Hot Lead, Confirmed Admission, and Lost
3. 2 sales teams: Kozhikode and Ernakulam admission teams
4. 3 employees with proper job positions and user accounts
5. 10 demo leads at various stages in the admission pipeline

## Dependencies

- base
- crm
- hr
- crm_country_detect

## Author

SmartHive
https://www.smarthive.io

## License

LGPL-3
