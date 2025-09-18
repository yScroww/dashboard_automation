import os
import shutil
from datetime import datetime
from utils.logger import logger

def create_dated_copy(source_path: str, dest_dir: str):
    """
    Cria uma cópia de um arquivo e o renomeia com a data atual.
    """
    try:
        if not os.path.exists(source_path):
            logger.error(f"Erro: O arquivo de origem não foi encontrado em: {source_path}")
            return None
            
        file_name = os.path.basename(source_path)
        base_name, file_extension = os.path.splitext(file_name)
        
        # Constrói o novo nome do arquivo com a data
        today_date = datetime.now().strftime('%Y-%m-%d')
        new_file_name = f"{base_name} {today_date}{file_extension}"
        
        # Cria o caminho completo para o novo arquivo
        new_file_path = os.path.join(dest_dir, new_file_name)
        
        # Copia o arquivo
        shutil.copy2(source_path, new_file_path)
        
        logger.info(f"Cópia criada com sucesso em: {new_file_path}")
        return new_file_path
    
    except Exception as e:
        logger.error(f"Erro ao criar a cópia do arquivo: {e}")
        return None