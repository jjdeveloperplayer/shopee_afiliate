from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import ProductPromo
from .services import ShopeeAPIService, GeminiAPIService
from .image_utils import PromoImageGenerator
from .forms import ProductURLForm


def home(request):
    """Página inicial com formulário"""
    if request.method == 'POST':
        form = ProductURLForm(request.POST)
        
        if form.is_valid():
            product_url = form.cleaned_data['product_url']
            
            try:
                # Inicializa serviços
                shopee_service = ShopeeAPIService()
                
                # Extrai IDs da URL
                shop_id, item_id = shopee_service.extract_product_ids_from_url(product_url)
                
                if not item_id:
                    messages.error(request, 
                                 "Não foi possível identificar o produto. "
                                 "Verifique se a URL está correta.")
                    return render(request, 'promo_generator/home.html', {'form': form})
                
                # Busca informações do produto
                product_info = shopee_service.get_product_info(
                    shop_id=shop_id,
                    item_id=item_id
                )

                if not product_info:
                    messages.error(request,
                                 "Produto não encontrado ou não disponível para afiliados.")
                    return render(request, 'promo_generator/home.html', {'form': form})

                # Gera texto promocional com Gemini
                gemini_service = GeminiAPIService()
                promo_text = gemini_service.generate_promo_text(product_info)
                
                # Gera imagem promocional
                image_generator = PromoImageGenerator()
                promo_image = image_generator.create_promo_image(
                    product_image_url=product_info.get('imageUrl', ''),
                    product_name=product_info.get('productName', ''),
                    price_min=product_info.get('priceMin'),
                    commission_rate=product_info.get('commissionRate'),
                    rating=product_info.get('ratingStar')
                )
                
                # Gera link de afiliado
                affiliate_link = shopee_service.generate_affiliate_link(
                    product_info.get('productLink', product_url)
                ) or product_info.get('offerLink', product_url)
                
                # Salva no banco de dados
                promo = ProductPromo.objects.create(
                    product_url=product_url,
                    product_name=product_info.get('productName', 'Produto'),
                    product_image_url=product_info.get('imageUrl', ''),
                    price_min=product_info.get('priceMin'),
                    price_max=product_info.get('priceMax'),
                    commission_rate=product_info.get('commissionRate'),
                    shop_name=product_info.get('shopName'),
                    rating=product_info.get('ratingStar'),
                    promo_text=promo_text,
                    affiliate_link=affiliate_link
                )
                
                # Salva a imagem gerada
                image_file = image_generator.save_to_content_file(
                    promo_image,
                    filename=f'promo_{promo.id}.jpg'
                )
                promo.promo_image.save(f'promo_{promo.id}.jpg', image_file, save=True)
                
                messages.success(request, 'Material promocional gerado com sucesso! 🎉')
                return redirect('promo_detail', promo_id=promo.id)
                
            except Exception as e:
                messages.error(request, f'Erro ao processar: {str(e)}')
                return render(request, 'promo_generator/home.html', {'form': form})
    else:
        form = ProductURLForm()
    
    # Mostra últimas promoções geradas
    recent_promos = ProductPromo.objects.all()[:6]
    
    context = {
        'form': form,
        'recent_promos': recent_promos
    }
    
    return render(request, 'promo_generator/home.html', context)


def promo_detail(request, promo_id):
    """Página de detalhes da promoção gerada"""
    promo = get_object_or_404(ProductPromo, id=promo_id)
    
    # Incrementa contador de visualizações
    promo.views += 1
    promo.save(update_fields=['views'])
    
    context = {
        'promo': promo
    }
    
    return render(request, 'promo_generator/promo_detail.html', context)


def promo_list(request):
    """Lista todas as promoções geradas"""
    promos = ProductPromo.objects.all()
    
    context = {
        'promos': promos
    }
    
    return render(request, 'promo_generator/promo_list.html', context)


def api_test(request):
    """View para testar as APIs (desenvolvimento)"""
    results = {
        'shopee_configured': bool(ShopeeAPIService().api_key),
        'gemini_configured': bool(GeminiAPIService().api_key),
    }
    
    return JsonResponse(results)
