# 🚀 Shopee Promo Generator

Aplicação Django para gerar automaticamente materiais promocionais para afiliados da Shopee.

## 📋 Funcionalidades

- ✅ Extração automática de informações de produtos via API da Shopee
- ✅ Geração de imagens promocionais atrativas com design profissional
- ✅ Criação de textos promocionais persuasivos usando Google Gemini AI (gratuito)
- ✅ Geração de links de afiliado curtos
- ✅ Interface amigável para copiar texto e baixar imagens
- ✅ Histórico de promoções geradas
- ✅ Sistema de compartilhamento social integrado

## 🛠️ Tecnologias Utilizadas

- **Django 4.2** - Framework web Python
- **Pillow** - Processamento e geração de imagens
- **Google Gemini API** - Geração de textos com IA (gratuito)
- **Shopee Affiliate API** - Integração com produtos da Shopee
- **Bootstrap 5** - Interface responsiva e moderna
- **Font Awesome** - Ícones

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone <seu-repositorio>
cd shopee_promo
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv

# No Linux/Mac:
source venv/bin/activate

# No Windows:
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione suas credenciais:

#### 🔑 Obtendo a API Key do Shopee

1. Acesse: https://open.shopee.com.br/
2. Faça login com sua conta de afiliado Shopee
3. Crie uma aplicação e obtenha:
   - `SHOPEE_AFFILIATE_ID`: Seu ID de afiliado
   - `SHOPEE_API_KEY`: Chave da API

#### 🤖 Obtendo a API Key do Google Gemini (GRATUITO)

1. Acesse: https://makersuite.google.com/app/apikey
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave gerada para `GEMINI_API_KEY`

**Observação:** A API do Gemini é gratuita e tem limite generoso para uso pessoal!

### 5. Execute as migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crie um superusuário (opcional)

```bash
python manage.py createsuperuser
```

### 7. Inicie o servidor

```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000

## 🎯 Como Usar

1. **Cole o link do produto da Shopee**
   - Acesse a Shopee e copie o link de qualquer produto
   - Cole no campo da página inicial

2. **Aguarde a geração**
   - A aplicação vai buscar informações do produto
   - Gerar uma imagem promocional profissional
   - Criar um texto persuasivo com IA

3. **Copie e compartilhe**
   - Baixe a imagem gerada
   - Copie o texto promocional
   - Use seu link de afiliado para compartilhar

## 📁 Estrutura do Projeto

```
shopee_promo/
├── manage.py
├── requirements.txt
├── .env.example
├── shopee_promo/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── promo_generator/
    ├── models.py           # Modelo de dados
    ├── views.py            # Lógica das views
    ├── forms.py            # Formulários
    ├── services.py         # Integrações com APIs
    ├── image_utils.py      # Geração de imagens
    ├── urls.py             # URLs do app
    ├── admin.py            # Admin Django
    └── templates/
        └── promo_generator/
            ├── base.html
            ├── home.html
            ├── promo_detail.html
            └── promo_list.html
```

## 🎨 Personalizações

### Modificar o design das imagens

Edite o arquivo `promo_generator/image_utils.py`:

- `output_size`: Tamanho da imagem final
- `accent_color`: Cor principal (padrão: laranja Shopee)
- `create_promo_image()`: Lógica de geração da imagem

### Ajustar os prompts da IA

Edite o arquivo `promo_generator/services.py`, método `generate_promo_text()`:

- Modifique o `prompt` para ajustar o estilo do texto
- Ajuste `temperature` para controlar a criatividade (0.0 a 1.0)
- Modifique `maxOutputTokens` para textos mais longos/curtos

## 🔧 Configurações Avançadas

### Configurar para Produção

1. Altere `DEBUG = False` no `settings.py`
2. Configure `ALLOWED_HOSTS` com seu domínio
3. Use um banco de dados robusto (PostgreSQL)
4. Configure arquivos estáticos com WhiteNoise ou CDN
5. Use um servidor WSGI como Gunicorn

```bash
# Instalar Gunicorn
pip install gunicorn

# Rodar com Gunicorn
gunicorn shopee_promo.wsgi:application --bind 0.0.0.0:8000
```

### Deploy no Heroku

```bash
# Adicione ao Procfile:
web: gunicorn shopee_promo.wsgi

# Configure as variáveis de ambiente no Heroku
heroku config:set SHOPEE_AFFILIATE_ID=seu_id
heroku config:set SHOPEE_API_KEY=sua_key
heroku config:set GEMINI_API_KEY=sua_key
```

## 🐛 Troubleshooting

### Erro ao gerar imagem

- Verifique se o Pillow está instalado corretamente
- No Linux, instale: `sudo apt-get install python3-dev python3-pillow`

### Erro na API do Gemini

- Verifique se a API Key está correta
- Confirme que não excedeu o limite gratuito
- Acesse https://makersuite.google.com/ para verificar o status

### Erro na API da Shopee

- Verifique se suas credenciais estão corretas
- Confirme que sua conta de afiliado está ativa
- Verifique se o produto é elegível para afiliados

## 💡 Dicas para Afiliados

1. **Use imagens de alta qualidade**: Produtos com boas fotos convertem mais
2. **Teste diferentes textos**: A IA gera textos variados a cada execução
3. **Personalize o texto**: Você pode editar o texto antes de copiar
4. **Compartilhe estrategicamente**: Teste diferentes horários e redes sociais
5. **Acompanhe métricas**: Use o campo de visualizações para ver o engajamento

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 👨‍💻 Desenvolvedor

Desenvolvido para ajudar afiliados da Shopee a criar materiais promocionais profissionais de forma automática.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abrir um Pull Request

## 📞 Suporte

Se encontrar problemas ou tiver sugestões:

1. Verifique a seção de Troubleshooting
2. Abra uma issue no GitHub
3. Entre em contato através do email do desenvolvedor

---

**Feito com ❤️ para afiliados Shopee | Powered by Django + Gemini AI**
