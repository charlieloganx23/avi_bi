"""
Exemplo de uso dos módulos do Power BI Assistant
"""

import pandas as pd
import sys
sys.path.append('.')

from modules.data_analyzer import DataAnalyzer
from modules.color_generator import ColorGenerator
from modules.layout_engine import LayoutEngine
from modules.powerbi_exporter import PowerBIExporter


def exemplo_completo():
    """Exemplo de fluxo completo"""
    
    print("=" * 60)
    print("POWER BI DESIGN ASSISTANT - EXEMPLO")
    print("=" * 60)
    
    # 1. Criar dados de exemplo
    print("\n1. Criando dados de exemplo...")
    df = pd.DataFrame({
        'Data': pd.date_range('2024-01-01', periods=100, freq='D'),
        'Vendas': [1000 + i*10 + (i%7)*50 for i in range(100)],
        'Categoria': ['A', 'B', 'C'] * 33 + ['A'],
        'Região': ['Norte', 'Sul', 'Leste', 'Oeste'] * 25,
        'Lucro': [500 + i*5 + (i%5)*30 for i in range(100)]
    })
    print(f"✓ Dataset criado: {len(df)} linhas, {len(df.columns)} colunas")
    
    # 2. Analisar dados
    print("\n2. Analisando dados...")
    analyzer = DataAnalyzer()
    analysis = analyzer.analyze_dataframe(df)
    
    print(f"✓ Qualidade: {analysis['data_quality']['completeness_score']}%")
    print(f"✓ Visualizações sugeridas: {len(analysis['suggested_visuals'])}")
    
    print("\n   Top 3 visualizações sugeridas:")
    for i, viz in enumerate(analysis['suggested_visuals'][:3], 1):
        print(f"   {i}. {viz['type']} - {viz['title']}")
        print(f"      Prioridade: {viz['priority']}")
    
    # 3. Gerar paleta de cores
    print("\n3. Gerando paleta de cores...")
    color_gen = ColorGenerator()
    
    # Tenta diferentes abordagens
    palette1 = color_gen.get_preset_palette("modern_dark")
    print(f"✓ Paleta preset: {palette1['name']}")
    print(f"   Cores: {', '.join(palette1['colors'][:3])}...")
    
    palette2 = color_gen.generate_from_base_color("#1E88E5", "complementary", 5)
    print(f"\n✓ Paleta complementar gerada")
    print(f"   Cores: {', '.join(palette2['colors'])}")
    
    palette3 = color_gen.suggest_palette_for_data("financial", "professional")
    print(f"\n✓ Paleta sugerida para dados financeiros")
    print(f"   Nome: {palette3['name']}")
    
    # Valida contraste
    contrast = color_gen.validate_accessibility(
        palette1['foreground'],
        palette1['background']
    )
    print(f"\n✓ Validação de acessibilidade:")
    print(f"   Contraste: {contrast['contrast_ratio']}:1")
    print(f"   WCAG AA: {'✓' if contrast['wcag_aa_normal'] else '✗'}")
    print(f"   Rating: {contrast['rating']}")
    
    # 4. Criar layout
    print("\n4. Criando layout...")
    layout_engine = LayoutEngine()
    
    # Lista templates disponíveis
    templates = layout_engine.list_templates()
    print(f"✓ Templates disponíveis: {len(templates)}")
    
    # Gera layout
    layout = layout_engine.generate_layout("executive_summary", 6)
    print(f"\n✓ Layout '{layout['template']}' gerado")
    print(f"   Canvas: {layout['canvas']['width']}x{layout['canvas']['height']}px")
    print(f"   Visuais: {len(layout['visuals'])}")
    
    print("\n   Posições dos visuais:")
    for visual in layout['visuals'][:3]:
        pos = visual['position']
        print(f"   - {visual['id']}: {pos['width']}x{pos['height']}px em ({pos['x']}, {pos['y']})")
    
    # 5. Exportar
    print("\n5. Exportando para Power BI...")
    exporter = PowerBIExporter()
    
    # Exporta tema
    theme_json = exporter.export_theme(palette1, "ExemploTema")
    print("✓ Tema JSON gerado")
    
    # Exporta guia de layout
    layout_guide = exporter.generate_layout_guide(layout)
    print("✓ Guia de layout gerado")
    
    # Cria pacote completo
    files = exporter.create_theme_bundle(palette1, layout, "exemplo_export")
    print(f"\n✓ Pacote completo exportado:")
    for file_type, file_path in files.items():
        print(f"   - {file_type}: {file_path}")
    
    # 6. Gerar script Python
    print("\n6. Gerando script Python de análise...")
    python_script = exporter.generate_python_script(analysis, palette1)
    
    with open("exemplo_export/analise_exploratoria.py", "w", encoding="utf-8") as f:
        f.write(python_script)
    print("✓ Script Python gerado: exemplo_export/analise_exploratoria.py")
    
    print("\n" + "=" * 60)
    print("EXEMPLO CONCLUÍDO!")
    print("=" * 60)
    print("\nArquivos gerados na pasta 'exemplo_export/':")
    print("- theme.json (tema para Power BI)")
    print("- layout_guide.md (guia de implementação)")
    print("- README.md (documentação)")
    print("- analise_exploratoria.py (script Python)")
    print("\n✨ Importe o tema no Power BI: View > Themes > Browse for themes")


def exemplo_paletas():
    """Exemplo focado em paletas"""
    
    print("\n" + "=" * 60)
    print("EXEMPLO: EXPLORAÇÃO DE PALETAS")
    print("=" * 60)
    
    color_gen = ColorGenerator()
    
    # Mostra todos os presets
    print("\n📌 Paletas Preset Disponíveis:")
    for preset_name in color_gen.list_presets():
        palette = color_gen.get_preset_palette(preset_name)
        print(f"\n{palette['name']}")
        print(f"  Cores: {', '.join(palette['colors'][:5])}")
        print(f"  Primária: {palette['primary']}")
    
    # Esquemas de cores
    print("\n\n📌 Esquemas de Cores a partir de #3498DB:")
    schemes = ["analogous", "complementary", "triadic", "tetradic", "monochromatic"]
    
    for scheme in schemes:
        palette = color_gen.generate_from_base_color("#3498DB", scheme, 5)
        print(f"\n{scheme.title()}:")
        print(f"  {', '.join(palette['colors'])}")
    
    # Gradientes
    print("\n\n📌 Gradientes:")
    gradient = color_gen.generate_gradient("#FF6B6B", "#4ECDC4", 7)
    print("  De vermelho para turquesa:")
    print(f"  {' → '.join(gradient)}")


def exemplo_layouts():
    """Exemplo focado em layouts"""
    
    print("\n" + "=" * 60)
    print("EXEMPLO: TEMPLATES DE LAYOUT")
    print("=" * 60)
    
    layout_engine = LayoutEngine()
    
    # Lista todos os templates
    templates = layout_engine.list_templates()
    
    print("\n📌 Templates Disponíveis:\n")
    for template in templates:
        print(f"{template['display_name']}")
        print(f"  {template['description']}")
        print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "paletas":
            exemplo_paletas()
        elif sys.argv[1] == "layouts":
            exemplo_layouts()
        else:
            print("Uso: python exemplo.py [paletas|layouts]")
    else:
        exemplo_completo()
