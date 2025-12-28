"""
Power BI Connector - Integração com Power BI Desktop via MCP
"""
from typing import Dict, List, Any, Optional
import json
import subprocess
import re
import socket
from .mcp_powerbi_client import MCPPowerBIClient


class PowerBIConnector:
    """Conecta e interage com Power BI Desktop usando powerbi-modeling-mcp"""
    
    def __init__(self):
        self.connections = []
        self.active_connection = None
        self.model_info = None
        self.connection_name = None
        self.mcp_client = MCPPowerBIClient()
    
    def is_connected(self) -> bool:
        """Verifica se está conectado a uma instância do Power BI"""
        if self.active_connection is None:
            return False
        
        # Verifica se a porta ainda está aberta
        port = self.active_connection.get('port')
        if port and not self._is_port_open('localhost', port):
            print("⚠️ Conexão perdida - porta não está mais acessível")
            self.active_connection = None
            return False
        
        return True
    
    def list_local_instances(self) -> List[Dict[str, str]]:
        """
        Lista instâncias locais do Power BI Desktop abertas
        
        Returns:
            Lista de instâncias disponíveis (porta, nome do arquivo)
        """
        try:
            instances = []
            process_ids = []
            
            # 1. Busca processos do Power BI Desktop
            print("🔍 Buscando processos do Power BI Desktop...")
            result = subprocess.run(
                ['powershell', '-Command', 
                 'Get-Process | Where-Object {$_.ProcessName -like "*PBIDesktop*" -or $_.ProcessName -like "*msmdsrv*"} | Select-Object Id, ProcessName, MainWindowTitle | Format-Table -HideTableHeaders'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0 and result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        parts = line.strip().split(maxsplit=1)
                        if len(parts) >= 1:
                            try:
                                pid = int(parts[0])
                                title = parts[1] if len(parts) > 1 else 'PowerBI Model'
                                process_ids.append((pid, title))
                            except ValueError:
                                continue
            
            print(f"✅ Encontrados {len(process_ids)} processo(s) do Power BI Desktop")
            
            # 2. Para cada processo, busca portas abertas
            if process_ids:
                for pid, title in process_ids:
                    print(f"🔌 Buscando portas do processo {pid} ({title})...")
                    
                    # Busca portas TCP abertas deste processo
                    port_result = subprocess.run(
                        ['powershell', '-Command',
                         f'Get-NetTCPConnection | Where-Object {{$_.OwningProcess -eq {pid} -and $_.State -eq "Listen"}} | Select-Object -ExpandProperty LocalPort | Select-Object -First 1'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    if port_result.returncode == 0 and port_result.stdout.strip():
                        try:
                            port = int(port_result.stdout.strip())
                            print(f"✅ Porta encontrada: {port}")
                            instances.append({
                                'name': f'localhost:{port}',
                                'port': port,
                                'dataset': title,
                                'process_id': pid
                            })
                        except ValueError:
                            print(f"⚠️ Porta inválida no output: {port_result.stdout}")
            
            # 3. Se não encontrou via processo, tenta scan de portas comuns
            if not instances:
                print("🔍 Tentando portas comuns do Analysis Services...")
                # Portas dinâmicas típicas do Analysis Services
                test_ports = [64562, 64000, 63000, 62000, 61000, 60000, 59000, 58000, 57000, 56000, 55000]
                
                for port in test_ports:
                    if self._is_port_open('localhost', port):
                        print(f"✅ Porta {port} está aberta!")
                        instances.append({
                            'name': f'localhost:{port}',
                            'port': port,
                            'dataset': 'PowerBI Model'
                        })
                        break  # Encontrou uma, suficiente
            
            self.connections = instances
            
            if instances:
                print(f"\n✅ Total: {len(instances)} instância(s) disponível(is)")
            else:
                print("\n⚠️ Nenhuma instância encontrada")
                print("💡 Dica: Abra o Power BI Desktop e carregue um arquivo .pbix")
            
            return instances
            
        except Exception as e:
            print(f"❌ Erro ao listar instâncias: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def connect_to_desktop(self, port: int = None, dataset_name: str = None) -> bool:
        """
        Conecta a uma instância do Power BI Desktop
        
        Args:
            port: Porta da instância (auto-detecta se None)
            dataset_name: Nome do dataset (auto-detecta se None)
        
        Returns:
            True se conectou com sucesso
        """
        try:
            # Se não especificou porta, tenta auto-detectar
            if port is None:
                instances = self.list_local_instances()
                if not instances:
                    print("❌ Nenhuma instância do Power BI Desktop encontrada")
                    return False
                
                # Usa a primeira instância encontrada
                port = instances[0].get('port')
                dataset_name = instances[0].get('dataset', 'Model')
            
            # Verifica se a porta está acessível
            if not self._is_port_open('localhost', port):
                print(f"❌ Porta {port} não está acessível")
                return False
            
            # Cria string de conexão
            connection_string = f"Data Source=localhost:{port}"
            if dataset_name:
                connection_string += f";Initial Catalog={dataset_name}"
            
            # Conecta via MCP Client
            mcp_connected = self.mcp_client.connect(connection_string)
            
            # Armazena informações da conexão
            self.active_connection = {
                'name': f'PowerBI_{port}',
                'connection_string': connection_string,
                'port': port,
                'dataset': dataset_name or 'Model',
                'data_source': f'localhost:{port}',
                'mcp_enabled': mcp_connected
            }
            
            self.connection_name = f'PowerBI_{port}'
            
            print(f"✅ Conectado ao Power BI Desktop")
            print(f"   📊 Dataset: {dataset_name or 'Model'}")
            print(f"   🔌 Porta: {port}")
            print(f"   🔗 Connection String: {connection_string}")
            if mcp_connected:
                print(f"   ✅ MCP Client: Ativo (queries DAX disponíveis)")
            else:
                print(f"   ⚠️ MCP Client: Modo offline (análise limitada)")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def connect_to_pbix(self, pbix_path: str) -> bool:
        """
        Conecta a um arquivo .pbix específico (deve estar aberto no Power BI Desktop)
        
        Args:
            pbix_path: Caminho do arquivo .pbix
        
        Returns:
            True se conectou com sucesso
        """
        # Lista instâncias e procura pela que tem o arquivo
        instances = self.list_local_instances()
        
        for instance in instances:
            if pbix_path.lower() in instance.get('database', '').lower():
                return self.connect_to_desktop(
                    port=instance.get('port'),
                    dataset_name=instance.get('database')
                )
        
        print(f"⚠️ Arquivo {pbix_path} não encontrado nas instâncias abertas")
        print("💡 Abra o arquivo no Power BI Desktop primeiro")
        return False
    
    def get_model_structure(self) -> Dict[str, Any]:
        """
        Obtém a estrutura completa do modelo Power BI
        
        Returns:
            Estrutura do modelo (tabelas, colunas, medidas, relações)
        """
        if not self.active_connection:
            print("❌ Não conectado ao Power BI")
            return {}
        
        try:
            structure = {
                'tables': [],
                'measures': [],
                'relationships': [],
                'cultures': []
            }
            
            # Executa query DAX para listar tabelas e colunas
            dax_query = """
            EVALUATE
            SELECTCOLUMNS(
                INFO.TABLES(),
                "TableName", [Name],
                "TableType", [Type],
                "IsHidden", [IsHidden]
            )
            """
            
            tables_result = self._execute_dax_query(dax_query)
            
            if tables_result:
                for table in tables_result.get('rows', []):
                    table_info = {
                        'name': table.get('TableName'),
                        'type': table.get('TableType'),
                        'hidden': table.get('IsHidden', False),
                        'columns': []
                    }
                    
                    # Busca colunas da tabela
                    columns = self._get_table_columns(table_info['name'])
                    table_info['columns'] = columns
                    
                    structure['tables'].append(table_info)
            
            # Busca medidas
            measures_query = """
            EVALUATE
            SELECTCOLUMNS(
                INFO.MEASURES(),
                "MeasureName", [Name],
                "TableName", [TableName],
                "Expression", [Expression]
            )
            """
            
            measures_result = self._execute_dax_query(measures_query)
            if measures_result:
                structure['measures'] = measures_result.get('rows', [])
            
            self.model_info = structure
            return structure
            
        except Exception as e:
            print(f"❌ Erro ao obter estrutura: {e}")
            return {}
    
    def _get_table_columns(self, table_name: str) -> List[Dict[str, Any]]:
        """Obtém colunas de uma tabela específica"""
        try:
            query = f"""
            EVALUATE
            SELECTCOLUMNS(
                FILTER(INFO.COLUMNS(), [TableName] = "{table_name}"),
                "ColumnName", [ExplicitName],
                "DataType", [DataType],
                "IsHidden", [IsHidden]
            )
            """
            
            result = self._execute_dax_query(query)
            return result.get('rows', []) if result else []
            
        except Exception as e:
            print(f"⚠️ Erro ao obter colunas de {table_name}: {e}")
            return []
    
    def execute_dax_query(self, query: str, max_rows: int = 1000) -> Dict[str, Any]:
        """
        Executa uma query DAX no modelo conectado
        
        Args:
            query: Query DAX
            max_rows: Máximo de linhas a retornar
        
        Returns:
            Resultado da query
        """
        return self._execute_dax_query(query, max_rows)
    
    def _execute_dax_query(self, query: str, max_rows: int = 1000) -> Dict[str, Any]:
        """Executa query DAX via MCP Client"""
        if not self.active_connection:
            return {'rows': []}
        
        # Tenta usar MCP Client primeiro
        if self.active_connection.get('mcp_enabled') and self.mcp_client.connection:
            try:
                result = self.mcp_client.execute_dax_query(query, max_rows)
                if result.get('success'):
                    return result
                else:
                    print(f"⚠️ Erro MCP: {result.get('error', 'Unknown')}")
            except Exception as e:
                print(f"⚠️ Erro ao executar via MCP: {e}")
        
        # Fallback: retorna estrutura vazia
        print(f"⚠️ Query DAX não disponível (MCP offline)")
        return {'rows': [], 'columns': []}
    
    def get_sample_data(self, table_name: str, rows: int = 100) -> Dict[str, Any]:
        """
        Obtém dados de amostra de uma tabela
        
        Args:
            table_name: Nome da tabela
            rows: Número de linhas
        
        Returns:
            Dados da tabela
        """
        query = f"""
        EVALUATE
        TOPN({rows}, '{table_name}')
        """
        
        return self.execute_dax_query(query, rows)
    
    def get_measures_list(self) -> List[Dict[str, str]]:
        """
        Lista todas as medidas do modelo
        
        Returns:
            Lista de medidas
        """
        if self.model_info and 'measures' in self.model_info:
            return self.model_info['measures']
        
        structure = self.get_model_structure()
        return structure.get('measures', [])
    
    def get_tables_list(self) -> List[Dict[str, Any]]:
        """
        Lista todas as tabelas do modelo
        
        Returns:
            Lista de tabelas
        """
        if self.model_info and 'tables' in self.model_info:
            return self.model_info['tables']
        
        structure = self.get_model_structure()
        return structure.get('tables', [])
    
    def analyze_model_for_visuals(self) -> Dict[str, Any]:
        """
        Analisa o modelo e sugere visualizações baseadas na estrutura
        
        Returns:
            Análise com sugestões de visuais
        """
        structure = self.get_model_structure()
        
        analysis = {
            'summary': {
                'total_tables': len(structure.get('tables', [])),
                'total_measures': len(structure.get('measures', [])),
                'visible_tables': len([t for t in structure.get('tables', []) if not t.get('hidden', False)])
            },
            'suggested_visuals': [],
            'data_types': {},
            'recommendations': []
        }
        
        # Analisa tipos de dados disponíveis
        for table in structure.get('tables', []):
            if table.get('hidden'):
                continue
            
            for column in table.get('columns', []):
                data_type = column.get('DataType', 'Unknown')
                
                if data_type not in analysis['data_types']:
                    analysis['data_types'][data_type] = []
                
                analysis['data_types'][data_type].append({
                    'table': table['name'],
                    'column': column.get('ColumnName')
                })
        
        # Gera sugestões baseadas nos tipos de dados
        has_dates = 'DateTime' in analysis['data_types'] or 'Date' in analysis['data_types']
        has_numbers = any(t in analysis['data_types'] for t in ['Int64', 'Double', 'Decimal'])
        has_text = 'String' in analysis['data_types']
        
        if has_dates and has_numbers:
            analysis['suggested_visuals'].append({
                'type': 'line_chart',
                'title': 'Tendência ao longo do tempo',
                'priority': 'high',
                'reason': 'Modelo tem colunas de data e valores numéricos'
            })
        
        if has_text and has_numbers:
            analysis['suggested_visuals'].append({
                'type': 'bar_chart',
                'title': 'Comparação por categoria',
                'priority': 'high',
                'reason': 'Modelo tem categorias e valores para comparar'
            })
        
        # Verifica se há medidas
        if structure.get('measures'):
            analysis['suggested_visuals'].append({
                'type': 'kpi_card',
                'title': 'KPIs Principais',
                'priority': 'high',
                'reason': f'{len(structure["measures"])} medidas disponíveis no modelo',
                'measures': [m.get('MeasureName') for m in structure['measures'][:5]]
            })
        
        # Recomendações
        if analysis['summary']['total_tables'] > 10:
            analysis['recommendations'].append({
                'type': 'layout',
                'message': 'Modelo complexo - recomendado usar "Detailed Analysis" layout',
                'priority': 'medium'
            })
        
        if analysis['summary']['total_measures'] > 10:
            analysis['recommendations'].append({
                'type': 'visual',
                'message': 'Muitas medidas - considere criar múltiplas páginas',
                'priority': 'medium'
            })
        
        return analysis
    
    def disconnect(self) -> bool:
        """
        Desconecta do Power BI
        
        Returns:
            True se desconectou com sucesso
        """
        if not self.active_connection:
            return True
        
        try:
            # Desconecta MCP Client
            self.mcp_client.disconnect()
            
            # Limpa informações da conexão
            self.active_connection = None
            self.model_info = None
            self.connection_name = None
            
            print("✅ Desconectado do Power BI")
            return True
            
        except Exception as e:
            print(f"⚠️ Erro ao desconectar: {e}")
            return False
    
    def get_connection_status(self) -> Dict[str, Any]:
        """
        Verifica status da conexão
        
        Returns:
            Status da conexão
        """
        if not self.active_connection:
            return {
                'connected': False,
                'message': 'Não conectado'
            }
        
        return {
            'connected': True,
            'connection_name': self.active_connection.get('name'),
            'dataset': self.active_connection.get('dataset'),
            'port': self.active_connection.get('port')
        }
    
    def _is_port_open(self, host: str, port: int) -> bool:
        """Verifica se uma porta está aberta"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    # Novos métodos usando MCP Client integrado
    
    def create_measure(self, table_name: str, measure_name: str, expression: str) -> Dict[str, Any]:
        """
        Cria medida DAX no modelo via MCP
        
        Args:
            table_name: Nome da tabela
            measure_name: Nome da medida
            expression: Expressão DAX
            
        Returns:
            Resultado da operação
        """
        if not self.active_connection or not self.active_connection.get('mcp_enabled'):
            return {
                'success': False,
                'message': 'MCP não disponível ou desconectado'
            }
        
        return self.mcp_client.create_measure(table_name, measure_name, expression)
    
    def apply_theme(self, theme_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aplica tema de cores ao modelo via MCP
        
        Args:
            theme_json: Definição do tema
            
        Returns:
            Resultado da operação
        """
        if not self.active_connection or not self.active_connection.get('mcp_enabled'):
            return {
                'success': False,
                'message': 'MCP não disponível ou desconectado'
            }
        
        return self.mcp_client.apply_theme(theme_json)
    
    def validate_dax(self, expression: str) -> Dict[str, bool]:
        """
        Valida expressão DAX via MCP
        
        Args:
            expression: Expressão DAX
            
        Returns:
            Resultado da validação
        """
        if not self.active_connection or not self.active_connection.get('mcp_enabled'):
            return {
                'valid': False,
                'error': 'MCP não disponível'
            }
        
        return self.mcp_client.validate_dax(expression)
