from django.db import models
from django.utils import timezone


class ProductPromo(models.Model):
    """Model para armazenar promoções geradas"""
    
    product_url = models.URLField(verbose_name="URL do Produto")
    product_name = models.CharField(max_length=500, verbose_name="Nome do Produto")
    product_image_url = models.URLField(verbose_name="URL da Imagem Original")
    
    # Informações do produto
    price_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    commission_rate = models.CharField(max_length=20, null=True, blank=True)
    shop_name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.CharField(max_length=10, null=True, blank=True)
    
    # Conteúdo gerado
    promo_text = models.TextField(verbose_name="Texto Promocional", max_length=500)
    promo_image = models.ImageField(upload_to='promos/', verbose_name="Imagem Gerada")
    
    # Link de afiliado
    affiliate_link = models.URLField(verbose_name="Link de Afiliado", blank=True)
    
    # Metadados
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Criado em")
    views = models.IntegerField(default=0, verbose_name="Visualizações")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Promoção de Produto"
        verbose_name_plural = "Promoções de Produtos"
    
    def __str__(self):
        return f"{self.product_name[:50]} - {self.created_at.strftime('%d/%m/%Y')}"
