# Dashbords Automation

This project automates the generation, conversion, and distribution of
reports (PDFs, Excels, PowerPoints) with direct integration to WhatsApp
Web for automated sharing.

## 📂 Project Structure

    app/
     ├── handlers/                 # Main business logic
     │   ├── excel_handler.py       # Excel processing and handling
     │   ├── pdf_converter.py       # PDF conversion utilities
     │   ├── whatsapp_sender.py     # WhatsApp Web automation for sending files
     │
     ├── services/
     │   ├── automation_service.py  # Orchestration of automation processes
     │
    config/
     ├── settings.py                # Environment variables and configurations
     ├── .env                       # Local secrets and paths
     │
    utils/
     ├── file_handler.py            # File system utilities
     ├── logger.py                  # Logging setup and configuration
     ├── system_handler.py          # System-level helpers
     │
    chrome-data/                    # Chrome session cache (user data)
    pdfs/                           # Folder containing generated PDFs
    User_Data/                      # WhatsApp Web profile persistence
    main.py                         # Main entry point for full automation
    mini_main.py                    # Minimal entry point for WhatsApp PDF sending only
    requirements.txt                # Python dependencies

## 🚀 Features

-   Automated processing of Excel and PDF files
-   Conversion and preparation of reports
-   Integration with **WhatsApp Web** for automatic report sharing
-   Logging system for debugging and monitoring
-   Configurable with environment variables via `.env`

## ⚙️ Setup

### 1. Clone the repository

``` bash
git clone https://github.com/your-username/dashbords-automation.git
cd dashbords-automation
```

### 2. Create and activate a virtual environment

``` bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate    # Windows
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file (or copy from `example.env`) and set the following
variables:

    WHATSAPP_GROUP_NAME=Your Group Name
    DESCARGA_PATH=./pdfs

## ▶️ Usage

### Run full automation

``` bash
python main.py
```

### Run WhatsApp-only automation (send PDFs)

``` bash
python mini_main.py
```

## 📝 Logging

Logs are automatically generated and saved in the `logs/` directory for
each run.

## 🔧 Requirements

-   Python 3.10+
-   Google Chrome (latest)
-   ChromeDriver (managed automatically with `webdriver_manager`)

## 📌 Notes

-   WhatsApp Web requires an active session. The first run will ask you
    to scan the QR code. Session data will be stored inside `User_Data/`
    for persistence.
-   Make sure Chrome is installed and compatible with
    `webdriver_manager`.

------------------------------------------------------------------------

### 📄 License

MIT License – feel free to use and adapt.