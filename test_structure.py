"""
Teste específico de obtenção de estrutura do modelo
"""
import sys
sys.path.insert(0, '.')

from modules.powerbi_connector import PowerBIConnector

print("🔍 TESTE: Obter Estrutura do Modelo\n")

# Conectar
connector = PowerBIConnector()
instances = connector.list_local_instances()

if not instances:
    print("❌ Nenhuma instância encontrada")
    sys.exit(1)

print(f"✅ Conectando à porta {instances[0]['port']}...")
connector.connect_to_desktop(port=instances[0]['port'])

# Obter estrutura
print("\n📊 Obtendo estrutura do modelo...")
structure = connector.get_model_structure()

if structure:
    print(f"\n✅ Estrutura obtida:")
    print(f"   📊 Tabelas: {len(structure.get('tables', []))}")
    print(f"   📏 Medidas: {len(structure.get('measures', []))}")
    print(f"   🔗 Relacionamentos: {len(structure.get('relationships', []))}")
    
    # Listar primeiras 5 tabelas
    if structure.get('tables'):
        print(f"\n   📋 Primeiras tabelas:")
        for table in structure['tables'][:5]:
            cols = len(table.get('columns', []))
            print(f"   - {table['name']} ({cols} colunas)")
else:
    print("❌ Estrutura vazia")

connector.disconnect()
print("\n✅ Teste concluído!")
