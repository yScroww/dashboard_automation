import os
import time
import xlwings as xw
from typing import Callable, Optional

from app.handlers.excel_handler import (
    update_descarga,
    update_pedido_recomendado,
    update_sem_compras,
)
from app.handlers.pdf_converter import convert_to_pdf
from app.handlers.whatsapp_sender import send_pdfs_via_whatsapp

from utils.file_handler import create_dated_copy
from utils.logger import logger
from utils.system_handler import kill_excel_process

from config.settings import (
    DESCARGA_PATH,
    PDF_OUTPUT_PATH,
    PEDIDO_RECOMENDADO_PATH,
    SEM_COMPRAS_PATH,
)


def automate_and_convert(
    workbook_path: str,
    output_path: str,
    update_function: Callable[[xw.Book], None],
    sheets_to_include: list,
    print_area: Optional[str] = None,
) -> Optional[str]:
    """
    Orchestrates Excel workflow:
    - Open workbook
    - Apply update function
    - Export selected sheets to PDF
    - Save and close workbook
    Returns path to generated PDF or None on failure.
    """
    app = None
    workbook = None

    try:
        app = xw.App(visible=False)
        workbook = app.books.open(workbook_path)
        logger.info(f"Workbook opened: {os.path.basename(workbook_path)}")

        time.sleep(2)  # Delay for stability
        update_function(workbook)

        file_name = os.path.splitext(os.path.basename(workbook_path))[0]
        output_pdf_path = os.path.join(output_path, f"{file_name}.pdf")

        convert_to_pdf(
            workbook,
            output_pdf_path,
            sheets_to_include=sheets_to_include,
            print_area=print_area,
        )

        workbook.save()
        logger.info(f"PDF generated: {output_pdf_path}")
        return output_pdf_path

    except Exception as e:
        logger.error(f"Automation failed for {workbook_path}: {e}")
        return None

    finally:
        if workbook:
            workbook.close()
        if app:
            app.quit()
        logger.info("Excel process terminated.")


def run_automations():
    """
    Runs all Excel automations sequentially and sends PDFs via WhatsApp.
    """
    kill_excel_process()

    generated_pdfs = []

    # --- Descarga Report ---
    if DESCARGA_PATH and os.path.exists(DESCARGA_PATH) and PDF_OUTPUT_PATH is not None:
        pdf = automate_and_convert(
            DESCARGA_PATH,
            PDF_OUTPUT_PATH,
            update_descarga,
            sheets_to_include=[0],
            print_area="A1:AI377"
        )
        if pdf:
            generated_pdfs.append(pdf)

    # --- Pedido Recomendado ---
    if PEDIDO_RECOMENDADO_PATH and os.path.exists(PEDIDO_RECOMENDADO_PATH) and PDF_OUTPUT_PATH is not None:
        dated_pedido_path = create_dated_copy(PEDIDO_RECOMENDADO_PATH, os.path.dirname(PEDIDO_RECOMENDADO_PATH))
        if dated_pedido_path:
            pdf = automate_and_convert(
                dated_pedido_path,
                PDF_OUTPUT_PATH,
                update_pedido_recomendado,
                sheets_to_include=[1],
            )
            if pdf:
                generated_pdfs.append(pdf)

    # --- Sem Compras ---
    if SEM_COMPRAS_PATH and os.path.exists(SEM_COMPRAS_PATH) and PDF_OUTPUT_PATH is not None:
        pdf = automate_and_convert(
            SEM_COMPRAS_PATH,
            PDF_OUTPUT_PATH,
            update_sem_compras,
            sheets_to_include=[0],
        )
        if pdf:
            generated_pdfs.append(pdf)

    # --- WhatsApp Sending ---
    if generated_pdfs and PDF_OUTPUT_PATH is not None:
        logger.info("Sending PDFs via WhatsApp...")
        send_pdfs_via_whatsapp(PDF_OUTPUT_PATH)
    elif not generated_pdfs:
        logger.warning("No PDFs generated. Skipping WhatsApp sending.")
    else:
        logger.error("PDF_OUTPUT_PATH is None. Cannot send PDFs via WhatsApp.")


if __name__ == "__main__":
    run_automations()
