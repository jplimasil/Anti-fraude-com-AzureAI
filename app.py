import streamlit as st
from services.blob_service import upload_to_blob
from services.credit_card_service import analyze_credit_card

def configure_interface():
    st.title("Upload de arquivos DIO - Desafio 1 - Azure - Fake Docs")
    uploaded_file = st.file_uploader("Escolha um arquivo para upload", type=["pdf", "png", "jpg", "jpeg"])

    if uploaded_file is not None:
        fileName = uploaded_file.name
        #Enviar para o blob storage
        blob_url= upload_to_blob(uploaded_file, fileName)
        if blob_url:
            st.write(f"Arquivo '{fileName}' enviado com sucesso!")
            credit_card_info = analyze_credit_card(blob_url)
            show_image_and_validation(blob_url, credit_card_info)
         
        else:
            st.write(f"URL do arquivo no Blob Storage: {blob_url}")

def show_image_and_validation(blob_url, credit_card_info):
    st.image(blob_url, caption="Imagem enviado",use_column_width=True)
    st.write("Resultado da validação")
    if credit_card_info and credit_card_info["card_name"]:
        st.markdown(f"<h1 style='color:blue;'>Cartão Válido: {credit_card_info['card_name']}</h1>", unsafe_allow_html=True)
        st.write(f"Nome do Titular: {credit_card_info['card_name']}")
        st.write(f"Banco Emissor: {credit_card_info['bank_name']}")
        st.write(f"Data de Validade: {credit_card_info['expiry_date']}")
    else:
        st.markdown("<h1 style='color:red;'>Cartão Inválido</h1>", unsafe_allow_html=True)
        st.write("Este cartão não é válido.")

if __name__ == "__main__":
    configure_interface()