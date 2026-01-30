import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- KONFIGURACJA ---
st.set_page_config(page_title="Cyfrowy Doradca", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# Funkcja pobierająca dane bez pamięci podręcznej (ttl=0), żeby widzieć zmiany od razu
def get_data():
    return conn.read(worksheet="dane", ttl=0)

try:
    df = get_data()
except Exception:
    st.error("⚠️ Błąd połączenia z bazą danych. Upewnij się, że dodałeś link w 'Secrets'.")
    st.stop()

# --- LOGOWANIE ---
if 'zalogowany' not in st.session_state:
    st.session_state['zalogowany'] = False
    st.session_state['user_row'] = -1

if not st.session_state['zalogowany']:
    st.title("🔐 Logowanie")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.info("Zaloguj się, aby przejść do Lekcji 1.")
        login_input = st.text_input("Login")
        pass_input = st.text_input("Hasło", type="password")
        
        if st.button("Zaloguj"):
            # Sprawdzenie czy login i hasło pasują do bazy
            user = df[(df['login'] == login_input) & (df['haslo'] == pass_input)]
            if not user.empty:
                st.session_state['zalogowany'] = True
                st.session_state['user_row'] = user.index[0]
                st.session_state['imie'] = user['imie_nazwisko'].values[0]
                st.rerun()
            else:
                st.error("Błędne dane. Spróbuj: login=uczen, hasło=1234")

else:
    # --- TREŚĆ DLA ZALOGOWANEGO UCZNIA ---
    imie = st.session_state['imie']
    idx = st.session_state['user_row']
    
    # Pobranie aktualnych danych ucznia z tabeli
    current_data = df.iloc[idx]

    # Menu boczne
    with st.sidebar:
        st.header(f"Witaj, {imie}!")
        wybor = st.radio("Nawigacja:", ["Lekcja 1: Poznaję Siebie"])
        if st.button("Wyloguj"):
            st.session_state['zalogowany'] = False
            st.rerun()

    # --- LEKCJA 1 ---
    if wybor == "Lekcja 1: Poznaję Siebie":
        st.title("🧩 Lekcja 1: Poznaję Siebie")
        st.markdown("**Cel:** Zastanów się nad swoimi mocnymi stronami. Nie ma złych odpowiedzi!")
        
        with st.form("form_lekcja1"):
            
            # Zadanie 1: Umiejętności (z listy w PDF)
            st.subheader("1. Twoje Umiejętności")
            st.caption("Zaznacz te, które najlepiej Cię opisują:")
            
            lista_umiejetnosci = [
                "Szybkie podejmowanie decyzji", "Dotrzymywanie terminów", "Improwizacja",
                "Szybka adaptacja", "Słuchanie innych", "Organizowanie wydarzeń",
                "Szybkie uczenie się", "Przekazywanie wiedzy", "Inicjowanie działań",
                "Logiczne myślenie", "Nawiązywanie kontaktów", "Przemawianie publiczne",
                "Wytrwałość", "Szybkie liczenie", "Obserwacja", "Wyciąganie wniosków", 
                "Jednoczenie ludzi", "Dobra pamięć", "Łączenie faktów"
            ]
            
            # Odczytanie wcześniej zapisanych (jeśli są)
            saved_skills = str(current_data['l1_umiejetnosci'])
            default_skills = [x.strip() for x in saved_skills.split(",")] if saved_skills != "nan" else []
            # Filtrujemy tylko te, które są na liście (by uniknąć błędów)
            final_defaults = [x for x in default_skills if x in lista_umiejetnosci]

            odp_umiejetnosci = st.multiselect("Wybierz z listy:", lista_umiejetnosci, default=final_defaults)
            
            st.divider()

            # Zadanie 2: Lubię / Nie lubię
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("2. Ulubione przedmioty")
                saved_fav = str(current_data['l1_ulubione']) if str(current_data['l1_ulubione']) != "nan" else ""
                odp_ulubione = st.text_area("Co lubisz i dlaczego?", value=saved_fav)
            
            with c2:
                st.subheader("3. Czego nie lubię?")
                saved_hate = str(current_data['l1_nielubiane']) if str(current_data['l1_nielubiane']) != "nan" else ""
                odp_nielubiane = st.text_area("Jakich przedmiotów nie lubisz?", value=saved_hate)

            st.divider()
            
            # Zadanie 3: Duma i Przyszłość
            st.subheader("4. Z czego jesteś dumny/a?")
            saved_duma = str(current_data['l1_duma']) if str(current_data['l1_duma']) != "nan" else ""
            odp_duma = st.text_input("Za co chwalą Cię inni?", value=saved_duma)
            
            c3, c4 = st.columns(2)
            with c3:
                st.write("💰 **Gdyby finanse nie grały roli...**")
                saved_money = str(current_data['l1_finanse_ok']) if str(current_data['l1_finanse_ok']) != "nan" else ""
                odp_finanse = st.text_area("Jaki zawód byś wybrał/a?", value=saved_money)
            with c4:
                st.write("⛔ **Anty-Praca**")
                saved_anti = str(current_data['l1_anty_praca']) if str(current_data['l1_anty_praca']) != "nan" else ""
                odp_anty = st.text_area("Czego na pewno nie chcesz robić?", value=saved_anti)

            st.subheader("5. Cel na 5 lat")
            saved_cele = str(current_data['l1_cele_5lat']) if str(current_data['l1_cele_5lat']) != "nan" else ""
            odp_cele = st.text_input("Czego chcesz się nauczyć?", value=saved_cele)

            # Przycisk wysyłania
            submit = st.form_submit_button("💾 Zapisz Lekcję 1")
            
            if submit:
                # Aktualizacja danych w tabeli
                df.at[idx, 'l1_umiejetnosci'] = ",".join(odp_umiejetnosci)
                df.at[idx, 'l1_ulubione'] = odp_ulubione
                df.at[idx, 'l1_nielubiane'] = odp_nielubiane
                df.at[idx, 'l1_duma'] = odp_duma
                df.at[idx, 'l1_finanse_ok'] = odp_finanse
                df.at[idx, 'l1_anty_praca'] = odp_anty
                df.at[idx, 'l1_cele_5lat'] = odp_cele
                
                # Wysłanie do Google Sheets
                conn.update(worksheet="dane", data=df)
                st.success("Zapisano pomyślnie!")
