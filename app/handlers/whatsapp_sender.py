import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from utils.logger import logger
from config.settings import WHATSAPP_GROUP_NAME
from typing import Optional

def send_pdfs_via_whatsapp(pdf_folder: str, group_name: Optional[str] = WHATSAPP_GROUP_NAME, max_attempts: int = 3):
    """
    Envia cada PDF da pasta para o grupo do WhatsApp separadamente.
    Lida com input invisível do botão 'Documento' do WhatsApp Web.
    """
    driver = None
    try:
        logger.info("Starting WhatsApp automation...")

        # --- Configuração do Chrome ---
        options = webdriver.ChromeOptions()
        user_data_dir = os.path.join(os.getcwd(), "User_Data")
        os.makedirs(user_data_dir, exist_ok=True)
        options.add_argument(f"--user-data-dir={user_data_dir}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--remote-allow-origins=*")
        options.add_argument("--remote-debugging-port=9222")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://web.whatsapp.com/")
        wait = WebDriverWait(driver, 60)

        # --- Espera login ---
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
        logger.info("WhatsApp Web ready.")

        # --- Seleciona grupo ---
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.click()
        if not group_name:
            logger.error("Group name must not be None.")
            return
        search_box.send_keys(group_name)
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[@title='{group_name}']"))).click()
        logger.info(f"Opened group: {group_name}")

        # --- Itera pelos PDFs ---
        pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]
        if not pdf_files:
            logger.warning("No PDFs found in folder.")
            return

        for file in pdf_files:
            file_path = os.path.join(pdf_folder, file)
            logger.info(f"Processing file: {file_path}")

            attempt = 0
            while attempt < max_attempts:
                try:
                    # --- Clicar no "+" para abrir menu ---
                    plus_btn = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='plus-rounded']"))
                    )
                    plus_btn.click()
                    time.sleep(0.5)

                    # --- Encontrar o input escondido dentro do botão "Documento" ---
                    document_div = wait.until(
                        EC.presence_of_element_located((By.XPATH, "//div[.//span[text()='Documento']]"))
                    )
                    file_input = document_div.find_element(By.XPATH, ".//input[@type='file']")
                    file_input.send_keys(file_path)
                    logger.info(f"PDF added: {file_path}")

                    # --- Espera botão enviar ficar clicável ---
                    send_btn = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Enviar']"))
                    )
                    send_btn.click()
                    logger.info(f"File sent successfully: {file_path}")
                    time.sleep(2)  # Pequena pausa entre mensagens
                    break  # sucesso, sai do loop

                except (TimeoutException, ElementClickInterceptedException) as e:
                    attempt += 1
                    logger.warning(f"Attempt {attempt}/{max_attempts} failed for {file}. Retrying...")
                    time.sleep(2)
                    if attempt >= max_attempts:
                        logger.error(f"Failed to send {file} after {max_attempts} attempts. Skipping.")
                        break
        time.sleep(5)  # Espera final para garantir envio
        logger.info("All PDFs processed via WhatsApp.")

    except Exception as e:
        logger.error(f"Error in WhatsApp automation: {e}")

    finally:
        if driver:
            driver.quit()
            logger.info("Chrome driver closed.")
