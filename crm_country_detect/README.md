# CRM Country Detection from Phone

## Overview
This Odoo 17 module enhances the CRM functionality by automatically detecting a lead's country from their phone number and displaying the corresponding country flag in the kanban view.

## Features
- Automatic country detection from phone numbers
- Country flag display in CRM kanban views
- Scheduled background processing for existing leads
- Improved lead management with geographic information

## Technical Details
The module uses Python libraries (phonenumbers and pycountry) to parse phone numbers and detect the country of origin. It then associates the country information with the lead and displays the flag in the UI.

## Dependencies
- crm
- External Python libraries:
  - phonenumbers
  - pycountry

## Installation
1. Install required Python dependencies: `pip install phonenumbers pycountry`
2. Install the module in Odoo
3. The module will automatically start detecting countries for new leads

## Configuration
No additional configuration is needed after installation. The module includes:
- Automatic country detection for new leads
- A scheduled action to process existing leads

## Usage
Once installed, the module will:
1. Automatically detect the country for new leads with phone numbers
2. Display country flags in kanban views
3. Run a scheduled task to process existing leads

## Author
Odoocrafts

## License
LGPL-3
