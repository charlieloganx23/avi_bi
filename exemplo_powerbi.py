"""
Exemplos de Uso do Power BI Design Assistant com Integração Power BI
"""

from modules.data_analyzer import DataAnalyzer
from modules.color_generator import ColorGenerator
from modules.layout_engine import LayoutEngine
from modules.powerbi_exporter import PowerBIExporter
from modules.powerbi_connector import PowerBIConnector
from modules.theme_applier import ThemeApplier
import pandas as pd
import json


def exemplo_conexao_powerbi():
    """Exemplo de conexão com Power BI Desktop"""
    print("=" * 60)
    print("EXEMPLO: Conexão com Power BI Desktop")
    print("=" * 60)
    
    # 1. Inicializar connector
    connector = PowerBIConnector()
    
    # 2. Listar instâncias disponíveis
    print("\n📡 Buscando instâncias do Power BI Desktop...")
    instances = connector.list_local_instances()
    
    if not instances:
        print("⚠️ Nenhuma instância encontrada.")
        print("💡 Certifique-se de que o Power BI Desktop está aberto com um arquivo .pbix")
        return
    
    print(f"✅ Encontradas {len(instances)} instância(s):")
    for idx, instance in enumerate(instances, 1):
        print(f"   {idx}. {instance.get('name')} (Porta: {instance.get('port')})")
    
    # 3. Conectar à primeira instância
    print(f"\n🔌 Conectando à primeira instância...")
    first_instance = instances[0]
    success = connector.connect_to_desktop(
        port=first_instance.get('port')
    )
    
    if not success:
        print("❌ Falha ao conectar")
        return
    
    print("✅ Conectado com sucesso!")
    
    # 4. Obter estrutura do modelo
    print("\n📊 Obtendo estrutura do modelo...")
    structure = connector.get_model_structure()
    
    print(f"   • Tabelas: {len(structure.get('tables', []))}")
    print(f"   • Medidas: {len(structure.get('measures', []))}")
    print(f"   • Relacionamentos: {len(structure.get('relationships', []))}")
    
    # 5. Listar tabelas
    if structure.get('tables'):
        print("\n📋 Tabelas encontradas:")
        for table in structure['tables'][:5]:  # Mostra apenas as 5 primeiras
            print(f"   • {table.get('name')} ({len(table.get('columns', []))} colunas)")
    
    # 6. Desconectar
    print("\n🔌 Desconectando...")
    connector.disconnect()
    print("✅ Desconectado")
    
    print("\n" + "=" * 60)
    print("EXEMPLO CONCLUÍDO!")
    print("=" * 60)


def exemplo_analise_modelo_powerbi():
    """Exemplo de análise completa de um modelo Power BI"""
    print("=" * 60)
    print("EXEMPLO: Análise de Modelo Power BI")
    print("=" * 60)
    
    # 1. Conectar ao Power BI
    connector = PowerBIConnector()
    
    print("\n📡 Conectando ao Power BI Desktop...")
    instances = connector.list_local_instances()
    
    if not instances:
        print("⚠️ Nenhuma instância encontrada. Abra o Power BI Desktop primeiro.")
        return
    
    connector.connect_to_desktop(port=instances[0].get('port'))
    print("✅ Conectado!")
    
    # 2. Criar analisador com o connector
    print("\n🔍 Analisando modelo...")
    analyzer = DataAnalyzer(powerbi_connector=connector)
    analysis = analyzer.analyze_powerbi_model()
    
    # 3. Mostrar resultados
    print(f"\n📊 Resumo da Análise:")
    print(f"   • Tabelas: {analysis['model_structure']['tables_count']}")
    print(f"   • Relacionamentos: {analysis['model_structure']['relationships_count']}")
    
    # 4. Saúde do modelo
    health = analysis['model_health']
    print(f"\n🏥 Saúde do Modelo:")
    print(f"   • Score: {health['score']}%")
    print(f"   • Status: {health['status']}")
    
    if health.get('issues'):
        print(f"   ⚠️ Problemas encontrados:")
        for issue in health['issues']:
            print(f"      - {issue}")
    
    # 5. Sugestões de visuais
    print(f"\n🎯 Visualizações Sugeridas:")
    for suggestion in analysis['suggested_visuals'][:3]:
        print(f"   • {suggestion['type'].replace('_', ' ').title()}")
        print(f"     Razão: {suggestion['reason']}")
    
    # 6. Desconectar
    connector.disconnect()
    
    print("\n" + "=" * 60)
    print("EXEMPLO CONCLUÍDO!")
    print("=" * 60)


def exemplo_aplicar_tema_powerbi():
    """Exemplo de aplicação de tema em modelo Power BI"""
    print("=" * 60)
    print("EXEMPLO: Aplicar Tema ao Power BI")
    print("=" * 60)
    
    # 1. Conectar
    connector = PowerBIConnector()
    
    print("\n📡 Conectando...")
    instances = connector.list_local_instances()
    
    if not instances:
        print("⚠️ Nenhuma instância encontrada.")
        return
    
    connector.connect_to_desktop(port=instances[0].get('port'))
    print("✅ Conectado!")
    
    # 2. Gerar paleta de cores
    print("\n🎨 Gerando paleta de cores...")
    color_gen = ColorGenerator()
    palette = color_gen.get_preset_palette('modern_dark')
    
    print(f"   Paleta: Modern Dark")
    print(f"   • Cores primárias: {len(palette['primary'])}")
    print(f"   • Cores de destaque: {len(palette['accent'])}")
    
    # 3. Criar configuração de tema
    theme_config = {
        'name': 'Modern Dark Theme',
        'version': '1.0',
        'colors': palette,
        'measure_formats': {
            # Formatos personalizados para medidas
            'Total Sales': 'R$ #,##0.00',
            'Growth %': '0.00%'
        }
    }
    
    # 4. Aplicar tema
    print("\n🎨 Aplicando tema ao modelo...")
    theme_applier = ThemeApplier(connector)
    result = theme_applier.apply_theme(theme_config)
    
    if result.get('success'):
        print("✅ Tema aplicado com sucesso!")
        
        print("\n📋 Detalhes da aplicação:")
        for item in result['applied']:
            print(f"   • {item.get('type')}: {item.get('status')}")
    else:
        print("❌ Erro ao aplicar tema")
        for error in result.get('errors', []):
            print(f"   • {error}")
    
    # 5. Desconectar
    connector.disconnect()
    
    print("\n" + "=" * 60)
    print("EXEMPLO CONCLUÍDO!")
    print("=" * 60)


def exemplo_workflow_completo_powerbi():
    """Exemplo de workflow completo: Conectar -> Analisar -> Aplicar Tema -> Exportar"""
    print("=" * 60)
    print("EXEMPLO: Workflow Completo com Power BI")
    print("=" * 60)
    
    # 1. CONEXÃO
    print("\n📡 ETAPA 1: Conectando ao Power BI...")
    connector = PowerBIConnector()
    instances = connector.list_local_instances()
    
    if not instances:
        print("⚠️ Nenhuma instância encontrada.")
        return
    
    connector.connect_to_desktop(port=instances[0].get('port'))
    print("✅ Conectado!")
    
    # 2. ANÁLISE
    print("\n🔍 ETAPA 2: Analisando modelo...")
    analyzer = DataAnalyzer(powerbi_connector=connector)
    analysis = analyzer.analyze_powerbi_model()
    
    print(f"   • {analysis['model_structure']['tables_count']} tabelas")
    print(f"   • Score de saúde: {analysis['model_health']['score']}%")
    print(f"   • {len(analysis['suggested_visuals'])} visualizações sugeridas")
    
    # 3. GERAÇÃO DE TEMA
    print("\n🎨 ETAPA 3: Gerando tema personalizado...")
    color_gen = ColorGenerator()
    
    # Gera paleta baseada em cor personalizada
    base_color = "#1E88E5"  # Azul corporativo
    palette = color_gen.generate_from_base_color(base_color, scheme='complementary')
    
    print(f"   • Paleta complementar gerada a partir de {base_color}")
    print(f"   • {len(palette['primary'])} cores primárias")
    
    # 4. APLICAÇÃO DO TEMA
    print("\n🎨 ETAPA 4: Aplicando tema...")
    theme_applier = ThemeApplier(connector)
    
    theme_config = {
        'name': 'Custom Corporate Theme',
        'version': '1.0',
        'colors': palette
    }
    
    result = theme_applier.apply_theme(theme_config)
    
    if result.get('success'):
        print("   ✅ Tema aplicado!")
    else:
        print("   ⚠️ Tema parcialmente aplicado")
    
    # 5. EXPORTAÇÃO
    print("\n💾 ETAPA 5: Exportando configurações...")
    
    # Exporta análise
    with open('exemplo_powerbi_export/analise_modelo.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print("   ✅ Análise exportada: analise_modelo.json")
    
    # Exporta tema
    with open('exemplo_powerbi_export/tema_aplicado.json', 'w', encoding='utf-8') as f:
        json.dump(theme_config, f, indent=2, ensure_ascii=False)
    
    print("   ✅ Tema exportado: tema_aplicado.json")
    
    # 6. DESCONEXÃO
    print("\n🔌 ETAPA 6: Finalizando...")
    connector.disconnect()
    print("   ✅ Desconectado")
    
    print("\n" + "=" * 60)
    print("WORKFLOW COMPLETO CONCLUÍDO!")
    print("=" * 60)
    print("\n📁 Arquivos gerados em: exemplo_powerbi_export/")
    print("   • analise_modelo.json")
    print("   • tema_aplicado.json")


def exemplo_comparar_modelos():
    """Exemplo: Comparar múltiplos modelos Power BI"""
    print("=" * 60)
    print("EXEMPLO: Comparação de Modelos")
    print("=" * 60)
    
    connector = PowerBIConnector()
    instances = connector.list_local_instances()
    
    if len(instances) < 2:
        print("⚠️ Este exemplo requer pelo menos 2 instâncias do Power BI abertas")
        print(f"   Encontradas: {len(instances)}")
        return
    
    models_analysis = []
    
    # Analisa cada modelo
    for idx, instance in enumerate(instances[:2], 1):
        print(f"\n📊 Analisando Modelo {idx}...")
        
        connector.connect_to_desktop(port=instance.get('port'))
        analyzer = DataAnalyzer(powerbi_connector=connector)
        analysis = analyzer.analyze_powerbi_model()
        
        models_analysis.append({
            'instance': instance.get('name'),
            'tables': analysis['model_structure']['tables_count'],
            'health_score': analysis['model_health']['score'],
            'visuals_suggested': len(analysis['suggested_visuals'])
        })
        
        connector.disconnect()
    
    # Comparação
    print("\n📊 COMPARAÇÃO:")
    print("-" * 60)
    print(f"{'Métrica':<25} {'Modelo 1':<15} {'Modelo 2':<15}")
    print("-" * 60)
    print(f"{'Instância':<25} {models_analysis[0]['instance'][:14]:<15} {models_analysis[1]['instance'][:14]:<15}")
    print(f"{'Tabelas':<25} {models_analysis[0]['tables']:<15} {models_analysis[1]['tables']:<15}")
    print(f"{'Score de Saúde':<25} {models_analysis[0]['health_score']:<15} {models_analysis[1]['health_score']:<15}")
    print(f"{'Visuais Sugeridos':<25} {models_analysis[0]['visuals_suggested']:<15} {models_analysis[1]['visuals_suggested']:<15}")
    print("-" * 60)
    
    # Recomendação
    best_model = 1 if models_analysis[0]['health_score'] > models_analysis[1]['health_score'] else 2
    print(f"\n🏆 Modelo {best_model} possui melhor score de saúde!")
    
    print("\n" + "=" * 60)
    print("EXEMPLO CONCLUÍDO!")
    print("=" * 60)


# Menu interativo
def main():
    """Menu principal de exemplos"""
    print("\n" + "=" * 60)
    print("Power BI Design Assistant - Exemplos com Integração Power BI")
    print("=" * 60)
    print("\nEscolha um exemplo:")
    print("1. Conexão Básica com Power BI")
    print("2. Análise de Modelo Power BI")
    print("3. Aplicar Tema ao Power BI")
    print("4. Workflow Completo")
    print("5. Comparar Múltiplos Modelos")
    print("0. Executar todos os exemplos")
    
    choice = input("\nDigite o número do exemplo: ")
    
    if choice == "1":
        exemplo_conexao_powerbi()
    elif choice == "2":
        exemplo_analise_modelo_powerbi()
    elif choice == "3":
        exemplo_aplicar_tema_powerbi()
    elif choice == "4":
        exemplo_workflow_completo_powerbi()
    elif choice == "5":
        exemplo_comparar_modelos()
    elif choice == "0":
        exemplo_conexao_powerbi()
        print("\n")
        exemplo_analise_modelo_powerbi()
        print("\n")
        exemplo_aplicar_tema_powerbi()
        print("\n")
        exemplo_workflow_completo_powerbi()
    else:
        print("❌ Opção inválida")


if __name__ == "__main__":
    main()
