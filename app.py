import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Cyfrowy Doradca", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    return conn.read(ttl=0)

try:
    df = get_data()
except Exception as e:
    st.error(f"⚠️ Błąd połączenia: {e}")
    st.stop()

if 'zalogowany' not in st.session_state:
    st.session_state['zalogowany'] = False

if not st.session_state['zalogowany']:
    st.title("🔐 Logowanie")
    login_input = st.text_input("Login")
    pass_input = st.text_input("Hasło", type="password")
    if st.button("Zaloguj"):
        user = df[(df['login'].astype(str) == login_input) & (df['haslo'].astype(str) == pass_input)]
        if not user.empty:
            st.session_state['zalogowany'] = True
            st.session_state['user_row'] = user.index[0]
            st.session_state['imie'] = user['imie_nazwisko'].values[0]
            st.rerun()
else:
    imie = st.session_state['imie']
    idx = st.session_state['user_row']
    current_data = df.iloc[idx]

    with st.sidebar:
        st.header(f"Witaj, {imie}!")
        wybor = st.radio("Menu lekcji:", ["Lekcja 1: Poznaję Siebie", "Lekcja 2: Temperament"])
        if st.button("Wyloguj"):
            st.session_state['zalogowany'] = False
            st.rerun()

    if wybor == "Lekcja 1: Poznaję Siebie":
        st.title("🧩 Lekcja 1: Poznaję Siebie")
        # ... (kod z poprzedniej lekcji pozostaje bez zmian w Twoim app.py) ...
        st.info("Tutaj znajduje się formularz Lekcji 1.")

    elif wybor == "Lekcja 2: Temperament":
        st.title("⚖️ Lekcja 2: Temperament a zawód")
        st.write("Wypełnij poniższy test, aby poznać swój dominujący typ temperamentu.")
        
        # Definicja pytań i przypisanie do typów (S-Sangwinik, C-Choleryk, M-Melancholik, F-Flegmatyk)
        pytania = [
            ("1. Lubię być w centrum uwagi.", "S"),
            ("2. Często podejmuję szybkie decyzje.", "C"),
            ("3. Często analizuję różne sytuacje i staram się przewidzieć ich konsekwencje.", "M"),
            ("4. Jestem spokojny i opanowany nawet w stresujących sytuacjach.", "F"),
            ("5. Lubię nawiązywać nowe znajomości.", "S"),
            ("6. Mam tendencję do dominowania w grupie.", "C"),
            ("7. Lubię szczegółowo planować swoje działania.", "M"),
            ("8. Nie lubię się spieszyć i wolę działać we własnym tempie.", "F"),
            ("9. Łatwo nawiązuję kontakty z innymi.", "S"),
            ("10. Jestem zdecydowany i pewny siebie.", "C"),
            ("11. Często rozmyślam nad sensem życia i moim miejscem na świecie.", "M"),
            ("12. W sytuacjach konfliktowych staram się unikać konfrontacji.", "F"),
            ("13. Często żartuję i staram się rozładować napięcie w grupie.", "S"),
            ("14. Lubię wyznaczać cele i dążyć do ich realizacji.", "C"),
            ("15. Jestem perfekcjonistą i staram się wszystko robić jak najlepiej.", "M"),
            ("16. Lubię działać w uporządkowany i systematyczny sposób.", "F"),
            ("17. Często jestem duszą towarzystwa.", "S"),
            ("18. Lubię rywalizację i wyzwania.", "C"),
            ("19. Jestem bardzo wrażliwy na krytykę.", "M"),
            ("20. Mam zdolność do pracy pod presją czasu.", "F")
        ]

        skala = {
            "Zdecydowanie nie": 1,
            "Raczej nie": 2,
            "Trudno powiedzieć": 3,
            "Raczej tak": 4,
            "Zdecydowanie tak": 5
        }

        wyniki = {"S": 0, "C": 0, "M": 0, "F": 0}
        
        with st.form("test_temperamentu"):
            for i, (tekst, typ) in enumerate(pytania):
                odp = st.select_slider(tekst, options=list(skala.keys()), value="Trudno powiedzieć", key=f"q{i}")
                wyniki[typ] += skala[odp]
            
            refleksja = st.text_area("Twoje wnioski - który typ u Ciebie dominuje i jak to wpływa na wybór zawodu?")
            
            if st.form_submit_button("Oblicz i zapisz wyniki"):
                df.at[idx, 'l2_sangwinik'] = wyniki["S"]
                df.at[idx, 'l2_choleryk'] = wyniki["C"]
                df.at[idx, 'l2_melancholik'] = wyniki["M"]
                df.at[idx, 'l2_flegmatyk'] = wyniki["F"]
                df.at[idx, 'l2_opis'] = refleksja
                
                conn.update(data=df)
                st.success(f"Wyniki zapisane! S: {wyniki['S']}, C: {wyniki['C']}, M: {wyniki['M']}, F: {wyniki['F']}")
                
                # Wyświetlenie interpretacji
                max_typ = max(wyniki, key=wyniki.get)
                opisy = {
                    "S": "Jesteś Sangwinikiem – osobą towarzyską i optymistyczną.",
                    "C": "Jesteś Cholerykiem – osobą dynamiczną i nastawioną na cel.",
                    "M": "Jesteś Melancholikiem – osobą analityczną i wrażliwą.",
                    "F": "Jesteś Flegmatykiem – osobą spokojną i cierpliwą."
                }
                st.info(opisy[max_typ])
