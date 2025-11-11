import streamlit as st
import PyPDF2
from ollama import chat

# Configuração do agente
MODEL = "tinyllama"
SYSTEM = "Você é um agente pedagógico offline. Responda SEMPRE em PORTUGUÊS BRASILEIRO."

def gerar(resumo_da_tarefa, entrada):
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"Tarefa: {resumo_da_tarefa}\n\nEntrada:\n{entrada}"}
    ]
    response = chat(model=MODEL, messages=messages)
    return response["message"]["content"]

def ler_pdf(arquivo):
    reader = PyPDF2.PdfReader(arquivo)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text() or ""
    return texto

# Interface Streamlit
st.set_page_config(page_title="Agente Pedagógico Offline", layout="centered")
st.title("📚 Agente Pedagógico Offline")
st.markdown("Carregue um PDF e gere materiais pedagógicos automaticamente.")

uploaded_file = st.file_uploader("Escolha um PDF", type="pdf")

if uploaded_file:
    texto_pdf = ler_pdf(uploaded_file)
    st.info(f"PDF carregado com {len(texto_pdf)} caracteres.")
    
    opcao = st.selectbox("Escolha a tarefa:", [
        "Gerar questões",
        "Gerar plano de aula",
        "Dar feedback a redação",
        "Fazer análise didática"
    ])
    
    if st.button("Gerar"):
        with st.spinner("Gerando..."):
            if opcao == "Gerar questões":
                instrucao = "Gerar 5 QUESTÕES em PORTUGUÊS BRASILEIRO sobre o texto: 2 de compreensão, 2 de aplicação, 1 de análise. Incluir gabarito."
            elif opcao == "Gerar plano de aula":
                instrucao = "Gerar um PLANO DE AULA em PORTUGUÊS BRASILEIRO com: objetivos, etapas (3 blocos), atividade prática, avaliação e lição de casa."
            elif opcao == "Dar feedback a redação":
                instrucao = "Atue como MEDIADOR PEDAGÓGICO em PORTUGUÊS BRASILEIRO: pontos fortes, pontos a melhorar e sugestão de reescrita."
            else:
                instrucao = "Fazer uma ANÁLISE DIDÁTICA em PORTUGUÊS BRASILEIRO: síntese, mapa de conceitos, lacunas e 3 atividades mão na massa."
            
            resposta = gerar(instrucao, texto_pdf[:2000])  # limita para evitar sobrecarga
            st.success("✅ Resultado gerado:")
            st.write(resposta)