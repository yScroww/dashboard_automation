import os
import time
import xlwings as xw
from typing import Optional
from utils.logger import logger

def get_used_range(sheet):
    """
    Retorna o endereço da área utilizada em uma aba (ex: 'A1:F100').
    """
    try:
        last_cell = sheet.api.UsedRange.SpecialCells(11)  # xlCellTypeLastCell = 11
        last_row = last_cell.Row
        last_col = last_cell.Column

        start_cell = sheet.range((1, 1)).get_address(False, False)
        end_cell = sheet.range((last_row, last_col)).get_address(False, False)
        return f"{start_cell}:{end_cell}"
    except Exception as e:
        logger.error(f"Error detecting used range for sheet '{sheet.name}': {e}")
        return None

def convert_to_pdf(workbook: xw.Book, output_path: Optional[str], sheets_to_include: Optional[list] = None, print_area: Optional[str] = None):
    """
    Converts specific sheets (by index) to a PDF file.
    If print_area is not provided, auto-detects the used range.
    """
    try:
        if output_path is None:
            logger.error("Error: The provided output_path is not a valid string.")
            return

        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")

        if sheets_to_include:
            logger.info(f"Exporting sheets by index: {sheets_to_include}")
            for idx in sheets_to_include:
                try:
                    sheet = workbook.sheets[idx]

                    # Definir área de impressão (manual ou automática)
                    area = print_area or get_used_range(sheet)
                    if area:
                        sheet.api.PageSetup.PrintArea = area
                        logger.info(f"Print area set to '{area}' for sheet '{sheet.name}'.")

                    # Exporta apenas essa aba
                    sheet.api.ExportAsFixedFormat(0, output_path)
                    logger.info(f"Sheet '{sheet.name}' exported to PDF at: {output_path}")

                except Exception as e:
                    logger.error(f"Error exporting sheet index {idx}: {e}")
        else:
            workbook.api.ExportAsFixedFormat(0, output_path)
            logger.warning("No sheet indexes provided, exported the entire workbook.")

        time.sleep(2)
        logger.info(f"PDF successfully created at: {output_path}")

    except Exception as e:
        logger.error(f"Error converting workbook to PDF: {e}")
