"""
Diagnóstico e Configuração - Localizar DLLs do Analysis Services
"""
import os
import sys
from pathlib import Path

print("=" * 70)
print("🔍 DIAGNÓSTICO: Localizar DLLs do Analysis Services")
print("=" * 70)

# Locais comuns onde o SSMS instala as DLLs
dll_locations = [
    # Program Files
    r"C:\Program Files\Microsoft SQL Server\*\Tools\Binn",
    r"C:\Program Files (x86)\Microsoft SQL Server\*\Tools\Binn",
    r"C:\Program Files\Microsoft SQL Server\*\SDK\Assemblies",
    r"C:\Program Files (x86)\Microsoft SQL Server\*\SDK\Assemblies",
    
    # Windows Assembly (GAC)
    r"C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Microsoft.AnalysisServices.AdomdClient",
    r"C:\Windows\Microsoft.NET\assembly\GAC_64\Microsoft.AnalysisServices.AdomdClient",
    
    # Versões específicas
    r"C:\Program Files\Microsoft SQL Server\150\SDK\Assemblies",  # SQL 2019
    r"C:\Program Files\Microsoft SQL Server\160\SDK\Assemblies",  # SQL 2022
    
    # NuGet packages (se instalado via Visual Studio)
    r"C:\Users\*\.nuget\packages\microsoft.analysisservices.adomdclient",
]

print("\n1️⃣ Procurando DLLs nos locais padrão...\n")

found_dlls = []

for location_pattern in dll_locations:
    # Expande wildcards
    if '*' in location_pattern:
        base = location_pattern.split('*')[0]
        if os.path.exists(base):
            for root, dirs, files in os.walk(base):
                for file in files:
                    if file.endswith('.dll') and 'AnalysisServices' in file:
                        full_path = os.path.join(root, file)
                        found_dlls.append(full_path)
                        print(f"✅ Encontrado: {full_path}")
    else:
        if os.path.exists(location_pattern):
            for file in os.listdir(location_pattern):
                if file.endswith('.dll') and 'AnalysisServices' in file:
                    full_path = os.path.join(location_pattern, file)
                    found_dlls.append(full_path)
                    print(f"✅ Encontrado: {full_path}")

if not found_dlls:
    print("❌ Nenhuma DLL encontrada nos locais padrão")
    print("\n💡 Vamos procurar manualmente...")
    
    # Busca mais profunda
    print("\n2️⃣ Buscando em Program Files... (pode levar alguns segundos)")
    
    for root in [r"C:\Program Files", r"C:\Program Files (x86)"]:
        if os.path.exists(root):
            for dirpath, dirnames, filenames in os.walk(root):
                # Pular diretórios grandes/desnecessários
                dirnames[:] = [d for d in dirnames if d not in ['Windows Kits', 'WindowsApps', 'Common Files']]
                
                for filename in filenames:
                    if 'Microsoft.AnalysisServices.AdomdClient.dll' in filename or \
                       'Microsoft.AnalysisServices.Tabular.dll' in filename:
                        full_path = os.path.join(dirpath, filename)
                        found_dlls.append(full_path)
                        print(f"✅ Encontrado: {full_path}")

print(f"\n{'=' * 70}")
print(f"📊 RESUMO: Encontradas {len(found_dlls)} DLL(s)")
print('=' * 70)

if found_dlls:
    print("\n3️⃣ DLLs importantes:\n")
    
    adomd_dlls = [d for d in found_dlls if 'AdomdClient' in d]
    tabular_dlls = [d for d in found_dlls if 'Tabular' in d]
    
    if adomd_dlls:
        print("📦 ADOMD Client:")
        for dll in adomd_dlls:
            print(f"   - {dll}")
    
    if tabular_dlls:
        print("\n📦 Tabular Object Model:")
        for dll in tabular_dlls:
            print(f"   - {dll}")
    
    # Selecionar melhor DLL (mais recente)
    best_adomd = None
    best_tabular = None
    
    if adomd_dlls:
        # Preferir versões em SDK\Assemblies e mais recentes (160 > 150)
        for dll in sorted(adomd_dlls, reverse=True):
            if 'SDK' in dll and 'Assemblies' in dll:
                best_adomd = dll
                break
        if not best_adomd:
            best_adomd = adomd_dlls[0]
    
    if tabular_dlls:
        for dll in sorted(tabular_dlls, reverse=True):
            if 'SDK' in dll and 'Assemblies' in dll:
                best_tabular = dll
                break
        if not best_tabular:
            best_tabular = tabular_dlls[0]
    
    print(f"\n{'=' * 70}")
    print("✅ SOLUÇÃO: Adicionar DLLs ao PATH do Python")
    print('=' * 70)
    
    if best_adomd or best_tabular:
        dll_dir = os.path.dirname(best_adomd if best_adomd else best_tabular)
        
        print(f"\n📂 Diretório recomendado: {dll_dir}\n")
        
        print("4️⃣ Como configurar:\n")
        print("Opção A - Adicionar ao código Python:")
        print("-" * 70)
        print("import sys")
        print("import os")
        print(f"dll_path = r'{dll_dir}'")
        print("if dll_path not in sys.path:")
        print("    sys.path.append(dll_path)")
        print("os.environ['PATH'] = dll_path + os.pathsep + os.environ.get('PATH', '')")
        print("-" * 70)
        
        print("\nOpção B - Criar arquivo de configuração:")
        print("-" * 70)
        config_content = f"""# Configuração DLLs Analysis Services
import sys
import os

# Adicionar diretório das DLLs
dll_path = r'{dll_dir}'
if dll_path not in sys.path:
    sys.path.append(dll_path)

# Adicionar ao PATH do sistema
os.environ['PATH'] = dll_path + os.pathsep + os.environ.get('PATH', '')

print(f"✅ DLLs Analysis Services configuradas: {{dll_path}}")
"""
        
        with open('config_dlls.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print("✅ Arquivo 'config_dlls.py' criado!")
        print("-" * 70)
        
        print("\n5️⃣ Próximos passos:\n")
        print("1. Importe config_dlls.py no início do seu código:")
        print("   import config_dlls")
        print("   from modules.powerbi_connector import PowerBIConnector")
        print("")
        print("2. OU execute o teste:")
        print("   python test_with_dlls.py")
        print("")
        print("3. Reinicie o Streamlit para aplicar mudanças")

else:
    print("\n❌ PROBLEMA: SSMS instalado mas DLLs não encontradas")
    print("\n💡 Soluções:")
    print("1. Reinstalar SSMS: https://aka.ms/ssmsfullsetup")
    print("2. OU instalar Client Libraries separadamente:")
    print("   https://docs.microsoft.com/analysis-services/client-libraries")
    print("3. Verificar se SSMS foi instalado completamente (não foi cancelado)")

print(f"\n{'=' * 70}")
print("✅ Diagnóstico concluído!")
print('=' * 70)
