import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
import pandas as pd
import uuid
import os

# Inicializa Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("key.json")
    firebase_admin.initialize_app(cred)

# Conecta com o Firestore
db = firestore.client()

# Inicializa Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("key.json")
    firebase_admin.initialize_app(cred)

# Conecta com o Firestore
db = firestore.client()

# TÍTULO CENTRALIZADO
st.markdown("""
    <h1 style='text-align: center; color: #333; font-size: 36px;'>🏗️ Diário de Obra - Gestão</h1>
""", unsafe_allow_html=True)

# DEFINIÇÃO DOS BLOCOS E COLEÇÕES
BLOCOS = {
    "Cadastro": ["Empresa", "Proprietário"],
    "Obra": ["Mão de Obra"],
    "Dados Gerais": ["Diário", "Equipamentos", "Materiais", "Plano de Aproveitamento", "Resíduos", "Uso"],
}

# MENU HORIZONTAL COM ESTILO PERSONALIZADO
st.markdown("""
    <style>
        .menu-container {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-bottom: 30px;
        }
        .menu-container select {
            padding: 8px;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

menu_cols = st.columns([1, 1])
with menu_cols[0]:
    bloco = st.selectbox("Registros:", list(BLOCOS.keys()), key="menu_bloco")
with menu_cols[1]:
    colecoes_do_bloco = BLOCOS[bloco]
    colecao_selecionada = st.selectbox("Itens de registro:", colecoes_do_bloco, key="menu_colecao")

st.markdown(f"<h3 style='text-align: center;'>📂 Item do registro selecionado: <code>{colecao_selecionada}</code></h3>", unsafe_allow_html=True)

# Dicionário com os campos por coleção
CAMPOS_REGISTRO = {
    "Empresa": ["CNPJ", "Endereço"],
}

# Seção para adicionar novo documento
with st.expander("➕ Adicionar novo documento", expanded=False):
    campos = CAMPOS_REGISTRO.get(colecao_selecionada, [])
    novo_doc = {}

    with st.form(key=f"form_{colecao_selecionada}"):
        st.markdown(f"### Novo registro em **{colecao_selecionada}**")
        for campo in campos:
            novo_doc[campo] = st.text_input(f"{campo.capitalize()}")

        submitted = st.form_submit_button("💾 Salvar documento")
        if submitted:
            try:
                db.collection(colecao_selecionada).add(novo_doc)
                st.success("✅ Documento adicionado com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro ao salvar documento: {str(e)}")


# FUNÇÕES FIRESTORE
@st.cache_data(ttl=60)
def get_documents_from_collection(collection_name):
    try:
        docs = db.collection(collection_name).stream()
        return [doc.to_dict() | {"_id": doc.id} for doc in docs]
    except Exception as e:
        st.error(f"Erro ao buscar documentos da coleção '{collection_name}': {str(e)}")
        return []

def update_document(collection, doc_id, updated_data):
    try:
        db.collection(collection).document(doc_id).set(updated_data)
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar documento: {str(e)}")
        return False

def delete_document(collection, doc_id):
    try:
        db.collection(collection).document(doc_id).delete()
        return True
    except Exception as e:
        st.error(f"Erro ao excluir documento: {str(e)}")
        return False

# CARREGAMENTO DOS DOCUMENTOS
with st.spinner(f"Carregando documentos de {colecao_selecionada}..."):
    documents = get_documents_from_collection(colecao_selecionada)

if documents:
    st.markdown(f"**Total de documentos:** {len(documents)}")
    fields = [k for k in documents[0].keys() if k != "_id"]

    # VISUALIZAÇÃO E TABELA LADO A LADO
    col_vis, col_tab = st.columns([2, 1])  # largura: 2/3 para docs, 1/3 para tabela

    with col_vis.expander("📄 Visualização dos documentos", expanded=True):
        search_term = st.text_input("🔍 Filtrar documentos por palavra-chave:")
        filtered_docs = [
            doc for doc in documents
            if any(search_term.lower() in str(value).lower() for value in doc.values())
        ] if search_term else documents

        # Paginação
        page_size = 10
        total = len(filtered_docs)
        max_page = max((total - 1) // page_size + 1, 1)
        if 'page' not in st.session_state:
            st.session_state.page = 1

        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("← Anterior") and st.session_state.page > 1:
                st.session_state.page -= 1
        with col3:
            if st.button("Próximo →") and st.session_state.page < max_page:
                st.session_state.page += 1
        with col2:
            st.markdown(f"**Página {st.session_state.page} de {max_page}**")

        start = (st.session_state.page - 1) * page_size
        end = start + page_size

        for doc in filtered_docs[start:end]:
            with st.expander(f"🧾 Documento ID: {doc['_id']}"):
                edited_data = {}
                for key, value in doc.items():
                    if key == "_id":
                        continue
                    novo_valor = st.text_input(f"{key}:", value=str(value), key=f"{doc['_id']}_{key}")
                    edited_data[key] = novo_valor

                col_edit, col_del = st.columns(2)
                with col_edit:
                    if st.button("Atualizar", key=f"update_{doc['_id']}"):
                        if update_document(colecao_selecionada, doc["_id"], edited_data):
                            st.success("Documento atualizado!")
                            st.rerun()

                with col_del:
                    if st.button("Excluir", key=f"delete_{doc['_id']}"):
                        if delete_document(colecao_selecionada, doc["_id"]):
                            st.warning("Documento excluído!")
                            st.rerun()

    with col_tab.expander("📊 Tabela de dados", expanded=True):
        df = pd.DataFrame(filtered_docs).drop(columns="_id", errors="ignore")
        st.dataframe(df, use_container_width=True)
else:
    st.warning("Nenhum documento encontrado neste tipo de registro.")
