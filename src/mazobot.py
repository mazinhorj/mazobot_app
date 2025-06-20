import streamlit as st
import os
import pypdf
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import YoutubeLoader
from youtube_transcript_api._errors import NoTranscriptFound
from tempfile import NamedTemporaryFile
# import traceback

# Verifica se o pypdf está instalado
# try:
#     import pypdf
# except ImportError:
#     st.warning("O pacote pypdf não está instalado. Instalando...")
#     import subprocess
#     import sys
#     subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
#     import pypdf

# Configuração da API Key
api_key = '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'
os.environ['GROQ_API_KEY'] = api_key

# Função para gerar a resposta do bot
def resposta_do_bot(mensagens, documento):
    sys_msg = 'Você é um assistente amigável chamado MazoBot. Utilize estas informações para resumir conteúdos de diferentes fontes e fornecer insights: {informacoes}.'
    msg_model = [('system', sys_msg)]
    msg_model += mensagens
    template = ChatPromptTemplate.from_messages(msg_model)
    chat = ChatGroq(model='llama-3.3-70b-versatile')
    chain = template | chat
    resposta = chain.invoke({'informacoes': documento}).content
    return resposta

# Funções para resumir conteúdos de diferentes fontes
def resumo_site(url_site):
    loader = WebBaseLoader(url_site)
    lista_docs = loader.load()
    documento = ''
    for doc in lista_docs:
        documento += doc.page_content
    return documento

def resumo_pdf(caminho_arquivo):
    loader = PyPDFLoader(caminho_arquivo)
    lista_docs = loader.load()
    documento = ''
    for doc in lista_docs:
        documento += doc.page_content
    if not documento:
        raise ValueError('Nenhum conteúdo encontrado no PDF.')
    return documento

def resumo_video(url_video):
    try:
        loader = YoutubeLoader.from_youtube_url(
            url_video,
            language=['pt']
        )
        lista_docs = loader.load()
        documento = ''
        for doc in lista_docs:
            documento += doc.page_content
        if not documento:
            raise ValueError('Nenhuma legenda encontrada para o vídeo no idioma português.')
        return documento
    except NoTranscriptFound:
        raise ValueError('Não foi possível encontrar legendas para este vídeo no idioma português.')
    except Exception as e:
        raise ValueError(f'Ocorreu um erro ao tentar carregar as legendas do vídeo: {e}')

# Configuração da interface Streamlit
st.set_page_config(page_title="MazoBot", page_icon="🤖")
st.title("MazoBot - Assistente de Resumos")

# Sidebar para seleção do tipo de fonte
with st.sidebar:
    st.header("Configurações")
    source_type = st.radio(
        "Selecione o tipo de fonte:",
        ["Texto Direto", "Site", "PDF", "Vídeo"],
        index=0
    )

# Upload de arquivo PDF
uploaded_file = None
if source_type == "PDF":
    uploaded_file = st.file_uploader("Carregue um arquivo PDF", type="pdf")

# Inicialização do histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.current_document = ""

# Exibir histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do usuário baseada no tipo de fonte
if source_type == "Texto Direto":
    user_input = st.chat_input("Digite sua mensagem...")
    source_input = None
elif source_type == "Site":
    source_input = st.text_input("Digite a URL do site:")
    user_input = st.chat_input("Digite sua pergunta sobre o site...")
elif source_type == "PDF":
    source_input = None  # Agora usamos o uploaded_file
    user_input = st.chat_input("Digite sua pergunta sobre o PDF...")
elif source_type == "Vídeo":
    source_input = st.text_input("Digite a URL do vídeo do YouTube:")
    user_input = st.chat_input("Digite sua pergunta sobre o vídeo...")

# Processamento quando o usuário envia uma mensagem
if user_input:
    # Adiciona mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    documento = ''
    try:
        if source_type == 'Site' and source_input:
            documento = resumo_site(source_input)
            st.session_state.current_document = documento
        elif source_type == 'PDF' and uploaded_file is not None:
            # Salva o arquivo temporariamente
            with NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            documento = resumo_pdf(tmp_file_path)
            st.session_state.current_document = documento
            
            # Remove o arquivo temporário
            os.unlink(tmp_file_path)
        elif source_type == 'Vídeo' and source_input:
            documento = resumo_video(source_input)
            st.session_state.current_document = documento
        
        # Usa o documento atual se já tiver sido processado
        if not documento and st.session_state.current_document:
            documento = st.session_state.current_document
        
        mensagens = [('user', user_input)]
        resposta = resposta_do_bot(mensagens, documento if documento else "Nenhum documento fornecido.")
        
        # Adiciona resposta ao histórico
        st.session_state.messages.append({"role": "assistant", "content": resposta})
        with st.chat_message("assistant"):
            st.markdown(resposta)
            
    except ValueError as e:
        error_msg = str(e)
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        with st.chat_message("assistant"):
            st.error(error_msg)