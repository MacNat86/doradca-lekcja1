import streamlit as st
import pandas as pd

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Cyfrowy Doradca Zawodowy", layout="wide")

# Logika logowania (Login: admin, Hasło: 123)
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

    # --- LEKCJA 1 (Twoja stała treść) ---
    if wybor == "Lekcja 1: Poznaję Siebie":
        st.title("🧩 Lekcja 1: Poznaję Siebie")
        with st.form("l1_form"):
            st.subheader("1. Moje Umiejętności")
            lista_umiejetnosci = ["Szybkie podejmowanie decyzji", "Dotrzymywanie terminów", "Umiejętność improwizacji", "Szybkie adaptowanie się", "Słuchanie innych", "Organizowanie wydarzeń", "Szybkie uczenie się", "Przekazywanie wiedzy innym", "Inicjowanie działań", "Logiczne myślenie", "Łatwość w nawiązywaniu kontaktów", "Przemawianie publiczne", "Wytrwałe dążenie do celu", "Szybkie liczenie", "Uważne obserwowanie", "Wyciąganie wniosków", "Jednoczenie ludzi", "Dobra pamięć", "Łączenie faktów"]
            st.multiselect("Zaznacz swoje umiejętności:", options=lista_umiejetnosci)
            c1, c2 = st.columns(2)
            with c1: st.text_area("2. Jakie przedmioty lubisz i co Ci się w nich podoba?")
            with c2: st.text_area("3. Jakich przedmiotów nie lubisz i dlaczego?")
            st.text_input("4. Za co chwalą Cię inni? Z czego Ty jesteś dumny/a?")
            c3, c4 = st.columns(2)
            with c3: st.text_area("5. Gdyby pieniądze nie grały roli, jaki zawód chciałbyś wykonywać?")
            with c4: st.text_area("6. W jakim zawodzie na pewno nie chciałbyś pracować?")
            st.text_input("7. Czego chciałbyś/chciałabyś się nauczyć w przeciągu 5 lat?")
            if st.form_submit_button("Zapisz Lekcję 1"):
                st.success("Zapisano.")

    # --- LEKCJA 2 (Twoja stała treść) ---
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

    # --- LEKCJA 3: RÓŻNE MÓZGI (Zmodyfikowana zgodnie z prośbą) ---
    elif wybor == "Lekcja 3: Różne mózgi - różne zawody":
        st.title("🧠 Lekcja 3: Różne mózgi - różne zawody")
        st.info("Wybierz odpowiedzi, które najlepiej Cię opisują. Kolejność opcji jest wymieszana.")

        # Definicja pytań (L = Lewa, R = Prawa)
        questions = [
            {"q": "1. Co robisz, gdy napotykasz problem?", "L": "Analizuję problem krok po kroku i szukam logicznego rozwiązania.", "R": "Staram się znaleźć twórcze, nietypowe rozwiązanie."},
            {"q": "2. Jak zazwyczaj zapamiętujesz nowe informacje?", "R": "Łatwiej zapamiętuję, gdy widzę obrazy lub schematy.", "L": "Lubię robić notatki i układać informacje w logiczną całość."},
            {"q": "3. Jakie przedmioty w szkole lubisz najbardziej?", "L": "Matematyka, język polski, nauki ścisłe.", "R": "Plastyka, muzyka, zajęcia techniczne."},
            {"q": "4. Jak podchodzisz do organizacji czasu?", "R": "Działam spontanicznie i lubię improwizować.", "L": "Zawsze planuję swój dzień i trzymam się ustalonego harmonogramu."},
            {"q": "5. Jak wyrażasz swoje emocje?", "L": "Często werbalnie opisuję swoje uczucia.", "R": "Wyrażam emocje przez sztukę, muzykę lub ruch."},
            {"q": "6. Jak lubisz pracować nad projektami?", "R": "Wolę podejście całościowe i twórcze, z naciskiem na wizję końcową.", "L": "Skupiam się na szczegółach i analizie danych."},
            {"q": "7. Co jest dla Ciebie łatwiejsze?", "L": "Rozwiązywanie zadań logicznych i matematycznych.", "R": "Tworzenie prac plastycznych lub muzycznych."},
            {"q": "8. Jak radzisz sobie z nauką nowych rzeczy?", "R": "Wolę uczyć się przez doświadczenie i eksperymenty.", "L": "Wolę szczegółowe instrukcje i ścisłe wytyczne."},
            {"q": "9. Co wolisz robić w wolnym czasie?", "L": "Czytać książki, rozwiązywać krzyżówki lub uczyć się czegoś nowego.", "R": "Rysować, grać na instrumencie, tworzyć coś własnymi rękami."},
            {"q": "10. Jak zazwyczaj rozwiązujesz konflikt?", "R": "Staram się zrozumieć emocje innych i szukam kreatywnych rozwiązań.", "L": "Rozmawiam i staram się znaleźć racjonalne rozwiązanie."}
        ]

        user_answers = []
        with st.form("brain_test"):
            for item in questions:
                # Wyświetlamy opcje w kolejności zdefiniowanej w słowniku (już wymieszanej)
                ans = st.radio(item["q"], [item["L"], item["R"]])
                user_answers.append((ans, item["L"], item["R"]))
            
            submitted = st.form_submit_button("📊 Zobacz wynik i wykres")

        if submitted:
            count_l = sum(1 for ans, l, r in user_answers if ans == l)
            count_r = sum(1 for ans, l, r in user_answers if ans == r)

            st.divider()
            
            # --- WYKRES PORÓWNAWCZY ---
            st.subheader("Twój profil dominacji półkul")
            chart_data = pd.DataFrame({
                'Półkula': ['Lewa (Logiczna)', 'Prawa (Kreatywna)'],
                'Punkty': [count_l, count_r]
            })
            st.bar_chart(chart_data.set_index('Półkula'))

            # --- INTERPRETACJA ---
            if count_l > count_r:
                st.success(f"Dominacja LEWEJ półkuli ({count_l} pkt)")
                st.write("**Charakterystyka:** Logiczne myślenie, analityczność i systematyczność. [cite: 37]")
                st.write("**Zawody:** Analityk, Programista, Inżynier, Prawnik. [cite: 40-44]")
            elif count_r > count_l:
                st.success(f"Dominacja PRAWEJ półkuli ({count_r} pkt)")
                st.write("**Charakterystyka:** Kreatywność, intuicja i wyobraźnia wizualna. [cite: 49]")
                st.write("**Zawody:** Grafik, Projektant, Muzyk, Architekt, Projektant gier. [cite: 52-55, 59]")
            else:
                st.info("Zrównoważona dominacja obu półkul (5:5)")
                st.write("**Charakterystyka:** Łączysz logikę z innowacyjnością. [cite: 63]")
                st.write("**Zawody:** Menedżer, Psycholog, Przedsiębiorca. [cite: 65, 68, 69]")
