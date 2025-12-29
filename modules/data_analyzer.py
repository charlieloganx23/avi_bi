"""
Analisador de Dados - Detecta tipos de dados e sugere visualizações apropriadas
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from collections import Counter


class DataAnalyzer:
    """Analisa datasets e sugere visualizações ideais"""
    
    def __init__(self, powerbi_connector=None):
        self.column_types = {}
        self.statistics = {}
        self.recommendations = []
        self.powerbi_connector = powerbi_connector
    
    def analyze_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analisa um DataFrame e retorna insights completos"""
        if df is None or df.empty:
            return {"error": "DataFrame vazio ou inválido"}
        
        analysis = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_analysis": {},
            "relationships": [],
            "suggested_visuals": [],
            "data_quality": {}
        }
        
        # Analisa cada coluna
        for col in df.columns:
            analysis["column_analysis"][col] = self._analyze_column(df[col])
        
        # Detecta relacionamentos
        analysis["relationships"] = self._detect_relationships(df)
        
        # Sugere visualizações
        analysis["suggested_visuals"] = self._suggest_visualizations(df, analysis["column_analysis"])
        
        # Qualidade dos dados
        analysis["data_quality"] = self._assess_data_quality(df)
        
        return analysis
    
    def _analyze_column(self, series: pd.Series) -> Dict[str, Any]:
        """Analisa uma coluna individual"""
        col_info = {
            "name": series.name,
            "dtype": str(series.dtype),
            "null_count": int(series.isnull().sum()),
            "null_percentage": float(series.isnull().sum() / len(series) * 100),
            "unique_count": int(series.nunique()),
            "detected_type": self._detect_semantic_type(series)
        }
        
        # Estatísticas específicas por tipo
        if pd.api.types.is_numeric_dtype(series):
            col_info.update({
                "min": float(series.min()) if not series.isnull().all() else None,
                "max": float(series.max()) if not series.isnull().all() else None,
                "mean": float(series.mean()) if not series.isnull().all() else None,
                "median": float(series.median()) if not series.isnull().all() else None,
                "std": float(series.std()) if not series.isnull().all() else None
            })
        elif pd.api.types.is_datetime64_any_dtype(series):
            col_info.update({
                "min_date": str(series.min()) if not series.isnull().all() else None,
                "max_date": str(series.max()) if not series.isnull().all() else None,
                "date_range_days": (series.max() - series.min()).days if not series.isnull().all() else None
            })
        else:
            # Categórica
            top_values = series.value_counts().head(10)
            col_info.update({
                "top_values": top_values.to_dict(),
                "cardinality": "high" if series.nunique() > len(series) * 0.5 else "low"
            })
        
        return col_info
    
    def _detect_semantic_type(self, series: pd.Series) -> str:
        """Detecta o tipo semântico da coluna"""
        # Se já é numérico
        if pd.api.types.is_numeric_dtype(series):
            # Verifica se é identificador
            if series.nunique() == len(series):
                return "identifier"
            # Verifica se é percentagem (valores entre 0 e 1 ou 0 e 100)
            if series.between(0, 1).all() or series.between(0, 100).all():
                return "percentage"
            # Verifica se é moeda (valores altos com 2 decimais)
            if series.apply(lambda x: isinstance(x, (int, float)) and abs(x) > 10).any():
                return "currency"
            return "metric"
        
        # Se é datetime
        if pd.api.types.is_datetime64_any_dtype(series):
            return "date"
        
        # Tenta converter para datetime (silenciosamente)
        try:
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                pd.to_datetime(series, errors='raise')
            return "date"
        except:
            pass
        
        # Categórica
        unique_ratio = series.nunique() / len(series)
        if unique_ratio < 0.05:
            return "low_cardinality_category"
        elif unique_ratio < 0.5:
            return "category"
        else:
            return "high_cardinality_text"
    
    def _detect_relationships(self, df: pd.DataFrame) -> List[Dict[str, str]]:
        """Detecta possíveis relacionamentos entre colunas"""
        relationships = []
        
        # Procura por chaves estrangeiras (colunas com nomes similares)
        columns = df.columns.tolist()
        for i, col1 in enumerate(columns):
            for col2 in columns[i+1:]:
                # Verifica se os nomes sugerem relacionamento
                if any(keyword in col1.lower() for keyword in ['id', 'key', 'code']) or \
                   any(keyword in col2.lower() for keyword in ['id', 'key', 'code']):
                    # Verifica se há valores em comum
                    common_values = set(df[col1].dropna()) & set(df[col2].dropna())
                    if len(common_values) > 0:
                        relationships.append({
                            "from": col1,
                            "to": col2,
                            "type": "potential_foreign_key",
                            "strength": len(common_values) / min(df[col1].nunique(), df[col2].nunique())
                        })
        
        return relationships
    
    def _suggest_visualizations(self, df: pd.DataFrame, column_analysis: Dict) -> List[Dict[str, Any]]:
        """Sugere visualizações baseadas nos dados"""
        suggestions = []
        
        # Conta tipos de colunas
        numeric_cols = [col for col, info in column_analysis.items() 
                       if info['detected_type'] in ['metric', 'currency', 'percentage']]
        date_cols = [col for col, info in column_analysis.items() 
                    if info['detected_type'] == 'date']
        category_cols = [col for col, info in column_analysis.items() 
                        if info['detected_type'] in ['category', 'low_cardinality_category']]
        
        # Série temporal
        if date_cols and numeric_cols:
            suggestions.append({
                "type": "line_chart",
                "priority": "high",
                "columns": {"x": date_cols[0], "y": numeric_cols[:3]},
                "reason": "Série temporal detectada - perfeito para análise de tendências",
                "title": f"Evolução de {', '.join(numeric_cols[:3])} ao longo do tempo"
            })
        
        # Comparação categórica
        if category_cols and numeric_cols:
            suggestions.append({
                "type": "bar_chart",
                "priority": "high",
                "columns": {"category": category_cols[0], "value": numeric_cols[0]},
                "reason": "Comparação entre categorias",
                "title": f"{numeric_cols[0]} por {category_cols[0]}"
            })
        
        # Distribuição
        if len(numeric_cols) >= 1:
            suggestions.append({
                "type": "histogram",
                "priority": "medium",
                "columns": {"value": numeric_cols[0]},
                "reason": "Análise de distribuição de valores",
                "title": f"Distribuição de {numeric_cols[0]}"
            })
        
        # Correlação
        if len(numeric_cols) >= 2:
            suggestions.append({
                "type": "scatter_plot",
                "priority": "medium",
                "columns": {"x": numeric_cols[0], "y": numeric_cols[1]},
                "reason": "Análise de correlação entre métricas",
                "title": f"Relação entre {numeric_cols[0]} e {numeric_cols[1]}"
            })
        
        # KPI Cards
        if numeric_cols:
            suggestions.append({
                "type": "kpi_card",
                "priority": "high",
                "columns": {"metrics": numeric_cols[:4]},
                "reason": "Métricas principais em destaque",
                "title": "KPIs Principais"
            })
        
        # Composição (Pie/Donut)
        if category_cols and numeric_cols:
            cat_info = column_analysis[category_cols[0]]
            if cat_info['unique_count'] <= 7:
                suggestions.append({
                    "type": "donut_chart",
                    "priority": "medium",
                    "columns": {"category": category_cols[0], "value": numeric_cols[0]},
                    "reason": "Poucas categorias - ideal para visualizar proporções",
                    "title": f"Composição de {numeric_cols[0]} por {category_cols[0]}"
                })
        
        # Heatmap para múltiplas métricas
        if len(numeric_cols) >= 3:
            suggestions.append({
                "type": "heatmap",
                "priority": "low",
                "columns": {"metrics": numeric_cols},
                "reason": "Múltiplas métricas - visualização de padrões",
                "title": "Mapa de Calor de Correlações"
            })
        
        return sorted(suggestions, key=lambda x: {"high": 3, "medium": 2, "low": 1}[x['priority']], reverse=True)
    
    def _assess_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Avalia a qualidade dos dados"""
        total_cells = df.shape[0] * df.shape[1]
        null_cells = df.isnull().sum().sum()
        
        quality = {
            "completeness_score": round((1 - null_cells / total_cells) * 100, 2),
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "null_cells": int(null_cells),
            "duplicate_rows": int(df.duplicated().sum()),
            "issues": []
        }
        
        # Identifica problemas
        if quality["completeness_score"] < 80:
            quality["issues"].append("⚠️ Alta taxa de valores nulos (>20%)")
        
        if quality["duplicate_rows"] > len(df) * 0.05:
            quality["issues"].append("⚠️ Muitas linhas duplicadas (>5%)")
        
        # Verifica colunas com muitos valores únicos
        for col in df.columns:
            if df[col].nunique() == len(df):
                quality["issues"].append(f"ℹ️ Coluna '{col}' parece ser um identificador único")
        
        if not quality["issues"]:
            quality["issues"].append("✅ Dados em boa qualidade")
        
        return quality
    
    def generate_summary_text(self, analysis: Dict[str, Any]) -> str:
        """Gera um resumo textual da análise"""
        summary = f"""
📊 **Resumo da Análise de Dados**

**Dimensões:**
- {analysis['rows']:,} linhas
- {analysis['columns']} colunas

**Qualidade dos Dados:**
- Completude: {analysis['data_quality']['completeness_score']}%
- Duplicatas: {analysis['data_quality']['duplicate_rows']}

**Visualizações Sugeridas:**
"""
        for i, suggestion in enumerate(analysis['suggested_visuals'][:5], 1):
            summary += f"\n{i}. **{suggestion['type'].replace('_', ' ').title()}**: {suggestion['reason']}"
        
        return summary
    
    def analyze_powerbi_model(self) -> Dict[str, Any]:
        """
        Analisa um modelo Power BI conectado via powerbi_connector.
        
        Returns:
            Dict com estrutura do modelo, tabelas, medidas, relacionamentos
        """
        if not self.powerbi_connector or not self.powerbi_connector.is_connected():
            raise ValueError("PowerBIConnector não está conectado")
        
        # Obter estrutura do modelo
        model_structure = self.powerbi_connector.get_model_structure()
        
        # Análise de tabelas e colunas
        tables_analysis = []
        for table in model_structure.get('tables', []):
            table_info = {
                'name': table['name'],
                'type': table.get('type', 'Table'),
                'columns_count': len(table.get('columns', [])),
                'measures_count': len(table.get('measures', [])),
                'columns': [],
                'measures': []
            }
            
            # Analisar colunas
            for column in table.get('columns', []):
                col_info = {
                    'name': column.get('ColumnName') or column.get('name', 'Unknown'),
                    'dataType': column.get('DataType') or column.get('dataType', 'Unknown'),
                    'semantic_type': self._map_powerbi_to_semantic_type(column),
                    'suggested_format': self._suggest_format_for_column(column)
                }
                table_info['columns'].append(col_info)
            
            # Analisar medidas
            for measure in table.get('measures', []):
                measure_info = {
                    'name': measure.get('MeasureName') or measure.get('name', 'Unknown'),
                    'expression': measure.get('Expression') or measure.get('expression', ''),
                    'format': measure.get('formatString', '')
                }
                table_info['measures'].append(measure_info)
            
            tables_analysis.append(table_info)
        
        # Análise de relacionamentos
        relationships = model_structure.get('relationships', [])
        relationships_analysis = []
        for rel in relationships:
            relationships_analysis.append({
                'from_table': rel.get('fromTable'),
                'from_column': rel.get('fromColumn'),
                'to_table': rel.get('toTable'),
                'to_column': rel.get('toColumn'),
                'cardinality': rel.get('cardinality', 'Unknown')
            })
        
        # Sugerir visualizações baseadas no modelo
        visual_analysis = self.powerbi_connector.analyze_model_for_visuals()
        
        return {
            'connection_info': {
                'status': 'connected',
                'connection_name': self.powerbi_connector.connection_name
            },
            'model_structure': {
                'tables_count': len(tables_analysis),
                'relationships_count': len(relationships_analysis)
            },
            'tables': tables_analysis,
            'relationships': relationships_analysis,
            'suggested_visuals': visual_analysis.get('suggested_visuals', []),
            'visual_summary': visual_analysis.get('summary', {}),
            'visual_recommendations': visual_analysis.get('recommendations', []),
            'model_health': self._assess_model_health(tables_analysis, relationships_analysis)
        }
    
    def _map_powerbi_to_semantic_type(self, column: Dict) -> str:
        """Mapeia tipo de dado Power BI para tipo semântico"""
        data_type = (column.get('DataType') or column.get('dataType', '')).lower()
        column_name = (column.get('ColumnName') or column.get('name', '')).lower()
        
        # Mapeamento por tipo de dado
        if data_type in ['datetime', 'date']:
            return 'date'
        elif data_type in ['int64', 'decimal', 'double']:
            # Verificar pelo nome se é métrica ou identificador
            if any(word in column_name for word in ['id', 'key', 'code', 'number']):
                return 'identifier'
            elif '%' in column_name or 'percent' in column_name:
                return 'percentage'
            elif any(word in column_name for word in ['value', 'amount', 'total', 'sum']):
                return 'metric'
            elif any(word in column_name for word in ['price', 'cost', 'revenue']):
                return 'currency'
            return 'metric'
        elif data_type == 'string':
            return 'category'
        elif data_type == 'boolean':
            return 'boolean'
        
        return 'unknown'
    
    def _suggest_format_for_column(self, column: Dict) -> str:
        """Sugere formato adequado para coluna Power BI"""
        data_type = (column.get('DataType') or column.get('dataType', '')).lower()
        column_name = (column.get('ColumnName') or column.get('name', '')).lower()
        
        if data_type in ['datetime', 'date']:
            return 'dd/mm/yyyy'
        elif data_type in ['int64', 'decimal', 'double']:
            if '%' in column_name or 'percent' in column_name:
                return '0.00%'
            elif any(word in column_name for word in ['price', 'cost', 'revenue', 'value']):
                return 'R$ #,##0.00'
            return '#,##0.00'
        
        return 'General'
    
    def _assess_model_health(self, tables: List[Dict], relationships: List[Dict]) -> Dict:
        """Avalia saúde do modelo Power BI"""
        issues = []
        
        # Verificar tabelas sem relacionamentos
        connected_tables = set()
        for rel in relationships:
            connected_tables.add(rel['from_table'])
            connected_tables.add(rel['to_table'])
        
        unconnected_tables = [t['name'] for t in tables if t['name'] not in connected_tables and len(tables) > 1]
        if unconnected_tables:
            issues.append(f"Tabelas sem relacionamentos: {', '.join(unconnected_tables)}")
        
        # Verificar medidas vs colunas calculadas
        total_measures = sum(t['measures_count'] for t in tables)
        if total_measures == 0:
            issues.append("💡 Recomendação: Criar medidas DAX para métricas principais (ex: Total Vendas = SUM([Valor]))")
        elif total_measures < 3:
            issues.append(f"Apenas {total_measures} medida(s) - considere adicionar mais KPIs")
        
        # Score de saúde
        health_score = 100
        health_score -= len(unconnected_tables) * 10
        health_score -= (10 if total_measures == 0 else 5 if total_measures < 3 else 0)
        health_score = max(0, health_score)
        
        return {
            'score': health_score,
            'status': 'good' if health_score >= 80 else 'warning' if health_score >= 60 else 'poor',
            'issues': issues
        }
