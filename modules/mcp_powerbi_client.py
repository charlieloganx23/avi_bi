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
