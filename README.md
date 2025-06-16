# MazoBot Web App - Instruções de Execução e Implantação

## Visão Geral

O MazoBot Web App é uma aplicação web desenvolvida em Flask que permite aos usuários interagir com um chatbot inteligente capaz de resumir conteúdos de diferentes fontes:

- Sites web
- Documentos PDF (locais ou URLs)
- Vídeos do YouTube (através de legendas)

## Estrutura do Projeto

```
mazobot_web_app/
├── venv/                    # Ambiente virtual Python
├── src/
│   ├── main.py             # Arquivo principal da aplicação Flask
│   ├── templates/
│   │   └── index.html      # Interface web do chatbot
│   ├── static/             # Arquivos estáticos (CSS, JS, imagens)
│   ├── models/             # Modelos de banco de dados
│   ├── routes/             # Rotas adicionais do Flask
│   └── database/           # Banco de dados SQLite
└── requirements.txt        # Dependências do projeto
```

## Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Chave de API do Groq (para o modelo de linguagem)

## Instalação e Configuração

### 1. Clonar ou baixar o projeto

Certifique-se de ter todos os arquivos do projeto em um diretório local.

### 2. Configurar o ambiente virtual

```bash
cd mazobot_web_app
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar a chave de API

Edite o arquivo `src/main.py` e substitua a chave de API do Groq pela sua própria:

```python
api_key = 'sua_chave_api_groq_aqui'
```

**Importante:** Para uso em produção, recomenda-se usar variáveis de ambiente para armazenar a chave de API de forma segura.

## Execução Local

### 1. Ativar o ambiente virtual

```bash
cd mazobot_web_app
source venv/bin/activate
```

### 2. Executar a aplicação

```bash
python src/main.py
```

### 3. Acessar a aplicação

Abra seu navegador e acesse: `http://localhost:5000`

A aplicação estará disponível e pronta para uso.

## Como Usar

### 1. Selecionar a fonte de conteúdo

Na interface web, escolha uma das opções:
- **Site Web**: Para resumir conteúdo de páginas web
- **Documento PDF**: Para resumir arquivos PDF (local ou URL)
- **Vídeo do YouTube**: Para resumir vídeos através de suas legendas

### 2. Inserir a URL ou caminho

- Para sites: Digite a URL completa (ex: https://www.exemplo.com)
- Para PDFs: Digite o caminho do arquivo local ou URL que termine com .pdf
- Para vídeos: Digite a URL do vídeo do YouTube

### 3. Carregar a fonte

Clique em "Carregar Fonte" para processar o conteúdo.

### 4. Conversar com o MazoBot

Após carregar a fonte, você pode fazer perguntas sobre o conteúdo carregado. O MazoBot irá responder baseado nas informações extraídas.

## Funcionalidades

### Validação de Entrada
- **PDFs**: Verifica se arquivos locais existem e têm extensão .pdf
- **URLs de PDF**: Verifica se a URL termina com .pdf
- **Vídeos do YouTube**: Trata erros quando legendas não estão disponíveis

### Tratamento de Erros
- Mensagens informativas quando não é possível extrair conteúdo
- Validação de entrada antes do processamento
- Feedback claro para o usuário em caso de problemas

### Interface Responsiva
- Design adaptável para desktop e mobile
- Interface limpa e intuitiva
- Feedback visual durante o carregamento

## Dependências Principais

- **Flask**: Framework web
- **langchain-groq**: Integração com o modelo Groq
- **langchain-community**: Carregadores de documentos
- **youtube-transcript-api**: Extração de legendas do YouTube
- **beautifulsoup4**: Parsing de conteúdo web

## Solução de Problemas

### Erro: "No module named 'bs4'"
```bash
pip install beautifulsoup4
```

### Erro: "No transcript found"
- Verifique se o vídeo do YouTube possui legendas em português
- Alguns vídeos podem não ter legendas disponíveis

### Erro: "Invalid PDF path"
- Verifique se o caminho do arquivo está correto
- Para URLs, certifique-se de que termina com .pdf

### Problemas de conexão com Groq
- Verifique se a chave de API está correta
- Confirme se há conexão com a internet

## Considerações de Segurança

### Para Produção

1. **Variáveis de Ambiente**: Use variáveis de ambiente para a chave de API
```python
import os
api_key = os.environ.get('GROQ_API_KEY')
```

2. **HTTPS**: Configure HTTPS para comunicação segura

3. **Validação de Entrada**: Implemente validação adicional para URLs e arquivos

4. **Rate Limiting**: Considere implementar limitação de taxa para evitar abuso

5. **Logs**: Implemente sistema de logs para monitoramento

## Implantação

### Opção 1: Servidor Local
A aplicação já está configurada para rodar em `0.0.0.0:5000`, permitindo acesso de outros dispositivos na rede local.

### Opção 2: Serviços de Cloud
Para implantação em produção, considere:
- Heroku
- AWS EC2
- Google Cloud Platform
- DigitalOcean

### Configurações para Produção

1. **Servidor WSGI**: Use Gunicorn ou uWSGI
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

2. **Proxy Reverso**: Configure Nginx como proxy reverso

3. **Banco de Dados**: Para aplicações maiores, considere PostgreSQL ou MySQL

## Suporte e Manutenção

### Atualizações de Dependências
```bash
pip freeze > requirements.txt
```

### Backup
- Faça backup regular do código
- Para aplicações com dados importantes, configure backup do banco de dados

### Monitoramento
- Monitore logs de erro
- Acompanhe uso de recursos (CPU, memória)
- Monitore tempo de resposta da API

## Contato

Para dúvidas ou suporte, consulte a documentação das bibliotecas utilizadas ou entre em contato com a equipe de desenvolvimento.

