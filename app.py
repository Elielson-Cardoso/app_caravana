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

# Funções de persistência de dados
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

# Formatação de telefone
def format_phone(input_number):
    digits = re.sub(r'\D', '', input_number)[:11]
    if len(digits) >= 11:
        return f'({digits[:2]}) {digits[2]} {digits[3:7]}-{digits[7:]}'
    return digits

# Interface principal
st.title("Templo de Campinas 🕌")
st.subheader("Cadastro para Caravana 18/04 🚌")

# Container do formulário de cadastro
with st.container(border=True):
    st.markdown("### 📝 Formulário de Cadastro")
    
    with st.form("cadastro_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome Completo*", max_chars=50)
            rg = st.text_input("RG*", max_chars=20)
        
        with col2:
            idade = st.number_input("Idade*", min_value=12, max_value=120, value=18)
            # Campo de celular corrigido
            celular = st.text_input("Celular*", 
                                  max_chars=16,
                                  placeholder="(00) 0 0000-0000",
                                  value=st.session_state.get('temp_phone', ''))
        
        ala = st.selectbox(
            "Caravana da ala*", 
            options=["Ala Geisel", "Ala Marechal Rondom", 
                    "Ala Independencia", "Ala Bauru", "Ala Bela Vista"]
        )
        
        organizacao = st.radio(
            "Organização*",
            options=["Quórum de Élderes", "Sociedade de Socorro", 
                    "Moças", "Rapazes", "Primária"],
            horizontal=True
        )
        
        ordenancas = st.multiselect(
            "Ordenanças que fará*",
            options=["Batistério", "Confirmação", "Iniciatória", 
                    "Investidura", "Selamento"]
        )
        
        submitted = st.form_submit_button("✅ Salvar Cadastro")

# Processar cadastro
if submitted:
    error_messages = []
    phone_digits = re.sub(r'\D', '', celular)
    
    # Validações
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
            # Limpar o campo de forma segura
            st.session_state.temp_phone = ''
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")

# Container de visualização de dados
with st.container(border=True):
    st.markdown("### 📋 Lista de Inscritos")
    
    if st.button("🔒 Exibir Inscrições", key="ver_inscricoes"):
        st.session_state.show_table = True

    if st.session_state.get('show_table', False):
        if 'authenticated' not in st.session_state:
            password = st.text_input("Digite a senha para visualizar:", type="password")
            if password == "alageisel2025":
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
                                    type="primary"):
                        clear_excel()
                        st.success("✅ Tabela limpa com sucesso!")
                        st.rerun()
                    
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("Nenhum registro encontrado")
                    
            except Exception as e:
                st.error(f"Erro ao carregar dados: {str(e)}")

# Rodapé
st.markdown("---")
st.markdown(
    """<div style='text-align: center; color: #6b7280;'>
    <p>Desenvolvido com ❤️ para a Caravana ao Templo</p>
    <small>v3.1 | Dúvidas contate o líder da ala</small>
    </div>""",
    unsafe_allow_html=True
)