import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Cyfrowy Doradca Zawodowy", layout="wide")

# AUTOMATYCZNA NAPRAWA KLUCZA (To eliminuje ValueError)
conf = st.secrets["connections"]["gsheets"].to_dict()
if "private_key" in conf:
    conf["private_key"] = conf["private_key"].replace("\\n", "\n")

# Nawiązanie połączenia z użyciem poprawionej konfiguracji
conn = st.connection("gsheets", type=GSheetsConnection, **conf)

def get_data():
    return conn.read(ttl=0)

try:
    df = get_data()
except Exception as e:
    st.error(f"⚠️ Błąd połączenia z bazą danych: {e}")
    st.stop()

# --- SYSTEM LOGOWANIA ---
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
        st.subheader("POZNAJĘ SIEBIE // CO LUBIĘ? JAKIE MAM UMIEJĘTNOŚCI?")
        
        with st.form("form_lekcja1"):
            st.markdown("### Twoje Umiejętności")
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
            
            odp1 = st.text_area("Ulubione przedmioty:", value=str(current_data['l1_ulubione']) if str(current_data['l1_ulubione']) != "nan" else "")
            odp2 = st.text_area("Czego nie lubisz?", value=str(current_data['l1_nielubiane']) if str(current_data['l1_nielubiane']) != "nan" else "")

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
            with c1: s_pkt = st.number_input("SANGWINIK", min_value=0, value=int(current_data['l2_sangwinik']) if not pd.isna(current_data['l2_sangwinik']) else 0)
            with c2: c_pkt = st.number_input("CHOLERYK", min_value=0, value=int(current_data['l2_choleryk']) if not pd.isna(current_data['l2_choleryk']) else 0)
            with c3: m_pkt = st.number_input("MELANCHOLIK", min_value=0, value=int(current_data['l2_melancholik']) if not pd.isna(current_data['l2_melancholik']) else 0)
            with c4: f_pkt = st.number_input("FLEGMATYK", min_value=0, value=int(current_data['l2_flegmatyk']) if not pd.isna(current_data['l2_flegmatyk']) else 0)
            
            if st.form_submit_button("📊 Przelicz i Zapisz"):
                df.at[idx, 'l2_sangwinik'] = s_pkt
                df.at[idx, 'l2_choleryk'] = c_pkt
                df.at[idx, 'l2_melancholik'] = m_pkt
                df.at[idx, 'l2_flegmatyk'] = f_pkt
                conn.update(data=df)
                st.success("Zapisano!")
                chart_data = pd.DataFrame({'Typ': ['S', 'C', 'M', 'F'], 'Punkty': [s_pkt, c_pkt, m_pkt, f_pkt]})
                st.bar_chart(chart_data.set_index('Typ'))
