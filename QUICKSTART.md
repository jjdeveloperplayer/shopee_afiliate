# 🚀 GUIA DE INÍCIO RÁPIDO

## Passos para começar em 5 minutos:

### 1️⃣ Instale as dependências
```bash
cd shopee_promo
pip install -r requirements.txt
```

### 2️⃣ Configure as APIs (IMPORTANTE!)

#### 🔑 API do Google Gemini (GRÁTIS e OBRIGATÓRIA)
1. Acesse: https://makersuite.google.com/app/apikey
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave

#### 🛍️ API da Shopee (Opcional para testes)
1. Acesse: https://open.shopee.com.br/
2. Crie uma aplicação
3. Copie o Affiliate ID e API Key

#### 📝 Crie o arquivo .env
```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione pelo menos o Gemini:
```
GEMINI_API_KEY=sua_chave_aqui
```

### 3️⃣ Configure o banco de dados
```bash
python manage.py migrate
```

### 4️⃣ Execute o servidor
```bash
python manage.py runserver
```

### 5️⃣ Acesse a aplicação
Abra no navegador: http://127.0.0.1:8000

---

## 🎯 Como usar SEM a API da Shopee (para testes)

Se você não tiver acesso à API da Shopee ainda, a aplicação funcionará com funcionalidade limitada:

- ✅ Você pode gerar textos promocionais com IA
- ✅ Você pode criar imagens promocionais
- ⚠️ Não poderá buscar produtos automaticamente da Shopee
- ⚠️ Não poderá gerar links de afiliado curtos

**Solução temporária:** Use as informações manualmente:
1. Copie o link do produto da Shopee
2. A aplicação tentará extrair informações básicas
3. Você pode complementar os dados manualmente no admin

---

## 🆘 Problemas comuns

### "No module named 'PIL'"
```bash
pip install Pillow
```

### "API key inválida"
- Verifique se copiou a chave corretamente
- Certifique-se de que não há espaços extras
- Confirme que está usando o arquivo .env correto

### "Produto não encontrado"
- Verifique se o link da Shopee está correto
- Confirme que o produto é elegível para afiliados
- Tente com outro produto

---

## 💡 Dica profissional

Para obter os melhores resultados:

1. **Configure PELO MENOS o Gemini API** (é grátis!)
2. Cole links de produtos populares da Shopee
3. Edite o texto gerado se necessário
4. Baixe a imagem e compartilhe nas redes sociais
5. Use seu link de afiliado para rastrear vendas

---

## 📞 Precisa de ajuda?

- Leia o README.md completo
- Execute `python test_app.py` para diagnosticar problemas
- Verifique os logs de erro no terminal

Boas vendas! 🚀💰
