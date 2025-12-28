"""
Gerador de Paletas de Cores - Cria combinações harmônicas e profissionais
"""
import colorsys
import random
from typing import List, Dict, Tuple
import math


class ColorGenerator:
    """Gera paletas de cores profissionais e harmônicas"""
    
    # Paletas base inspiradas em designs modernos
    PRESET_PALETTES = {
        "modern_dark": {
            "name": "Modern Dark",
            "primary": "#1E88E5",
            "secondary": "#FFA726",
            "accent": "#26C6DA",
            "background": "#121212",
            "foreground": "#FFFFFF",
            "colors": ["#1E88E5", "#FFA726", "#26C6DA", "#66BB6A", "#AB47BC"]
        },
        "minimal_light": {
            "name": "Minimal Light",
            "primary": "#2C3E50",
            "secondary": "#E74C3C",
            "accent": "#3498DB",
            "background": "#FFFFFF",
            "foreground": "#2C3E50",
            "colors": ["#2C3E50", "#E74C3C", "#3498DB", "#1ABC9C", "#F39C12"]
        },
        "corporate_blue": {
            "name": "Corporate Blue",
            "primary": "#003F87",
            "secondary": "#0066CC",
            "accent": "#00A3E0",
            "background": "#F5F7FA",
            "foreground": "#1A1A1A",
            "colors": ["#003F87", "#0066CC", "#00A3E0", "#5AC8FA", "#8E8E93"]
        },
        "vibrant_gradient": {
            "name": "Vibrant Gradient",
            "primary": "#6B46C1",
            "secondary": "#F093FB",
            "accent": "#4FACFE",
            "background": "#FFFFFF",
            "foreground": "#1A202C",
            "colors": ["#6B46C1", "#F093FB", "#4FACFE", "#00F2FE", "#FA709A"]
        },
        "nature_earth": {
            "name": "Nature Earth",
            "primary": "#2D6A4F",
            "secondary": "#52B788",
            "accent": "#95D5B2",
            "background": "#FFFFFF",
            "foreground": "#1B4332",
            "colors": ["#1B4332", "#2D6A4F", "#52B788", "#95D5B2", "#D8F3DC"]
        },
        "sunset_warm": {
            "name": "Sunset Warm",
            "primary": "#FF6B6B",
            "secondary": "#FFD93D",
            "accent": "#6BCF7F",
            "background": "#FFF8F3",
            "foreground": "#2C3639",
            "colors": ["#FF6B6B", "#FFD93D", "#6BCF7F", "#95E1D3", "#F38181"]
        },
        "tech_neon": {
            "name": "Tech Neon",
            "primary": "#00FFF0",
            "secondary": "#FF00E5",
            "accent": "#FFE600",
            "background": "#0A0E27",
            "foreground": "#FFFFFF",
            "colors": ["#00FFF0", "#FF00E5", "#FFE600", "#00FF88", "#7B2FFF"]
        }
    }
    
    def __init__(self):
        self.current_palette = None
    
    def get_preset_palette(self, name: str) -> Dict:
        """Retorna uma paleta pré-definida"""
        return self.PRESET_PALETTES.get(name, self.PRESET_PALETTES["modern_dark"])
    
    def list_presets(self) -> List[str]:
        """Lista todas as paletas disponíveis"""
        return list(self.PRESET_PALETTES.keys())
    
    def generate_from_base_color(self, base_color: str, scheme: str = "analogous", count: int = 5) -> Dict:
        """
        Gera uma paleta a partir de uma cor base
        
        Schemes: analogous, complementary, triadic, tetradic, monochromatic, split_complementary
        """
        rgb = self._hex_to_rgb(base_color)
        hsv = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        
        colors = []
        
        if scheme == "analogous":
            colors = self._generate_analogous(hsv, count)
        elif scheme == "complementary":
            colors = self._generate_complementary(hsv, count)
        elif scheme == "triadic":
            colors = self._generate_triadic(hsv, count)
        elif scheme == "tetradic":
            colors = self._generate_tetradic(hsv, count)
        elif scheme == "monochromatic":
            colors = self._generate_monochromatic(hsv, count)
        elif scheme == "split_complementary":
            colors = self._generate_split_complementary(hsv, count)
        else:
            colors = self._generate_analogous(hsv, count)
        
        return {
            "name": f"{scheme.title()} ({base_color})",
            "primary": colors[0] if colors else base_color,
            "secondary": colors[1] if len(colors) > 1 else base_color,
            "accent": colors[2] if len(colors) > 2 else base_color,
            "background": "#FFFFFF",
            "foreground": "#1A1A1A",
            "colors": colors,
            "scheme": scheme
        }
    
    def _generate_analogous(self, hsv: Tuple[float, float, float], count: int) -> List[str]:
        """Cores análogas (próximas na roda de cores)"""
        h, s, v = hsv
        colors = []
        step = 30 / 360  # 30 graus
        
        for i in range(count):
            offset = (i - count // 2) * step
            new_h = (h + offset) % 1.0
            colors.append(self._hsv_to_hex(new_h, s, v))
        
        return colors
    
    def _generate_complementary(self, hsv: Tuple[float, float, float], count: int) -> List[str]:
        """Cores complementares (opostas na roda)"""
        h, s, v = hsv
        colors = [self._hsv_to_hex(h, s, v)]
        
        # Cor complementar (180 graus)
        comp_h = (h + 0.5) % 1.0
        colors.append(self._hsv_to_hex(comp_h, s, v))
        
        # Variações
        for i in range(count - 2):
            if i % 2 == 0:
                var_h = (h + (i + 1) * 0.1) % 1.0
            else:
                var_h = (comp_h + (i + 1) * 0.1) % 1.0
            colors.append(self._hsv_to_hex(var_h, s * 0.8, v))
        
        return colors[:count]
    
    def _generate_triadic(self, hsv: Tuple[float, float, float], count: int) -> List[str]:
        """Cores triádicas (120 graus de separação)"""
        h, s, v = hsv
        colors = []
        
        for i in range(3):
            new_h = (h + i / 3) % 1.0
            colors.append(self._hsv_to_hex(new_h, s, v))
        
        # Adiciona variações se precisar de mais cores
        while len(colors) < count:
            base_idx = len(colors) % 3
            new_h = (h + base_idx / 3 + 0.05 * len(colors)) % 1.0
            colors.append(self._hsv_to_hex(new_h, s * 0.8, v * 0.9))
        
        return colors[:count]
    
    def _generate_tetradic(self, hsv: Tuple[float, float, float], count: int) -> List[str]:
        """Cores tetrádicas (90 graus de separação)"""
        h, s, v = hsv
        colors = []
        
        for i in range(4):
            new_h = (h + i / 4) % 1.0
            colors.append(self._hsv_to_hex(new_h, s, v))
        
        # Variações
        while len(colors) < count:
            base_idx = len(colors) % 4
            new_h = (h + base_idx / 4 + 0.03 * len(colors)) % 1.0
            colors.append(self._hsv_to_hex(new_h, s * 0.8, v * 0.9))
        
        return colors[:count]
    
    def _generate_monochromatic(self, hsv: Tuple[float, float, float], count: int) -> List[str]:
        """Cores monocromáticas (mesma matiz, diferentes saturações/valores)"""
        h, s, v = hsv
        colors = []
        
        for i in range(count):
            factor = 0.3 + (i / (count - 1)) * 0.7 if count > 1 else 1
            new_s = s * factor
            new_v = 0.4 + factor * 0.6
            colors.append(self._hsv_to_hex(h, new_s, new_v))
        
        return colors
    
    def _generate_split_complementary(self, hsv: Tuple[float, float, float], count: int) -> List[str]:
        """Cores complementares divididas"""
        h, s, v = hsv
        colors = [self._hsv_to_hex(h, s, v)]
        
        # Duas cores adjacentes à complementar
        comp_h = (h + 0.5) % 1.0
        colors.append(self._hsv_to_hex((comp_h - 30/360) % 1.0, s, v))
        colors.append(self._hsv_to_hex((comp_h + 30/360) % 1.0, s, v))
        
        # Variações
        while len(colors) < count:
            idx = len(colors) % 3
            base_h = h if idx == 0 else (comp_h - 30/360 if idx == 1 else comp_h + 30/360)
            new_h = (base_h + 0.05 * len(colors)) % 1.0
            colors.append(self._hsv_to_hex(new_h, s * 0.8, v * 0.9))
        
        return colors[:count]
    
    def generate_gradient(self, color1: str, color2: str, steps: int = 5) -> List[str]:
        """Gera um gradiente entre duas cores"""
        rgb1 = self._hex_to_rgb(color1)
        rgb2 = self._hex_to_rgb(color2)
        
        gradient = []
        for i in range(steps):
            factor = i / (steps - 1) if steps > 1 else 0
            r = int(rgb1[0] + (rgb2[0] - rgb1[0]) * factor)
            g = int(rgb1[1] + (rgb2[1] - rgb1[1]) * factor)
            b = int(rgb1[2] + (rgb2[2] - rgb1[2]) * factor)
            gradient.append(self._rgb_to_hex(r, g, b))
        
        return gradient
    
    def suggest_palette_for_data(self, data_type: str, mood: str = "professional") -> Dict:
        """
        Sugere uma paleta baseada no tipo de dados e mood
        
        data_type: financial, marketing, operations, sales, hr, tech
        mood: professional, creative, energetic, calm, modern
        """
        suggestions = {
            ("financial", "professional"): "corporate_blue",
            ("financial", "modern"): "modern_dark",
            ("marketing", "creative"): "vibrant_gradient",
            ("marketing", "energetic"): "sunset_warm",
            ("operations", "professional"): "minimal_light",
            ("sales", "energetic"): "tech_neon",
            ("hr", "calm"): "nature_earth",
            ("tech", "modern"): "modern_dark",
        }
        
        key = (data_type.lower(), mood.lower())
        palette_name = suggestions.get(key, "modern_dark")
        
        return self.get_preset_palette(palette_name)
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Converte HEX para RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _rgb_to_hex(self, r: int, g: int, b: int) -> str:
        """Converte RGB para HEX"""
        return f"#{r:02x}{g:02x}{b:02x}".upper()
    
    def _hsv_to_hex(self, h: float, s: float, v: float) -> str:
        """Converte HSV para HEX"""
        rgb = colorsys.hsv_to_rgb(h, s, v)
        r, g, b = [int(x * 255) for x in rgb]
        return self._rgb_to_hex(r, g, b)
    
    def get_contrast_color(self, hex_color: str) -> str:
        """Retorna preto ou branco baseado no contraste"""
        rgb = self._hex_to_rgb(hex_color)
        # Luminância relativa
        luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255
        return "#FFFFFF" if luminance < 0.5 else "#000000"
    
    def validate_accessibility(self, color1: str, color2: str) -> Dict[str, any]:
        """Valida contraste de cores para acessibilidade (WCAG)"""
        rgb1 = self._hex_to_rgb(color1)
        rgb2 = self._hex_to_rgb(color2)
        
        # Calcula luminância relativa
        def relative_luminance(rgb):
            rgb_norm = [c / 255 for c in rgb]
            rgb_linear = []
            for c in rgb_norm:
                if c <= 0.03928:
                    rgb_linear.append(c / 12.92)
                else:
                    rgb_linear.append(((c + 0.055) / 1.055) ** 2.4)
            return 0.2126 * rgb_linear[0] + 0.7152 * rgb_linear[1] + 0.0722 * rgb_linear[2]
        
        l1 = relative_luminance(rgb1)
        l2 = relative_luminance(rgb2)
        
        # Contraste
        contrast = (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)
        
        return {
            "contrast_ratio": round(contrast, 2),
            "wcag_aa_normal": contrast >= 4.5,
            "wcag_aa_large": contrast >= 3.0,
            "wcag_aaa_normal": contrast >= 7.0,
            "wcag_aaa_large": contrast >= 4.5,
            "rating": "Excelente" if contrast >= 7 else "Bom" if contrast >= 4.5 else "Regular" if contrast >= 3 else "Ruim"
        }
