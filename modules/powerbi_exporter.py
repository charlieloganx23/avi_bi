"""
Exportador para Power BI - Gera arquivos de tema JSON e scripts
"""
import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class PowerBIExporter:
    """Exporta configurações para o Power BI"""
    
    def __init__(self):
        self.export_history = []
    
    def export_theme(self, palette: Dict[str, Any], name: str = None) -> str:
        """
        Exporta paleta de cores como tema JSON do Power BI
        
        Args:
            palette: Dicionário com cores
            name: Nome do tema
        
        Returns:
            JSON do tema formatado
        """
        if not name:
            name = palette.get("name", "Custom Theme")
        
        # Estrutura de tema do Power BI
        theme = {
            "name": name,
            "dataColors": palette.get("colors", []),
            "background": palette.get("background", "#FFFFFF"),
            "foreground": palette.get("foreground", "#000000"),
            "tableAccent": palette.get("primary", palette.get("colors", ["#1E88E5"])[0])
        }
        
        # Cores adicionais para visuais específicos
        if "primary" in palette:
            theme["primary"] = palette["primary"]
        if "secondary" in palette:
            theme["secondary"] = palette["secondary"]
        if "accent" in palette:
            theme["accent"] = palette["accent"]
        
        # Configurações avançadas de tema
        theme["visualStyles"] = {
            "*": {
                "*": {
                    "background": [
                        {
                            "color": {"solid": {"color": palette.get("background", "#FFFFFF")}},
                            "transparency": 0
                        }
                    ],
                    "border": [
                        {
                            "color": {"solid": {"color": palette.get("primary", "#E0E0E0")}},
                            "show": False
                        }
                    ]
                }
            },
            "page": {
                "*": {
                    "background": [
                        {
                            "color": {"solid": {"color": palette.get("background", "#FFFFFF")}},
                            "transparency": 0
                        }
                    ]
                }
            }
        }
        
        # Estilo de texto
        theme["textClasses"] = {
            "title": {
                "fontSize": 16,
                "fontFace": "Segoe UI",
                "color": palette.get("foreground", "#000000")
            },
            "header": {
                "fontSize": 14,
                "fontFace": "Segoe UI Semibold",
                "color": palette.get("foreground", "#000000")
            },
            "label": {
                "fontSize": 11,
                "fontFace": "Segoe UI",
                "color": palette.get("foreground", "#777777")
            }
        }
        
        return json.dumps(theme, indent=2)
    
    def export_dax_measures(self, measures: List[Dict[str, str]]) -> str:
        """
        Gera código DAX para medidas
        
        Args:
            measures: Lista de medidas com name, expression, format
        
        Returns:
            Código DAX formatado
        """
        dax_code = "// Medidas Geradas Automaticamente\n"
        dax_code += f"// Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for measure in measures:
            name = measure.get("name", "Measure")
            expression = measure.get("expression", "0")
            format_string = measure.get("format", "")
            description = measure.get("description", "")
            
            dax_code += f"{name} = \n"
            if description:
                dax_code += f"    // {description}\n"
            dax_code += f"    {expression}\n"
            if format_string:
                dax_code += f"    // Format: {format_string}\n"
            dax_code += "\n"
        
        return dax_code
    
    def generate_layout_guide(self, layout: Dict[str, Any]) -> str:
        """
        Gera guia de posicionamento para o layout
        
        Args:
            layout: Layout gerado pelo LayoutEngine
        
        Returns:
            Texto com instruções de posicionamento
        """
        guide = f"# Guia de Layout - {layout.get('template', 'Custom')}\n\n"
        guide += f"**Canvas:** {layout['canvas']['width']}x{layout['canvas']['height']} pixels\n\n"
        guide += "## Posicionamento dos Visuais\n\n"
        
        for visual in layout.get("visuals", []):
            pos = visual["position"]
            guide += f"### {visual['id']}\n"
            guide += f"- **Tipo:** {visual.get('type', 'chart')}\n"
            guide += f"- **Sugestão:** {visual.get('suggested_visual', 'Visual')}\n"
            guide += f"- **Posição:** X={pos['x']}, Y={pos['y']}\n"
            guide += f"- **Tamanho:** {pos['width']}x{pos['height']} pixels\n"
            guide += f"- **Prioridade:** {visual.get('priority', 'medium')}\n\n"
        
        guide += "\n## Como Aplicar no Power BI\n\n"
        guide += "1. Configure a página com as dimensões do canvas\n"
        guide += "2. Adicione cada visual na posição especificada\n"
        guide += "3. Ajuste os tamanhos conforme indicado\n"
        guide += "4. Siga a hierarquia de prioridades para ordenação Z\n"
        
        return guide
    
    def export_visual_configuration(self, visual_type: str, data_columns: Dict[str, str]) -> Dict[str, Any]:
        """
        Gera configuração de visual
        
        Args:
            visual_type: Tipo do visual (bar, line, scatter, etc)
            data_columns: Mapeamento de campos (x, y, legend, etc)
        
        Returns:
            Configuração do visual
        """
        config = {
            "visualType": visual_type,
            "projections": {},
            "prototypeQuery": {},
            "metadata": {
                "created": datetime.now().isoformat(),
                "generator": "PowerBI-Assistant"
            }
        }
        
        # Mapeamento de campos baseado no tipo de visual
        if visual_type in ["barChart", "columnChart"]:
            config["projections"]["Category"] = [data_columns.get("category", "")]
            config["projections"]["Y"] = [data_columns.get("value", "")]
            if "legend" in data_columns:
                config["projections"]["Series"] = [data_columns["legend"]]
        
        elif visual_type == "lineChart":
            config["projections"]["Category"] = [data_columns.get("x", "")]
            config["projections"]["Y"] = [data_columns.get("y", "")]
            if "series" in data_columns:
                config["projections"]["Series"] = [data_columns["series"]]
        
        elif visual_type == "scatterChart":
            config["projections"]["X"] = [data_columns.get("x", "")]
            config["projections"]["Y"] = [data_columns.get("y", "")]
            if "size" in data_columns:
                config["projections"]["Size"] = [data_columns["size"]]
            if "legend" in data_columns:
                config["projections"]["Series"] = [data_columns["legend"]]
        
        elif visual_type in ["pieChart", "donutChart"]:
            config["projections"]["Category"] = [data_columns.get("category", "")]
            config["projections"]["Y"] = [data_columns.get("value", "")]
        
        elif visual_type == "card":
            config["projections"]["Values"] = [data_columns.get("value", "")]
        
        elif visual_type == "table":
            config["projections"]["Values"] = list(data_columns.values())
        
        return config
    
    def generate_python_script(self, analysis: Dict[str, Any], palette: Dict[str, Any]) -> str:
        """
        Gera script Python para análise exploratória
        
        Args:
            analysis: Análise de dados
            palette: Paleta de cores
        
        Returns:
            Script Python
        """
        script = """
# Script de Análise Exploratória
# Gerado automaticamente pelo Power BI Assistant

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração de cores
COLORS = {colors}

# Carregue seus dados aqui
# df = pd.read_csv('seu_arquivo.csv')
# ou
# df = pd.read_excel('seu_arquivo.xlsx')

# Análise de dados básica
print("Resumo dos dados:")
print(df.info())
print("\\nEstatísticas descritivas:")
print(df.describe())

# Visualizações sugeridas
{visualizations}

# Salvar dashboard
# fig.write_html('dashboard.html')
"""
        
        # Formata cores
        colors_str = json.dumps(palette.get("colors", []), indent=4)
        
        # Gera código de visualizações
        viz_code = ""
        for i, visual in enumerate(analysis.get("suggested_visuals", [])[:5], 1):
            viz_type = visual.get("type", "bar_chart")
            columns = visual.get("columns", {})
            title = visual.get("title", f"Visual {i}")
            
            if viz_type == "line_chart" and "x" in columns and "y" in columns:
                viz_code += f"""
# {title}
fig{i} = px.line(df, 
                x='{columns["x"]}', 
                y={columns["y"]},
                title='{title}',
                color_discrete_sequence=COLORS)
fig{i}.show()
"""
            
            elif viz_type == "bar_chart" and "category" in columns and "value" in columns:
                viz_code += f"""
# {title}
fig{i} = px.bar(df, 
               x='{columns["category"]}', 
               y='{columns["value"]}',
               title='{title}',
               color_discrete_sequence=COLORS)
fig{i}.show()
"""
        
        return script.format(colors=colors_str, visualizations=viz_code)
    
    def export_to_file(self, content: str, filename: str, file_type: str = "json") -> str:
        """
        Salva conteúdo em arquivo
        
        Args:
            content: Conteúdo a salvar
            filename: Nome do arquivo
            file_type: Tipo do arquivo (json, txt, py, dax)
        
        Returns:
            Path do arquivo salvo
        """
        if not filename.endswith(f".{file_type}"):
            filename = f"{filename}.{file_type}"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.export_history.append({
            "filename": filename,
            "type": file_type,
            "timestamp": datetime.now().isoformat()
        })
        
        return filename
    
    def create_theme_bundle(self, palette: Dict[str, Any], layout: Dict[str, Any], 
                           output_dir: str = "powerbi_export") -> Dict[str, str]:
        """
        Cria um pacote completo de exportação
        
        Args:
            palette: Paleta de cores
            layout: Layout do dashboard
            output_dir: Diretório de saída
        
        Returns:
            Dicionário com paths dos arquivos criados
        """
        import os
        
        # Cria diretório se não existir
        os.makedirs(output_dir, exist_ok=True)
        
        files = {}
        
        # Exporta tema
        theme_json = self.export_theme(palette)
        theme_file = os.path.join(output_dir, "theme.json")
        with open(theme_file, 'w', encoding='utf-8') as f:
            f.write(theme_json)
        files["theme"] = theme_file
        
        # Exporta guia de layout
        layout_guide = self.generate_layout_guide(layout)
        layout_file = os.path.join(output_dir, "layout_guide.md")
        with open(layout_file, 'w', encoding='utf-8') as f:
            f.write(layout_guide)
        files["layout"] = layout_file
        
        # Cria README
        readme = f"""
# Power BI Dashboard Theme

Pacote de tema e layout gerado automaticamente.

## Arquivos Incluídos

- `theme.json`: Tema de cores para importar no Power BI
- `layout_guide.md`: Guia de posicionamento dos visuais

## Como Usar

### Aplicar Tema

1. Abra seu arquivo .pbix no Power BI Desktop
2. Vá em **View** > **Themes** > **Browse for themes**
3. Selecione o arquivo `theme.json`
4. Clique em **Open**

### Aplicar Layout

1. Leia o arquivo `layout_guide.md`
2. Siga as instruções de posicionamento
3. Ajuste conforme necessário para seu caso de uso

## Cores do Tema

{json.dumps(palette.get("colors", []), indent=2)}

---
Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        readme_file = os.path.join(output_dir, "README.md")
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme)
        files["readme"] = readme_file
        
        return files
