"""
Motor de Templates de Layout - Define layouts profissionais para dashboards
"""
from typing import Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class VisualPosition:
    """Posição e tamanho de um visual no canvas"""
    x: int
    y: int
    width: int
    height: int
    z_index: int = 0


class LayoutEngine:
    """Gera layouts profissionais para dashboards do Power BI"""
    
    # Dimensões padrão do canvas do Power BI (em pixels)
    CANVAS_WIDTH = 1280
    CANVAS_HEIGHT = 720
    
    # Templates de layout predefinidos
    TEMPLATES = {
        "executive_summary": {
            "name": "Executive Summary",
            "description": "Layout focado em KPIs principais com destaque visual",
            "layout": "grid",
            "sections": [
                {"type": "kpi_row", "height": 150, "count": 4},
                {"type": "main_chart", "height": 370},
                {"type": "supporting_charts", "height": 200, "count": 2}
            ]
        },
        "detailed_analysis": {
            "name": "Detailed Analysis",
            "description": "Layout balanceado para análise detalhada com múltiplos visuais",
            "layout": "grid",
            "sections": [
                {"type": "title_bar", "height": 80},
                {"type": "filters", "width": 280, "side": "left"},
                {"type": "main_content", "charts": 6}
            ]
        },
        "single_focus": {
            "name": "Single Focus",
            "description": "Um visual principal com suporte mínimo",
            "layout": "centered",
            "sections": [
                {"type": "header", "height": 100},
                {"type": "main_visual", "height": 520},
                {"type": "footer_metrics", "height": 100}
            ]
        },
        "comparison_view": {
            "name": "Comparison View",
            "description": "Layout para comparar múltiplas métricas lado a lado",
            "layout": "columns",
            "sections": [
                {"type": "left_panel", "width": "50%"},
                {"type": "right_panel", "width": "50%"}
            ]
        },
        "storytelling": {
            "name": "Storytelling Dashboard",
            "description": "Layout narrativo com fluxo visual guiado",
            "layout": "flow",
            "sections": [
                {"type": "hero_section", "height": 300},
                {"type": "insight_cards", "height": 220, "count": 3},
                {"type": "detail_section", "height": 200}
            ]
        },
        "modern_minimal": {
            "name": "Modern Minimal",
            "description": "Design minimalista com muito espaço em branco",
            "layout": "asymmetric",
            "sections": [
                {"type": "featured_kpi", "position": "top_left", "size": "large"},
                {"type": "secondary_metrics", "position": "top_right", "count": 3},
                {"type": "main_chart", "position": "bottom", "width": "full"}
            ]
        }
    }
    
    def __init__(self):
        self.current_layout = None
    
    def generate_layout(self, template_name: str, visual_count: int = None) -> Dict[str, Any]:
        """
        Gera um layout completo baseado no template
        
        Args:
            template_name: Nome do template a usar
            visual_count: Número de visuais a acomodar (opcional)
        
        Returns:
            Dicionário com posições de todos os visuais
        """
        if template_name not in self.TEMPLATES:
            template_name = "detailed_analysis"
        
        template = self.TEMPLATES[template_name]
        
        # Gera layout específico baseado no tipo
        if template["layout"] == "grid":
            return self._generate_grid_layout(template, visual_count)
        elif template["layout"] == "centered":
            return self._generate_centered_layout(template)
        elif template["layout"] == "columns":
            return self._generate_columns_layout(template)
        elif template["layout"] == "flow":
            return self._generate_flow_layout(template)
        elif template["layout"] == "asymmetric":
            return self._generate_asymmetric_layout(template)
        
        return self._generate_grid_layout(template, visual_count)
    
    def _generate_grid_layout(self, template: Dict, visual_count: int = None) -> Dict[str, Any]:
        """Gera layout em grade"""
        layout = {
            "template": template["name"],
            "canvas": {"width": self.CANVAS_WIDTH, "height": self.CANVAS_HEIGHT},
            "visuals": []
        }
        
        padding = 20
        gap = 15
        current_y = padding
        visual_id = 1
        
        for section in template["sections"]:
            if section["type"] == "kpi_row":
                # Linha de KPIs
                count = section.get("count", 4)
                kpi_width = (self.CANVAS_WIDTH - 2 * padding - (count - 1) * gap) // count
                kpi_height = section["height"]
                
                for i in range(count):
                    x = padding + i * (kpi_width + gap)
                    layout["visuals"].append({
                        "id": f"kpi_{visual_id}",
                        "type": "card",
                        "position": asdict(VisualPosition(x, current_y, kpi_width, kpi_height)),
                        "suggested_visual": "KPI Card",
                        "priority": "high"
                    })
                    visual_id += 1
                
                current_y += kpi_height + gap
            
            elif section["type"] == "main_chart":
                # Gráfico principal
                width = self.CANVAS_WIDTH - 2 * padding
                height = section["height"]
                
                layout["visuals"].append({
                    "id": f"main_chart_{visual_id}",
                    "type": "chart",
                    "position": asdict(VisualPosition(padding, current_y, width, height)),
                    "suggested_visual": "Line Chart or Bar Chart",
                    "priority": "high"
                })
                visual_id += 1
                current_y += height + gap
            
            elif section["type"] == "supporting_charts":
                # Gráficos de suporte
                count = section.get("count", 2)
                chart_width = (self.CANVAS_WIDTH - 2 * padding - (count - 1) * gap) // count
                chart_height = section["height"]
                
                for i in range(count):
                    x = padding + i * (chart_width + gap)
                    layout["visuals"].append({
                        "id": f"support_chart_{visual_id}",
                        "type": "chart",
                        "position": asdict(VisualPosition(x, current_y, chart_width, chart_height)),
                        "suggested_visual": "Supporting Chart",
                        "priority": "medium"
                    })
                    visual_id += 1
        
        return layout
    
    def _generate_centered_layout(self, template: Dict) -> Dict[str, Any]:
        """Gera layout centralizado"""
        layout = {
            "template": template["name"],
            "canvas": {"width": self.CANVAS_WIDTH, "height": self.CANVAS_HEIGHT},
            "visuals": []
        }
        
        padding = 40
        gap = 20
        current_y = padding
        
        for section in template["sections"]:
            if section["type"] == "header":
                width = self.CANVAS_WIDTH - 2 * padding
                height = section["height"]
                
                layout["visuals"].append({
                    "id": "header",
                    "type": "text",
                    "position": asdict(VisualPosition(padding, current_y, width, height)),
                    "suggested_visual": "Title/Header",
                    "priority": "high"
                })
                current_y += height + gap
            
            elif section["type"] == "main_visual":
                # Visual centralizado e grande
                width = self.CANVAS_WIDTH - 2 * padding
                height = section["height"]
                
                layout["visuals"].append({
                    "id": "main_visual",
                    "type": "chart",
                    "position": asdict(VisualPosition(padding, current_y, width, height)),
                    "suggested_visual": "Featured Chart",
                    "priority": "highest"
                })
                current_y += height + gap
            
            elif section["type"] == "footer_metrics":
                # Métricas no rodapé
                width = self.CANVAS_WIDTH - 2 * padding
                height = section["height"]
                
                layout["visuals"].append({
                    "id": "footer_metrics",
                    "type": "metrics",
                    "position": asdict(VisualPosition(padding, current_y, width, height)),
                    "suggested_visual": "Metric Row",
                    "priority": "medium"
                })
        
        return layout
    
    def _generate_columns_layout(self, template: Dict) -> Dict[str, Any]:
        """Gera layout em colunas"""
        layout = {
            "template": template["name"],
            "canvas": {"width": self.CANVAS_WIDTH, "height": self.CANVAS_HEIGHT},
            "visuals": []
        }
        
        padding = 20
        gap = 20
        
        # Divide em duas colunas
        col_width = (self.CANVAS_WIDTH - 2 * padding - gap) // 2
        
        # Coluna esquerda
        layout["visuals"].append({
            "id": "left_panel",
            "type": "container",
            "position": asdict(VisualPosition(padding, padding, col_width, self.CANVAS_HEIGHT - 2 * padding)),
            "suggested_visual": "Container for left visuals",
            "priority": "high"
        })
        
        # Coluna direita
        layout["visuals"].append({
            "id": "right_panel",
            "type": "container",
            "position": asdict(VisualPosition(padding + col_width + gap, padding, col_width, self.CANVAS_HEIGHT - 2 * padding)),
            "suggested_visual": "Container for right visuals",
            "priority": "high"
        })
        
        return layout
    
    def _generate_flow_layout(self, template: Dict) -> Dict[str, Any]:
        """Gera layout em fluxo narrativo"""
        layout = {
            "template": template["name"],
            "canvas": {"width": self.CANVAS_WIDTH, "height": self.CANVAS_HEIGHT},
            "visuals": []
        }
        
        padding = 30
        gap = 15
        current_y = padding
        
        for section in template["sections"]:
            if section["type"] == "hero_section":
                # Seção hero grande
                width = self.CANVAS_WIDTH - 2 * padding
                height = section["height"]
                
                layout["visuals"].append({
                    "id": "hero",
                    "type": "hero",
                    "position": asdict(VisualPosition(padding, current_y, width, height)),
                    "suggested_visual": "Hero Visual",
                    "priority": "highest"
                })
                current_y += height + gap
            
            elif section["type"] == "insight_cards":
                # Cards de insights
                count = section.get("count", 3)
                card_width = (self.CANVAS_WIDTH - 2 * padding - (count - 1) * gap) // count
                card_height = section["height"]
                
                for i in range(count):
                    x = padding + i * (card_width + gap)
                    layout["visuals"].append({
                        "id": f"insight_card_{i+1}",
                        "type": "card",
                        "position": asdict(VisualPosition(x, current_y, card_width, card_height)),
                        "suggested_visual": "Insight Card",
                        "priority": "high"
                    })
                
                current_y += card_height + gap
            
            elif section["type"] == "detail_section":
                width = self.CANVAS_WIDTH - 2 * padding
                height = section["height"]
                
                layout["visuals"].append({
                    "id": "details",
                    "type": "detail",
                    "position": asdict(VisualPosition(padding, current_y, width, height)),
                    "suggested_visual": "Detail Chart",
                    "priority": "medium"
                })
        
        return layout
    
    def _generate_asymmetric_layout(self, template: Dict) -> Dict[str, Any]:
        """Gera layout assimétrico moderno"""
        layout = {
            "template": template["name"],
            "canvas": {"width": self.CANVAS_WIDTH, "height": self.CANVAS_HEIGHT},
            "visuals": []
        }
        
        padding = 30
        gap = 20
        
        # KPI grande no canto superior esquerdo
        featured_width = 400
        featured_height = 300
        
        layout["visuals"].append({
            "id": "featured_kpi",
            "type": "kpi",
            "position": asdict(VisualPosition(padding, padding, featured_width, featured_height)),
            "suggested_visual": "Featured KPI",
            "priority": "highest"
        })
        
        # Métricas menores no canto superior direito
        small_kpi_width = (self.CANVAS_WIDTH - featured_width - 3 * padding - 2 * gap) // 1
        small_kpi_height = (featured_height - gap) // 3
        
        for i in range(3):
            y = padding + i * (small_kpi_height + gap // 2)
            layout["visuals"].append({
                "id": f"secondary_kpi_{i+1}",
                "type": "kpi",
                "position": asdict(VisualPosition(featured_width + 2 * padding + gap, y, small_kpi_width, small_kpi_height)),
                "suggested_visual": "Secondary KPI",
                "priority": "medium"
            })
        
        # Gráfico grande na parte inferior
        main_chart_y = featured_height + 2 * padding + gap
        main_chart_height = self.CANVAS_HEIGHT - main_chart_y - padding
        
        layout["visuals"].append({
            "id": "main_chart",
            "type": "chart",
            "position": asdict(VisualPosition(padding, main_chart_y, self.CANVAS_WIDTH - 2 * padding, main_chart_height)),
            "suggested_visual": "Main Chart",
            "priority": "high"
        })
        
        return layout
    
    def optimize_layout(self, layout: Dict[str, Any], priorities: List[str] = None) -> Dict[str, Any]:
        """
        Otimiza um layout existente baseado em prioridades
        
        Args:
            layout: Layout a otimizar
            priorities: Lista de IDs de visuais em ordem de prioridade
        
        Returns:
            Layout otimizado
        """
        if not priorities:
            return layout
        
        # Reordena z-index baseado em prioridades
        for i, visual_id in enumerate(priorities):
            for visual in layout["visuals"]:
                if visual["id"] == visual_id:
                    visual["position"]["z_index"] = len(priorities) - i
        
        return layout
    
    def get_responsive_layout(self, layout: Dict[str, Any], target_width: int, target_height: int) -> Dict[str, Any]:
        """
        Adapta um layout para diferentes resoluções
        
        Args:
            layout: Layout original
            target_width: Largura alvo
            target_height: Altura alvo
        
        Returns:
            Layout adaptado
        """
        scale_x = target_width / self.CANVAS_WIDTH
        scale_y = target_height / self.CANVAS_HEIGHT
        
        responsive_layout = layout.copy()
        responsive_layout["canvas"] = {"width": target_width, "height": target_height}
        responsive_layout["visuals"] = []
        
        for visual in layout["visuals"]:
            pos = visual["position"]
            new_visual = visual.copy()
            new_visual["position"] = {
                "x": int(pos["x"] * scale_x),
                "y": int(pos["y"] * scale_y),
                "width": int(pos["width"] * scale_x),
                "height": int(pos["height"] * scale_y),
                "z_index": pos.get("z_index", 0)
            }
            responsive_layout["visuals"].append(new_visual)
        
        return responsive_layout
    
    def list_templates(self) -> List[Dict[str, str]]:
        """Lista todos os templates disponíveis"""
        return [
            {
                "name": name,
                "display_name": template["name"],
                "description": template["description"]
            }
            for name, template in self.TEMPLATES.items()
        ]
