# 🚀 Guia de Início Rápido - Power BI Design Assistant

## Instalação Rápida (5 minutos)

### 1. Instale as dependências

```powershell
pip install -r requirements.txt
```

### 2. (Opcional) Configure a IA

Se quiser usar sugestões de IA, copie e configure:

```powershell
Copy-Item .env.example .env
```

Edite `.env` e adicione sua chave de API (OpenAI ou Anthropic)

### 3. Inicie o assistente

```powershell
streamlit run app.py
```

✅ Pronto! O navegador abrirá automaticamente.

---

## Primeiro Uso (3 minutos)

### Opção 1: Com seus dados

1. **Carregue um arquivo CSV ou Excel**
   - Clique em "Browse files"
   - Selecione seu arquivo
   
2. **Explore as abas**
   - 📈 Preview: Veja seus dados
   - 🔍 Análise: Obtenha insights automáticos
   - 🎨 Cores: Escolha uma paleta profissional
   - 📐 Layout: Selecione um template
   - 💾 Exportar: Baixe o tema para Power BI

### Opção 2: Teste com exemplo

Execute o script de exemplo:

```powershell
python exemplo.py
```

Isso criará uma pasta `exemplo_export/` com todos os arquivos prontos!

---

## Aplicar no Power BI (2 minutos)

### Importar Tema

1. Abra seu arquivo `.pbix` no Power BI Desktop
2. Vá em **View** > **Themes** > **Browse for themes**
3. Selecione o arquivo `.json` exportado
4. Clique **Open**

✨ Seu tema está aplicado!

### Aplicar Layout

1. Leia o arquivo `layout_guide.md`
2. Crie seus visuais seguindo as posições sugeridas
3. Ajuste conforme necessário

---

## Dicas Rápidas

### 💡 Melhores Práticas

- **Análise de dados**: Sempre verifique a qualidade dos dados antes
- **Paletas**: Use paletas preset para começar rapidamente
- **Layouts**: Escolha baseado no propósito do dashboard:
  - Executive Summary → Para apresentações executivas
  - Detailed Analysis → Para análises detalhadas
  - Single Focus → Para destacar uma métrica principal

### ⚡ Atalhos

- `Ctrl + R`: Recarregar página no Streamlit
- `Shift + R`: Limpar cache e recarregar

### 🎨 Sugestões de Paletas

| Contexto | Paleta Recomendada |
|----------|-------------------|
| Dashboard Financeiro | Corporate Blue |
| Dashboard de Vendas | Vibrant Gradient |
| Dashboard Operacional | Minimal Light |
| Dashboard Executivo | Modern Dark |
| Dashboard Criativo | Sunset Warm |

---

## Resolução Rápida de Problemas

### Erro ao instalar dependências

```powershell
# Atualize o pip primeiro
python -m pip install --upgrade pip

# Tente novamente
pip install -r requirements.txt
```

### Streamlit não inicia

```powershell
# Teste se está instalado
streamlit --version

# Se não estiver, instale
pip install streamlit

# Tente com porta diferente
streamlit run app.py --server.port 8502
```

### IA não funciona

A IA é **opcional**! O assistente funciona perfeitamente sem ela, usando:
- Regras baseadas em análise de dados
- Paletas pré-configuradas
- Templates profissionais

Para ativar a IA:
1. Crie arquivo `.env`
2. Adicione sua chave: `OPENAI_API_KEY=sk-...`
3. Reinicie o aplicativo

---

## Próximos Passos

### Explore mais recursos:

1. **Teste diferentes paletas**
   ```python
   python exemplo.py paletas
   ```

2. **Veja todos os layouts**
   ```python
   python exemplo.py layouts
   ```

3. **Use o módulo standalone**
   ```python
   from modules.color_generator import ColorGenerator
   
   gen = ColorGenerator()
   palette = gen.generate_from_base_color("#FF6B6B", "complementary", 5)
   print(palette['colors'])
   ```

### Recursos adicionais:

- 📖 [README completo](README.md) - Documentação detalhada
- 🎨 [Templates](templates/) - Temas JSON prontos
- 💻 [Exemplo.py](exemplo.py) - Código de exemplo

---

## Precisa de Ajuda?

1. Verifique o [README.md](README.md) completo
2. Execute `python exemplo.py` para ver funcionando
3. Abra uma issue no repositório

---

**Tempo total: ~10 minutos do zero ao primeiro tema exportado! 🚀**
