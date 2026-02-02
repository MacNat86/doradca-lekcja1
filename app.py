import streamlit as st
import pandas as pd

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Cyfrowy Doradca Zawodowy", layout="wide")

# Logika logowania
if 'zalogowany' not in st.session_state:
    st.session_state['zalogowany'] = False

if not st.session_state['zalogowany']:
    st.title("🔐 Logowanie")
    login = st.text_input("Login")
    haslo = st.text_input("Hasło", type="password")
    if st.button("Zaloguj"):
        if login == "admin" and haslo == "123":
            st.session_state['zalogowany'] = True
            st.rerun()
        else:
            st.error("Błędne dane.")
else:
    with st.sidebar:
        st.header("Menu")
        wybor = st.radio("Wybierz lekcję:", [
            "Lekcja 1: Poznaję Siebie", 
            "Lekcja 2: Mój Temperament", 
            "Lekcja 3: Różne mózgi - różne zawody"
        ])
        st.divider()
        if st.button("Wyloguj"):
            st.session_state['zalogowany'] = False
            st.rerun()

    # --- LEKCJA 1: POZNAJĘ SIEBIE ---
    if wybor == "Lekcja 1: Poznaję Siebie":
        st.title("🧩 Lekcja 1: Poznaję Siebie")
        with st.form("l1_form"):
            st.subheader("1. Moje Umiejętności")
            lista_umiejetnosci = [
                "Szybkie podejmowanie decyzji", "Dotrzymywanie terminów", "Umiejętność improwizacji",
                "Szybkie adaptowanie się", "Słuchanie innych", "Organizowanie wydarzeń",
                "Szybkie uczenie się", "Przekazywanie wiedzy innym", "Inicjowanie działań",
                "Logiczne myślenie", "Łatwość w nawiązywaniu kontaktów", "Przemawianie publiczne",
                "Wytrwałe dążenie do celu", "Szybkie liczenie", "Uważne obserwowanie",
                "Wyciąganie wniosków", "Jednoczenie ludzi", "Dobra pamięć", "Łączenie faktów"
            ]
            st.multiselect("Zaznacz swoje umiejętności:", options=lista_umiejetnosci)
            
            c1, c2 = st.columns(2)
            with c1:
                st.text_area("2. Jakie przedmioty lubisz i co Ci się w nich podoba?")
            with c2:
                st.text_area("3. Jakich przedmiotów nie lubisz i dlaczego?")
            
            st.text_input("4. Za co chwalą Cię inni? Z czego Ty jesteś dumny/a?")
            
            c3, c4 = st.columns(2)
            with c3:
                st.text_area("5. Gdyby pieniądze nie grały roli, jaki zawód chciałbyś wykonywać?")
            with c4:
                st.text_area("6. W jakim zawodzie na pewno nie chciałbyś pracować?")
            
            st.text_input("7. Czego chciałbyś/chciałabyś się nauczyć w przeciągu 5 lat?")
            
            if st.form_submit_button("Zapisz Lekcję 1"):
                st.success("Zapisano odpowiedzi z Lekcji 1.")

    # --- LEKCJA 2: MÓJ TEMPERAMENT ---
    elif wybor == "Lekcja 2: Mój Temperament":
        st.title("⚖️ Lekcja 2: Mój Temperament")
        with st.form("l2_form"):
            col1, col2 = st.columns(2)
            s = col1.number_input("SANGWINIK", 0, 100)
            c = col2.number_input("CHOLERYK", 0, 100)
            m = col1.number_input("MELANCHOLIK", 0, 100)
            f = col2.number_input("FLEGMATYK", 0, 100)
            
            if st.form_submit_button("Pokaż wykres"):
                dane = pd.DataFrame({'Typ': ['S', 'C', 'M', 'F'], 'Punkty': [s, c, m, f]})
                st.bar_chart(dane.set_index('Typ'))

    # --- LEKCJA 3: RÓŻNE MÓZGI - RÓŻNE ZAWODY ---
    elif wybor == "Lekcja 3: Różne mózgi - różne zawody":
        st.title("🧠 Lekcja 3: Różne mózgi - różne zawody")
        st.subheader("Test Samooceny Dominacji Półkul Mózgowych")
        st.info("Przeczytaj uważnie każde pytanie i wybierz odpowiedź, która najlepiej opisuje Ciebie.")

        with st.form("test_mozgu"):
            # Pytania z PDF [cite: 5-35]
            q1 = st.radio("1. Co robisz, gdy napotykasz problem?", ["a) Analizuję problem krok po kroku i szukam logicznego rozwiązania.", "b) Staram się znaleźć twórcze, nietypowe rozwiązanie."])
            q2 = st.radio("2. Jak zazwyczaj zapamiętujesz nowe informacje?", ["a) Lubię robić notatki i układać informacje w logiczną całość.", "b) Łatwiej zapamiętuję, gdy widzę obrazy lub schematy."])
            q3 = st.radio("3. Jakie przedmioty w szkole lubisz najbardziej?", ["a) Matematyka, język polski, nauki ścisłe.", "b) Plastyka, muzyka, zajęcia techniczne."])
            q4 = st.radio("4. Jak podchodzisz do organizacji czasu?", ["a) Zawsze planuję swój dzień i trzymam się ustalonego harmonogramu.", "b) Działam spontanicznie i lubię improwizować."])
            q5 = st.radio("5. Jak wyrażasz swoje emocje?", ["a) Często werbalnie opisuję swoje uczucia.", "b) Wyrażam emocje przez sztukę, muzykę lub ruch."])
            q6 = st.radio("6. Jak lubisz pracować nad projektami?", ["a) Skupiam się na szczegółach i analizie danych.", "b) Wolę podejście całościowe i twórcze, z naciskiem na wizję końcową."])
            q7 = st.radio("7. Co jest dla Ciebie łatwiejsze?", ["a) Rozwiązywanie zadań logicznych i matematycznych.", "b) Tworzenie prac plastycznych lub muzycznych."])
            q8 = st.radio("8. Jak radzisz sobie z nauką nowych rzeczy?", ["a) Wolę szczegółowe instrukcje i ścisłe wytyczne.", "b) Wolę uczyć się przez doświadczenie i eksperymenty."])
            q9 = st.radio("9. Co wolisz robić w wolnym czasie?", ["a) Czytać książki, rozwiązywać krzyżówki lub uczyć się czegoś nowego.", "b) Rysować, grać na instrumencie, tworzyć coś własnymi rękami."])
            q10 = st.radio("10. Jak zazwyczaj rozwiązujesz konflikt?", ["a) Rozmawiam i staram się znaleźć racjonalne rozwiązanie.", "b) Staram się zrozumieć emocje innych i szukam kreatywnych rozwiązań."])

            if st.form_submit_button("📊 Sprawdź mój wynik"):
                odpowiedzi = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
                count_a = sum(1 for x in odpowiedzi if x.startswith("a"))
                count_b = sum(1 for x in odpowiedzi if x.startswith("b"))
                
                st.divider()
                if count_a > count_b:
                    st.success("Dominacja LEWEJ półkuli")
                    st.write("**Charakterystyka:** Logiczne myślenie, analityczność i systematyczność. [cite: 37]")
                    st.write("**Zawody:** Analityk finansowy, Programista, Inżynier, Nauczyciel matematyki, Prawnik. [cite: 40-44]")
                elif count_b > count_a:
                    st.success("Dominacja PRAWEJ półkuli")
                    st.write("**Charakterystyka:** Kreatywność, intuicja i wyobraźnia wizualna. [cite: 49]")
                    st.write("**Zawody:** Grafik, Projektant mody, Muzyk, Architekt, Projektant gier. [cite: 52-55, 59]")
                else:
                    st.info("Zrównoważona dominacja obu półkul")
                    st.write("**Charakterystyka:** Łączysz logikę z innowacyjnością. [cite: 63]")
                    st.write("**Zawody:** Menedżer projektów, Psycholog, Przedsiębiorca. [cite: 65, 68, 69]")
