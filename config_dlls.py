# Configuração DLLs Analysis Services
import sys
import os

# Adicionar diretório das DLLs
dll_path = r'C:\Program Files\Microsoft SQL Server\160\DTS\Binn'
if dll_path not in sys.path:
    sys.path.append(dll_path)

# Adicionar ao PATH do sistema
os.environ['PATH'] = dll_path + os.pathsep + os.environ.get('PATH', '')

print(f"✅ DLLs Analysis Services configuradas: {dll_path}")
