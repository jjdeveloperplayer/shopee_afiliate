from django.core.management.base import BaseCommand
from promo_generator.models import ProductPromo
from promo_generator.image_utils import PromoImageGenerator
import random


class Command(BaseCommand):
    help = 'Popula o banco de dados com promoções de exemplo para demonstração'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Criando promoções de exemplo...'))
        
        # Exemplos de produtos
        sample_products = [
            {
                'product_url': 'https://shopee.com.br/produto-exemplo-1',
                'product_name': 'Fone de Ouvido Bluetooth Premium com Cancelamento de Ruído',
                'price_min': '89.90',
                'price_max': '99.90',
                'commission_rate': '0.08',
                'shop_name': 'TechStore Brasil',
                'rating': '4.9',
                'promo_text': '''🎧 SUPER OFERTA! Fone Bluetooth Premium! 🎧

✨ Cancelamento de ruído ativo
🔋 40h de bateria
🎵 Som de alta qualidade
💎 Design premium

⭐ 4.9 estrelas - Clientes adoram!
💰 De R$ 99,90 por apenas R$ 89,90

🚚 FRETE GRÁTIS + Entrega Rápida!
👉 Aproveite antes que acabe!

#Fone #Bluetooth #Oferta #Shopee''',
            },
            {
                'product_url': 'https://shopee.com.br/produto-exemplo-2',
                'product_name': 'Smartwatch Fitness com Monitor Cardíaco',
                'price_min': '149.90',
                'price_max': '179.90',
                'commission_rate': '0.10',
                'shop_name': 'Gadgets & Cia',
                'rating': '4.7',
                'promo_text': '''⌚ IMPERDÍVEL! Smartwatch Fitness! ⌚

💪 Monitor cardíaco 24h
🏃 Rastreamento de exercícios
📱 Notificações do celular
🔋 7 dias de bateria

⭐ Avaliação 4.7 - Muito bem avaliado!
💰 A partir de R$ 149,90

🎁 BÔNUS: Pulseira extra grátis!
👆 Clique e garanta o seu agora!

#Smartwatch #Fitness #Saúde #Tecnologia''',
            },
            {
                'product_url': 'https://shopee.com.br/produto-exemplo-3',
                'product_name': 'Kit 3 Camisetas Premium 100% Algodão',
                'price_min': '59.90',
                'price_max': '79.90',
                'commission_rate': '0.12',
                'shop_name': 'Moda & Estilo',
                'rating': '4.8',
                'promo_text': '''👕 PROMOÇÃO RELÂMPAGO! Kit 3 Camisetas! 👕

✅ 100% Algodão premium
✅ Conforto incomparável
✅ Não desbota, não encolhe
✅ Várias cores disponíveis

⭐ 4.8 estrelas - Qualidade garantida!
💰 3 camisetas por R$ 59,90

🔥 APENAS HOJE com 25% OFF!
💨 Corre que está acabando!

#Moda #Camiseta #Oferta #Estilo''',
            },
        ]
        
        generator = PromoImageGenerator()
        
        for product_data in sample_products:
            try:
                # Gera imagem de exemplo
                promo_image = generator.create_promo_image(
                    product_image_url='https://via.placeholder.com/800',
                    product_name=product_data['product_name'],
                    price_min=product_data['price_min'],
                    commission_rate=product_data['commission_rate'],
                    rating=product_data['rating']
                )
                
                # Cria a promoção
                promo = ProductPromo.objects.create(
                    product_url=product_data['product_url'],
                    product_name=product_data['product_name'],
                    product_image_url='https://via.placeholder.com/800',
                    price_min=product_data['price_min'],
                    price_max=product_data.get('price_max'),
                    commission_rate=product_data['commission_rate'],
                    shop_name=product_data['shop_name'],
                    rating=product_data['rating'],
                    promo_text=product_data['promo_text'],
                    affiliate_link=product_data['product_url'],
                    views=random.randint(10, 150)
                )
                
                # Salva a imagem
                image_file = generator.save_to_content_file(
                    promo_image,
                    filename=f'demo_promo_{promo.id}.jpg'
                )
                promo.promo_image.save(f'demo_promo_{promo.id}.jpg', image_file, save=True)
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Criada: {product_data["product_name"][:50]}...')
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Erro ao criar {product_data["product_name"]}: {e}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 {len(sample_products)} promoções de exemplo criadas com sucesso!')
        )
        self.stdout.write(
            self.style.WARNING('\n💡 Acesse http://127.0.0.1:8000 para ver as promoções')
        )
