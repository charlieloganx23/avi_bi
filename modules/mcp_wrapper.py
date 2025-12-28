"""
Wrapper MCP para PowerBI Connector
Este módulo fornece uma interface entre o PowerBIConnector e os MCP tools
"""

# Este arquivo será importado pelo powerbi_connector para acessar os MCP tools
# através do ambiente onde eles estão disponíveis

def call_mcp_connection_operation(request):
    """
    Wrapper para chamar mcp_powerbi-model_connection_operations
    Este será chamado pelo copilot quando necessário
    """
    # Este é um placeholder - o Copilot substituirá com a chamada real
    return {
        'success': False,
        'error': 'MCP tool não disponível - execute via Copilot/Streamlit'
    }

def call_mcp_dax_operation(request):
    """
    Wrapper para chamar mcp_powerbi-model_dax_query_operations
    Este será chamado pelo copilot quando necessário
    """
    # Este é um placeholder - o Copilot substituirá com a chamada real
    return {
        'success': False,
        'error': 'MCP tool não disponível - execute via Copilot/Streamlit'
    }
