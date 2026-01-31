import streamlit as st
import pandas as pd

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Cyfrowy Doradca Zawodowy", layout="wide")

# Tworzymy prostą tabelę "w locie" zamiast pobierać ją z Google
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame([
        {"login": "uczen1", "haslo": "123", "imie_nazwisko": "Jan Kowalski"},
        {"login": "test", "haslo": "test", "imie_nazwisko": "Uczeń Testowy"}
    ])

# --- SYSTEM LOGOWANIA ---
if 'zalogowany' not in st.session_state:
    st.session_state['zalogowany'] = False

if not st.session_state['zalogowany']:
    st.title("🔐 Logowanie")
    login_input = st.text_input("Login (użyj: uczen1)")
    pass_input = st.text_input("Hasło (użyj: 123)", type="password")
    
    if st.button("Zaloguj"):
        df = st.session_state.df
        user = df[(df['login'] == login_input) & (df['haslo'] == pass_input)]
        if not user.empty:
            st.session_state['zalogowany'] = True
            st.session_state['imie'] = user['imie_nazwisko'].values[0]
            st.rerun()
        else:
            st.error("Błędny login lub hasło.")
else:
    with st.sidebar:
        st.header(f"Witaj, {st.session_state['imie']}!")
        wybor = st.radio("Wybierz lekcję:", ["Lekcja 1: Poznaję Siebie", "Lekcja 2: Mój Temperament"])
        if st.button("Wyloguj"):
            st.session_state['zalogowany'] = False
            st.rerun()

    if wybor == "Lekcja 1: Poznaję Siebie":
        st.title("🧩 Lekcja 1: Poznaję Siebie")
        st.subheader("CO LUBIĘ? JAKIE MAM UMIEJĘTNOŚCI?")
        
        with st.form("lekcja1"):
            st.multiselect("Zaznacz swoje umiejętności:", ["Szybkie decyzje", "Słuchanie", "Logika", "Praca w grupie"])
            st.text_area("Twoje ulubione przedmioty:")
            if st.form_submit_button("Zapisz (tylko na sesję)"):
                st.success("Dane zapisane tymczasowo!")

    elif wybor == "Lekcja 2: Mój Temperament":
        st.title("⚖️ Lekcja 2: Temperament")
        
        
        with st.form("lekcja2"):
            c1, c2, c3, c4 = st.columns(4)
            s = c1.number_input("SANGWINIK", 0, 100)
            c = c2.number_input("CHOLERYK", 0, 100)
            m = c3.number_input("MELANCHOLIK", 0, 100)
            f = c4.number_input("FLEGMATYK", 0, 100)
            
            if st.form_submit_button("Pokaż wykres"):
                chart_data = pd.DataFrame({
                    'Typ': ['S', 'C', 'M', 'F'],
                    'Punkty': [s, c, m, f]
                })
                st.bar_chart(chart_data.set_index('Typ'))
