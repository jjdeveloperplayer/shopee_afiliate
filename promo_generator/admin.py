from django.contrib import admin
from .models import ProductPromo


@admin.register(ProductPromo)
class ProductPromoAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'shop_name', 'price_min', 'commission_rate', 
                   'views', 'created_at']
    list_filter = ['created_at', 'shop_name']
    search_fields = ['product_name', 'shop_name', 'promo_text']
    readonly_fields = ['created_at', 'views']
    
    fieldsets = (
        ('Informações do Produto', {
            'fields': ('product_url', 'product_name', 'product_image_url', 
                      'shop_name', 'rating')
        }),
        ('Preços e Comissão', {
            'fields': ('price_min', 'price_max', 'commission_rate')
        }),
        ('Material Promocional', {
            'fields': ('promo_text', 'promo_image', 'affiliate_link')
        }),
        ('Estatísticas', {
            'fields': ('created_at', 'views')
        }),
    )
