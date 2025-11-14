"""
Serviços para integração com APIs externas (Shopee e Google Gemini)
"""
import hashlib
import hmac
import time
import re
import requests
from urllib.parse import urlparse, parse_qs
from django.conf import settings


class ShopeeAPIService:
    """Serviço para interagir com a API da Shopee Affiliate"""
    
    def __init__(self):
        self.api_url = settings.SHOPEE_API_URL
        self.affiliate_id = settings.SHOPEE_AFFILIATE_ID
        self.api_key = settings.SHOPEE_API_KEY

    def _generate_signature(self, timestamp, payload_str):
        """
        Gera assinatura SHA256 para autenticação
        Conforme documentação: SHA256(Credential + Timestamp + Payload + Secret)
        """
        # Monta o fator de assinatura: Credential + Timestamp + Payload + Secret
        signature_factor = f"{self.affiliate_id}{timestamp}{payload_str}{self.api_key}"

        # Calcula SHA256 (em lowercase hexadecimal)
        signature = hashlib.sha256(signature_factor.encode('utf-8')).hexdigest()

        return signature

    def _get_headers(self, payload_str, timestamp):
        """Gera headers de autenticação"""
        signature = self._generate_signature(timestamp, payload_str)

        # IMPORTANTE: A ordem é Credential, Timestamp, Signature (SEM ESPAÇOS após vírgulas)
        return {
            'Content-Type': 'application/json',
            'Authorization': f'SHA256 Credential={self.affiliate_id},Timestamp={timestamp},Signature={signature}'
        }

    def extract_product_ids_from_url(self, url):
        """
        Extrai shop_id e item_id de uma URL da Shopee
        Formato: https://shopee.com.br/product/{shop_id}/{item_id}
        """
        try:
            # Padrão para URL de produto
            pattern = r'shopee\.com\.br/.*?-i\.(\d+)\.(\d+)'
            match = re.search(pattern, url)

            if match:
                shop_id = int(match.group(1))
                item_id = int(match.group(2))
                return shop_id, item_id

            # Tenta outro formato
            parsed = urlparse(url)
            path_parts = parsed.path.split('/')

            if len(path_parts) >= 3:
                # Procura por números que parecem IDs
                for part in path_parts:
                    if part.isdigit() and len(part) > 5:
                        item_id = int(part)
                        return None, item_id

            return None, None
        except Exception as e:
            print(f"Erro ao extrair IDs: {e}")
            return None, None

    def get_product_info(self, shop_id=None, item_id=None, keyword=None):
        """
        Busca informações do produto na API da Shopee
        """
        try:
            # Query GraphQL para buscar produto
            if item_id:
                # Busca específica por item_id
                query = """query {
    productOfferV2(itemId: %d, page: 1, limit: 1) {
        nodes {
            itemId
            productName
            imageUrl
            priceMin
            priceMax
            commissionRate
            sellerCommissionRate
            shopeeCommissionRate
            shopName
            shopId
            ratingStar
            sales
            productLink
            offerLink
        }
    }
}""" % item_id
            elif keyword:
                # Busca por palavra-chave
                query = """query {
    productOfferV2(keyword: "%s", page: 1, limit: 1, sortType: 1) {
        nodes {
            itemId
            productName
            imageUrl
            priceMin
            priceMax
            commissionRate
            sellerCommissionRate
            shopeeCommissionRate
            shopName
            shopId
            ratingStar
            sales
            productLink
            offerLink
        }
    }
}""" % keyword
            else:
                return None

            # CRÍTICO: Remover quebras de linha MAS manter espaços
            # Substitui múltiplos espaços por um único espaço
            import re
            query_clean = re.sub(r'\s+', ' ', query).strip()
            payload_dict = {"query": query_clean}

            # Converter para string JSON
            import json
            payload_str = json.dumps(payload_dict, separators=(',', ':'))

            # Gerar timestamp
            timestamp = int(time.time())

            # Gerar headers com payload string
            headers = self._get_headers(payload_str, timestamp)

            # IMPORTANTE: Enviar como string, não como dict
            response = requests.post(self.api_url, data=payload_str, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Log para debug
            if 'errors' in data:
                print(f"Erro na API Shopee: {data}")
                return None

            if 'data' in data and 'productOfferV2' in data['data']:
                nodes = data['data']['productOfferV2'].get('nodes', [])
                if nodes:
                    return nodes[0]

            return None

        except Exception as e:
            print(f"Erro ao buscar produto: {e}")
            import traceback
            traceback.print_exc()
            return None

    def generate_affiliate_link(self, product_url, sub_ids=None):
        """
        Gera link de afiliado curto usando a API da Shopee
        """
        try:
            if sub_ids is None:
                # Usa apenas o primeiro sub_id, deixa os outros vazios mas não envia
                sub_ids = ["promo_generator"]

            # Remove strings vazias da lista
            sub_ids_clean = [sid for sid in sub_ids if sid and sid.strip()]

            # Se não tiver nenhum sub_id válido, usa um padrão
            if not sub_ids_clean:
                sub_ids_clean = ["promo"]

            # Limita a 5 sub_ids
            sub_ids_clean = sub_ids_clean[:5]

            # Monta a query com os sub_ids válidos
            sub_ids_str = ','.join([f'"{sid}"' for sid in sub_ids_clean])

            query = """mutation {
    generateShortLink(input: {
        originUrl: "%s",
        subIds: [%s]
    }) {
        shortLink
    }
}""" % (product_url, sub_ids_str)

            # CRÍTICO: Remover quebras de linha MAS manter espaços
            import re
            query_clean = re.sub(r'\s+', ' ', query).strip()
            payload_dict = {"query": query_clean}

            # Converter para string JSON
            import json
            payload_str = json.dumps(payload_dict, separators=(',', ':'))

            # Gerar timestamp
            timestamp = int(time.time())

            # Gerar headers
            headers = self._get_headers(payload_str, timestamp)

            # Enviar como string
            response = requests.post(self.api_url, data=payload_str, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Log para debug
            if 'errors' in data:
                print(f"Erro ao gerar link de afiliado: {data}")
                return None

            if 'data' in data and 'generateShortLink' in data['data']:
                return data['data']['generateShortLink'].get('shortLink')

            return None

        except Exception as e:
            print(f"Erro ao gerar link de afiliado: {e}")
            import traceback
            traceback.print_exc()
            return None


class GeminiAPIService:
    """Serviço para gerar texto promocional usando Google Gemini"""

    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY

    def generate_promo_text(self, product_info, product_description=None):
        """
        Gera texto promocional chamativo baseado nas informações do produto
        Envia a imagem do produto para o Gemini analisar e criar texto mais rico

        Args:
            product_info: Informações básicas do produto (da API Affiliate)
            product_description: Descrição detalhada do produto (da API pública) - opcional
        """
        try:
            # Tenta usar o SDK oficial primeiro
            try:
                from google import genai
                from google.genai import types

                # Configura o cliente com a API key
                client = genai.Client(api_key=self.api_key)

                product_name = product_info.get('productName', 'Produto')
                price_min = product_info.get('priceMin', '')
                price_max = product_info.get('priceMax', '')
                commission_rate = product_info.get('commissionRate', '0')
                shop_name = product_info.get('shopName', '')
                rating = product_info.get('ratingStar', '')
                sales = product_info.get('sales', 0)
                image_url = product_info.get('imageUrl', '')

                # Calcula desconto aproximado se tiver commission
                commission_percent = float(commission_rate) * 100 if commission_rate else 0

                # Baixa a imagem do produto com validação
                image_bytes = None
                mime_type = None
                if image_url:
                    try:
                        response = requests.get(image_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
                        if response.status_code == 200 and len(response.content) > 0:
                            # Detecta o tipo MIME da imagem
                            content_type = response.headers.get('content-type', '').lower()
                            if 'image/' in content_type:
                                mime_type = content_type
                            elif image_url.lower().endswith('.png'):
                                mime_type = 'image/png'
                            elif image_url.lower().endswith('.jpg') or image_url.lower().endswith('.jpeg'):
                                mime_type = 'image/jpeg'
                            elif image_url.lower().endswith('.webp'):
                                mime_type = 'image/webp'
                            else:
                                mime_type = 'image/jpeg'  # Fallback

                            # Valida tamanho (máx 20MB conforme docs)
                            if len(response.content) < 20 * 1024 * 1024:
                                image_bytes = response.content  # Guarda bytes direto, NÃO base64
                    except Exception as img_error:
                        print(f"Aviso: Não foi possível baixar a imagem: {img_error}")
                        pass

                # Adiciona descrição ao prompt se disponível
                description_section = ""
                if product_description:
                    # Limita a descrição a 800 caracteres para não sobrecarregar o prompt
                    desc_text = product_description[:800]
                    description_section = f"\n- Descrição do Produto: {desc_text}"

                # Monta o prompt para o Gemini
                prompt = f"""Analise esta imagem do produto e crie um texto promocional CHAMATIVO e PERSUASIVO para divulgar na Shopee:

INFORMAÇÕES DO PRODUTO:
- Nome: {product_name}
- Loja: {shop_name}
- Preço: R$ {price_min}{f' - R$ {price_max}' if price_max and price_max != price_min else ''}
- Avaliação: {rating} estrelas
- Vendas: {sales} unidades vendidas
- Comissão: {commission_percent:.1f}%{description_section}

INSTRUÇÕES:
1. OBSERVE A IMAGEM e descreva brevemente o que vê (cor, estilo, características visuais)
2. Use emojis estratégicos para chamar atenção
3. Destaque os benefícios VISUAIS e diferenciais do produto
4. Se houver descrição do produto, use-a para destacar características importantes
5. Crie senso de urgência (ofertas limitadas, estoque, etc)
6. Use linguagem informal e empolgante do Brasil
7. Inclua call-to-action forte
8. MÁXIMO 450 caracteres (seja direto e impactante)
9. NÃO invente características que não aparecem na imagem ou descrição
10. Foque em criar DESEJO de compra baseado no que VÊ e nas informações fornecidas

Gere APENAS o texto promocional, sem explicações extras."""

                # Prepara o conteúdo com ou sem imagem usando types.Part conforme documentação
                if image_bytes and mime_type:
                    # Envia com imagem usando types.Part.from_bytes() (método oficial)
                    try:
                        image_part = types.Part.from_bytes(
                            data=image_bytes,
                            mime_type=mime_type
                        )
                        contents = [prompt, image_part]
                    except Exception as img_error:
                        # Se falhar ao criar Part, usa só texto
                        contents = [prompt]
                        print(f"Aviso: Falha ao processar imagem: {img_error}, usando apenas texto")
                else:
                    # Envia só texto
                    contents = [prompt]
                    if image_url:
                        print("Aviso: Imagem não disponível, gerando texto sem análise visual")

                # Gera o conteúdo usando o SDK oficial com modelo que suporta visão
                response = client.models.generate_content(
                    model='gemini-2.5-flash',  # Suporta imagens
                    contents=contents
                )

                text = response.text.strip()[:500]
                return text

            except ImportError:
                # Fallback para API REST se SDK não estiver instalado
                return self._generate_with_rest_api(product_info, product_description)

        except Exception as e:
            print(f"Erro ao gerar texto com Gemini: {e}")
            import traceback
            traceback.print_exc()
            return self._generate_fallback_text(product_info)

    def _generate_with_rest_api(self, product_info, product_description=None):
        """Usa a API REST como fallback - com suporte a imagens"""
        try:
            import base64

            product_name = product_info.get('productName', 'Produto')
            price_min = product_info.get('priceMin', '')
            price_max = product_info.get('priceMax', '')
            rating = product_info.get('ratingStar', '')
            sales = product_info.get('sales', 0)
            image_url = product_info.get('imageUrl', '')

            # Baixa a imagem com validação
            image_data = None
            mime_type = None
            if image_url:
                try:
                    response = requests.get(image_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
                    if response.status_code == 200 and len(response.content) > 0:
                        # Detecta o tipo MIME da imagem
                        content_type = response.headers.get('content-type', '').lower()
                        if 'image/' in content_type:
                            mime_type = content_type
                        elif image_url.lower().endswith('.png'):
                            mime_type = 'image/png'
                        elif image_url.lower().endswith('.jpg') or image_url.lower().endswith('.jpeg'):
                            mime_type = 'image/jpeg'
                        elif image_url.lower().endswith('.webp'):
                            mime_type = 'image/webp'
                        else:
                            mime_type = 'image/jpeg'  # Fallback

                        # Valida tamanho (máx 4MB para o Gemini)
                        if len(response.content) < 4 * 1024 * 1024:
                            image_data = base64.b64encode(response.content).decode('utf-8')
                except Exception as img_error:
                    print(f"Aviso: Não foi possível baixar a imagem: {img_error}")
                    pass

            # Adiciona descrição ao prompt se disponível
            description_section = ""
            if product_description:
                # Limita a descrição a 800 caracteres para não sobrecarregar o prompt
                desc_text = product_description[:800]
                description_section = f"\n- Descrição do Produto: {desc_text}"

            prompt = f"""Analise esta imagem do produto e crie um texto promocional CHAMATIVO e PERSUASIVO para divulgar na Shopee:

INFORMAÇÕES DO PRODUTO:
- Nome: {product_name}
- Preço: R$ {price_min}{f' - R$ {price_max}' if price_max and price_max != price_min else ''}
- Avaliação: {rating} estrelas
- Vendas: {sales} unidades vendidas{description_section}

INSTRUÇÕES:
1. OBSERVE A IMAGEM e descreva brevemente o que vê (cor, estilo, características visuais)
2. Use emojis estratégicos para chamar atenção
3. Destaque os benefícios VISUAIS e diferenciais do produto
4. Se houver descrição do produto, use-a para destacar características importantes
5. Crie senso de urgência (ofertas limitadas, estoque, etc)
6. Use linguagem informal e empolgante do Brasil
7. Inclua call-to-action forte
8. MÁXIMO 450 caracteres (seja direto e impactante)
9. NÃO invente características que não aparecem na imagem ou descrição
10. Foque em criar DESEJO de compra baseado no que VÊ e nas informações fornecidas

Gere APENAS o texto promocional, sem explicações extras."""

            # URL atualizada da API v1
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash-exp:generateContent?key={self.api_key}"

            headers = {
                'Content-Type': 'application/json'
            }

            # Monta o payload com ou sem imagem
            if image_data and mime_type:
                try:
                    parts = [
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": image_data
                            }
                        },
                        {"text": prompt}
                    ]
                except:
                    # Se falhar, usa só texto
                    parts = [{"text": prompt}]
                    print("Aviso: Falha ao processar imagem, usando apenas texto")
            else:
                parts = [{"text": prompt}]
                if image_url:
                    print("Aviso: Imagem não disponível, gerando texto sem análise visual")

            payload = {
                "contents": [{
                    "parts": parts
                }],
                "generationConfig": {
                    "temperature": 0.9,
                    "maxOutputTokens": 300,
                    "topP": 0.95,
                }
            }

            response = requests.post(url, json=payload, headers=headers, timeout=20)
            response.raise_for_status()

            data = response.json()

            if 'candidates' in data and len(data['candidates']) > 0:
                text = data['candidates'][0]['content']['parts'][0]['text']
                return text.strip()[:500]

            return self._generate_fallback_text(product_info)

        except Exception as e:
            print(f"Erro ao gerar texto com API REST: {e}")
            import traceback
            traceback.print_exc()
            return self._generate_fallback_text(product_info)

    def _generate_fallback_text(self, product_info):
        """Gera um texto promocional simples caso a API falhe"""
        product_name = product_info.get('productName', 'Produto Incrível')
        price_min = product_info.get('priceMin', '0')
        rating = product_info.get('ratingStar', '5.0')

        return f"""🔥 OFERTA IMPERDÍVEL! 🔥

{product_name}

⭐ Avaliação {rating} estrelas
💰 A partir de R$ {price_min}
🚚 Entrega rápida e segura

✨ Aproveite essa oportunidade única!
👉 Clique no link e garanta o seu!

#Shopee #Oferta #Promoção"""