import streamlit as st

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Doradca SP56", page_icon="🏫")

# --- PROSTA BAZA UŻYTKOWNIKÓW (LOKALNA) ---
# Format: "użytkownik": "hasło"
USERS = {
    "student1": "sp56",
    "admin": "nauczyciel2024"
}

def login():
    st.title("Logowanie do Systemu Doradcy")
    username = st.text_input("Nazwa użytkownika")
    password = st.text_input("Hasło", type="password")
    
    if st.button("Zaloguj"):
        if username in USERS and USERS[username] == password:
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("Nieprawidłowe dane logowania")

# --- SPRAWDZENIE STATUSU LOGOWANIA ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
else:
    # --- MENU GŁÓWNE PO ZALOGOWANIU ---
    st.sidebar.button("Wyloguj", on_click=lambda: st.session_state.update({"logged_in": False}))
    
    st.title("Panel Lekcji Doradztwa Zawodowego")
    wybor_lekcji = st.selectbox(
        "Wybierz lekcję:",
        ["Strona Główna", "1. Poznajemy siebie", "2. Mój typ temperamentu"]
    )

    # --- LEKCJA 1 ---
    if wybor_lekcji == "1. Poznajemy siebie":
        st.header("Lekcja 1: Poznajemy siebie")
        st.write("W tej lekcji dowiesz się, jak analizować swoje mocne strony.")
        
        pytanie1 = st.text_area("Wymień swoje trzy główne zalety:")
        if st.button("Zapisz odpowiedzi (Lekcja 1)"):
            st.success("Odpowiedzi zostały zapisane tymczasowo!")

    # --- LEKCJA 2 ---
    elif wybor_lekcji == "2. Mój typ temperamentu":
        st.header("Lekcja 2: Mój typ temperamentu")
        st.write("Wybierz cechy, które najbardziej do Ciebie pasują:")
        
        typ = st.radio(
            "Jaki opis najlepiej Cię oddaje?",
            ["Energiczny i towarzyski", "Spokojny i analityczny", 
             "Wrażliwy i uczuciowy", "Zdecydowany i szybki"]
        )
        
        if st.button("Sprawdź wynik"):
            st.info(f"Twój zaznaczony profil to: {typ}. Porozmawiamy o tym na lekcji!")

    # --- STRONA GŁÓWNA ---
    else:
        st.write("Witaj w systemie! Wybierz lekcję z menu powyżej, aby rozpocząć.")
