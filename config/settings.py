from dotenv import load_dotenv
import os

load_dotenv(override=True)

DESCARGA_PATH = os.getenv("DESCARGA_PATH")
PEDIDO_RECOMENDADO_PATH = os.getenv("PEDIDO_RECOMENDADO_PATH")
SEM_COMPRAS_PATH = os.getenv("SEM_COMPRAS_PATH")
PDF_OUTPUT_PATH = os.getenv("PDF_OUTPUT_PATH")
WHATSAPP_GROUP_NAME = os.getenv("WHATSAPP_GROUP_NAME")
