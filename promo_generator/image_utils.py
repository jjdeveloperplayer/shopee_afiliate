"""
Utilitários para geração de imagens promocionais
"""
import io
import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from django.core.files.base import ContentFile


class PromoImageGenerator:
    """Gerador de imagens promocionais atrativas"""
    
    def __init__(self):
        self.output_size = (1080, 1080)  # Formato quadrado para redes sociais
        self.background_color = (255, 250, 245)  # Cor suave de fundo
        self.accent_color = (255, 87, 34)  # Laranja vibrante (cor da Shopee)
    
    def download_image(self, url):
        """Baixa imagem de uma URL"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return Image.open(io.BytesIO(response.content))
        except Exception as e:
            print(f"Erro ao baixar imagem: {e}")
            return None
    
    def create_gradient_background(self, size, color1, color2):
        """Cria um fundo com gradiente"""
        base = Image.new('RGB', size, color1)
        top = Image.new('RGB', size, color2)
        mask = Image.new('L', size)
        mask_data = []
        
        for y in range(size[1]):
            alpha = int(255 * (y / size[1]))
            mask_data.extend([alpha] * size[0])
        
        mask.putdata(mask_data)
        base.paste(top, (0, 0), mask)
        return base
    
    def add_shadow(self, image):
        """Adiciona sombra suave à imagem"""
        shadow = Image.new('RGBA', 
                          (image.width + 20, image.height + 20), 
                          (0, 0, 0, 0))
        
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.ellipse([10, 10, image.width + 10, image.height + 10], 
                           fill=(0, 0, 0, 40))
        
        shadow = shadow.filter(ImageFilter.GaussianBlur(10))
        shadow.paste(image, (10, 10), image if image.mode == 'RGBA' else None)
        
        return shadow
    
    def create_promo_image(self, product_image_url, product_name, price_min=None, 
                          commission_rate=None, rating=None):
        """
        Cria imagem promocional completa
        """
        try:
            # Baixa imagem do produto
            product_img = self.download_image(product_image_url)
            
            if not product_img:
                # Cria imagem placeholder se download falhar
                product_img = Image.new('RGB', (800, 800), (200, 200, 200))
                draw = ImageDraw.Draw(product_img)
                draw.text((400, 400), "Imagem\nIndisponível", 
                         fill=(100, 100, 100), anchor="mm")
            
            # Cria canvas principal com gradiente
            canvas = self.create_gradient_background(
                self.output_size,
                (255, 245, 240),  # Pêssego claro
                (255, 255, 255)   # Branco
            )
            
            draw = ImageDraw.Draw(canvas)
            
            # Adiciona borda decorativa laranja (cor Shopee)
            border_width = 15
            draw.rectangle([0, 0, self.output_size[0], border_width], 
                          fill=self.accent_color)
            draw.rectangle([0, self.output_size[1] - border_width, 
                          self.output_size[0], self.output_size[1]], 
                          fill=self.accent_color)
            
            # Prepara imagem do produto
            product_img = product_img.convert('RGB')
            
            # Redimensiona mantendo proporção
            max_product_size = 700
            product_img.thumbnail((max_product_size, max_product_size), 
                                 Image.Resampling.LANCZOS)
            
            # Centraliza a imagem do produto na parte superior
            product_x = (self.output_size[0] - product_img.width) // 2
            product_y = 80
            
            # Adiciona a imagem do produto
            canvas.paste(product_img, (product_x, product_y))
            
            # Adiciona retângulo branco semi-transparente para informações
            info_height = 250
            info_y = self.output_size[1] - info_height - 30
            
            # Desenha retângulo com cantos arredondados para as informações
            info_box = Image.new('RGBA', (self.output_size[0] - 80, info_height), 
                               (255, 255, 255, 240))
            canvas.paste(info_box, (40, info_y), info_box)
            
            # Desenha borda no retângulo de informações
            draw.rectangle([40, info_y, 
                          self.output_size[0] - 40, 
                          info_y + info_height],
                         outline=self.accent_color, width=3)
            
            # Adiciona textos com fonte padrão
            # Badge "OFERTA" no topo
            badge_size = (200, 60)
            badge_x = (self.output_size[0] - badge_size[0]) // 2
            badge_y = 15
            
            # Desenha badge
            draw.ellipse([badge_x, badge_y, 
                         badge_x + badge_size[0], 
                         badge_y + badge_size[1]], 
                        fill=(255, 215, 0))  # Dourado
            draw.ellipse([badge_x, badge_y, 
                         badge_x + badge_size[0], 
                         badge_y + badge_size[1]], 
                        outline=self.accent_color, width=3)
            
            # Texto do badge
            try:
                font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
                font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
                font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
                font_tiny = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
            except:
                font_large = font_medium = font_small = font_tiny = ImageFont.load_default()
            
            draw.text((badge_x + badge_size[0]//2, badge_y + badge_size[1]//2), 
                     "🔥 OFERTA 🔥", 
                     fill=(255, 87, 34), 
                     font=font_large,
                     anchor="mm")
            
            # Informações no retângulo inferior
            text_y = info_y + 20
            
            # Nome do produto (truncado se necessário)
            product_name_display = product_name[:60] + "..." if len(product_name) > 60 else product_name
            draw.text((self.output_size[0]//2, text_y + 20), 
                     product_name_display,
                     fill=(0, 0, 0),
                     font=font_small,
                     anchor="mt")
            
            # Preço
            if price_min:
                text_y += 80
                draw.text((self.output_size[0]//2, text_y), 
                         f"💰 R$ {price_min}",
                         fill=self.accent_color,
                         font=font_medium,
                         anchor="mm")
            
            # Avaliação e Comissão
            text_y += 60
            info_parts = []
            
            if rating:
                info_parts.append(f"⭐ {rating}")
            
            if commission_rate:
                commission_percent = float(commission_rate) * 100
                info_parts.append(f"💵 {commission_percent:.1f}% comissão")
            
            if info_parts:
                info_text = " | ".join(info_parts)
                draw.text((self.output_size[0]//2, text_y), 
                         info_text,
                         fill=(80, 80, 80),
                         font=font_tiny,
                         anchor="mm")
            
            # Call-to-action
            text_y += 50
            draw.text((self.output_size[0]//2, text_y), 
                     "👆 CLIQUE E COMPRE AGORA! 👆",
                     fill=self.accent_color,
                     font=font_small,
                     anchor="mm")
            
            return canvas
            
        except Exception as e:
            print(f"Erro ao criar imagem promocional: {e}")
            # Retorna imagem de erro
            error_img = Image.new('RGB', self.output_size, (255, 200, 200))
            draw = ImageDraw.Draw(error_img)
            draw.text((self.output_size[0]//2, self.output_size[1]//2),
                     "Erro ao gerar imagem",
                     fill=(200, 0, 0),
                     anchor="mm")
            return error_img
    
    def save_to_content_file(self, pil_image, filename="promo.jpg"):
        """Converte PIL Image para Django ContentFile"""
        buffer = io.BytesIO()
        pil_image.save(buffer, format='JPEG', quality=95)
        buffer.seek(0)
        return ContentFile(buffer.read(), name=filename)
