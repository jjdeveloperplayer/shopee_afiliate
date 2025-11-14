from django import forms


class ProductURLForm(forms.Form):
    """Formulário para inserir URL do produto"""
    
    product_url = forms.URLField(
        label='Link do Produto da Shopee',
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cole aqui o link do produto da Shopee...',
            'required': True
        }),
        help_text='Cole o link completo do produto da Shopee que você deseja promover'
    )
