from . import models
import os
import logging

_logger = logging.getLogger(__name__)

def post_init_hook(cr, registry):
    """Post-init hook to log module information for debugging"""
    module_path = os.path.dirname(os.path.abspath(__file__))
    _logger.info("CRM Custom module initialized. Module path: %s", module_path)
    
    # Check if security directory exists
    security_path = os.path.join(module_path, 'security')
    _logger.info("Security directory exists: %s", os.path.exists(security_path))
    
    # Check if access file exists
    access_file_path = os.path.join(security_path, 'ir.model.access.csv')
    _logger.info("Access file exists: %s", os.path.exists(access_file_path))
    
    # List directory contents
    if os.path.exists(security_path):
        _logger.info("Security directory contents: %s", os.listdir(security_path))