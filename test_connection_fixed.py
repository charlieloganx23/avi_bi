"""
Script de teste para verificar se a configuração das DLLs funcionou
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from modules.powerbi_connector import PowerBIConnector

def main():
    print("="*60)
    print("🧪 TESTE DE CONEXÃO COM CONFIGURAÇÃO DE DLL CORRIGIDA")
    print("="*60)
    
    connector = PowerBIConnector()
    
    print("\n📡 Buscando instâncias do Power BI Desktop...")
    instances = connector.list_local_instances()
    
    if not instances:
        print("❌ Nenhuma instância do Power BI encontrada")
        print("💡 Abra um arquivo .pbix no Power BI Desktop e tente novamente")
        return
    
    print(f"\n✅ Encontradas {len(instances)} instância(s):")
    for i, inst in enumerate(instances, 1):
        db_name = inst.get('database') or inst.get('dataset') or 'N/A'
        print(f"   {i}. {db_name} (porta {inst['port']})")
    
    print("\n🔌 Conectando à primeira instância...")
    instance = instances[0]
    
    success = connector.connect_to_desktop(
        port=instance['port'],
        dataset_name=instance.get('database') or instance.get('dataset')
    )
    
    if not success:
        print("❌ Falha na conexão")
        return
    
    print("\n🔍 Obtendo estrutura do modelo...")
    structure = connector.get_model_structure()
    
    print("\n" + "="*60)
    print("📊 RESULTADO DA ESTRUTURA DO MODELO")
    print("="*60)
    
    tables = structure.get('tables', [])
    measures = structure.get('measures', [])
    relationships = structure.get('relationships', [])
    
    print(f"\n📋 Tabelas: {len(tables)}")
    if tables:
        print("   Top 5:")
        for i, table in enumerate(tables[:5], 1):
            cols = len(table.get('columns', []))
            print(f"   {i}. {table['name']} ({cols} colunas)")
    
    print(f"\n📏 Medidas: {len(measures)}")
    if measures:
        print("   Top 5:")
        for i, measure in enumerate(measures[:5], 1):
            print(f"   {i}. {measure.get('MeasureName', 'N/A')}")
    
    print(f"\n🔗 Relacionamentos: {len(relationships)}")
    if relationships:
        print("   Top 3:")
        for i, rel in enumerate(relationships[:3], 1):
            print(f"   {i}. {rel.get('fromTable', 'N/A')}.{rel.get('fromColumn', 'N/A')} → {rel.get('toTable', 'N/A')}.{rel.get('toColumn', 'N/A')}")
    
    print("\n" + "="*60)
    if tables or measures or relationships:
        print("✅ SUCESSO! As DLLs foram carregadas corretamente!")
    else:
        print("⚠️ Conectou mas não obteve estrutura. Verificar configuração.")
    print("="*60)
    
    connector.disconnect()

if __name__ == "__main__":
    main()
