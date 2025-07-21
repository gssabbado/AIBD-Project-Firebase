import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# Inicializa Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("key.json")
    firebase_admin.initialize_app(cred)

# Conecta com o Firestore
db = firestore.client()

# Inicializa Firebase com tratamento de erro
if not firebase_admin._apps:
    try:
        cred_dict = dict(st.secrets["firebase"])
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        st.success("✅ Firebase conectado com sucesso!")
    except Exception as e:
        st.error(f"❌ Erro ao conectar Firebase: {str(e)}")
        st.stop()

try:
    db = firestore.client()
except Exception as e:
    st.error(f"❌ Erro ao conectar Firestore: {str(e)}")
    st.stop()

BLOCOS = {
    "Cadastro": ["Empresa", "Proprietario"],
    "Obra": ["Empresa", "Mao_de_Obra", "Proprietario"],
    "Diário": ["Equipamentos", "Materiais", "Plano_de_Aproveitamento", "Residuos", "Uso"],
}

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

st.set_page_config(page_title="Diário de Obra", layout="wide", page_icon="🏗️")
st.title("Diário de Obra - Gestão")

bloco = st.sidebar.radio("Selecione o bloco:", list(BLOCOS.keys()))
colecoes_do_bloco = BLOCOS[bloco]

colecao_selecionada = st.selectbox("Item do registro:", colecoes_do_bloco)
st.header(f"📂 Item do registro: {colecao_selecionada}")

# Adicionar indicador de carregamento
with st.spinner(f"Carregando documentos de {colecao_selecionada}..."):
    documents = get_documents_from_collection(colecao_selecionada)

if documents:
    st.markdown(f"**Total de documentos:** {len(documents)}")

    fields = [k for k in documents[0].keys() if k != "_id"]

    with st.expander("📄 Visualizar documentos"):
        search_term = st.text_input("🔍 Filtrar documentos por palavra-chave:")
        filtered_docs = [
            doc for doc in documents
            if any(search_term.lower() in str(value).lower() for value in doc.values())
        ] if search_term else documents

        sort_col1, sort_col2 = st.columns([2, 1])
        with sort_col1:
            sort_field = st.selectbox("Ordenar por campo:", fields, key="sort_field")
        with sort_col2:
            sort_order = st.radio("Ordem:", ["Crescente", "Decrescente"], horizontal=True, key="sort_order")

        filtered_docs.sort(
            key=lambda x: str(x.get(sort_field, "")),
            reverse=(sort_order == "Decrescente")
        )

        # Paginação com botões
        page_size = 10
        total = len(filtered_docs)
        max_page = max((total - 1) // page_size + 1, 1)

        if 'page' not in st.session_state:
            st.session_state.page = 1

        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ Anterior") and st.session_state.page > 1:
                st.session_state.page -= 1
        with col3:
            if st.button("Próximo ➡️") and st.session_state.page < max_page:
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
                    # Input para edição (string)
                    novo_valor = st.text_input(f"{key}:", value=str(value), key=f"{doc['_id']}_{key}")
                    edited_data[key] = novo_valor

                col_edit, col_del, col_save = st.columns(3)
                with col_edit:
                    if st.button("Atualizar", key=f"update_{doc['_id']}"):
                        if update_document(colecao_selecionada, doc["_id"], edited_data):
                            st.success("Documento atualizado!")
                            st.rerun()  # FIXED: Changed from st.experimental_rerun()

                with col_del:
                    if st.button("Excluir", key=f"delete_{doc['_id']}"):
                        if delete_document(colecao_selecionada, doc["_id"]):
                            st.warning("Documento excluído!")
                            st.rerun()  # FIXED: Changed from st.experimental_rerun()

    with st.expander("📊 Tabela de dados (com busca)"):
        if documents:  # Additional safety check
            df = pd.DataFrame(documents).drop(columns="_id", errors="ignore")
            st.dataframe(df, use_container_width=True)

else:
    st.warning("Nenhum documento encontrado neste tipo de registro.")
    
# Debug info (remove in production)
if st.sidebar.checkbox("🔧 Debug Info"):
    st.sidebar.write("Firebase Apps:", len(firebase_admin._apps))
    try:
        st.sidebar.write("Firestore client:", type(db).__name__)
    except:
        st.sidebar.write("Firestore client: Not initialized")