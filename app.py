import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- KONFIGURACJA ---
st.set_page_config(page_title="Cyfrowy Doradca", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    return conn.read(ttl=0)

try:
    df = get_data()
except Exception as e:
    st.error(f"⚠️ Błąd połączenia z bazą danych: {e}")
    st.stop()

# --- LOGOWANIE ---
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
            st.error("Błędne dane logowania.")
else:
    imie = st.session_state['imie']
    idx = st.session_state['user_row']
    current_data = df.iloc[idx]

    # --- MENU BOCZNE ---
    with st.sidebar:
        st.header(f"Witaj, {imie}!")
        wybor = st.radio("Wybierz zadanie:", ["Lekcja 1: Poznaję Siebie", "Lekcja 2: Test Temperamentu"])
        st.divider()
        if st.button("Wyloguj"):
            st.session_state['zalogowany'] = False
            st.rerun()

    # --- LEKCJA 1 (POWRÓT DO KODU) ---
    if wybor == "Lekcja 1: Poznaję Siebie":
        st.title("🧩 Lekcja 1: Poznaję Siebie")
        st.markdown("Zapisz swoje odpowiedzi i refleksje zgodnie z arkuszem.")
        
        with st.form("form_lekcja1"):
            st.subheader("Twoje Umiejętności")
            lista_umiejetnosci = ["Szybkie podejmowanie decyzji", "Dotrzymywanie terminów", "Improwizacja", "Szybka adaptacja", "Słuchanie innych", "Organizowanie wydarzeń", "Szybkie uczenie się", "Przekazywanie wiedzy", "Inicjowanie działań", "Logiczne myślenie", "Nawiązywanie kontaktów", "Przemawianie publiczne", "Wytrwałość", "Szybkie liczenie", "Obserwacja", "Wyciąganie wniosków", "Jednoczenie ludzi", "Dobra pamięć", "Łączenie faktów"]
            
            saved_skills = str(current_data['l1_umiejetnosci'])
            default_skills = [x.strip() for x in saved_skills.split(",")] if saved_skills != "nan" else []
            odp_umiejetnosci = st.multiselect("Zaznacz swoje mocne strony:", lista_umiejetnosci, default=[x for x in default_skills if x in lista_umiejetnosci])
            
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Co lubię?**")
                val_fav = str(current_data['l1_ulubione']) if str(current_data['l1_ulubione']) != "nan" else ""
                odp_ulubione = st.text_area("Ulubione przedmioty:", value=val_fav, key="l1_fav")
            with c2:
                st.write("**Czego nie lubię?**")
                val_hate = str(current_data['l1_nielubiane']) if str(current_data['l1_nielubiane']) != "nan" else ""
                odp_nielubiane = st.text_area("Nielubiane przedmioty:", value=val_hate, key="l1_hate")

            val_cele = str(current_data['l1_cele_5lat']) if str(current_data['l1_cele_5lat']) != "nan" else ""
            odp_cele = st.text_input("Cel na 5 lat:", value=val_cele)

            if st.form_submit_button("Zapisz Lekcję 1"):
                df.at[idx, 'l1_umiejetnosci'] = ",".join(odp_umiejetnosci)
                df.at[idx, 'l1_ulubione'] = odp_ulubione
                df.at[idx, 'l1_nielubiane'] = odp_nielubiane
                df.at[idx, 'l1_cele_5lat'] = odp_cele
                conn.update(data=df)
                st.success("Dane z Lekcji 1 zostały zaktualizowane!")

    # --- LEKCJA 2 (TEST TEMPERAMENTU) ---
    elif wybor == "Lekcja 2: Test Temperamentu":
        st.title("⚖️ Lekcja 2: Temperament a przyszły zawód")
        st.info("Zaznacz odpowiedzi zgodnie ze skalą (1-Zdecydowanie nie, 5-Zdecydowanie tak)[cite: 18, 19, 23].")
        
        pytania = [
            ("1. Lubię być w centrum uwagi.", "S"), ("2. Często podejmuję szybkie decyzje.", "C"),
            ("3. Często analizuję różne sytuacje i ich konsekwencje.", "M"), ("4. Jestem spokojny i opanowany w stresie.", "F"),
            ("5. Lubię nawiązywać nowe znajomości.", "S"), ("6. Mam tendencję do dominowania w grupie.", "C"),
            ("7. Lubię szczegółowo planować swoje działania.", "M"), ("8. Wolę działać we własnym tempie.", "F"),
            ("9. Łatwo nawiązuję kontakty z innymi.", "S"), ("10. Jestem zdecydowany i pewny siebie.", "C"),
            ("11. Często rozmyślam nad sensem życia.", "M"), ("12. Unikam konfrontacji w konfliktach.", "F"),
            ("13. Często żartuję w grupie.", "S"), ("14. Lubię wyznaczać i realizować cele.", "C"),
            ("15. Jestem perfekcjonistą.", "M"), ("16. Działam w uporządkowany sposób.", "F"),
            ("17. Często jestem duszą towarzystwa.", "S"), ("18. Lubię rywalizację i wyzwania.", "C"),
            ("19. Jestem bardzo wrażliwy na krytykę.", "M"), ("20. Potrafię pracować pod presją czasu.", "F")
        ] [cite: 25, 32, 38, 51, 52, 64, 65, 72, 86, 87, 93, 98, 107, 108, 119, 120, 126, 132, 138, 149]

        skala = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
        wyniki = {"S": 0, "C": 0, "M": 0, "F": 0}
        
        with st.form("test_temperamentu"):
            for i, (tekst, typ) in enumerate(pytania):
                odp = st.radio(tekst, options=list(skala.keys()), horizontal=True, index=2, key=f"t{i}")
                wyniki[typ] += skala[odp]
            
            refleksja = st.text_area("Twoje wnioski po teście:", value=str(current_data['l2_opis']) if str(current_data['l2_opis']) != "nan" else "")
            
            if st.form_submit_button("Oblicz i zapisz wyniki"):
                df.at[idx, 'l2_sangwinik'] = wyniki["S"]
                df.at[idx, 'l2_choleryk'] = wyniki["C"]
                df.at[idx, 'l2_melancholik'] = wyniki["M"]
                df.at[idx, 'l2_flegmatyk'] = wyniki["F"]
                df.at[idx, 'l2_opis'] = refleksja
                conn.update(data=df)
                st.success(f"Wyniki zapisane! Dominujący typ: {max(wyniki, key=wyniki.get)}")
