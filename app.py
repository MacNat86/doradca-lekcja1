import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- KONFIGURACJA ---
st.set_page_config(page_title="Cyfrowy Doradca", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# Funkcja pobierająca dane
def get_data():
    # Pobieramy dane bez sztywnej nazwy arkusza, by uniknąć błędów
    return conn.read(ttl=0)

try:
    df = get_data()
except Exception as e:
    st.error(f"⚠️ Błąd połączenia z bazą danych. Sprawdź 'Secrets'. Szczegóły: {e}")
    st.stop()

# --- LOGOWANIE ---
if 'zalogowany' not in st.session_state:
    st.session_state['zalogowany'] = False
    st.session_state['user_row'] = -1

if not st.session_state['zalogowany']:
    st.title("🔐 Logowanie")
    col1, col2 = st.columns([1, 2])
    with col1:
        login_input = st.text_input("Login")
        pass_input = st.text_input("Hasło", type="password")
        
        if st.button("Zaloguj"):
            # Szukamy użytkownika w kolumnach 'login' i 'haslo' [cite: 7]
            user = df[(df['login'].astype(str) == login_input) & (df['haslo'].astype(str) == pass_input)]
            if not user.empty:
                st.session_state['zalogowany'] = True
                st.session_state['user_row'] = user.index[0]
                st.session_state['imie'] = user['imie_nazwisko'].values[0]
                st.rerun()
            else:
                st.error("Błędne dane. Sprawdź login i hasło w Arkuszu Google.")

else:
    # --- LEKCJA 1: POZNAJĘ SIEBIE ---
    imie = st.session_state['imie']
    idx = st.session_state['user_row']
    current_data = df.iloc[idx]

    with st.sidebar:
        st.header(f"Witaj, {imie}!")
        wybor = st.radio("Menu:", ["Lekcja 1: Poznaję Siebie"])
        if st.button("Wyloguj"):
            st.session_state['zalogowany'] = False
            st.rerun()

    if wybor == "Lekcja 1: Poznaję Siebie":
        st.title("🧩 Lekcja 1: Poznaję Siebie")
        st.markdown("Zapisz swoje odpowiedzi i refleksje zgodnie z dzisiejszymi zajęciami[cite: 8].")
        
        with st.form("form_lekcja1"):
            # 1. Umiejętności 
            st.subheader("1. Twoje Umiejętności")
            lista_umiejetnosci = [
                "Szybkie podejmowanie decyzji", "Dotrzymywanie terminów", "Umiejętność improwizacji",
                "Szybkie adaptowanie się do nowych warunków", "Słuchanie innych", "Organizowanie wydarzeń",
                "Szybkie uczenie się", "Przekazywanie wiedzy innym", "Inicjowanie działań",
                "Logiczne myślenie", "Łatwość w nawiązywaniu kontaktów", "Przemawianie publiczne",
                "Wytrwałe dążenie do celu", "Szybkie liczenie", "Uważne obserwowanie",
                "Wyciąganie wniosków", "Jednoczenie ludzi", "Dobra pamięć", "Łączenie faktów"
            ]
            # [cite: 12]
            
            saved_skills = str(current_data['l1_umiejetnosci'])
            default_skills = [x.strip() for x in saved_skills.split(",")] if saved_skills != "nan" else []
            odp_umiejetnosci = st.multiselect("Wybierz swoje umiejętności z listy:", lista_umiejetnosci, default=[x for x in default_skills if x in lista_umiejetnosci])
            
            st.divider()

            # 2. Preferencje przedmiotowe 
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("2. Co lubię?")
                val_fav = str(current_data['l1_ulubione']) if str(current_data['l1_ulubione']) != "nan" else ""
                odp_ulubione = st.text_area("Twoje ulubione przedmioty i co Ci się w nich podoba? ", value=val_fav)
            
            with c2:
                st.subheader("3. Czego nie lubię?")
                val_hate = str(current_data['l1_nielubiane']) if str(current_data['l1_nielubiane']) != "nan" else ""
                odp_nielubiane = st.text_area("Przedmioty, których lubisz najmniej i dlaczego? ", value=val_hate)

            st.divider()
            
            # 3. Duma i Przyszłość 
            st.subheader("4. Refleksje")
            val_duma = str(current_data['l1_duma']) if str(current_data['l1_duma']) != "nan" else ""
            odp_duma = st.text_input("Za co zwykle chwalą Cię inni? Z czego jesteś dumny/dumna? ", value=val_duma)
            
            c3, c4 = st.columns(2)
            with c3:
                st.write("💰 **Praca marzeń**")
                val_fin = str(current_data['l1_finanse_ok']) if str(current_data['l1_finanse_ok']) != "nan" else ""
                odp_finanse = st.text_area("Gdybyś nie musiał(a) się martwić o finanse, jak wyglądałaby Twoja praca? ", value=val_fin)
            with c4:
                st.write("⛔ **Anty-Praca**")
                val_anti = str(current_data['l1_anty_praca']) if str(current_data['l1_anty_praca']) != "nan" else ""
                odp_anty = st.text_area("Jakiej pracy na pewno nie mógłbyś/mogłabyś wykonywać? ", value=val_anti)

            st.subheader("5. Plan na 5 lat")
            val_cele = str(current_data['l1_cele_5lat']) if str(current_data['l1_cele_5lat']) != "nan" else ""
            odp_cele = st.text_input("Czego chciał(a)byś się nauczyć w ciągu najbliższych 5 lat? ", value=val_cele)

            if st.form_submit_button("💾 Zapisz moje odpowiedzi"):
                df.at[idx, 'l1_umiejetnosci'] = ",".join(odp_umiejetnosci)
                df.at[idx, 'l1_ulubione'] = odp_ulubione
                df.at[idx, 'l1_nielubiane'] = odp_nielubiane
                df.at[idx, 'l1_duma'] = odp_duma
                df.at[idx, 'l1_finanse_ok'] = odp_finanse
                df.at[idx, 'l1_anty_praca'] = odp_anty
                df.at[idx, 'l1_cele_5lat'] = odp_cele
                
                conn.update(data=df)
                st.success("Świetnie! Twoje refleksje zostały zapisane w systemie.")
