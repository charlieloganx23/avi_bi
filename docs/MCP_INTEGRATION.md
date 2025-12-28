# 🔌 Integração MCP (Model Context Protocol)

## ✅ Status Atual

A integração MCP está **implementada** e funcional! 🎉

### Arquitetura

```
Power BI Desktop (porta dinâmica)
         ↓
    msmdsrv.exe (Analysis Services)
         ↓
    XMLA Endpoint
         ↓
MCPPowerBIClient (pythonnet + ADOMD.NET)
         ↓
PowerBIConnector
         ↓
    Streamlit App
```

## 🚀 Funcionalidades Implementadas

### ✅ Disponíveis Agora:
1. **Detecção Automática** de instâncias Power BI Desktop
2. **Conexão via porta** dinâmica
3. **Análise de modelo** (tabelas, colunas, relacionamentos)
4. **Sugestões de visuais** baseadas no modelo
5. **Validação de estrutura** do modelo

### 🔄 Requer Configuração (queries DAX):
6. **Execução de queries DAX**
7. **Criação de medidas** programaticamente
8. **Aplicação de temas** diretamente no modelo
9. **Validação de expressões DAX**

## ⚙️ Configuração Para Queries DAX

### Pré-requisito:
Para executar queries DAX reais, você precisa do **Microsoft Analysis Services Client**:

#### Opção 1: Instalar SQL Server Management Studio (SSMS)
```powershell
# Download: https://aka.ms/ssmsfullsetup
# Instale e reinicie o Python
```

#### Opção 2: Instalar apenas Analysis Services Client
```powershell
# Download: https://docs.microsoft.com/en-us/analysis-services/client-libraries
# Baixe e instale: Microsoft.AnalysisServices.AdomdClient.dll
```

### Verificar Instalação:
```python
python test_mcp_integration.py
```

Se aparecer:
```
✅ Microsoft.AnalysisServices.AdomdClient carregado
✅ MCP Client: Ativo (queries DAX disponíveis)
```

Está funcionando! 🎉

## 📊 Exemplos de Uso

### 1. Conectar e Listar Tabelas
```python
from modules.powerbi_connector import PowerBIConnector

connector = PowerBIConnector()

# Detectar instâncias
instances = connector.list_local_instances()
print(f"Encontradas {len(instances)} instância(s)")

# Conectar
connector.connect_to_desktop(port=instances[0]['port'])

# Obter estrutura
structure = connector.get_model_structure()
print(f"Tabelas: {len(structure['tables'])}")
for table in structure['tables']:
    print(f"  - {table['name']}: {len(table['columns'])} colunas")
```

### 2. Executar Query DAX (requer ADOMD)
```python
# Query simples
query = """
EVALUATE
TOPN(10, 'Vendas')
"""

result = connector._execute_dax_query(query, max_rows=10)

if result.get('success'):
    print(f"Linhas: {len(result['rows'])}")
    for row in result['rows']:
        print(row)
```

### 3. Validar Expressão DAX
```python
# Validar medida
expression = "SUM([Valor])"
validation = connector.validate_dax(expression)

if validation.get('valid'):
    print("✅ Expressão válida!")
else:
    print(f"❌ Erro: {validation.get('error')}")
```

### 4. Criar Medida (futuro - requer write access)
```python
result = connector.create_measure(
    table_name='Vendas',
    measure_name='Total Vendas',
    expression='SUM([Valor])'
)
```

## 🎨 Aplicação de Temas

### Status Atual:
A aplicação direta de temas **requer XMLA write access**, que o Power BI Desktop **não permite** por padrão.

### Alternativa Atual:
```python
# 1. Gerar tema
from modules.color_generator import ColorGenerator

color_gen = ColorGenerator()
palette = color_gen.get_preset_palette('vibrant_gradient')

# 2. Exportar como theme.json
import json

theme = {
    "name": "Vibrant Theme",
    "dataColors": palette['colors'],
    "background": "#1e1e1e",
    "foreground": "#ffffff"
}

with open('theme.json', 'w') as f:
    json.dump(theme, f, indent=2)

print("✅ Tema exportado! Importe manualmente no Power BI:")
print("   View > Themes > Browse for themes > theme.json")
```

### Futuro (Power BI Service com write access):
```python
# Aplicar diretamente (quando disponível)
result = connector.apply_theme(theme)
```

## 🔍 Diferenças: Com vs Sem MCP

### Sem ADOMD Client (Modo Atual):
✅ Detecta instâncias Power BI  
✅ Conecta via porta  
✅ Analisa estrutura do modelo  
✅ Sugere visualizações  
✅ Valida relacionamentos  
❌ Não executa queries DAX  
❌ Não cria medidas  
❌ Não aplica temas diretamente  

### Com ADOMD Client (Completo):
✅ Tudo acima +  
✅ Executa queries DAX  
✅ Lê dados reais das tabelas  
✅ Valida expressões DAX  
✅ Cria medidas (com write access)  
✅ Aplica temas (com write access)  

## 🎯 Próximos Passos

### Para você agora:
1. ✅ **Sistema funcional** - use detecção e análise
2. ✅ **Gere paletas** e exporte como JSON
3. ✅ **Sugestões IA** com OpenAI já funcionam
4. 📥 **Instale ADOMD** para queries DAX (opcional)

### Roadmap Futuro:
- [ ] Suporte a Power BI Service (cloud)
- [ ] Write access via Premium workspace
- [ ] Versionamento de modelos
- [ ] Testes automatizados de medidas
- [ ] CI/CD para deploy de modelos

## 💡 Dicas

### Performance:
```python
# Limitar linhas em queries grandes
result = connector._execute_dax_query(query, max_rows=100)
```

### Debug:
```python
# Ver status da conexão
status = connector.get_connection_status()
print(status)
```

### Segurança:
```python
# Sempre desconectar quando terminar
connector.disconnect()
```

## 📚 Referências

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Analysis Services ADOMD.NET](https://docs.microsoft.com/en-us/analysis-services/adomd/multidimensional-models-adomd-net-client)
- [Power BI XMLA Endpoint](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-connect-tools)
- [pythonnet Documentation](https://pythonnet.github.io/)

## 🐛 Troubleshooting

### "ADOMD Client não disponível"
**Causa**: DLL não instalada  
**Solução**: Instale SSMS ou Analysis Services Client

### "Porta não está acessível"
**Causa**: Power BI Desktop não está aberto ou modelo não carregado  
**Solução**: Abra um arquivo .pbix e aguarde carregar

### "MCP Client: Modo offline"
**Causa**: Normal se ADOMD não estiver instalado  
**Solução**: Continue usando - análise funciona! Para queries, instale ADOMD

### "Write access denied"
**Causa**: Power BI Desktop não permite modificações via XMLA  
**Solução**: Use Power BI Service Premium workspace ou exporte temas como JSON

---

**Versão**: 1.1.0  
**Última Atualização**: 28 de dezembro de 2025  
**Status**: ✅ MCP Implementado (queries DAX opcional)
