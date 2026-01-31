import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Cyfrowy Doradca Zawodowy", layout="wide")

# FUNKCJA NAPRAWIAJĄCA KLUCZ (Zapobiega błędom formatowania w Secrets)
def get_fixed_connection():
    try:
        # Pobieramy dane z secrets
        s = st.secrets["connections"]["gsheets"]
        # Budujemy słownik ręcznie, naprawiając znaki nowej linii
        creds = {
            "type": s["type"],
            "project_id": s["project_id"],
            "private_key_id": s["private_key_id"],
            "private_key": s["private_key"].replace("\\n", "\n"),
            "client_email": s["client_email"],
            "client_id": s["client_id"],
            "auth_uri": s["auth_uri"],
            "token_uri": s["token_uri"],
            "auth_provider_x509_cert_url": s["auth_provider_x509_cert_url"],
            "client_x509_cert_url": s["client_x509_cert_url"],
        }
        return st.connection("gsheets", type=GSheetsConnection, **creds)
    except Exception as e:
        st.error(f"Problem z konfiguracją klucza w Secrets: {e}")
        st.stop()

conn = get_fixed_connection()

def get_data():
    return conn.read(ttl=0)

try:
    df = get_data()
except Exception as e:
    st.error(f"⚠️ Błąd połączenia z bazą danych Google Sheets: {e}")
    st.info("Sprawdź, czy adres URL arkusza w Secrets jest poprawny.")
    st.stop()

# --- SYSTEM LOGOWANIA ---
if 'zalogowany' not in st.session_state:
    st.session_state['zalogowany'] = False

if not st.session_state['zalogowany']:
    st.title("🔐 Logowanie")
    login_input = st.text_input("Login")
    pass_input = st.text_input("Hasło", type="password")
    if st.button("Zaloguj"):
        # Konwersja na string, żeby uniknąć problemów z typami danych
        user = df[(df['login'].astype(str) == str(login_input)) & (df['haslo'].astype(str) == str(pass_input))]
        if not user.empty:
            st.session_state['zalogowany'] = True
            st.session_state['user_row'] = user.index[0]
            st.session_state['imie'] = user['imie_nazwisko'].values[0]
            st.rerun()
        else:
            st.error("Błędny login lub hasło.")
else:
    imie = st.session_state['imie']
    idx = st.session_state['user_row']
    current_data = df.iloc[idx]

    with st.sidebar:
        st.header(f"Witaj, {imie}!")
        wybor = st.radio("Wybierz lekcję:", ["Lekcja 1: Poznaję Siebie", "Lekcja 2: Mój Temperament"])
        st.divider()
        if st.button("Wyloguj"):
            st.session_state['zalogowany'] = False
            st.rerun()

    # --- LEKCJA 1 ---
    if wybor == "Lekcja 1: Poznaję Siebie":
        st.title("🧩 Lekcja 1: Poznaję Siebie")
        st.subheader("CO LUBIĘ? JAKIE MAM UMIEJĘTNOŚCI?")
        
        with st.form("form_lekcja1"):
            st.markdown("### Your Skills")
            lista_umiejetnosci = [
                "Szybkie podejmowanie decyzji", "Dotrzymywanie terminów", "Umiejętność improwizacji",
                "Szybka adaptacja do nowych warunków", "Słuchanie innych", "Organizowanie wydarzeń",
                "Szybkie uczenie się", "Przekazywanie wiedzy innym", "Inicjowanie działań",
                "Logiczne myślenie", "Łatwość w nawiązywaniu kontaktów", "Przemawianie publiczne",
                "Wytrwałe dążenie do celu", "Szybkie liczenie", "Uważne obserwowanie",
                "Wyciąganie wniosków", "Jednoczenie ludzi", "Dobra pamięć", "Łączenie faktów"
            ]
            saved_skills = str(current_data['l1_umiejetnosci'])
            default_skills = [x.strip() for x in saved_skills.split(",")] if saved_skills != "nan" else []
            odp_umiejetnosci = st.multiselect("Zaznacz swoje umiejętności:", lista_umiejetnosci, default=[x for x in default_skills if x in lista_umiejetnosci])
            
            st.divider()
            
            odp1 = st.text_area("Jakie są Twoje ulubione przedmioty?", value=str(current_data['l1_ulubione']) if str(current_data['l1_ulubione']) != "nan" else "")
            odp2 = st.text_area("Jakich nie lubisz?", value=str(current_data['l1_nielubiane']) if str(current_data['l1_nielubiane']) != "nan" else "")

            if st.form_submit_button("💾 Zapisz Lekcję 1"):
                df.at[idx, 'l1_umiejetnosci'] = ",".join(odp_umiejetnosci)
                df.at[idx, 'l1_ulubione'] = odp1
                df.at[idx, 'l1_nielubiane'] = odp2
                conn.update(data=df)
                st.success("Zapisano!")

    # --- LEKCJA 2 ---
    elif wybor == "Lekcja 2: Mój Temperament":
        st.title("⚖️ Lekcja 2: Temperament a zawód")
        
        with st.form("form_wyniki_temp"):
            c1, c2, c3, c4 = st.columns(4)
            with c1: s_pkt = st.number_input("SANGWINIK", value=int(current_data['l2_sangwinik']) if not pd.isna(current_data['l2_sangwinik']) else 0)
            with c2: c_pkt = st.number_input("CHOLERYK", value=int(current_data['l2_choleryk']) if not pd.isna(current_data['l2_choleryk']) else 0)
            with c3: m_pkt = st.number_input("MELANCHOLIK", value=int(current_data['l2_melancholik']) if not pd.isna(current_data['l2_melancholik']) else 0)
            with c4: f_pkt = st.number_input("FLEGMATYK", value=int(current_data['l2_flegmatyk']) if not pd.isna(current_data['l2_flegmatyk']) else 0)
            
            if st.form_submit_button("📊 Zapisz i pokaż wykres"):
                df.at[idx, 'l2_sangwinik'] = s_pkt
                df.at[idx, 'l2_choleryk'] = c_pkt
                df.at[idx, 'l2_melancholik'] = m_pkt
                df.at[idx, 'l2_flegmatyk'] = f_pkt
                conn.update(data=df)
                st.bar_chart(pd.DataFrame({'Typ': ['S', 'C', 'M', 'F'], 'Pkt': [s_pkt, c_pkt, m_pkt, f_pkt]}).set_index('Typ'))
