import xlwings as xw
import os
from datetime import datetime, timedelta
from typing import Callable
from utils.logger import logger

# --- Main Processor ---
def process_workbook(workbook_path: str, update_function: Callable[[xw.Book], None]):
    """
    Generic function to open, process, and save a spreadsheet.
    It takes the file path and an update function as parameters.
    """
    if not os.path.exists(workbook_path):
        logger.error(f"Error: The file was not found at the path: {workbook_path}")
        return False
    return True

# --- Specific Update Functions ---
# CORRIGIDO: A função agora espera receber um objeto 'sheet'
def update_dates(sheet: xw.Sheet, cell_reference: str):
    """
    Function that updates the date in a specific cell in the spreadsheet.
    """
    try:
        cell = sheet.range(cell_reference)

        cell.clear_contents()
        
        cell.number_format = 'dd/mm/aaaa'
        cell.value = datetime.now().date()

        logger.info(f"Date updated to {datetime.now().strftime('%d/%m/%Y')} in cell {cell_reference}.")
    except Exception as e:
        logger.error(f"Error updating date in cell {cell_reference}: {e}")

def update_queries(workbook: xw.Book):
    """
    Function to refresh all queries and formulas in the workbook.
    """
    try:
        workbook.api.RefreshAll()
        workbook.app.api.CalculateUntilAsyncQueriesDone()
        logger.info("All queries and formulas were successfully updated.")
    except Exception as e:
        logger.error(f"Error updating queries: {e}")

# --- Funções específicas de atualização de planilha ---
def update_descarga(workbook: xw.Book):
    """
    Combines date, day, and query updates for the 'Descarga' workbook.
    """
    logger.info("Starting update for 'Relatorio de Descarga'...")
    
    # CORRIGIDO: Agora a gente passa a aba correta para a função
    update_dates(workbook.sheets[0], 'AH2')
    update_days(workbook)
    update_queries(workbook)
    
    logger.info("Update for 'Relatorio de Descarga' completed.")

def update_pedido_recomendado(workbook: xw.Book):
    """
    Updates the date and refreshes queries for the 'Pedido Recomendado' workbook.
    """
    logger.info("Starting update for 'Pedido Recomendado'...")
    
    sheet = workbook.sheets[1]
    date_cell = 'D3'
    
    update_dates(sheet, date_cell)
    update_queries(workbook)
    
    logger.info("Update for 'Pedido Recomendado' completed.")

def update_days(workbook: xw.Book):
    """
    Calculates and updates the number of business days and calendar days for the current month.
    """
    try:
        sheet = workbook.sheets[0]
        
        today = datetime.now().date()
        
        # Cálculo dos Dias Corridos (Dias úteis que já se passaram)
        business_days_completed = 0
        start_of_month = today.replace(day=1)
        current_day = start_of_month
        
        while current_day <= today:
            if current_day.weekday() < 5:
                business_days_completed += 1
            current_day += timedelta(days=1)

        # Cálculo dos Dias Úteis (Total do mês - 2)
        total_business_days = 0
        current_day = start_of_month
        while current_day.month == today.month:
            if current_day.weekday() < 5:
                total_business_days += 1
            current_day += timedelta(days=1)
        
        final_business_days = total_business_days - 2
        
        sheet.range('AI5').value = final_business_days
        sheet.range('AI6').value = business_days_completed
        
        logger.info(f"Updated business days ({final_business_days}) and calendar days ({business_days_completed}).")
    except Exception as e:
        logger.error(f"Error updating days: {e}")

def update_sem_compras(workbook: xw.Book):
    """
    Updates the date and refreshes queries for the 'Sem Compras' workbook.
    """
    logger.info("Starting update for 'Sem Compras'...")
    try:
        # Pega a segunda aba (índice 1)
        sheet = workbook.sheets[1]

        update_dates(sheet, "O2") 
        update_queries(workbook)

    except Exception as e:
        logger.error(f"Error updating 'Sem Compras': {e}")
    logger.info("Update for 'Sem Compras' completed.")