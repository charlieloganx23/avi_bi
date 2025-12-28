# 🔧 Guia de Conexão com Power BI Desktop

## ✅ Problema Resolvido!

A detecção de instâncias do Power BI Desktop agora está funcionando corretamente.

## 📊 Seu Power BI Detectado

- **Arquivo aberto**: `api_siplag_v3`
- **Porta**: `64562`
- **Status**: ✅ Conectável

## 🚀 Como Conectar

### Opção 1: Via Interface Streamlit (Recomendado)

1. **Abra a interface**:
   ```
   http://localhost:8501
   ```

2. **Navegue até**: Modo de Operação → **"🔌 Conectar ao Power BI"**

3. **Clique em**: "🔎 Buscar Instâncias do Power BI Desktop"

4. **Resultado esperado**:
   ```
   ✅ Encontradas 1 instância(s)
   localhost:64562 (Porta: 64562)
   ```

5. **Clique em**: "Conectar" ao lado da instância

### Opção 2: Via Código Python

```python
from modules.powerbi_connector import PowerBIConnector

# Criar connector
connector = PowerBIConnector()

# Listar instâncias
instances = connector.list_local_instances()
# Output: [{'name': 'localhost:64562', 'port': 64562, 'dataset': 'api_siplag_v3'}]

# Conectar à primeira instância
success = connector.connect_to_desktop(port=instances[0]['port'])
print(f"Conectado: {success}")

# Usar o connector...
# ...

# Desconectar
connector.disconnect()
```

### Opção 3: Conexão Direta (se souber a porta)

```python
connector = PowerBIConnector()
connector.connect_to_desktop(port=64562)
```

## 🔍 Como Funciona a Detecção

O sistema agora usa 3 métodos em cascata:

1. **Busca de Processos**: Identifica processos `PBIDesktop` rodando
2. **Detecção de Portas**: Para cada processo, busca as portas TCP abertas
3. **Scan de Portas Comuns**: Se os métodos anteriores falharem, testa portas comuns (60000-65000)

## ⚠️ Notas Importantes

### Power BI Desktop PRECISA estar:

- ✅ **Aberto** (processo rodando)
- ✅ **Com arquivo .pbix carregado** 
- ✅ **Modelo totalmente carregado** (não em modo de carregamento)

### Portas Dinâmicas

O Power BI Desktop usa **portas dinâmicas** que mudam a cada abertura. Por isso:

- ❌ NÃO use portas fixas hardcoded
- ✅ SEMPRE use `list_local_instances()` primeiro
- ✅ A porta pode mudar se você fechar e reabrir o Power BI

### Limitações Atuais

Devido à arquitetura dos MCP tools:

1. **MCP tools** (que fornecem dados detalhados do modelo) só funcionam através do Copilot
2. **Detecção básica** (processos e portas) funciona em Python standalone
3. **Funcionalidades avançadas** (queries DAX, análise de modelo) requerem conexão via XMLA

## 🔐 Próximos Passos para Funcionalidade Completa

Para que as queries DAX e análise de modelo funcionem, você tem 2 opções:

### Opção A: Usar powerbi-modeling-mcp via Copilot (atual)
- ✅ Detecção de instâncias funciona
- ⏳ Queries DAX requerem integração adicional

### Opção B: Usar biblioteca Python para XMLA
Instalar biblioteca que se conecta diretamente:

```bash
pip install xmla-client
```

Isso permitiria queries DAX diretamente via Python sem depender do MCP.

## 🧪 Testar Conexão

Execute o script de teste:

```bash
python test_connection.py
```

Saída esperada:
```
✅ Power BI Desktop está rodando!
✅ Encontradas 1 instância(s):
   1. localhost:64562 (Porta: 64562)
```

## 📞 Solução de Problemas

### "Nenhuma instância encontrada"

1. ✅ Confirme que o Power BI Desktop está aberto:
   ```powershell
   Get-Process | Where-Object {$_.ProcessName -like "*PBIDesktop*"}
   ```

2. ✅ Verifique se tem um arquivo .pbix aberto (não apenas o Power BI iniciado)

3. ✅ Execute o teste de conexão para diagnóstico:
   ```bash
   python test_connection.py
   ```

### "Erro ao conectar"

- A porta pode ter mudado - execute `list_local_instances()` novamente
- O arquivo pode estar sendo recarregado - aguarde finalizar

### Performance

- A busca de portas pode levar 5-10 segundos na primeira vez
- Após encontrar uma vez, o processo é instantâneo

## 📝 Exemplo Completo

```python
from modules.powerbi_connector import PowerBIConnector
from modules.data_analyzer import DataAnalyzer
from modules.color_generator import ColorGenerator
from modules.theme_applier import ThemeApplier

# 1. CONECTAR
print("Conectando ao Power BI...")
connector = PowerBIConnector()
instances = connector.list_local_instances()

if not instances:
    print("❌ Power BI não encontrado")
    exit()

print(f"✅ Encontrado: {instances[0]['dataset']} na porta {instances[0]['port']}")
connector.connect_to_desktop(port=instances[0]['port'])

# 2. ANALISAR
print("Analisando modelo...")
analyzer = DataAnalyzer(powerbi_connector=connector)
analysis = analyzer.analyze_powerbi_model()

print(f"📊 Tabelas: {analysis['model_structure']['tables_count']}")
print(f"🏥 Saúde: {analysis['model_health']['score']}%")

# 3. APLICAR TEMA
print("Aplicando tema...")
color_gen = ColorGenerator()
palette = color_gen.get_preset_palette('modern_dark')

theme_applier = ThemeApplier(connector)
result = theme_applier.apply_theme({
    'name': 'Modern Dark',
    'colors': palette
})

print(f"✅ Tema aplicado: {result['success']}")

# 4. DESCONECTAR
connector.disconnect()
print("🔌 Desconectado")
```

---

**Status**: ✅ Conexão funcionando | ⏳ Queries DAX em implementação
