"""
Assistente de IA - Integração com OpenAI/Claude para sugestões contextualizadas
"""
import os
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


class AIAssistant:
    """Assistente de IA para sugestões criativas de visualização"""
    
    def __init__(self, provider: str = "openai"):
        """
        Inicializa o assistente de IA
        
        Args:
            provider: 'openai' ou 'anthropic'
        """
        self.provider = provider.lower()
        self.client = None
        self.model = os.getenv("AI_MODEL", "gpt-4-turbo-preview")
        
        if self.provider == "openai":
            self._init_openai()
        elif self.provider == "anthropic":
            self._init_anthropic()
    
    def _init_openai(self):
        """Inicializa cliente OpenAI"""
        try:
            import openai
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.client = openai.OpenAI(api_key=api_key)
            else:
                print("⚠️ OPENAI_API_KEY não encontrada. Configure no arquivo .env")
        except ImportError:
            print("⚠️ Biblioteca openai não instalada. Execute: pip install openai")
    
    def _init_anthropic(self):
        """Inicializa cliente Anthropic"""
        try:
            import anthropic
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                self.client = anthropic.Anthropic(api_key=api_key)
            else:
                print("⚠️ ANTHROPIC_API_KEY não encontrada. Configure no arquivo .env")
        except ImportError:
            print("⚠️ Biblioteca anthropic não instalada. Execute: pip install anthropic")
    
    def is_available(self) -> bool:
        """Verifica se o assistente está disponível"""
        return self.client is not None
    
    def suggest_visualizations(self, data_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sugere visualizações baseadas na análise de dados usando IA
        
        Args:
            data_analysis: Resultado da análise de dados
        
        Returns:
            Sugestões detalhadas de visualizações
        """
        if not self.is_available():
            return self._fallback_suggestions(data_analysis)
        
        # Prepara contexto para a IA
        prompt = self._build_visualization_prompt(data_analysis)
        
        try:
            response = self._call_ai(prompt)
            return self._parse_visualization_response(response)
        except Exception as e:
            print(f"⚠️ Erro ao chamar IA: {e}")
            return self._fallback_suggestions(data_analysis)
    
    def suggest_color_palette(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sugere paletas de cores baseadas no contexto dos dados
        
        Args:
            context: Contexto (tipo de dados, mood, indústria, etc.)
        
        Returns:
            Sugestões de paletas
        """
        if not self.is_available():
            return self._fallback_colors(context)
        
        prompt = self._build_color_prompt(context)
        
        try:
            response = self._call_ai(prompt)
            return self._parse_color_response(response)
        except Exception as e:
            print(f"⚠️ Erro ao chamar IA: {e}")
            return self._fallback_colors(context)
    
    def suggest_layout(self, visual_count: int, dashboard_purpose: str) -> Dict[str, Any]:
        """
        Sugere layout baseado no propósito do dashboard
        
        Args:
            visual_count: Número de visuais
            dashboard_purpose: Propósito do dashboard
        
        Returns:
            Sugestões de layout
        """
        if not self.is_available():
            return self._fallback_layout(visual_count)
        
        prompt = self._build_layout_prompt(visual_count, dashboard_purpose)
        
        try:
            response = self._call_ai(prompt)
            return self._parse_layout_response(response)
        except Exception as e:
            print(f"⚠️ Erro ao chamar IA: {e}")
            return self._fallback_layout(visual_count)
    
    def generate_insights(self, data_summary: Dict[str, Any]) -> List[str]:
        """
        Gera insights baseados nos dados
        
        Args:
            data_summary: Resumo dos dados
        
        Returns:
            Lista de insights
        """
        if not self.is_available():
            return self._fallback_insights(data_summary)
        
        prompt = self._build_insights_prompt(data_summary)
        
        try:
            response = self._call_ai(prompt)
            return self._parse_insights_response(response)
        except Exception as e:
            print(f"⚠️ Erro ao chamar IA: {e}")
            return self._fallback_insights(data_summary)
    
    def _call_ai(self, prompt: str) -> str:
        """Chama a API de IA apropriada"""
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em visualização de dados e design de dashboards do Power BI. Forneça sugestões criativas, práticas e profissionais."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message.content
        
        elif self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        
        return ""
    
    def _build_visualization_prompt(self, data_analysis: Dict[str, Any]) -> str:
        """Constrói prompt para sugestões de visualização"""
        cols_info = "\n".join([
            f"- {col}: {info['detected_type']} ({info['unique_count']} valores únicos)"
            for col, info in data_analysis.get("column_analysis", {}).items()
        ])
        
        return f"""
Analise os seguintes dados e sugira as 5 melhores visualizações para Power BI:

**Dados:**
- {data_analysis.get('rows', 0)} linhas
- {data_analysis.get('columns', 0)} colunas

**Colunas:**
{cols_info}

**Qualidade dos Dados:**
- Completude: {data_analysis.get('data_quality', {}).get('completeness_score', 0)}%

Forneça sugestões específicas incluindo:
1. Tipo de visual (bar chart, line chart, scatter, etc)
2. Colunas a usar (eixos, legendas, valores)
3. Razão da sugestão
4. Título sugerido
5. Prioridade (alta, média, baixa)

Formato: JSON com array de objetos.
"""
    
    def _build_color_prompt(self, context: Dict[str, Any]) -> str:
        """Constrói prompt para sugestões de cores"""
        return f"""
Sugira uma paleta de cores profissional para um dashboard Power BI com o seguinte contexto:

**Tipo de Dados:** {context.get('data_type', 'geral')}
**Mood/Estilo:** {context.get('mood', 'profissional')}
**Indústria:** {context.get('industry', 'negócios')}
**Público-alvo:** {context.get('audience', 'executivos')}

Forneça:
1. Nome da paleta
2. 5-7 cores em formato HEX
3. Cor primária, secundária e de destaque
4. Cor de fundo e texto
5. Justificativa das escolhas

Formato: JSON
"""
    
    def _build_layout_prompt(self, visual_count: int, purpose: str) -> str:
        """Constrói prompt para sugestões de layout"""
        return f"""
Sugira um layout ideal para um dashboard Power BI com:

**Número de visuais:** {visual_count}
**Propósito:** {purpose}

Considere:
- Hierarquia visual
- Fluxo de leitura
- Importância relativa de cada visual
- Espaçamento e proporções
- Princípios de design moderno

Forneça sugestões de template e organização.
Formato: JSON
"""
    
    def _build_insights_prompt(self, data_summary: Dict[str, Any]) -> str:
        """Constrói prompt para geração de insights"""
        return f"""
Baseado nos seguintes dados, gere 3-5 insights acionáveis:

{str(data_summary)}

Os insights devem ser:
- Específicos e baseados nos dados
- Acionáveis
- Relevantes para negócios
- Claros e concisos

Formato: JSON array de strings
"""
    
    def _parse_visualization_response(self, response: str) -> Dict[str, Any]:
        """Parse da resposta de visualização"""
        import json
        try:
            # Tenta extrair JSON da resposta
            start = response.find('[')
            end = response.rfind(']') + 1
            if start >= 0 and end > start:
                suggestions = json.loads(response[start:end])
                return {"suggestions": suggestions, "source": "ai"}
        except:
            pass
        
        return {"suggestions": [], "source": "ai", "raw_response": response}
    
    def _parse_color_response(self, response: str) -> Dict[str, Any]:
        """Parse da resposta de cores"""
        import json
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                palette = json.loads(response[start:end])
                return {"palette": palette, "source": "ai"}
        except:
            pass
        
        return {"palette": {}, "source": "ai", "raw_response": response}
    
    def _parse_layout_response(self, response: str) -> Dict[str, Any]:
        """Parse da resposta de layout"""
        import json
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                layout = json.loads(response[start:end])
                return {"layout": layout, "source": "ai"}
        except:
            pass
        
        return {"layout": {}, "source": "ai", "raw_response": response}
    
    def _parse_insights_response(self, response: str) -> List[str]:
        """Parse da resposta de insights"""
        import json
        try:
            start = response.find('[')
            end = response.rfind(']') + 1
            if start >= 0 and end > start:
                insights = json.loads(response[start:end])
                return insights
        except:
            pass
        
        # Fallback: divide por linhas
        lines = [line.strip() for line in response.split('\n') if line.strip()]
        return [line.lstrip('- ').lstrip('* ').lstrip('• ') for line in lines if len(line) > 10][:5]
    
    def _fallback_suggestions(self, data_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Sugestões fallback sem IA"""
        return {
            "suggestions": data_analysis.get("suggested_visuals", []),
            "source": "rule_based"
        }
    
    def _fallback_colors(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Cores fallback sem IA"""
        return {
            "palette": {
                "name": "Default Professional",
                "colors": ["#1E88E5", "#FFA726", "#26C6DA", "#66BB6A", "#AB47BC"]
            },
            "source": "preset"
        }
    
    def _fallback_layout(self, visual_count: int) -> Dict[str, Any]:
        """Layout fallback sem IA"""
        template = "detailed_analysis" if visual_count > 4 else "executive_summary"
        return {
            "layout": {"template": template},
            "source": "rule_based"
        }
    
    def _fallback_insights(self, data_summary: Dict[str, Any]) -> List[str]:
        """Insights fallback sem IA"""
        return [
            "Analise as tendências ao longo do tempo",
            "Compare métricas principais entre categorias",
            "Identifique outliers e anomalias",
            "Monitore KPIs críticos"
        ]
