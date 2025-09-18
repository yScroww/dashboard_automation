import os
from utils.logger import logger

def kill_excel_process():
    """
    Forcibly terminates any running Excel process.
    This is a fail-safe to prevent files from being left open.
    """
    try:
        os.system('taskkill /f /im EXCEL.EXE')
        logger.info("Excel process terminated successfully.")
    except Exception as e:
        logger.error(f"Failed to terminate Excel process: {e}")