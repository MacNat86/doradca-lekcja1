import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Cyfrowy Doradca Zawodowy", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

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
    st.title("🔐 Logowanie do Systemu")
    col1, _ = st.columns([1, 2])
    with col1:
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

    # --- MENU BOCZNE ---
    with st.sidebar:
        st.header(f"Witaj, {imie}!")
        wybor = st.radio("Wybierz moduł:", ["Lekcja 1: Poznaję Siebie", "Lekcja 2: Test Temperamentu"])
        st.divider()
        if st.button("Wyloguj"):
            st.session_state['zalogowany'] = False
            st.rerun()

    # --- LEKCJA 1 (ZGODNIE Z PDF 1) ---
    if wybor == "Lekcja 1: Poznaję Siebie":
        st.title("🧩 Lekcja 1: Poznaję Siebie")
        st.subheader("POZNAJĘ SIEBIE // CO LUBIĘ? JAKIE MAM UMIEJĘTNOŚCI?")
        
        with st.form("form_lekcja1"):
            st.markdown("### Twoje Umiejętności")
            st.caption("Zastanów się, jakie masz umiejętności. Pomyśl o swoich zainteresowaniach, o tym w jakich tematach posiadasz wiedzę. Zaznacz wszystkie swoje umiejętności (nawet drobne).")
            
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
            odp_umiejetnosci = st.multiselect("Wybierz z listy:", lista_umiejetnosci, default=[x for x in default_skills if x in lista_umiejetnosci])
            
            st.divider()
            
            # Pytania dokładnie z pliku 1.pdf
            q1 = "Jakie są Twoje ulubione przedmioty szkolne? Co Ci się w nich podoba?"
            q2 = "Jakie przedmioty szkolne lubisz najmniej? Dlaczego?"
            q3 = "Za co zwykle chwalą Cię inni? Z czego Ty sam(a) jesteś dumny/dumna?"
            q4 = "Gdybyś nie musiał(a) się martwić o finanse, jak wyglądałaby Twoja wymarzona praca? Jak wyobrażasz sobie typowy dzień w takiej pracy?"
            q5 = "Czego zupełnie nie lubisz robić? Jakiej pracy na pewno nie mógłbyś/mogłabyś wykonywać w przyszłości? Dlaczego?"
            q6 = "Czego chciał(a)byś się nauczyć w ciągu najbliższych 5 lat? Umiejętności/wiedzę z jakiego obszaru pogłębić? (nie tylko w szkole, również na własną rękę)"

            st.write(f"**{q1}**")
            val1 = str(current_data['l1_ulubione']) if str(current_data['l1_ulubione']) != "nan" else ""
            odp1 = st.text_area("Twoja odpowiedź:", value=val1, key="q1", label_visibility="collapsed")

            st.write(f"**{q2}**")
            val2 = str(current_data['l1_nielubiane']) if str(current_data['l1_nielubiane']) != "nan" else ""
            odp2 = st.text_area("Twoja odpowiedź:", value=val2, key="q2", label_visibility="collapsed")

            st.write(f"**{q3}**")
            val3 = str(current_data['l1_duma']) if str(current_data['l1_duma']) != "nan" else ""
            odp3 = st.text_area("Twoja odpowiedź:", value=val3, key="q3", label_visibility="collapsed")

            st.write(f"**{q4}**")
            val4 = str(current_data['l1_finanse_ok']) if str(current_data['l1_finanse_ok']) != "nan" else ""
            odp4 = st.text_area("Twoja odpowiedź:", value=val4, key="q4", label_visibility="collapsed")

            st.write(f"**{q5}**")
            val5 = str(current_data['l1_anty_praca']) if str(current_data['l1_anty_praca']) != "nan" else ""
            odp5 = st.text_area("Twoja odpowiedź:", value=val5, key="q5", label_visibility="collapsed")

            st.write(f"**{q6}**")
            val6 = str(current_data['l1_cele_5lat']) if str(current_data['l1_cele_5lat']) != "nan" else ""
            odp6 = st.text_area("Twoja odpowiedź:", value=val6, key="q6", label_visibility="collapsed")

            if st.form_submit_button("💾 Zapisz moje refleksje"):
                df.at[idx, 'l1_umiejetnosci'] = ",".join(odp_umiejetnosci)
                df.at[idx, 'l1_ulubione'] = odp1
                df.at[idx, 'l1_nielubiane'] = odp2
                df.at[idx, 'l1_duma'] = odp3
                df.at[idx, 'l1_finanse_ok'] = odp4
                df.at[idx, 'l1_anty_praca'] = odp5
                df.at[idx, 'l1_cele_5lat'] = odp6
                conn.update(data=df)
                st.success("Wszystkie odpowiedzi z Lekcji 1 zostały zapisane!")

    # --- LEKCJA 2 (ZGODNIE Z TESTEM TEMPERAMENTU) ---
    elif wybor == "Lekcja 2: Test Temperamentu":
        st.title("⚖️ Lekcja 2: Temperament a zawód")
        st.write("Oceń stwierdzenia w skali 1-5 (1: Zdecydowanie nie, 5: Zdecydowanie tak).")
        
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
        ]

        skala = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
        wyniki = {"S": 0, "C": 0, "M": 0, "F": 0}
        
        with st.form("form_test_temp"):
            for i, (tekst, typ) in enumerate(pytania):
                odp = st.radio(tekst, options=list(skala.keys()), horizontal=True, index=2, key=f"quest_{i}")
                wyniki[typ] += skala[odp]
            
            st.divider()
            ref_val = str(current_data['l2_opis']) if 'l2_opis' in df.columns and str(current_data['l2_opis']) != "nan" else ""
            refleksja = st.text_area("Twoje wnioski po teście temperamentu:", value=ref_val)
            
            if st.form_submit_button("🚀 Oblicz i Zapisz Wyniki"):
                df.at[idx, 'l2_sangwinik'] = wyniki["S"]
                df.at[idx, 'l2_choleryk'] = wyniki["C"]
                df.at[idx, 'l2_melancholik'] = wyniki["M"]
                df.at[idx, 'l2_flegmatyk'] = wyniki["F"]
                df.at[idx, 'l2_opis'] = refleksja
                
                conn.update(data=df)
                
                max_typ = max(wyniki, key=wyniki.get)
                mapa_typow = {"S": "SANGWINIK", "C": "CHOLERYK", "M": "MELANCHOLIK", "F": "FLEGMATYK"}
                st.success(f"Wyniki zapisane! Dominujący typ: {mapa_typow[max_typ]}")
                
                wyniki_df = pd.DataFrame({
                    'Typ': ['Sangwinik', 'Choleryk', 'Melancholik', 'Flegmatyk'],
                    'Punkty': [wyniki["S"], wyniki["C"], wyniki["M"], wyniki["F"]]
                })
                st.bar_chart(wyniki_df.set_index('Typ'))
