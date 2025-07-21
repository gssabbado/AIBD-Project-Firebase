import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
import pandas as pd
import uuid
import os

# inicializando e conectando com o Firebase
if not firebase_admin._apps:
    cred_dict = dict(st.secrets["firebase"])
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# título da página (centro e tamanho da fonte)
st.markdown("""
    <h1 style='text-align: center; color: #333; font-size: 36px;'>🏗️ Diário de Obra - Gestão</h1>
""", unsafe_allow_html=True)

# registros disponíveis para selecionar e os tipos
BLOCOS = {
    "Corporativo": ["Contrato","Empresa", "Proprietário"],
    "Jornada de Trabalho": ["Obra", "Mão de Obra"],
    "Dados Gerais": ["Diário", "Equipamentos", "Materiais", "Plano de Aproveitamento", "Resíduos", "Uso"],
}

# menu com dropdown de cada ação
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
    bloco = st.selectbox("Registros:", list(BLOCOS.keys()), key="menu_bloco") # ação da seleção de registro
with menu_cols[1]:
    colecoes_do_bloco = BLOCOS[bloco]
    colecao_selecionada = st.selectbox("Itens de registro:", colecoes_do_bloco, key="menu_colecao") # ação da seleção de tipo de registro

st.markdown(f"<h3 style='text-align: center;'>📂 Item do registro selecionado: <code>{colecao_selecionada}</code></h3>", unsafe_allow_html=True) # indicador do que foi selecionado para visualizar 

# itens de registros e as respectivas informações de acordo com o que é fornecido no banco
CAMPOS_REGISTRO = {
    "Contrato": ["Cont_CodEmpresa", "Cont_CodObra", "Cont_CodProp"],
    "Empresa": ["CodEmpresa", "CNPJ"],
    "Proprietário": ["CodProp", "NomeProp", "CPF"],
    "Obra": ["CodObra", "Endereco", "Fotos", "Data_inicio", "Data_previsao"],
    "Mão de Obra": ["CodFuncionario", "Foto", "Salario", "RG", "CPF", "Cargo", "Nome"],
    "Diário": ["CodDiario", "Endereco", "Fotos", "Obs_Geral", "Obs_Func", "Data", "Clima"],
    "Equipamentos": ["CodEquipamento", "Tipo", "Marca"],
    "Materiais": ["CodMaterial", "Tipo", "Quantidade", "Unidade", "Custo"],
    "Plano de Aproveitamento":["CodPlano", "Descricao", "Emp_Empresa",],
    "Resíduos": ["Classe", "PA_CodPlano"],
    "Uso": ["Uso_CodMaterial", "Uso_Classe", "Inicial", "Subsequente"]
    
}

# ação para adicionar novo documento
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


# função do firestone
@st.cache_data(ttl=60)
def get_documents_from_collection(collection_name):
    try:
        docs = db.collection(collection_name).stream()
        return [doc.to_dict() | {"_id": doc.id} for doc in docs]
    except Exception as e:
        st.error(f"Erro ao buscar documentos da coleção '{collection_name}': {str(e)}")
        return [] # acessar documentos dos registros

def update_document(collection, doc_id, updated_data):
    try:
        db.collection(collection).document(doc_id).set(updated_data)
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar documento: {str(e)}")
        return False # atualizar documento

def delete_document(collection, doc_id):
    try:
        db.collection(collection).document(doc_id).delete()
        return True
    except Exception as e:
        st.error(f"Erro ao excluir documento: {str(e)}")
        return False # deletar documento

# acessar dados do banco
with st.spinner(f"Carregando documentos de {colecao_selecionada}..."):
    documents = get_documents_from_collection(colecao_selecionada)

if documents:
    st.markdown(f"**Total de documentos:** {len(documents)}")
    fields = [k for k in documents[0].keys() if k != "_id"]

    # design da visualização dos dados
    col_vis, col_tab = st.columns([2, 1])  # largura: 2/3 para docs, 1/3 para tabela

    with col_vis.expander("📄 Visualização dos documentos", expanded=True):
        search_term = st.text_input("🔍 Filtrar documentos por palavra-chave:")
        filtered_docs = [
            doc for doc in documents
            if any(search_term.lower() in str(value).lower() for value in doc.values())
        ] if search_term else documents

        # configurações de paginação
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
                    confirm = st.checkbox(f"Confirmar exclusão", key=f"check_{doc['_id']}")
                    if st.button("Excluir", key=f"delete_{doc['_id']}"):
                        if confirm:
                            if delete_document(colecao_selecionada, doc["_id"]):
                                st.success("Documento excluído!")
                                st.rerun()
                    else:
                        st.warning("⚠️ Marque a caixa de confirmação antes de excluir.")


    with col_tab.expander("📊 Tabela de dados", expanded=True):
        df = pd.DataFrame(filtered_docs).drop(columns="_id", errors="ignore")
        st.dataframe(df, use_container_width=True)
else:
    st.warning("Nenhum documento encontrado neste tipo de registro.")