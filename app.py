import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

# Inicializa Firebase
if not firebase_admin._apps:
    cred_dict = json.loads(st.secrets["firebase"].to_json())
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

# Conecta com o Firestore
db = firestore.client()

# Função para listar as coleções disponíveis (manualmente ou dinamicamente)
def get_collections():
    # Você pode obter dinamicamente com:
    # return [col.id for col in db.collections()]
    # Ou definir manualmente:
    return [
        "Aluguel", "Cadastro", "Consumo", "Contrato", "Diario", "Empresa",
        "Equipamentos", "Mao_de_Obra", "Materiais", "Obra",
        "Plano_de_Aproveitamento", "Proprietario", "Recebimento",
        "Residuos", "Trabalho", "Uso"
    ]

# Função para buscar documentos de uma coleção
def get_documents_from_collection(collection_name):
    try:
        docs = db.collection(collection_name).stream()
        return [doc.to_dict() | {"_id": doc.id} for doc in docs]
    except Exception as e:
        st.error(f"Erro ao buscar documentos: {e}")
        return []

# UI
st.set_page_config(page_title="📁 Visualizador Firestore", layout="wide")
st.title("📁 Visualizador de Dados do Firestore")

# Seleção de coleção
collections = get_collections()
selected_collection = st.selectbox("Escolha uma coleção para visualizar os dados:", collections)

# Busca e exibição dos dados
if selected_collection:
    documents = get_documents_from_collection(selected_collection)

    st.subheader(f"📄 {len(documents)} documentos encontrados em `{selected_collection}`")

    if documents:
        for doc in documents:
            with st.expander(f"🧾 Documento ID: {doc['_id']}"):
                for key, value in doc.items():
                    if key != "_id":
                        st.markdown(f"**{key}:** {value}")
    else:
        st.info("Nenhum documento encontrado nesta coleção.")
