import streamlit as st
import pandas as pd
from datetime import datetime
import os
import re

# Configuração da página
st.set_page_config(
    page_title="Cadastro para Caravana",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Customizado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    * {
        font-family: 'Poppins', sans-serif;
    }

    .main-title {
        color: #2b5876;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        font-size: 2.5rem !important;
    }

    .subheader {
        color: #4e4376 !important;
        text-align: center;
        font-weight: 500 !important;
        margin-bottom: 2rem !important;
    }

    .stContainer {
        border: 1px solid #e0e0e0 !important;
        border-radius: 15px !important;
        padding: 2rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        background: white !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(116, 79, 168, 0.4) !important;
    }

    .footer {
        text-align: center;
        padding: 1.5rem;
        color: #6b7280;
        margin-top: 2rem;
        border-top: 1px solid #e5e7eb;
    }

    .stTextInput>div>div>input {
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
    }

    .stNumberInput>div>div>input {
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
    }

    .stRadio>div {
        gap: 2rem !important;
    }

    .stRadio [role="radio"] {
        padding: 0.5rem 1rem !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
    }

    .stRadio [role="radio"][aria-checked="true"] {
        border-color: #667eea !important;
        background: #f0f4ff !important;
    }
</style>
""", unsafe_allow_html=True)

# Funções de persistência de dados (mantidas iguais)
def load_or_create_excel():
    excel_file = 'caravana.xlsx'
    if os.path.exists(excel_file):
        return pd.read_excel(excel_file)
    return pd.DataFrame(columns=[
        'nome', 'idade', 'rg', 'celular', 'organizacao', 
        'ordenancas', 'ala', 'data_cadastro'
    ])

def save_to_excel(data):
    df = load_or_create_excel()
    new_row = pd.DataFrame([data])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel('caravana.xlsx', index=False)

def clear_excel():
    pd.DataFrame(columns=[
        'nome', 'idade', 'rg', 'celular', 'organizacao', 
        'ordenancas', 'ala', 'data_cadastro'
    ]).to_excel('caravana.xlsx', index=False)

# Formatação de telefone (mantida igual)
def format_phone(input_number):
    digits = re.sub(r'\D', '', input_number)[:11]
    if len(digits) >= 11:
        return f'({digits[:2]}) {digits[2]} {digits[3:7]}-{digits[7:]}'
    return digits

# Interface principal
st.markdown('<h1 class="main-title">⛪ Templo de Campinas</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="subheader">📋 Formulário de Cadastro para Caravana 12/07 🚌</h2>', unsafe_allow_html=True)

# Container do formulário de cadastro
with st.container(border=True):
    with st.form("cadastro_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome Completo*", max_chars=50, help="Digite seu nome completo")
            rg = st.text_input("RG*", max_chars=20, help="Apenas números")
        
        with col2:
            idade = st.number_input("Idade*", min_value=1, max_value=120, value=18)
            celular = st.text_input("Celular*", 
                                   max_chars=16,
                                   placeholder="(00) 0 0000-0000",
                                   value=st.session_state.get('temp_phone', ''),
                                   help="Formato: (DD) 9 9999-9999")
        
        ala = st.selectbox(
            "Caravana da ala*", 
            options=["Ala Geisel", "Ala Marechal Rondom", 
                    "Ala Independencia", "Ala Bauru", "Ala Bela Vista"],
            index=0
        )
        
        organizacao = st.radio(
            "Organização*",
            options=["Quórum de Élderes", "Sociedade de Socorro", 
                    "Moças", "Rapazes", "Primária"],
            horizontal=True
        )
        
        ordenancas = st.multiselect(
            "Ordenanças que fará*",
            options=["Própria","Batistério", "Confirmação", "Iniciatória", 
                    "Investidura", "Selamento"],
            #default=["Própria"]
        )
        
        submitted = st.form_submit_button("✅ Enviar Cadastro")

# Processar cadastro (mantido igual)
if submitted:
    error_messages = []
    phone_digits = re.sub(r'\D', '', celular)
    
    if not nome.strip(): error_messages.append("Nome completo é obrigatório")
    if not rg.strip(): error_messages.append("RG é obrigatório")
    if len(phone_digits) != 11: error_messages.append("Celular deve ter 11 dígitos")
    if not ordenancas: error_messages.append("Selecione pelo menos uma ordenança")
    
    if error_messages:
        for error in error_messages: st.error(f"⚠️ {error}")
    else:
        try:
            save_to_excel({
                'nome': nome.strip(),
                'idade': idade,
                'rg': rg.strip(),
                'celular': format_phone(phone_digits),
                'organizacao': organizacao,
                'ordenancas': "/".join(ordenancas),
                'ala': ala,
                'data_cadastro': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            st.success("✅ Cadastro realizado com sucesso!")
            st.balloons()
            st.session_state.temp_phone = ''
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")

# Container de visualização de dados
with st.container(border=True):
    if st.button("🔒 Exibir Inscritos", key="ver_inscricoes", type="primary"):
        st.session_state.show_table = True

    if st.session_state.get('show_table', False):
        if 'authenticated' not in st.session_state:
            password = st.text_input("🔑 Digite a senha para visualizar:", type="password")
            if password == "estacabauru2025":
                st.session_state.authenticated = True
                st.rerun()
            elif password:
                st.error("Senha incorreta!")
        
        if st.session_state.get('authenticated', False):
            try:
                df = load_or_create_excel()
                
                if not df.empty:
                    cols = st.columns([1,4])
                    if cols[0].button("🧹 Limpar Tabela", 
                                    help="Ação irreversível!", 
                                    type="secondary"):
                        clear_excel()
                        st.success("✅ Tabela limpa com sucesso!")
                        st.rerun()
                    
                    # Estilização da tabela
                    st.markdown("""
                    <style>
                        .dataframe {
                            border-radius: 8px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        }
                        .dataframe th {
                            background: #f8f9fa !important;
                        }
                        .dataframe tr:nth-child(even) {
                            background-color: #f8f9fa;
                        }
                    </style>
                    """, unsafe_allow_html=True)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("📭 Nenhum registro encontrado")
                    
            except Exception as e:
                st.error(f"Erro ao carregar dados: {str(e)}")

# Rodapé estilizado
st.markdown("""
<div class="footer">
    <p>Desenvolvido com ❤️ para a Caravana ao Templo</p>
    <small>v3.2 | Dúvidas contate a Presidência do Quórum</small>
</div>
""", unsafe_allow_html=True)