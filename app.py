import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

#  Config page
st.set_page_config(page_title="ShopVite Assistant", page_icon="🤖")

st.title("🤖 Assistant FAQ ShopVite")

#  HEALTH CHECK
st.subheader("🔧 Statut API")

if st.button("Vérifier API"):
    try:
        res = requests.get(f"{API_URL}/health")

        if res.status_code == 200:
            st.success(res.json())
        else:
            st.error("API en erreur")

    except:
        st.error("API non disponible")

#  QUESTION
st.subheader("💬 Pose ta question")

question = st.text_input("Entrez votre question")

#  ENVOI
if st.button("Envoyer"):

    
    if question.strip() == "":
        st.warning("Veuillez entrer une question")

    else:
        try:
            with st.spinner("Recherche en cours... ⏳"):
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"question": question}
                )

            data = response.json()

            
            if response.status_code != 200:
                st.markdown("### ❌ Erreur")
                st.error(data.get("detail", "Erreur inconnue"))
                st.info("Essayez une question liée aux produits, livraison ou garantie.")

            
            else:
                st.markdown("### 📌 Réponse")
                st.write(data.get("answer", ""))

                st.markdown("### 📚 Sources")
                st.write(data.get("sources", []))

                st.markdown("### 🎯 Confiance")
                st.write(data.get("confidence", ""))

        except Exception as e:
            st.error(f"Erreur : {e}")