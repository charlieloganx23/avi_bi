"""
Teste da análise de visuais após correção das chaves
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from modules.powerbi_connector import PowerBIConnector
from modules.data_analyzer import DataAnalyzer

def main():
    print("="*60)
    print("🧪 TESTE DE ANÁLISE DE VISUAIS")
    print("="*60)
    
    # Conectar ao Power BI
    connector = PowerBIConnector()
    
    print("\n📡 Buscando instâncias...")
    instances = connector.list_local_instances()
    
    if not instances:
        print("❌ Nenhuma instância encontrada")
        return
    
    print(f"✅ Encontrada(s) {len(instances)} instância(s)")
    
    # Conectar
    instance = instances[0]
    print(f"\n🔌 Conectando à porta {instance['port']}...")
    
    success = connector.connect_to_desktop(
        port=instance['port'],
        dataset_name=instance.get('database') or instance.get('dataset')
    )
    
    if not success:
        print("❌ Falha na conexão")
        return
    
    print("✅ Conectado!")
    
    # Criar analyzer
    print("\n🔍 Criando analyzer...")
    analyzer = DataAnalyzer(powerbi_connector=connector)
    
    # Executar análise
    print("\n📊 Executando análise de visuais...")
    try:
        analysis = analyzer.analyze_powerbi_model()
        
        print("\n" + "="*60)
        print("✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
        print("="*60)
        
        # Mostrar resumo
        print(f"\n📋 Tabelas analisadas: {analysis['model_structure']['tables_count']}")
        print(f"🔗 Relacionamentos: {analysis['model_structure']['relationships_count']}")
        
        if analysis.get('tables'):
            print(f"\n📊 Primeiras 3 tabelas:")
            for i, table in enumerate(analysis['tables'][:3], 1):
                print(f"   {i}. {table['name']}")
                print(f"      - Colunas: {table['columns_count']}")
                print(f"      - Medidas: {table['measures_count']}")
                
                if table.get('columns'):
                    print(f"      - Primeira coluna: {table['columns'][0]['name']} ({table['columns'][0]['dataType']})")
        
        if analysis.get('suggested_visuals'):
            print(f"\n💡 Visuais sugeridos: {len(analysis['suggested_visuals'])}")
            for i, visual in enumerate(analysis['suggested_visuals'][:3], 1):
                print(f"   {i}. {visual.get('type', 'N/A')} - {visual.get('title', 'N/A')}")
        
        print("\n" + "="*60)
        print("✅ TESTE PASSOU!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ ERRO na análise: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        connector.disconnect()

if __name__ == "__main__":
    main()
