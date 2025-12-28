# 📊 Power BI Design Assistant

Assistente inteligente para criação de layouts e visuais profissionais para Power BI, com suporte de IA para sugestões contextualizadas.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🚀 Recursos Principais

### 📈 Análise Inteligente de Dados
- Análise automática de tipos de dados
- Detecção de relacionamentos
- Avaliação de qualidade dos dados
- Sugestões de visualizações baseadas nos dados

### 🎨 Gerador de Paletas de Cores
- 7+ paletas profissionais pré-configuradas
- Geração baseada em esquemas de cores (análogo, complementar, triádico, etc)
- Sugestões contextualizadas por tipo de dados e mood
- Validação de acessibilidade (WCAG)
- Gradientes personalizados

### 📐 Templates de Layout
- 6 templates profissionais prontos
- Layouts responsivos
- Posicionamento otimizado de visuais
- Hierarquia visual inteligente

### 🤖 Assistente de IA
- Integração com OpenAI GPT-4 ou Claude 3
- Sugestões criativas de visualizações
- Recomendações de paletas contextualizadas
- Geração de insights automática

### 💾 Exportação para Power BI
- Geração de arquivos de tema (.json)
- Guias de layout detalhados
- Scripts Python para análise exploratória
- Pacotes completos de exportação

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone ou baixe este repositório**

```bash
git clone <seu-repositorio>
cd bi-auto
```

2. **Crie um ambiente virtual (recomendado)**

```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate
```

3. **Instale as dependências**

```powershell
pip install -r requirements.txt
```

4. **Configure as chaves de API (opcional, para IA)**

Copie o arquivo `.env.example` para `.env`:

```powershell
Copy-Item .env.example .env
```

Edite o arquivo `.env` e adicione sua chave:

```env
# Para OpenAI
OPENAI_API_KEY=sk-...

# OU para Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Modelo a usar
AI_MODEL=gpt-4-turbo-preview
```

## 🎯 Como Usar

### Iniciar a Aplicação

```powershell
streamlit run app.py
```

O navegador abrirá automaticamente em `http://localhost:8501`

### Fluxo de Trabalho Recomendado

1. **Carregue seus dados**
   - Suporta CSV e Excel
   - Formatos aceitos: `.csv`, `.xlsx`, `.xls`

2. **Analise seus dados**
   - Visualize estatísticas
   - Veja sugestões de visualizações
   - Identifique problemas de qualidade

3. **Escolha uma paleta**
   - Use presets profissionais
   - Gere a partir de uma cor base
   - Ou deixe a IA sugerir

4. **Selecione um layout**
   - Escolha entre 6 templates
   - Visualize o posicionamento
   - Ajuste conforme necessário

5. **Exporte para Power BI**
   - Download do tema JSON
   - Guia de implementação
   - Pacote completo

## 📚 Módulos

### `data_analyzer.py`
Analisa datasets e sugere visualizações ideais baseadas em:
- Tipos de dados detectados
- Cardinalidade das colunas
- Relacionamentos entre dados
- Qualidade dos dados

### `color_generator.py`
Gera paletas harmônicas usando:
- Teoria das cores (HSV)
- Esquemas clássicos (análogo, complementar, etc)
- Validação WCAG para acessibilidade
- Presets profissionais

### `layout_engine.py`
Cria layouts profissionais:
- Templates pré-configurados
- Posicionamento otimizado
- Layouts responsivos
- Hierarquia visual

### `ai_assistant.py`
Integração com IAs para:
- Sugestões contextualizadas
- Insights automáticos
- Recomendações criativas
- Análise semântica

### `powerbi_exporter.py`
Exportação em múltiplos formatos:
- Temas JSON do Power BI
- Guias de layout Markdown
- Scripts Python
- Pacotes completos

## 🎨 Templates de Paletas Disponíveis

1. **Modern Dark** - Design moderno com fundo escuro
2. **Minimal Light** - Minimalista e clean
3. **Corporate Blue** - Profissional para negócios
4. **Vibrant Gradient** - Cores vibrantes com gradientes
5. **Nature Earth** - Tons naturais e terrosos
6. **Sunset Warm** - Cores quentes inspiradas no pôr do sol
7. **Tech Neon** - Estilo tecnológico com neon

## 📐 Templates de Layout Disponíveis

1. **Executive Summary** - Foco em KPIs com destaque
2. **Detailed Analysis** - Balanceado para análise detalhada
3. **Single Focus** - Um visual principal
4. **Comparison View** - Comparações lado a lado
5. **Storytelling** - Fluxo narrativo guiado
6. **Modern Minimal** - Minimalista com muito espaço

## 🔧 Configuração Avançada

### Usando OpenAI

```python
# No arquivo .env
OPENAI_API_KEY=sk-...
AI_MODEL=gpt-4-turbo-preview
```

Modelos suportados:
- `gpt-4-turbo-preview` (recomendado)
- `gpt-3.5-turbo` (mais rápido, mais econômico)

### Usando Anthropic Claude

```python
# No arquivo .env
ANTHROPIC_API_KEY=sk-ant-...
AI_MODEL=claude-3-sonnet-20240229
```

Modelos suportados:
- `claude-3-opus-20240229` (mais capaz)
- `claude-3-sonnet-20240229` (balanceado)

## 📖 Exemplos de Uso

### Análise Rápida

```python
from modules.data_analyzer import DataAnalyzer
import pandas as pd

# Carrega dados
df = pd.read_csv('vendas.csv')

# Analisa
analyzer = DataAnalyzer()
analysis = analyzer.analyze_dataframe(df)

# Visualiza sugestões
for suggestion in analysis['suggested_visuals']:
    print(f"{suggestion['type']}: {suggestion['title']}")
```

### Gerar Paleta Customizada

```python
from modules.color_generator import ColorGenerator

gen = ColorGenerator()

# Gera paleta complementar a partir de azul
palette = gen.generate_from_base_color("#1E88E5", "complementary", 5)

print(palette['colors'])
# ['#1E88E5', '#E5881E', ...]
```

### Criar Layout

```python
from modules.layout_engine import LayoutEngine

engine = LayoutEngine()

# Gera layout para 6 visuais
layout = engine.generate_layout("executive_summary", 6)

# Acessa posições
for visual in layout['visuals']:
    print(f"{visual['id']}: {visual['position']}")
```

## 🐛 Solução de Problemas

### Erro ao importar módulos

```powershell
# Certifique-se de estar no diretório correto
cd c:\Users\darkf\OneDrive\Documentos\bi-auto

# Ative o ambiente virtual
.\venv\Scripts\Activate

# Reinstale dependências
pip install -r requirements.txt
```

### IA não está funcionando

1. Verifique se o arquivo `.env` existe
2. Confirme que a chave de API está correta
3. Teste a conexão:

```python
from modules.ai_assistant import AIAssistant

ai = AIAssistant()
print(ai.is_available())  # Deve retornar True
```

### Streamlit não abre no navegador

```powershell
# Execute manualmente com porta específica
streamlit run app.py --server.port 8502
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novos recursos
- Submeter pull requests
- Melhorar documentação

## 📄 Licença

MIT License - veja LICENSE para detalhes

## 🙏 Agradecimentos

- Streamlit pela framework incrível
- OpenAI e Anthropic pelas APIs de IA
- Comunidade Power BI pelas inspirações

## 📞 Suporte

Precisa de ajuda? Abra uma issue no repositório ou entre em contato.

---

**Desenvolvido com ❤️ para facilitar o design de dashboards profissionais**

## 🗺️ Roadmap

- [ ] Integração direta com Power BI Service API
- [ ] Geração automática de DAX
- [ ] Templates adicionais de layout
- [ ] Suporte para temas escuros/claros
- [ ] Biblioteca de ícones e imagens
- [ ] Exportação para Figma
- [ ] Modo colaborativo
- [ ] Galeria de exemplos comunitários
