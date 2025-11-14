# 🎉 SHOPEE PROMO GENERATOR - PROJETO COMPLETO

## 📦 O QUE FOI CRIADO

Uma aplicação Django completa que automatiza a criação de materiais promocionais para afiliados da Shopee, incluindo:

### ✨ Funcionalidades Principais

1. **Geração Automática de Imagens**
   - Design profissional e atrativo
   - Cores da marca Shopee (laranja vibrante)
   - Informações do produto destacadas
   - Formato otimizado para redes sociais (1080x1080px)

2. **Texto Promocional com IA**
   - Usa Google Gemini (GRATUITO!)
   - Textos persuasivos e chamativos
   - Limitado a 500 caracteres
   - Personalizável após geração

3. **Integração com API Shopee**
   - Busca automática de informações do produto
   - Preços, avaliações, comissões
   - Geração de links de afiliado curtos
   - Suporte para múltiplos formatos de URL

4. **Interface Moderna**
   - Design responsivo (mobile-friendly)
   - Bootstrap 5
   - Ícones Font Awesome
   - Cópia com um clique
   - Download direto das imagens

---

## 🚀 COMO USAR

### Opção 1: Uso Completo (COM APIs configuradas)

1. **Instale as dependências**
```bash
cd shopee_promo
pip install -r requirements.txt
```

2. **Configure o arquivo .env**
```bash
cp .env.example .env
```

Edite `.env` e adicione:
```
# OBRIGATÓRIO (Gratuito)
GEMINI_API_KEY=sua_chave_aqui

# OPCIONAL (mas recomendado)
SHOPEE_AFFILIATE_ID=seu_id_aqui
SHOPEE_API_KEY=sua_key_aqui
```

**Como obter as chaves:**

🤖 **Google Gemini (GRÁTIS):**
- Acesse: https://makersuite.google.com/app/apikey
- Faça login com Google
- Clique em "Create API Key"
- Copie e cole no .env

🛍️ **Shopee Affiliate:**
- Acesse: https://open.shopee.com.br/
- Registre-se como afiliado
- Crie uma aplicação
- Copie as credenciais

3. **Prepare o banco de dados**
```bash
python manage.py migrate
python manage.py createsuperuser  # Opcional
```

4. **Execute o servidor**
```bash
python manage.py runserver
```

5. **Acesse a aplicação**
http://127.0.0.1:8000

---

### Opção 2: Demonstração Rápida (SEM APIs)

Quer apenas testar a interface? Sem problemas!

```bash
cd shopee_promo
pip install -r requirements.txt
python manage.py migrate
python manage.py create_demo_promos  # Cria exemplos
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/list/

Você verá promoções de exemplo já criadas!

---

## 📂 ESTRUTURA DO PROJETO

```
shopee_promo/
│
├── 📄 README.md              # Documentação completa
├── 📄 QUICKSTART.md          # Guia de início rápido
├── 📄 requirements.txt       # Dependências Python
├── 📄 .env.example           # Exemplo de variáveis de ambiente
├── 📄 .gitignore            # Arquivos ignorados pelo Git
├── 📄 manage.py             # Gerenciador Django
├── 📄 test_app.py           # Script de testes
│
├── shopee_promo/            # Configurações do projeto
│   ├── settings.py          # Configurações Django
│   ├── urls.py              # URLs principais
│   ├── wsgi.py              # WSGI para produção
│   └── asgi.py              # ASGI para async
│
└── promo_generator/         # App principal
    ├── models.py            # Modelo de dados (ProductPromo)
    ├── views.py             # Lógica das views
    ├── forms.py             # Formulário de URL
    ├── urls.py              # URLs do app
    ├── admin.py             # Interface admin
    ├── services.py          # Integração APIs (Shopee + Gemini)
    ├── image_utils.py       # Geração de imagens
    │
    ├── templates/           # Templates HTML
    │   └── promo_generator/
    │       ├── base.html
    │       ├── home.html
    │       ├── promo_detail.html
    │       └── promo_list.html
    │
    └── management/commands/ # Comandos personalizados
        └── create_demo_promos.py
```

---

## 🎯 FLUXO DE USO DA APLICAÇÃO

1. **Usuário cola link do produto Shopee**
   ↓
2. **Sistema extrai IDs do produto**
   ↓
3. **Busca informações via API Shopee**
   - Nome, preço, loja, avaliação
   - Taxa de comissão
   ↓
4. **Gera imagem promocional**
   - Design automático com PIL/Pillow
   - Logo/badges/destaques
   ↓
5. **Gera texto com IA (Gemini)**
   - Texto persuasivo
   - Emojis estratégicos
   - Call-to-action
   ↓
6. **Gera link de afiliado**
   - Link curto da Shopee
   - Rastreável
   ↓
7. **Exibe resultado**
   - Imagem para download
   - Texto para copiar
   - Link de afiliado
   - Botões de compartilhamento social

---

## 🔧 TECNOLOGIAS USADAS

- **Backend:** Django 4.2
- **Processamento de Imagens:** Pillow
- **IA de Texto:** Google Gemini API (gratuito)
- **API de Produtos:** Shopee Affiliate API
- **Frontend:** Bootstrap 5 + Font Awesome
- **Banco de Dados:** SQLite (desenvolvimento) / PostgreSQL (produção)

---

## 💡 DICAS PARA MAXIMIZAR RESULTADOS

### Para Afiliados:

1. **Escolha produtos populares**
   - Alta avaliação (4.5+)
   - Muitas vendas
   - Boa comissão

2. **Personalize o texto**
   - A IA gera uma base
   - Você pode editar antes de copiar
   - Adapte para seu público

3. **Teste horários diferentes**
   - Manhã: 8h-10h
   - Almoço: 12h-14h
   - Noite: 19h-21h

4. **Use múltiplas redes**
   - WhatsApp Status
   - Instagram Stories
   - Facebook
   - Twitter/X
   - Telegram

5. **Acompanhe métricas**
   - Use o sistema de visualizações
   - Teste produtos diferentes
   - Veja o que converte mais

### Para Desenvolvedores:

1. **Personalize o design**
   - Edite `image_utils.py`
   - Mude cores, fontes, layout

2. **Ajuste os prompts da IA**
   - Edite `services.py`
   - Mude o estilo do texto gerado

3. **Adicione features**
   - Sistema de agendamento
   - Analytics avançado
   - Integração com mais redes sociais

---

## 🐛 RESOLUÇÃO DE PROBLEMAS

### "ImportError: No module named PIL"
```bash
pip install Pillow
```

### "GEMINI_API_KEY não configurada"
- Configure no arquivo .env
- Obtenha gratuitamente em: https://makersuite.google.com/app/apikey

### "Produto não encontrado"
- Verifique se o link está correto
- Teste com outro produto
- Confirme se tem API Shopee configurada

### "Erro ao gerar imagem"
No Linux, instale:
```bash
sudo apt-get install python3-dev python3-pillow libjpeg-dev zlib1g-dev
```

### "Template não encontrado"
```bash
python manage.py collectstatic
```

---

## 🚀 DEPLOY EM PRODUÇÃO

### Heroku

```bash
# Instalar Heroku CLI e fazer login
heroku create seu-app-nome

# Configurar variáveis
heroku config:set GEMINI_API_KEY=sua_chave
heroku config:set SHOPEE_AFFILIATE_ID=seu_id
heroku config:set SHOPEE_API_KEY=sua_key

# Deploy
git push heroku main
heroku run python manage.py migrate
```

### PythonAnywhere / DigitalOcean / AWS

1. Configure um servidor com Python 3.8+
2. Instale as dependências
3. Configure nginx + gunicorn
4. Use PostgreSQL em produção
5. Configure variáveis de ambiente
6. Execute migrations
7. Collectstatic para arquivos estáticos

---

## 📊 MÉTRICAS E ANALYTICS

A aplicação já rastreia:
- Número de visualizações por promoção
- Data de criação
- Produtos mais promovidos

Para analytics avançado, considere integrar:
- Google Analytics
- Hotjar
- Mixpanel

---

## 🤝 CONTRIBUINDO

Melhorias bem-vindas:

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/MinhaFeature`
3. Commit: `git commit -m 'Add MinhaFeature'`
4. Push: `git push origin feature/MinhaFeature`
5. Abra um Pull Request

---

## 📄 LICENÇA

Este projeto está sob a licença MIT. Você pode:
- ✅ Usar comercialmente
- ✅ Modificar
- ✅ Distribuir
- ✅ Uso privado

---

## 🎓 APRENDIZADOS DO PROJETO

Este projeto demonstra:
- Integração com APIs RESTful (Shopee)
- Uso de IA generativa (Gemini)
- Processamento de imagens com Python
- Arquitetura MVC com Django
- Design responsivo
- UX/UI focado em conversão

---

## 📞 SUPORTE

Problemas ou dúvidas?

1. Leia o README.md
2. Execute `python test_app.py`
3. Verifique os logs
4. Abra uma issue no GitHub

---

## 🎉 SUCESSO!

Você agora tem uma ferramenta completa para turbinar suas vendas como afiliado Shopee!

**Próximos passos:**
1. Configure as APIs
2. Teste com produtos reais
3. Compartilhe suas promoções
4. Acompanhe os resultados
5. Otimize e lucre! 💰

---

**Desenvolvido com ❤️ para afiliados Shopee**
**Powered by Django + Google Gemini AI**
