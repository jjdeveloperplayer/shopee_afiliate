#!/usr/bin/env python
"""
Script de teste para verificar se o generate_affiliate_link está funcionando
"""
import os
import django

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopee_promo.settings')
django.setup()

from promo_generator.services import ShopeeAPIService


def test_affiliate_link():
    """Testa a geração de link de afiliado"""
    print("=" * 80)
    print("TESTE: Geração de Link de Afiliado")
    print("=" * 80)

    # URL de exemplo
    product_url = "https://shopee.com.br/product/1081365967/20297519409"

    print(f"\n1. URL do produto: {product_url}")

    shopee_service = ShopeeAPIService()

    # Testa com sub_ids padrão
    print("\n2. Testando geração de link de afiliado...")
    print("   Sub IDs: ['promo', '', '', '', ''] (padrão)")

    affiliate_link = shopee_service.generate_affiliate_link(product_url)

    if affiliate_link:
        print("\n✅ Link de afiliado gerado com sucesso!")
        print(f"   Link: {affiliate_link}")
    else:
        print("\n❌ Falha ao gerar link de afiliado")

    # Testa com sub_ids personalizados
    print("\n3. Testando com sub_ids personalizados...")
    custom_sub_ids = ["teste", "afiliado", "123", "", ""]
    print(f"   Sub IDs: {custom_sub_ids}")

    affiliate_link2 = shopee_service.generate_affiliate_link(
        product_url,
        sub_ids=custom_sub_ids
    )

    if affiliate_link2:
        print("\n✅ Link de afiliado gerado com sucesso!")
        print(f"   Link: {affiliate_link2}")
    else:
        print("\n❌ Falha ao gerar link de afiliado")

    print("\n" + "=" * 80)
    print("Teste concluído!")
    print("=" * 80)


if __name__ == '__main__':
    test_affiliate_link()