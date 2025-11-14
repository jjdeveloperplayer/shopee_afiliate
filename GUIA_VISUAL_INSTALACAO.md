# 🎬 GUIA VISUAL - INSTALAÇÃO PASSO A PASSO

## 📋 CHECKLIST PRÉ-INSTALAÇÃO

Antes de começar, você precisa ter instalado:

- [ ] Python 3.8 ou superior
- [ ] pip (gerenciador de pacotes Python)
- [ ] Git (opcional, mas recomendado)
- [ ] Navegador web moderno

---

## 🚀 INSTALAÇÃO - 10 PASSOS SIMPLES

### PASSO 1: Verifique o Python
```bash
python --version
# ou
python3 --version
```
**Resultado esperado:** `Python 3.8.x` ou superior

---

### PASSO 2: Navegue até a pasta do projeto
```bash
cd shopee_promo
```
**Dica:** Use `ls` (Linux/Mac) ou `dir` (Windows) para listar arquivos

---

### PASSO 3: Crie ambiente virtual (OPCIONAL mas recomendado)
```bash
# Linux/Mac:
python3 -m venv venv
source venv/bin/activate

# Windows:
python -m venv venv
venv\Scripts\activate
```
**Resultado esperado:** `(venv)` aparece no início do prompt

---

### PASSO 4: Instale as dependências
```bash
pip install -r requirements.txt
```
**Resultado esperado:** 
```
Installing collected packages: Django, Pillow, requests...
Successfully installed Django-4.2.7 Pillow-10.1.0 ...
```

---

### PASSO 5: Configure o arquivo .env
```bash
# Linux/Mac:
cp .env.example .env

# Windows:
copy .env.example .env
```

Abra o arquivo `.env` com um editor de texto e adicione:
```
GEMINI_API_KEY=sua_chave_aqui
```

**Como obter a chave:**
1. Acesse: https://makersuite.google.com/app/apikey
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie e cole no arquivo .env

---

### PASSO 6: Prepare o banco de dados
```bash
python manage.py migrate
```
**Resultado esperado:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, promo_generator
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

---

### PASSO 7: (OPCIONAL) Crie dados de demonstração
```bash
python manage.py create_demo_promos
```
**Resultado esperado:**
```
✅ Criada: Fone de Ouvido Bluetooth Premium...
✅ Criada: Smartwatch Fitness com Monitor Cardíaco...
✅ Criada: Kit 3 Camisetas Premium 100% Algodão...
🎉 3 promoções de exemplo criadas com sucesso!
```

---

### PASSO 8: Execute o servidor
```bash
python manage.py runserver
```
**Resultado esperado:**
```
Django version 4.2.7, using settings 'shopee_promo.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

---

### PASSO 9: Abra no navegador
Acesse: **http://127.0.0.1:8000**

**Você deverá ver:**
- 🎨 Página inicial colorida
- 📝 Formulário para colar link
- 🔥 "Shopee Promo Generator" no topo

---

### PASSO 10: Teste a aplicação

**Se você criou os dados de demo:**
1. Clique em "Minhas Promoções" no menu
2. Você verá 3 promoções de exemplo
3. Clique em uma para ver detalhes

**Se não criou os dados de demo:**
1. Cole um link de produto da Shopee
2. Clique em "Gerar Material Promocional"
3. Aguarde o processamento
4. Veja o resultado!

---

## 🎯 PRIMEIRA PROMOÇÃO - PASSO A PASSO

### 1. Encontre um produto na Shopee
- Acesse: https://shopee.com.br
- Busque por qualquer produto
- Exemplo: "fone bluetooth"

### 2. Copie o link do produto
- Clique no produto
- Copie a URL da barra de endereços
- Exemplo: `https://shopee.com.br/Fone-de-Ouvido-i.123456.789012345`

### 3. Cole na aplicação
- Volte para http://127.0.0.1:8000
- Cole o link no campo
- Clique em "Gerar Material Promocional"

### 4. Aguarde o processamento
Você verá:
```
⏳ Buscando informações do produto...
🤖 Gerando texto com IA...
🎨 Criando imagem promocional...
✅ Pronto!
```

### 5. Use o material gerado
- 📥 **Baixe a imagem** (botão verde)
- 📋 **Copie o texto** (botão azul)
- 🔗 **Use o link de afiliado**

### 6. Compartilhe
- WhatsApp Status
- Instagram Stories  
- Facebook
- Twitter/X
- Telegram

---

## 🔍 VERIFICANDO SE FUNCIONOU

### Teste 1: Servidor rodando?
```bash
curl http://127.0.0.1:8000
```
**Deve retornar:** HTML da página

### Teste 2: APIs configuradas?
```bash
python test_app.py
```
**Deve mostrar:**
```
🔑 API Shopee configurada: ✅ Sim
🤖 API Gemini configurada: ✅ Sim
```

### Teste 3: Banco de dados OK?
```bash
python manage.py shell
>>> from promo_generator.models import ProductPromo
>>> ProductPromo.objects.count()
```
**Deve retornar:** número de promoções criadas

---

## 🐛 PROBLEMAS COMUNS E SOLUÇÕES

### ❌ "python: command not found"
**Solução:** Use `python3` em vez de `python`

### ❌ "pip: command not found"
**Solução:** Instale o pip:
```bash
# Linux:
sudo apt-get install python3-pip

# Mac:
brew install python

# Windows:
Baixe de python.org
```

### ❌ "ModuleNotFoundError: No module named 'django'"
**Solução:** Instale as dependências:
```bash
pip install -r requirements.txt
```

### ❌ "Port already in use"
**Solução:** Use outra porta:
```bash
python manage.py runserver 8001
```
Acesse: http://127.0.0.1:8001

### ❌ "GEMINI_API_KEY not configured"
**Solução:**
1. Crie o arquivo .env (copie do .env.example)
2. Adicione a chave do Gemini
3. Reinicie o servidor

### ❌ "Template does not exist"
**Solução:**
```bash
python manage.py collectstatic --noinput
```

### ❌ Imagem não carrega
**Solução:** Verifique se a pasta `media/` existe:
```bash
mkdir -p media/promos
```

---

## 📊 ESTRUTURA VISUAL DO PROJETO

```
shopee_promo/
│
├── 📂 shopee_promo/          ← Configurações Django
│   ├── ⚙️ settings.py        (APIs, banco de dados)
│   ├── 🔗 urls.py            (rotas principais)
│   └── 🌐 wsgi.py            (servidor web)
│
├── 📂 promo_generator/       ← Aplicação principal
│   ├── 📊 models.py          (estrutura de dados)
│   ├── 👁️ views.py           (lógica de exibição)
│   ├── 🔧 services.py        (integração APIs)
│   ├── 🎨 image_utils.py     (geração de imagens)
│   │
│   └── 📂 templates/         ← Interface visual
│       ├── 🏠 home.html      (página inicial)
│       ├── 👁️ promo_detail.html (detalhes)
│       └── 📋 promo_list.html    (lista)
│
├── 📄 requirements.txt       ← Lista de dependências
├── 📄 .env.example          ← Exemplo de configuração
├── 📄 manage.py             ← Gerenciador Django
└── 📄 README.md             ← Documentação
```

---

## 🎨 FLUXO VISUAL DA APLICAÇÃO

```
┌─────────────────┐
│  USUÁRIO ENTRA  │
│   na aplicação  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PÁGINA INICIAL │
│  - Formulário   │
│  - Exemplos     │
└────────┬────────┘
         │
         │ Cola link do produto
         ▼
┌─────────────────┐
│  PROCESSAMENTO  │
│  - Busca API    │
│  - Gera texto   │
│  - Cria imagem  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  RESULTADO      │
│  - Imagem 🎨    │
│  - Texto 📝     │
│  - Link 🔗      │
└────────┬────────┘
         │
         │ Download + Copiar
         ▼
┌─────────────────┐
│  COMPARTILHAR   │
│  - WhatsApp     │
│  - Instagram    │
│  - Facebook     │
└─────────────────┘
```

---

## 📱 INTERFACE VISUAL

### Página Inicial
```
╔════════════════════════════════════════╗
║  🔥 Shopee Promo Generator            ║
╠════════════════════════════════════════╣
║                                        ║
║  🚀 Crie Promoções Incríveis!         ║
║                                        ║
║  ┌──────────────────────────────────┐ ║
║  │ Cole o Link do Produto           │ ║
║  │ [____________________________]   │ ║
║  │                                  │ ║
║  │  [🔥 Gerar Material Promocional] │ ║
║  └──────────────────────────────────┘ ║
║                                        ║
║  ⭐ Promoções Recentes                ║
║  [📸][📸][📸][📸][📸][📸]             ║
║                                        ║
╚════════════════════════════════════════╝
```

### Página de Resultado
```
╔════════════════════════════════════════╗
║  Resultado da Promoção                 ║
╠════════════════════════════════════════╣
║                                        ║
║  🎨 IMAGEM PROMOCIONAL    📝 TEXTO     ║
║  ┌──────────────┐         ┌─────────┐ ║
║  │              │         │🔥 SUPER │ ║
║  │   PRODUTO    │         │OFERTA!  │ ║
║  │              │         │         │ ║
║  │   R$ 99,90   │         │⭐⭐⭐⭐⭐│ ║
║  │              │         │         │ ║
║  └──────────────┘         │Compre já│ ║
║                           └─────────┘ ║
║  [📥 Baixar Imagem]   [📋 Copiar]     ║
║                                        ║
║  🔗 Link de Afiliado:                 ║
║  [shope.ee/xxxxx] [📋]                ║
║                                        ║
║  Compartilhar:                        ║
║  [WhatsApp] [Facebook] [Twitter]      ║
║                                        ║
╚════════════════════════════════════════╝
```

---

## ✅ CHECKLIST PÓS-INSTALAÇÃO

Após instalar, verifique:

- [ ] Servidor rodando sem erros
- [ ] Página inicial carrega corretamente
- [ ] Formulário aparece e é clicável
- [ ] Pode acessar "Minhas Promoções"
- [ ] Se criou demos, eles aparecem
- [ ] Imagens carregam corretamente
- [ ] Pode copiar texto
- [ ] Pode baixar imagens

Se TUDO acima está ✅, você está pronto! 🎉

---

## 🎓 PRÓXIMOS PASSOS

Agora que instalou:

1. **Configure as APIs** (Gemini + Shopee)
2. **Teste com produto real** da Shopee
3. **Compartilhe primeira promoção**
4. **Acompanhe resultados**
5. **Otimize e escale**

---

## 🆘 AINDA COM PROBLEMAS?

1. **Leia o README.md completo**
2. **Execute `python test_app.py`**
3. **Verifique os logs no terminal**
4. **Procure o erro no Google**
5. **Abra uma issue no GitHub**

---

**🎉 PARABÉNS! VOCÊ INSTALOU A APLICAÇÃO! 🎉**

Agora é só usar e lucrar! 💰

---

*Este guia foi criado com ❤️ para facilitar sua vida*  
*Qualquer dúvida, consulte a documentação completa*
