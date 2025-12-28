# 📊 Power BI Design Assistant - Integração com Power BI Desktop

## Novidades: Conexão Direta com Power BI

O assistente agora suporta **conexão direta com o Power BI Desktop** via powerbi-modeling-mcp, permitindo:

✨ **Funcionalidades Principais:**

- 🔌 **Conexão Automática**: Detecta instâncias do Power BI Desktop em execução
- 📊 **Análise de Modelos**: Analisa tabelas, medidas, relacionamentos e estrutura
- 🎨 **Aplicação de Temas**: Aplica paletas de cores diretamente no modelo
- 🏥 **Saúde do Modelo**: Avalia a qualidade e integridade do modelo
- 💾 **Exportação**: Exporta análises e configurações

## 🚀 Como Usar

### 1. Via Interface Streamlit

```bash
streamlit run app.py
```

Na interface, selecione o modo **"🔌 Conectar ao Power BI"**:

1. **Buscar Instâncias**: Clique em "Buscar Instâncias do Power BI Desktop"
2. **Conectar**: Escolha uma instância e clique em "Conectar"
3. **Analisar**: Explore a estrutura do modelo, análise de visuais, e aplicação de temas

### 2. Via Exemplos em Python

```bash
python exemplo_powerbi.py
```

Escolha entre os exemplos:
- **1**: Conexão básica
- **2**: Análise de modelo
- **3**: Aplicar tema
- **4**: Workflow completo
- **5**: Comparar múltiplos modelos

### 3. Programaticamente

```python
from modules.powerbi_connector import PowerBIConnector
from modules.data_analyzer import DataAnalyzer
from modules.theme_applier import ThemeApplier

# Conectar
connector = PowerBIConnector()
instances = connector.list_local_instances()
connector.connect_to_desktop(port=instances[0]['port'])

# Analisar
analyzer = DataAnalyzer(powerbi_connector=connector)
analysis = analyzer.analyze_powerbi_model()

print(f"Tabelas: {analysis['model_structure']['tables_count']}")
print(f"Score de Saúde: {analysis['model_health']['score']}%")

# Aplicar tema
from modules.color_generator import ColorGenerator

color_gen = ColorGenerator()
palette = color_gen.get_preset_palette('modern_dark')

theme_applier = ThemeApplier(connector)
result = theme_applier.apply_theme({
    'name': 'Modern Dark',
    'colors': palette
})

# Desconectar
connector.disconnect()
```

## 📋 Requisitos

Para usar a integração com Power BI:

1. **Power BI Desktop** deve estar aberto com um arquivo .pbix
2. Os **MCP tools** devem estar disponíveis:
   - `mcp_powerbi_model_connection_operations`
   - `mcp_powerbi_model_dax_query_operations`

## 🎯 Funcionalidades Detalhadas

### Análise de Modelo

O analisador detecta:
- **Tipos de dados**: Identifica datas, métricas, categorias, identificadores
- **Relacionamentos**: Mapeia conexões entre tabelas
- **Medidas DAX**: Lista todas as medidas do modelo
- **Saúde**: Avalia problemas como tabelas desconectadas

### Aplicação de Temas

O aplicador de temas pode:
- Aplicar paletas de cores predefinidas
- Gerar paletas customizadas
- Configurar formatos de medidas
- Adicionar metadados de tema ao modelo

### Sugestões de Visualizações

Baseado na análise do modelo, sugere:
- Tipos de visuais adequados (gráficos, tabelas, KPIs)
- Medidas relevantes para cada visual
- Layouts recomendados

## 🔧 Arquitetura Técnica

### Módulos Principais

```
modules/
├── powerbi_connector.py    # Conexão com Power BI via MCP
├── theme_applier.py         # Aplicação de temas
├── data_analyzer.py         # Análise de modelos (estendido)
├── color_generator.py       # Geração de paletas
├── layout_engine.py         # Templates de layout
└── powerbi_exporter.py      # Exportação de configurações
```

### Fluxo de Trabalho

```
1. PowerBIConnector.list_local_instances()
   ↓
2. PowerBIConnector.connect_to_desktop()
   ↓
3. PowerBIConnector.get_model_structure()
   ↓
4. DataAnalyzer.analyze_powerbi_model()
   ↓
5. ColorGenerator.get_preset_palette()
   ↓
6. ThemeApplier.apply_theme()
   ↓
7. PowerBIConnector.disconnect()
```

## 🎨 Exemplos de Paletas

As seguintes paletas estão disponíveis:

- **modern_dark**: Tema escuro moderno (azul/laranja)
- **minimal_light**: Minimalista claro
- **corporate_blue**: Azul corporativo profissional
- **vibrant_gradient**: Gradiente vibrante
- **nature_earth**: Tons terrosos
- **sunset_warm**: Cores quentes
- **tech_neon**: Neon tecnológico

## 🆘 Solução de Problemas

### "Nenhuma instância encontrada"

- ✅ Certifique-se de que o Power BI Desktop está aberto
- ✅ Verifique se um arquivo .pbix está carregado
- ✅ Confirme que você tem permissões de conexão

### "Erro ao conectar"

- ✅ A porta pode estar incorreta - tente listar novamente
- ✅ O Power BI pode ter sido reiniciado - reconecte
- ✅ Verifique logs no console para detalhes

### "Erro ao aplicar tema"

- ⚠️ A aplicação direta de temas requer permissões de escrita
- 💡 Considere usar a exportação de tema e aplicar manualmente
- 💡 Algumas configurações podem não ser suportadas via MCP

## 📚 Recursos Adicionais

- **README.md**: Documentação completa do projeto
- **INICIO_RAPIDO.md**: Guia de início rápido
- **DEMONSTRACAO.md**: Casos de uso práticos
- **exemplo.py**: Exemplos com arquivos CSV/Excel
- **exemplo_powerbi.py**: Exemplos com Power BI Desktop

## 🔄 Workflows Combinados

Você pode combinar análise de arquivos (CSV/Excel) com análise de modelos Power BI:

```python
# 1. Analisar dados de origem (CSV)
import pandas as pd
df = pd.read_csv('dados.csv')
analyzer = DataAnalyzer()
csv_analysis = analyzer.analyze_dataframe(df)

# 2. Conectar ao Power BI
connector = PowerBIConnector()
connector.connect_to_desktop(port=12345)
analyzer_pbi = DataAnalyzer(powerbi_connector=connector)
pbi_analysis = analyzer_pbi.analyze_powerbi_model()

# 3. Comparar e recomendar
# (Lógica personalizada de comparação)

# 4. Aplicar melhorias
theme_applier = ThemeApplier(connector)
# ... aplicar tema baseado na análise combinada
```

## 🌟 Próximos Passos

Explore os exemplos incluídos para ver todo o potencial da integração!

```bash
# Interface completa
streamlit run app.py

# Exemplos interativos
python exemplo_powerbi.py

# Exemplos anteriores (CSV/Excel)
python exemplo.py
```

---

**Desenvolvido com ❤️ para simplificar o design de dashboards Power BI**
