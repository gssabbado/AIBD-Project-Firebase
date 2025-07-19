import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import requests

# Inicializa o Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("key.json")
    firebase_admin.initialize_app(cred)

# Conexão com o Firestore
db = firestore.client()

# Função para salvar entrada
def save_diary_entry(date, work_done, notes):
    doc_ref = db.collection("diarios").document()
    doc_ref.set({
        "data": str(date),
        "atividades_realizadas": work_done,
        "observacoes": notes,
        "timestamp": datetime.now()
    })

# Função para recuperar entradas
def get_diary_entries():
    docs = db.collection("diarios").order_by("data").stream()
    entries = []
    for doc in docs:
        data = doc.to_dict()
        entries.append(data)
    return entries

# Interface
st.title("Diário de Obra")

# Formulário de entrada
st.header("Nova entrada")
with st.form("diary_form"):
    date = st.date_input("Data da Atividade")
    work_done = st.text_area("Atividades Realizadas")
    notes = st.text_area("Observações")
    submitted = st.form_submit_button("Salvar Entrada")

    if submitted:
        save_diary_entry(date, work_done, notes)
        st.success("Entrada salva com sucesso!")

# Listagem de entradas
st.header("Entradas salvas")

try:
    entries = get_diary_entries()
    if entries:
        for e in entries:
            st.subheader(f"{e['data']}")
            st.markdown(f"**Atividades:** {e['atividades_realizadas']}")
            st.markdown(f"**Observações:** {e['observacoes']}")
            st.markdown("---")
    else:
        st.info("Nenhuma entrada registrada ainda.")
except Exception as e:
    st.error(f"Erro ao carregar entradas: {e}")