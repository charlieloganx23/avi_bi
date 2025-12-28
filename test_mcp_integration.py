"""
Teste de Integração MCP - Power BI Connector
"""
import sys
sys.path.insert(0, '.')

from modules.powerbi_connector import PowerBIConnector

print("=" * 60)
print("🧪 TESTE DE INTEGRAÇÃO MCP")
print("=" * 60)

# Inicializar conector
print("\n1️⃣ Inicializando PowerBIConnector...")
connector = PowerBIConnector()
print("✅ Connector inicializado")

# Listar instâncias
print("\n2️⃣ Buscando instâncias do Power BI Desktop...")
instances = connector.list_local_instances()

if not instances:
    print("❌ Nenhuma instância encontrada")
    print("💡 Abra um arquivo .pbix no Power BI Desktop")
    sys.exit(1)

print(f"✅ Encontradas {len(instances)} instância(s):")
for inst in instances:
    print(f"   📊 Porta: {inst['port']}, Database: {inst.get('database', 'Unknown')}")

# Conectar à primeira instância
print("\n3️⃣ Conectando à primeira instância...")
port = instances[0]['port']
result = connector.connect_to_desktop(port=port)

if not result:
    print("❌ Falha ao conectar")
    sys.exit(1)

print("✅ Conexão estabelecida!")

# Verificar status MCP
mcp_enabled = connector.active_connection.get('mcp_enabled', False)
print(f"\n4️⃣ Status MCP: {'✅ Ativo' if mcp_enabled else '⚠️ Offline'}")

if mcp_enabled:
    print("\n5️⃣ Testando query DAX simples...")
    
    # Teste 1: Query básica
    test_query = """
    EVALUATE
    ROW("Test", "MCP Working", "Value", 42)
    """
    
    result = connector._execute_dax_query(test_query, max_rows=1)
    
    if result.get('success'):
        print("✅ Query executada com sucesso!")
        print(f"   Colunas: {result.get('columns', [])}")
        print(f"   Linhas: {len(result.get('rows', []))}")
        if result.get('rows'):
            print(f"   Primeira linha: {result['rows'][0]}")
    else:
        print(f"❌ Erro na query: {result.get('error')}")
    
    # Teste 2: Listar tabelas
    print("\n6️⃣ Obtendo estrutura do modelo...")
    structure = connector.get_model_structure()
    
    if structure and structure.get('tables'):
        print(f"✅ Modelo carregado!")
        print(f"   📊 Tabelas: {len(structure['tables'])}")
        print(f"   📏 Medidas: {len(structure.get('measures', []))}")
        
        # Listar primeiras 3 tabelas
        print("\n   Primeiras tabelas:")
        for table in structure['tables'][:3]:
            col_count = len(table.get('columns', []))
            print(f"   - {table['name']} ({col_count} colunas)")
    else:
        print("⚠️ Estrutura não disponível")
    
    # Teste 3: Validar DAX
    print("\n7️⃣ Testando validação DAX...")
    valid_expr = "1 + 1"
    validation = connector.validate_dax(valid_expr)
    
    if validation.get('valid'):
        print(f"✅ Expressão válida: {valid_expr}")
    else:
        print(f"❌ Expressão inválida: {validation.get('error')}")

else:
    print("⚠️ MCP offline - queries não disponíveis")
    print("💡 Verifique se pyadomd está instalado:")
    print("   pip install pyadomd")

# Desconectar
print("\n8️⃣ Desconectando...")
connector.disconnect()
print("✅ Desconectado")

print("\n" + "=" * 60)
print("✅ TESTE CONCLUÍDO!")
print("=" * 60)
