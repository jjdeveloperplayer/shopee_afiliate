#!/usr/bin/env python
"""
Script para testar as funcionalidades principais da aplicação
"""
import os
import django

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopee_promo.settings')
django.setup()

from promo_generator.services import ShopeeAPIService, GeminiAPIService
from promo_generator.image_utils import PromoImageGenerator


def test_url_extraction():
    """Testa a extração de IDs de URLs da Shopee"""
    print("=" * 60)
    print("TESTE 1: Extração de IDs de URLs")
    print("=" * 60)
    
    shopee = ShopeeAPIService()
    
    # URLs de exemplo
    test_urls = [
        "https://shopee.com.br/Smartphone-i.123456.789012345",
        "https://shopee.com.br/product/123456/789012345",
    ]
    
    for url in test_urls:
        shop_id, item_id = shopee.extract_product_ids_from_url(url)
        print(f"\nURL: {url}")
        print(f"Shop ID: {shop_id}")
        print(f"Item ID: {item_id}")
    
    print("\n✅ Teste de extração concluído!\n")


def test_api_configuration():
    """Testa se as APIs estão configuradas"""
    print("=" * 60)
    print("TESTE 2: Configuração das APIs")
    print("=" * 60)
    
    shopee = ShopeeAPIService()
    gemini = GeminiAPIService()
    
    print(f"\n🔑 API Shopee configurada: {'✅ Sim' if shopee.api_key else '❌ Não'}")
    print(f"🤖 API Gemini configurada: {'✅ Sim' if gemini.api_key else '❌ Não'}")
    
    if not shopee.api_key:
        print("\n⚠️  Configure SHOPEE_API_KEY no arquivo .env")
    
    if not gemini.api_key:
        print("⚠️  Configure GEMINI_API_KEY no arquivo .env")
        print("   Obtenha gratuitamente em: https://makersuite.google.com/app/apikey")
    
    print()


def test_image_generation():
    """Testa a geração de imagens"""
    print("=" * 60)
    print("TESTE 3: Geração de Imagens")
    print("=" * 60)
    
    generator = PromoImageGenerator()
    
    # Dados de exemplo
    product_info = {
        'productName': 'Smartphone XYZ 128GB',
        'priceMin': '1299.90',
        'rating': '4.8',
        'commissionRate': '0.05'
    }
    
    print("\n🎨 Gerando imagem de teste...")
    
    try:
        # Gera imagem com URL de placeholder
        image = generator.create_promo_image(
            product_image_url="https://via.placeholder.com/800",
            product_name=product_info['productName'],
            price_min=product_info['priceMin'],
            commission_rate=product_info['commissionRate'],
            rating=product_info['rating']
        )
        
        # Salva imagem de teste
        image.save('/tmp/test_promo.jpg', 'JPEG', quality=95)
        print("✅ Imagem gerada com sucesso!")
        print("📁 Salva em: /tmp/test_promo.jpg")
        
    except Exception as e:
        print(f"❌ Erro ao gerar imagem: {e}")
    
    print()


def test_gemini_text_generation():
    """Testa a geração de texto com Gemini"""
    print("=" * 60)
    print("TESTE 4: Geração de Texto com IA")
    print("=" * 60)
    
    gemini = GeminiAPIService()
    
    if not gemini.api_key:
        print("\n⚠️  API Gemini não configurada. Pulando teste...")
        print("   Configure GEMINI_API_KEY no .env para testar")
        print()
        return
    
    product_info = {
        'productName': 'Fone de Ouvido Bluetooth Premium',
        'priceMin': '89.90',
        'priceMax': '99.90',
        'shopName': 'TechStore',
        'rating': '4.9',
        'sales': 1500,
        'commissionRate': '0.08'
    }
    
    print("\n🤖 Gerando texto promocional...")
    
    try:
        text = gemini.generate_promo_text(product_info)
        print("\n" + "="*60)
        print("TEXTO GERADO:")
        print("="*60)
        print(text)
        print("="*60)
        print(f"\n✅ Texto gerado com sucesso! ({len(text)} caracteres)")
        
    except Exception as e:
        print(f"❌ Erro ao gerar texto: {e}")
        print("💡 Verifique se a API Key está correta")
    
    print()


def main():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("TESTE DA APLICAÇÃO SHOPEE PROMO GENERATOR")
    print("="*60 + "\n")
    
    try:
        test_url_extraction()
        test_api_configuration()
        test_image_generation()
        test_gemini_text_generation()
        
        print("="*60)
        print("TESTES CONCLUÍDOS!")
        print("="*60)
        print("\n💡 Próximos passos:")
        print("1. Configure as APIs no arquivo .env")
        print("2. Execute: python manage.py runserver")
        print("3. Acesse: http://127.0.0.1:8000")
        print()
        
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
