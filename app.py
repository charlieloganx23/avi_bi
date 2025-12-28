"""
Power BI Design Assistant
Assistente inteligente para criação de layouts e visuais profissionais para Power BI
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO
import json
import os

# Importa módulos do assistente
from modules.data_analyzer import DataAnalyzer
from modules.color_generator import ColorGenerator
from modules.layout_engine import LayoutEngine
from modules.ai_assistant import AIAssistant
from modules.powerbi_exporter import PowerBIExporter
from modules.powerbi_connector import PowerBIConnector
from modules.theme_applier import ThemeApplier


# Configuração da página
st.set_page_config(
    page_title="Power BI Design Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo customizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1E88E5 0%, #AB47BC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3rem;
        font-weight: 600;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 0.5rem 0;
    }
    .color-swatch {
        width: 60px;
        height: 60px;
        border-radius: 8px;
        display: inline-block;
        margin: 5px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


# Inicializa módulos
@st.cache_resource
def initialize_modules():
    return {
        'analyzer': DataAnalyzer(),
        'color_gen': ColorGenerator(),
        'layout': LayoutEngine(),
        'ai': AIAssistant(provider="openai"),  # ou "anthropic"
        'exporter': PowerBIExporter()
    }


def main():
    """Função principal da aplicação"""
    
    # Header
    st.markdown('<h1 class="main-header">📊 Power BI Design Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Crie dashboards profissionais com ajuda de IA</p>', unsafe_allow_html=True)
    
    # Inicializa módulos
    modules = initialize_modules()
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/power-bi.png", width=80)
        st.title("⚙️ Configurações")
        
        # Seleção de modo
        mode = st.radio(
            "Modo de Operação",
            ["🎨 Análise Completa", "🔌 Conectar ao Power BI", "🎨 Paletas de Cores", "📐 Templates de Layout", "🤖 Assistente IA"],
            help="Escolha o que deseja fazer"
        )
        
        st.divider()
        
        # Configurações de IA
        with st.expander("🤖 Configurações de IA"):
            ai_provider = st.selectbox("Provider", ["OpenAI", "Anthropic", "Desabilitado"])
            if ai_provider != "Desabilitado":
                st.info("Configure sua API key no arquivo .env")
                if modules['ai'].is_available():
                    st.success("✅ IA conectada")
                else:
                    st.warning("⚠️ API key não configurada")
        
        st.divider()
        
        # Informações
        st.markdown("### 📚 Recursos")
        st.markdown("""
        - Análise automática de dados
        - Sugestões de visualizações
        - Paletas de cores profissionais
        - Templates de layout
        - Exportação para Power BI
        """)
    
    # Conteúdo principal
    if mode == "🎨 Análise Completa":
        render_complete_analysis(modules)
    elif mode == "🔌 Conectar ao Power BI":
        render_powerbi_connection(modules)
    elif mode == "🎨 Paletas de Cores":
        render_color_generator(modules)
    elif mode == "📐 Templates de Layout":
        render_layout_templates(modules)
    elif mode == "🤖 Assistente IA":
        render_ai_assistant(modules)


def render_complete_analysis(modules):
    """Renderiza análise completa de dados"""
    st.header("📊 Análise Completa de Dados")
    
    # Upload de arquivo
    uploaded_file = st.file_uploader(
        "Carregue seus dados (CSV, Excel)",
        type=['csv', 'xlsx', 'xls'],
        help="Carregue o arquivo de dados para análise"
    )
    
    if uploaded_file is not None:
        # Lê o arquivo
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ Arquivo carregado: {len(df)} linhas, {len(df.columns)} colunas")
            
            # Tabs para organizar
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📈 Preview", "🔍 Análise", "🎨 Cores", "📐 Layout", "💾 Exportar"
            ])
            
            with tab1:
                st.subheader("Preview dos Dados")
                st.dataframe(df.head(20), use_container_width=True)
                
                # Estatísticas rápidas
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Linhas", f"{len(df):,}")
                with col2:
                    st.metric("Colunas", len(df.columns))
                with col3:
                    st.metric("Valores Nulos", f"{df.isnull().sum().sum():,}")
                with col4:
                    st.metric("Duplicatas", f"{df.duplicated().sum():,}")
            
            with tab2:
                st.subheader("🔍 Análise Detalhada")
                
                with st.spinner("Analisando dados..."):
                    analysis = modules['analyzer'].analyze_dataframe(df)
                
                # Qualidade dos dados
                st.markdown("### 📊 Qualidade dos Dados")
                quality = analysis['data_quality']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        "Score de Completude",
                        f"{quality['completeness_score']}%",
                        help="Percentual de células sem valores nulos"
                    )
                with col2:
                    st.metric("Duplicatas", quality['duplicate_rows'])
                
                # Issues
                if quality['issues']:
                    st.markdown("### ⚠️ Observações")
                    for issue in quality['issues']:
                        if "✅" in issue:
                            st.success(issue)
                        elif "⚠️" in issue:
                            st.warning(issue)
                        else:
                            st.info(issue)
                
                # Análise de colunas
                st.markdown("### 📊 Análise de Colunas")
                
                for col_name, col_info in analysis['column_analysis'].items():
                    with st.expander(f"📌 {col_name} ({col_info['detected_type']})"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Tipo", col_info['dtype'])
                            st.metric("Valores Únicos", col_info['unique_count'])
                        
                        with col2:
                            st.metric("Nulos", col_info['null_count'])
                            st.metric("% Nulos", f"{col_info['null_percentage']:.1f}%")
                        
                        with col3:
                            st.metric("Tipo Detectado", col_info['detected_type'])
                        
                        # Estatísticas específicas
                        if 'min' in col_info:
                            st.markdown("**Estatísticas Numéricas:**")
                            stats_col1, stats_col2, stats_col3 = st.columns(3)
                            with stats_col1:
                                st.write(f"Min: {col_info.get('min', 'N/A')}")
                            with stats_col2:
                                st.write(f"Média: {col_info.get('mean', 'N/A'):.2f}")
                            with stats_col3:
                                st.write(f"Max: {col_info.get('max', 'N/A')}")
                        
                        elif 'top_values' in col_info:
                            st.markdown("**Top Valores:**")
                            top_df = pd.DataFrame(
                                list(col_info['top_values'].items()),
                                columns=['Valor', 'Contagem']
                            )
                            st.dataframe(top_df, use_container_width=True)
                
                # Visualizações sugeridas
                st.markdown("### 💡 Visualizações Sugeridas")
                
                for i, suggestion in enumerate(analysis['suggested_visuals'][:5], 1):
                    priority_colors = {
                        'high': '🔴',
                        'medium': '🟡',
                        'low': '🟢'
                    }
                    
                    with st.expander(
                        f"{priority_colors[suggestion['priority']]} {i}. {suggestion['title']}"
                    ):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.write(f"**Tipo:** {suggestion['type'].replace('_', ' ').title()}")
                            st.write(f"**Razão:** {suggestion['reason']}")
                            st.write(f"**Colunas sugeridas:**")
                            st.json(suggestion['columns'])
                        
                        with col2:
                            priority_label = {
                                'high': '🔴 Alta',
                                'medium': '🟡 Média',
                                'low': '🟢 Baixa'
                            }
                            st.metric("Prioridade", priority_label[suggestion['priority']])
            
            with tab3:
                st.subheader("🎨 Paletas de Cores")
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown("### Gerar Paleta")
                    
                    palette_mode = st.radio(
                        "Modo",
                        ["Presets", "Gerar da cor base", "Sugestão por contexto"]
                    )
                    
                    if palette_mode == "Presets":
                        preset_names = modules['color_gen'].list_presets()
                        selected_preset = st.selectbox("Selecione", preset_names)
                        
                        if st.button("Aplicar Preset"):
                            st.session_state.current_palette = modules['color_gen'].get_preset_palette(selected_preset)
                    
                    elif palette_mode == "Gerar da cor base":
                        base_color = st.color_picker("Cor Base", "#1E88E5")
                        scheme = st.selectbox(
                            "Esquema",
                            ["analogous", "complementary", "triadic", "tetradic", "monochromatic"]
                        )
                        color_count = st.slider("Número de cores", 3, 10, 5)
                        
                        if st.button("Gerar Paleta"):
                            st.session_state.current_palette = modules['color_gen'].generate_from_base_color(
                                base_color, scheme, color_count
                            )
                    
                    else:
                        data_type = st.selectbox(
                            "Tipo de dados",
                            ["financial", "marketing", "operations", "sales", "hr", "tech"]
                        )
                        mood = st.selectbox(
                            "Mood",
                            ["professional", "creative", "energetic", "calm", "modern"]
                        )
                        
                        if st.button("Sugerir Paleta"):
                            st.session_state.current_palette = modules['color_gen'].suggest_palette_for_data(
                                data_type, mood
                            )
                
                with col2:
                    if 'current_palette' in st.session_state:
                        palette = st.session_state.current_palette
                        
                        st.markdown(f"### {palette.get('name', 'Paleta Atual')}")
                        
                        # Mostra cores
                        st.markdown("#### Cores Principais")
                        colors_html = ""
                        for color in palette.get('colors', []):
                            colors_html += f'<div class="color-swatch" style="background-color: {color};" title="{color}"></div>'
                        st.markdown(colors_html, unsafe_allow_html=True)
                        
                        # Detalhes
                        st.markdown("#### Detalhes")
                        detail_col1, detail_col2 = st.columns(2)
                        
                        with detail_col1:
                            st.write(f"**Primária:** {palette.get('primary', 'N/A')}")
                            st.write(f"**Secundária:** {palette.get('secondary', 'N/A')}")
                            st.write(f"**Destaque:** {palette.get('accent', 'N/A')}")
                        
                        with detail_col2:
                            st.write(f"**Fundo:** {palette.get('background', 'N/A')}")
                            st.write(f"**Texto:** {palette.get('foreground', 'N/A')}")
                        
                        # Validação de contraste
                        st.markdown("#### Validação de Acessibilidade")
                        contrast_check = modules['color_gen'].validate_accessibility(
                            palette.get('foreground', '#000000'),
                            palette.get('background', '#FFFFFF')
                        )
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Contraste", f"{contrast_check['contrast_ratio']}:1")
                        with col2:
                            st.metric("WCAG AA", "✅" if contrast_check['wcag_aa_normal'] else "❌")
                        with col3:
                            st.metric("Rating", contrast_check['rating'])
            
            with tab4:
                st.subheader("📐 Templates de Layout")
                
                # Lista templates
                templates = modules['layout'].list_templates()
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown("### Selecione um Template")
                    
                    selected_template = st.selectbox(
                        "Template",
                        [t['name'] for t in templates],
                        format_func=lambda x: next(t['display_name'] for t in templates if t['name'] == x)
                    )
                    
                    template_info = next(t for t in templates if t['name'] == selected_template)
                    st.info(template_info['description'])
                    
                    visual_count = st.number_input(
                        "Número de visuais",
                        min_value=1,
                        max_value=20,
                        value=6
                    )
                    
                    if st.button("Gerar Layout"):
                        layout = modules['layout'].generate_layout(selected_template, visual_count)
                        st.session_state.current_layout = layout
                
                with col2:
                    if 'current_layout' in st.session_state:
                        layout = st.session_state.current_layout
                        
                        st.markdown(f"### Layout: {layout['template']}")
                        st.markdown(f"**Canvas:** {layout['canvas']['width']}x{layout['canvas']['height']}px")
                        
                        # Visualização do layout
                        st.markdown("#### Visualização")
                        
                        # Cria figura plotly para visualizar layout
                        fig = go.Figure()
                        
                        for visual in layout['visuals']:
                            pos = visual['position']
                            
                            # Adiciona retângulo para cada visual
                            fig.add_shape(
                                type="rect",
                                x0=pos['x'],
                                y0=pos['y'],
                                x1=pos['x'] + pos['width'],
                                y1=pos['y'] + pos['height'],
                                line=dict(color="blue", width=2),
                                fillcolor="lightblue",
                                opacity=0.3
                            )
                            
                            # Adiciona texto
                            fig.add_annotation(
                                x=pos['x'] + pos['width']/2,
                                y=pos['y'] + pos['height']/2,
                                text=visual['id'],
                                showarrow=False,
                                font=dict(size=10)
                            )
                        
                        fig.update_xaxes(range=[0, layout['canvas']['width']], showgrid=True)
                        fig.update_yaxes(range=[layout['canvas']['height'], 0], showgrid=True)
                        fig.update_layout(
                            height=500,
                            width=800,
                            showlegend=False,
                            title="Preview do Layout"
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Detalhes dos visuais
                        st.markdown("#### Detalhes dos Visuais")
                        for visual in layout['visuals']:
                            with st.expander(f"{visual['id']}"):
                                st.write(f"**Tipo:** {visual['type']}")
                                st.write(f"**Sugestão:** {visual['suggested_visual']}")
                                st.write(f"**Prioridade:** {visual['priority']}")
                                st.json(visual['position'])
            
            with tab5:
                st.subheader("💾 Exportar para Power BI")
                
                export_col1, export_col2 = st.columns(2)
                
                with export_col1:
                    st.markdown("### 🎨 Exportar Tema")
                    
                    if 'current_palette' in st.session_state:
                        theme_name = st.text_input("Nome do Tema", "MeuTemaCustomizado")
                        
                        if st.button("Gerar Arquivo de Tema"):
                            theme_json = modules['exporter'].export_theme(
                                st.session_state.current_palette,
                                theme_name
                            )
                            
                            st.download_button(
                                label="📥 Download theme.json",
                                data=theme_json,
                                file_name=f"{theme_name}.json",
                                mime="application/json"
                            )
                            
                            st.success("✅ Tema gerado!")
                            st.info("Importe no Power BI: View > Themes > Browse for themes")
                    else:
                        st.warning("⚠️ Configure uma paleta na aba Cores primeiro")
                
                with export_col2:
                    st.markdown("### 📐 Exportar Guia de Layout")
                    
                    if 'current_layout' in st.session_state:
                        if st.button("Gerar Guia de Layout"):
                            layout_guide = modules['exporter'].generate_layout_guide(
                                st.session_state.current_layout
                            )
                            
                            st.download_button(
                                label="📥 Download layout_guide.md",
                                data=layout_guide,
                                file_name="layout_guide.md",
                                mime="text/markdown"
                            )
                            
                            st.success("✅ Guia gerado!")
                    else:
                        st.warning("⚠️ Configure um layout na aba Layout primeiro")
                
                st.divider()
                
                st.markdown("### 📦 Pacote Completo")
                
                if st.button("Gerar Pacote Completo de Exportação"):
                    if 'current_palette' in st.session_state and 'current_layout' in st.session_state:
                        with st.spinner("Gerando pacote..."):
                            files = modules['exporter'].create_theme_bundle(
                                st.session_state.current_palette,
                                st.session_state.current_layout,
                                "powerbi_export"
                            )
                        
                        st.success("✅ Pacote completo gerado!")
                        st.json(files)
                        st.info("📁 Verifique a pasta 'powerbi_export' no diretório do projeto")
                    else:
                        st.error("❌ Configure paleta e layout primeiro")
        
        except Exception as e:
            st.error(f"❌ Erro ao processar arquivo: {e}")
            st.exception(e)
    
    else:
        # Instruções
        st.info("👆 Carregue um arquivo de dados para começar a análise")
        
        # Exemplo
        with st.expander("📝 Ver exemplo de dados"):
            example_df = pd.DataFrame({
                'Data': pd.date_range('2024-01-01', periods=10),
                'Vendas': [1000, 1500, 1200, 1800, 2000, 1700, 2200, 2500, 2300, 2800],
                'Categoria': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C'],
                'Região': ['Sul', 'Norte', 'Sul', 'Norte', 'Sul', 'Norte', 'Sul', 'Norte', 'Sul', 'Norte']
            })
            st.dataframe(example_df)


def render_color_generator(modules):
    """Renderiza gerador de cores standalone"""
    st.header("🎨 Gerador de Paletas de Cores")
    st.markdown("Crie paletas profissionais para seus dashboards")
    
    # Similar ao tab de cores, mas expandido
    st.info("💡 Use esta seção para explorar e criar paletas sem carregar dados")


def render_layout_templates(modules):
    """Renderiza templates de layout standalone"""
    st.header("📐 Templates de Layout")
    st.markdown("Explore templates profissionais para dashboards")
    
    # Similar ao tab de layout, mas expandido
    st.info("💡 Use esta seção para explorar layouts sem carregar dados")


def render_ai_assistant(modules):
    """Renderiza assistente de IA"""
    st.header("🤖 Assistente de IA")
    
    if not modules['ai'].is_available():
        st.warning("⚠️ Assistente de IA não disponível. Configure sua API key no arquivo .env")
        st.code("""
# Adicione ao arquivo .env:
OPENAI_API_KEY=sua_chave_aqui
# ou
ANTHROPIC_API_KEY=sua_chave_aqui
        """)
        return
    
    st.success("✅ Assistente de IA conectado")
    
    # Chat interface
    st.markdown("### 💬 Conversa com o Assistente")
    
    user_input = st.text_area(
        "Descreva o que você precisa:",
        placeholder="Ex: Preciso de um dashboard para análise de vendas com foco em comparação mensal..."
    )
    
    if st.button("Obter Sugestões"):
        if user_input:
            with st.spinner("Pensando..."):
                # Aqui você pode integrar com a IA para sugestões livres
                st.info("🤖 Recurso de chat livre em desenvolvimento. Use a Análise Completa para sugestões baseadas em dados.")
        else:
            st.warning("Digite algo primeiro")


def render_powerbi_connection(modules):
    """Renderiza interface de conexão com Power BI Desktop"""
    st.header("🔌 Conectar ao Power BI Desktop")
    
    st.markdown("""
    Esta seção permite conectar-se a uma instância do Power BI Desktop em execução 
    e analisar o modelo de dados diretamente.
    """)
    
    # Inicializa connector se não existir
    if 'pbi_connector' not in st.session_state:
        st.session_state.pbi_connector = PowerBIConnector()
    
    connector = st.session_state.pbi_connector
    
    # Status da conexão
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📡 Status da Conexão")
        status = connector.get_connection_status()
        
        if status['connected']:
            st.success(f"✅ Conectado: {status.get('connection_name', 'Unknown')}")
            st.info(f"📊 Dataset: {status.get('dataset', 'N/A')}")
            
            if st.button("🔌 Desconectar"):
                connector.disconnect()
                st.rerun()
        else:
            st.warning("⚠️ Não conectado")
    
    with col2:
        st.metric("Estado", "Conectado" if status['connected'] else "Desconectado")
    
    st.divider()
    
    # Seção de conexão
    if not status['connected']:
        st.subheader("🔍 Conectar a uma Instância")
        
        # Listar instâncias disponíveis
        if st.button("🔎 Buscar Instâncias do Power BI Desktop"):
            with st.spinner("Buscando instâncias..."):
                instances = connector.list_local_instances()
                
                if instances:
                    st.session_state.available_instances = instances
                    st.success(f"✅ Encontradas {len(instances)} instância(s)")
                else:
                    st.warning("⚠️ Nenhuma instância encontrada. Certifique-se de que o Power BI Desktop está aberto.")
        
        # Mostrar instâncias disponíveis
        if 'available_instances' in st.session_state and st.session_state.available_instances:
            st.markdown("#### Instâncias Disponíveis:")
            
            for idx, instance in enumerate(st.session_state.available_instances):
                col_inst, col_btn = st.columns([3, 1])
                
                with col_inst:
                    st.write(f"**{instance.get('name', 'Unknown')}**")
                    st.caption(f"Porta: {instance.get('port', 'N/A')}")
                
                with col_btn:
                    if st.button(f"Conectar", key=f"connect_{idx}"):
                        with st.spinner(f"Conectando..."):
                            success = connector.connect_to_desktop(
                                port=instance.get('port'),
                                dataset_name=instance.get('dataset')
                            )
                            
                            if success:
                                st.success("✅ Conectado com sucesso!")
                                st.rerun()
                            else:
                                st.error("❌ Falha ao conectar")
        
        st.divider()
        
        # Conexão manual
        with st.expander("🔧 Conexão Manual"):
            st.markdown("Conecte-se manualmente especificando os detalhes:")
            
            manual_port = st.number_input("Porta", min_value=1000, max_value=65535, value=12345)
            manual_dataset = st.text_input("Nome do Dataset (opcional)")
            
            if st.button("Conectar Manualmente"):
                with st.spinner("Conectando..."):
                    success = connector.connect_to_desktop(
                        port=manual_port,
                        dataset_name=manual_dataset if manual_dataset else None
                    )
                    
                    if success:
                        st.success("✅ Conectado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Falha ao conectar")
    
    else:
        # Mostrar análise do modelo conectado
        st.subheader("📊 Análise do Modelo")
        
        tabs = st.tabs(["📋 Estrutura", "📈 Análise de Visuais", "🎨 Aplicar Tema", "💾 Exportar"])
        
        with tabs[0]:
            render_model_structure(connector)
        
        with tabs[1]:
            render_visual_analysis(connector, modules)
        
        with tabs[2]:
            render_theme_application(connector, modules)
        
        with tabs[3]:
            render_powerbi_export(connector, modules)


def render_model_structure(connector):
    """Renderiza estrutura do modelo Power BI"""
    st.markdown("### 📋 Estrutura do Modelo")
    
    if st.button("🔄 Atualizar Estrutura"):
        with st.spinner("Carregando estrutura..."):
            structure = connector.get_model_structure()
            st.session_state.pbi_structure = structure
    
    if 'pbi_structure' in st.session_state:
        structure = st.session_state.pbi_structure
        
        # Resumo
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📊 Tabelas", len(structure.get('tables', [])))
        
        with col2:
            st.metric("📏 Medidas", len(structure.get('measures', [])))
        
        with col3:
            st.metric("🔗 Relacionamentos", len(structure.get('relationships', [])))
        
        st.divider()
        
        # Detalhes das tabelas
        st.markdown("#### Tabelas:")
        for table in structure.get('tables', []):
            with st.expander(f"📊 {table.get('name', 'Unknown')}"):
                st.write(f"**Tipo:** {table.get('type', 'N/A')}")
                st.write(f"**Colunas:** {len(table.get('columns', []))}")
                
                if table.get('columns'):
                    st.markdown("**Lista de Colunas:**")
                    for col in table['columns']:
                        st.write(f"- {col.get('name')} ({col.get('dataType', 'Unknown')})")


def render_visual_analysis(connector, modules):
    """Renderiza análise de visualizações sugeridas"""
    st.markdown("### 📈 Análise de Visuais")
    
    if st.button("🔍 Analisar Modelo"):
        with st.spinner("Analisando modelo..."):
            # Usa o data_analyzer com o connector
            analyzer = DataAnalyzer(powerbi_connector=connector)
            analysis = analyzer.analyze_powerbi_model()
            st.session_state.pbi_analysis = analysis
    
    if 'pbi_analysis' in st.session_state:
        analysis = st.session_state.pbi_analysis
        
        # Mostrar sugestões de visuais
        st.markdown("#### 🎯 Visualizações Sugeridas:")
        
        for suggestion in analysis.get('suggested_visuals', []):
            with st.expander(f"📊 {suggestion.get('type', 'Unknown').replace('_', ' ').title()}"):
                st.write(f"**Prioridade:** {suggestion.get('priority', 'N/A')}")
                st.write(f"**Razão:** {suggestion.get('reason', 'N/A')}")
                
                if 'measures' in suggestion:
                    st.write(f"**Medidas Sugeridas:**")
                    for measure in suggestion['measures']:
                        st.write(f"- {measure}")
        
        # Saúde do modelo
        st.divider()
        st.markdown("#### 🏥 Saúde do Modelo:")
        
        health = analysis.get('model_health', {})
        score = health.get('score', 0)
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.metric("Score", f"{score}%")
        
        with col2:
            if health.get('issues'):
                st.warning("⚠️ Problemas Encontrados:")
                for issue in health['issues']:
                    st.write(f"- {issue}")
            else:
                st.success("✅ Modelo em bom estado!")


def render_theme_application(connector, modules):
    """Renderiza aplicação de tema"""
    st.markdown("### 🎨 Aplicar Tema")
    
    # Inicializa theme applier
    if 'theme_applier' not in st.session_state:
        st.session_state.theme_applier = ThemeApplier(connector)
    
    theme_applier = st.session_state.theme_applier
    
    st.info("⚠️ **Nota:** A aplicação direta de temas requer permissões de escrita no modelo Power BI.")
    
    # Seleção de paleta
    st.markdown("#### Escolha uma Paleta:")
    
    color_gen = modules['color_gen']
    presets = color_gen.get_available_presets()
    
    selected_preset = st.selectbox("Paleta Predefinida", presets)
    
    if selected_preset:
        palette = color_gen.get_preset_palette(selected_preset)
        
        # Mostrar cores
        st.markdown("**Cores Primárias:**")
        cols = st.columns(len(palette['primary']))
        for idx, color in enumerate(palette['primary']):
            with cols[idx]:
                st.markdown(
                    f'<div class="color-swatch" style="background-color: {color};"></div>',
                    unsafe_allow_html=True
                )
                st.caption(color)
        
        # Aplicar tema
        if st.button("🎨 Aplicar Tema ao Modelo"):
            with st.spinner("Aplicando tema..."):
                theme_config = {
                    'name': selected_preset,
                    'colors': palette,
                    'version': '1.0'
                }
                
                result = theme_applier.apply_theme(theme_config)
                
                if result.get('success'):
                    st.success("✅ Tema aplicado com sucesso!")
                    
                    with st.expander("📋 Detalhes"):
                        st.json(result)
                else:
                    st.error("❌ Erro ao aplicar tema")
                    st.write(result.get('errors', []))


def render_powerbi_export(connector, modules):
    """Renderiza exportação de dados do Power BI"""
    st.markdown("### 💾 Exportar Configurações")
    
    st.markdown("""
    Exporte o tema atual ou a análise do modelo para uso posterior.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Exportar Tema Atual"):
            theme_applier = ThemeApplier(connector)
            current_theme = theme_applier.export_current_theme()
            
            if current_theme:
                st.download_button(
                    label="💾 Baixar Tema (JSON)",
                    data=json.dumps(current_theme, indent=2),
                    file_name="power_bi_theme_export.json",
                    mime="application/json"
                )
            else:
                st.warning("⚠️ Não foi possível exportar o tema")
    
    with col2:
        if st.button("📥 Exportar Análise do Modelo"):
            if 'pbi_analysis' in st.session_state:
                analysis = st.session_state.pbi_analysis
                
                st.download_button(
                    label="💾 Baixar Análise (JSON)",
                    data=json.dumps(analysis, indent=2),
                    file_name="model_analysis.json",
                    mime="application/json"
                )
            else:
                st.warning("⚠️ Execute a análise do modelo primeiro")


if __name__ == "__main__":

    main()
