import streamlit as st
import pandas as pd

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Cyfrowy Doradca Zawodowy", layout="wide")

# Lista użytkowników wpisana na sztywno w kodzie (punkt wyjścia)
if 'df_uzytkownicy' not in st.session_state:
    st.session_state.df_uzytkownicy = pd.DataFrame([
        {"login": "uczen1", "haslo": "123", "imie_nazwisko": "Jan Kowalski"},
        {"login": "test", "haslo": "test", "imie_nazwisko": "Uczeń Testowy"}
    ])

# --- SYSTEM LOGOWANIA ---
if 'zalogowany' not in st.session_state:
    st.session_state['zalogowany'] = False

if not st.session_state['zalogowany']:
    st.title("🔐 Logowanie")
    st.info("Wpisz login: uczen1 i hasło: 123")
    login_input = st.text_input("Login")
    pass_input = st.text_input("Hasło", type="password")
    
    if st.button("Zaloguj"):
        df = st.session_state.df_uzytkownicy
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
        st.divider()
        if st.button("Wyloguj"):
            st.session_state['zalogowany'] = False
            st.rerun()

    # --- LEKCJA 1 (PEŁNA TREŚĆ) ---
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
            st.multiselect("Zaznacz swoje umiejętności:", lista_umiejetnosci)
            
            st.divider()
            
            st.write("**1. Jakie są Twoje ulubione przedmioty szkolne? Co Ci się w nich podoba?**")
            st.text_area("Odpowiedź:", key="q1")

            st.write("**2. Jakie przedmioty szkolne lubisz najmniej? Dlaczego?**")
            st.text_area("Odpowiedź:", key="q2")

            st.write("**3. Za co zwykle chwalą Cię inni? Z czego Ty sam(a) jesteś dumny/dumna?**")
            st.text_area("Odpowiedź:", key="q3")

            st.write("**4. Gdybyś nie musiał(a) się martwić o finanse, jak wyglądałaby Twoja wymarzona praca?**")
            st.text_area("Odpowiedź:", key="q4")

            st.write("**5. Jakiej pracy na pewno nie mógłbyś/mogłabyś wykonywać w przyszłości? Dlaczego?**")
            st.text_area("Odpowiedź:", key="q5")

            st.write("**6. Czego chciał(a)byś się nauczyć w ciągu najbliższych 5 lat?**")
            st.text_area("Odpowiedź:", key="q6")

            if st.form_submit_button("💾 Zapisz odpowiedzi (tymczasowo)"):
                st.success("Zapisano! (Dane są widoczne tylko w tej sesji)")

    # --- LEKCJA 2 ---
    elif wybor == "Lekcja 2: Mój Temperament":
        st.title("⚖️ Lekcja 2: Temperament a zawód")
        
        st.info("Wpisz wyniki testu z kartki, aby zobaczyć swój wykres.")
        
        with st.form("form_lekcja2"):
            col1, col2, col3, col4 = st.columns(4)
            s = col1.number_input("SANGWINIK", 0, 100, 0)
            c = col2.number_input("CHOLERYK", 0, 100, 0)
            m = col3.number_input("MELANCHOLIK", 0, 100, 0)
            f = col4.number_input("FLEGMATYK", 0, 100, 0)
            
            refleksja = st.text_area("Twoje wnioski:")
            
            if st.form_submit_button("📊 Generuj Wykres"):
                st.success("Wygenerowano podsumowanie!")
                chart_data = pd.DataFrame({
                    'Typ': ['Sangwinik', 'Choleryk', 'Melancholik', 'Flegmatyk'],
                    'Punkty': [s, c, m, f]
                })
                st.bar_chart(chart_data.set_index('Typ'))
