"""
MCP Power BI Client - Cliente para integração com Analysis Services via pythonnet
"""
from typing import Dict, List, Any, Optional
import json


class MCPPowerBIClient:
    """Cliente MCP para operações Power BI via Analysis Services"""
    
    def __init__(self):
        self.connection = None
        self.connection_string = None
        self._adomd_loaded = False
        self._load_adomd()
        
    def _load_adomd(self):
        """Carrega biblioteca ADOMD.NET via pythonnet"""
        try:
            import clr
            import sys
            import os
            
            # Adicionar diretórios conhecidos das DLLs ao PATH
            dll_paths = [
                r"C:\Program Files\Microsoft.NET\ADOMD.NET\160",
                r"C:\Program Files (x86)\Microsoft SQL Server Management Studio 20\Common7\IDE",
                r"C:\Program Files\Microsoft SQL Server\160\DTS\Binn",
                r"C:\Program Files\Microsoft SQL Server\160\SDK\Assemblies",
            ]
            
            for dll_path in dll_paths:
                if os.path.exists(dll_path) and dll_path not in sys.path:
                    sys.path.append(dll_path)
                    os.environ['PATH'] = dll_path + os.pathsep + os.environ.get('PATH', '')
            
            # Tentar adicionar referências para Microsoft.AnalysisServices.AdomdClient
            try:
                clr.AddReference("Microsoft.AnalysisServices.AdomdClient")
                self._adomd_loaded = True
                print("✅ Microsoft.AnalysisServices.AdomdClient carregado")
            except Exception as e:
                print(f"⚠️ ADOMD Client não disponível: {e}")
                print("💡 Para executar queries DAX, instale SQL Server Management Studio ou Analysis Services Client")
                self._adomd_loaded = False
                
        except ImportError:
            print("⚠️ pythonnet não disponível")
            self._adomd_loaded = False
    def connect(self, connection_string: str) -> bool:
        """
        Conecta ao Analysis Services
        
        Args:
            connection_string: String de conexão XMLA
            
        Returns:
            True se conectou com sucesso
        """
        if not self._adomd_loaded:
            print("⚠️ ADOMD Client não carregado - modo offline")
            return False
            
        try:
            import clr
            from Microsoft.AnalysisServices.AdomdClient import AdomdConnection
            
            self.connection_string = connection_string
            self.connection = AdomdConnection(connection_string)
            self.connection.Open()
            
            print("✅ Conectado ao Analysis Services via ADOMD.NET")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao conectar via ADOMD: {e}")
            self.connection = None
            return False
    
    def disconnect(self) -> bool:
        """Desconecta do Analysis Services"""
        if self.connection:
            try:
                self.connection.Close()  # Usar Close() com C maiúsculo
                self.connection = None
                print("✅ Desconectado do Analysis Services")
                return True
            except Exception as e:
                print(f"⚠️ Erro ao desconectar: {e}")
                return False
        return True
    
    def execute_dax_query(self, query: str, max_rows: int = 1000) -> Dict[str, Any]:
        """
        Executa query DAX no modelo
        
        Args:
            query: Query DAX a executar
            max_rows: Número máximo de linhas a retornar
            
        Returns:
            Resultado da query com estrutura {rows: [...], columns: [...]}
        """
        if not self.connection:
            return {'rows': [], 'columns': [], 'error': 'Não conectado'}
        
        try:
            from Microsoft.AnalysisServices.AdomdClient import AdomdCommand
            
            command = AdomdCommand(query, self.connection)
            reader = command.ExecuteReader()
            
            # Obter nomes das colunas
            columns = []
            for i in range(reader.FieldCount):
                columns.append(reader.GetName(i))
            
            # Obter linhas
            rows = []
            row_count = 0
            while reader.Read() and row_count < max_rows:
                row_dict = {}
                for i, col_name in enumerate(columns):
                    try:
                        value = reader.GetValue(i)
                        # Converter tipos .NET para Python
                        if value is not None:
                            value = str(value) if not isinstance(value, (int, float, bool)) else value
                        row_dict[col_name] = value
                    except:
                        row_dict[col_name] = None
                rows.append(row_dict)
                row_count += 1
            
            reader.Close()
            
            return {
                'success': True,
                'rows': rows,
                'columns': columns,
                'row_count': len(rows)
            }
            
        except Exception as e:
            print(f"❌ Erro ao executar DAX: {e}")
            return {
                'success': False,
                'rows': [],
                'columns': [],
                'error': str(e)
            }
    
    def get_model_structure(self) -> Dict[str, Any]:
        """
        Obtém estrutura do modelo (tabelas, colunas, medidas)
        
        Returns:
            Estrutura completa do modelo
        """
        structure = {
            'tables': [],
            'measures': [],
            'relationships': []
        }
        
        # Query para listar tabelas
        tables_query = """
        SELECT 
            [CATALOG_NAME],
            [SCHEMA_NAME] as TableName,
            [SCHEMA_OWNER] as TableType
        FROM $SYSTEM.DBSCHEMA_SCHEMATA
        """
        
        tables_result = self.execute_dax_query(tables_query, max_rows=10000)
        
        if tables_result.get('success'):
            for row in tables_result.get('rows', []):
                table_name = row.get('TableName', '')
                if table_name and not table_name.startswith('$'):
                    structure['tables'].append({
                        'name': table_name,
                        'type': row.get('TableType', 'Unknown'),
                        'columns': []
                    })
        
        # Query para listar colunas
        columns_query = """
        SELECT 
            [TABLE_NAME] as TableName,
            [COLUMN_NAME] as ColumnName,
            [DATA_TYPE] as DataType
        FROM $SYSTEM.DBSCHEMA_COLUMNS
        """
        
        columns_result = self.execute_dax_query(columns_query, max_rows=10000)
        
        if columns_result.get('success'):
            for row in columns_result.get('rows', []):
                table_name = row.get('TableName', '')
                column_name = row.get('ColumnName', '')
                
                # Encontrar tabela correspondente
                for table in structure['tables']:
                    if table['name'] == table_name:
                        table['columns'].append({
                            'ColumnName': column_name,
                            'DataType': row.get('DataType', 'Unknown')
                        })
                        break
        
        return structure
    
    def create_measure(self, table_name: str, measure_name: str, expression: str) -> Dict[str, Any]:
        """
        Cria uma nova medida DAX no modelo
        
        Args:
            table_name: Nome da tabela
            measure_name: Nome da medida
            expression: Expressão DAX
            
        Returns:
            Resultado da operação
        """
        # Esta funcionalidade requer XMLA write access
        # Por enquanto apenas simulamos
        return {
            'success': False,
            'message': 'Criação de medidas requer XMLA write access (Power BI Desktop não suporta)',
            'details': {
                'table': table_name,
                'measure': measure_name,
                'expression': expression
            }
        }
    
    def apply_theme(self, theme_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aplica tema de cores ao modelo
        
        Args:
            theme_json: Definição do tema em formato JSON
            
        Returns:
            Resultado da operação
        """
        # Esta funcionalidade requer XMLA write access
        # Por enquanto apenas simulamos
        return {
            'success': False,
            'message': 'Aplicação de temas requer XMLA write access',
            'theme': theme_json.get('name', 'Unknown')
        }
    
    def validate_dax(self, expression: str) -> Dict[str, bool]:
        """
        Valida expressão DAX
        
        Args:
            expression: Expressão DAX a validar
            
        Returns:
            Resultado da validação
        """
        try:
            # Tenta executar como query EVALUATE
            test_query = f"EVALUATE ROW(\"Result\", {expression})"
            result = self.execute_dax_query(test_query, max_rows=1)
            
            return {
                'valid': result.get('success', False),
                'error': result.get('error')
            }
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def apply_theme_tmsl(self, theme_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aplica tema ao modelo via TMSL (Tabular Model Scripting Language)
        
        Args:
            theme_json: JSON do tema Power BI
            
        Returns:
            Resultado da aplicação
        """
        if not self.connection or not self._adomd_loaded:
            return {
                'success': False,
                'message': 'Não conectado ao Analysis Services'
            }
        
        try:
            from Microsoft.AnalysisServices.AdomdClient import AdomdCommand
            
            # Criar script TMSL para aplicar tema
            # Temas são aplicados através de annotations no modelo
            tmsl_script = {
                "alter": {
                    "object": {
                        "database": self.connection.Database
                    },
                    "database": {
                        "annotations": [
                            {
                                "name": "PBI_ProTooling",
                                "value": json.dumps({
                                    "customThemes": [theme_json]
                                })
                            }
                        ]
                    }
                }
            }
            
            command = AdomdCommand(json.dumps(tmsl_script), self.connection)
            command.Execute()
            
            return {
                'success': True,
                'message': f'Tema "{theme_json.get("name", "Custom")}" aplicado com sucesso',
                'theme_name': theme_json.get('name', 'Custom')
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao aplicar tema: {str(e)}',
                'error': str(e)
            }
    
    def get_relationships(self) -> Dict[str, Any]:
        """
        Obtém todos os relacionamentos do modelo via TOM
        
        Returns:
            Lista de relacionamentos
        """
        if not self.connection or not self._adomd_loaded:
            return {
                'success': False,
                'message': 'Não conectado'
            }
        
        try:
            import clr
            import sys
            import os
            
            # Adicionar diretórios conhecidos das DLLs ao PATH
            dll_paths = [
                r"C:\Program Files\Microsoft.NET\ADOMD.NET\160",
                r"C:\Program Files (x86)\Microsoft SQL Server Management Studio 20\Common7\IDE",
                r"C:\Program Files\Microsoft SQL Server\160\DTS\Binn",
                r"C:\Program Files\Microsoft SQL Server\160\SDK\Assemblies",
            ]
            
            for dll_path in dll_paths:
                if os.path.exists(dll_path) and dll_path not in sys.path:
                    sys.path.append(dll_path)
                    os.environ['PATH'] = dll_path + os.pathsep + os.environ.get('PATH', '')
            
            # Carregar TOM
            clr.AddReference("Microsoft.AnalysisServices.Tabular")
            from Microsoft.AnalysisServices.Tabular import Server
            
            # Conectar via TOM
            server = Server()
            server.Connect(self.connection_string)
            
            if server.Databases.Count == 0:
                server.Disconnect()
                return {
                    'success': False,
                    'message': 'Nenhum database encontrado'
                }
            
            db = server.Databases[0]
            model = db.Model
            
            relationships = []
            
            # Iterar relacionamentos
            for rel in model.Relationships:
                relationships.append({
                    'RELATIONSHIP_NAME': rel.Name,
                    'FROM_TABLE': rel.FromTable.Name,
                    'FROM_COLUMN': rel.FromColumn.Name,
                    'TO_TABLE': rel.ToTable.Name,
                    'TO_COLUMN': rel.ToColumn.Name,
                    'CROSS_FILTERING_BEHAVIOR': str(rel.CrossFilteringBehavior),
                    'IS_ACTIVE': rel.IsActive,
                    'FROM_CARDINALITY': str(rel.FromCardinality),
                    'TO_CARDINALITY': str(rel.ToCardinality)
                })
            
            server.Disconnect()
            
            return {
                'success': True,
                'relationships': relationships,
                'count': len(relationships)
            }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao obter relacionamentos: {str(e)}',
                'error': str(e)
            }
    
    def create_relationship(self, from_table: str, from_column: str, 
                          to_table: str, to_column: str, 
                          cardinality: str = "ManyToOne",
                          cross_filter: str = "SingleDirection") -> Dict[str, Any]:
        """
        Cria um novo relacionamento via TMSL
        
        Args:
            from_table: Tabela de origem
            from_column: Coluna de origem
            to_table: Tabela de destino
            to_column: Coluna de destino
            cardinality: Cardinalidade (ManyToOne, OneToMany, OneToOne, ManyToMany)
            cross_filter: Direção do filtro (SingleDirection, BothDirections)
            
        Returns:
            Resultado da criação
        """
        if not self.connection or not self._adomd_loaded:
            return {
                'success': False,
                'message': 'Não conectado'
            }
        
        try:
            from Microsoft.AnalysisServices.AdomdClient import AdomdCommand
            
            tmsl_script = {
                "createOrReplace": {
                    "object": {
                        "database": self.connection.Database,
                        "table": from_table,
                        "relationship": f"{from_table}_{to_table}"
                    },
                    "relationship": {
                        "name": f"{from_table}_{to_table}",
                        "fromTable": from_table,
                        "fromColumn": from_column,
                        "toTable": to_table,
                        "toColumn": to_column,
                        "crossFilteringBehavior": cross_filter,
                        "cardinality": cardinality,
                        "isActive": True
                    }
                }
            }
            
            command = AdomdCommand(json.dumps(tmsl_script), self.connection)
            command.Execute()
            
            return {
                'success': True,
                'message': f'Relacionamento criado: {from_table}.{from_column} -> {to_table}.{to_column}',
                'relationship': f"{from_table}_{to_table}"
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao criar relacionamento: {str(e)}',
                'error': str(e)
            }
    
    def analyze_measure_performance(self, measure_name: str, iterations: int = 5) -> Dict[str, Any]:
        """
        Analisa performance de uma medida
        
        Args:
            measure_name: Nome da medida a analisar
            iterations: Número de execuções para média
            
        Returns:
            Estatísticas de performance
        """
        if not self.connection or not self._adomd_loaded:
            return {
                'success': False,
                'message': 'Não conectado'
            }
        
        try:
            import time
            
            execution_times = []
            
            for i in range(iterations):
                # Limpa cache antes de cada execução
                if i > 0:  # Não limpa na primeira para ter cold start
                    clear_cache_query = """
                    EVALUATE 
                    ROW("CacheClear", 1)
                    """
                    self.execute_dax_query(clear_cache_query, max_rows=1)
                
                # Executa medida e mede tempo
                query = f"""
                DEFINE
                    VAR _Start = NOW()
                    VAR _Result = [{measure_name}]
                    VAR _End = NOW()
                EVALUATE
                ROW(
                    "MeasureName", "{measure_name}",
                    "Result", _Result,
                    "ExecutionTime", _End - _Start
                )
                """
                
                start_time = time.time()
                result = self.execute_dax_query(query, max_rows=1)
                end_time = time.time()
                
                client_time = (end_time - start_time) * 1000  # em ms
                execution_times.append(client_time)
            
            # Calcula estatísticas
            avg_time = sum(execution_times) / len(execution_times)
            min_time = min(execution_times)
            max_time = max(execution_times)
            
            # Classificação de performance
            if avg_time < 100:
                performance_rating = "Excelente"
            elif avg_time < 500:
                performance_rating = "Boa"
            elif avg_time < 2000:
                performance_rating = "Aceitável"
            else:
                performance_rating = "Lenta"
            
            return {
                'success': True,
                'measure_name': measure_name,
                'iterations': iterations,
                'avg_time_ms': round(avg_time, 2),
                'min_time_ms': round(min_time, 2),
                'max_time_ms': round(max_time, 2),
                'cold_start_ms': round(execution_times[0], 2),
                'warm_avg_ms': round(sum(execution_times[1:]) / (len(execution_times) - 1), 2) if len(execution_times) > 1 else None,
                'performance_rating': performance_rating,
                'execution_times': [round(t, 2) for t in execution_times]
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao analisar performance: {str(e)}',
                'error': str(e)
            }
