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
            "Lekcja 3: Różne mózgi - różne zawody",
            "Lekcja 4: Rola zmysłów w karierze"
        ])
        st.divider()
        if st.button("Wyloguj"):
            st.session_state['zalogowany'] = False
            st.rerun()

    # --- LEKCJA 1 ---
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

    # --- LEKCJA 2 ---
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

    # --- LEKCJA 3 (10 PYTAŃ - PRZYWRÓCONE I WYMIESZANE) ---
    elif wybor == "Lekcja 3: Różne mózgi - różne zawody":
        st.title("🧠 Lekcja 3: Różne mózgi - różne zawody")
        questions_l3 = [
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
        with st.form("brain_test"):
            res_l3 = []
            for item in questions_l3:
                res_l3.append((st.radio(item["q"], [item["L"], item["R"]]), item["L"], item["R"]))
            if st.form_submit_button("📊 Wynik Półkul"):
                cl = sum(1 for a, l, r in res_l3 if a == l)
                cr = sum(1 for a, l, r in res_l3 if a == r)
                st.subheader("Twój profil dominacji półkul")
                st.bar_chart(pd.DataFrame({'Półkula': ['Lewa (Logiczna)', 'Prawa (Kreatywna)'], 'Pkt': [cl, cr]}).set_index('Półkula'))
                if cl > cr:
                    st.success(f"Dominacja LEWEJ półkuli ({cl} pkt)")
                    st.write("**Charakterystyka:** Logiczne myślenie, analityczność i systematyczność[cite: 37].")
                    st.write("**Zawody:** Analityk, Programista, Inżynier, Nauczyciel matematyki, Prawnik, Specjalista AI, Inżynier robotyki [cite: 40-48].")
                elif cr > cl:
                    st.success(f"Dominacja PRAWEJ półkuli ({cr} pkt)")
                    st.write("**Charakterystyka:** Kreatywność, intuicja i wyobraźnia wizualna[cite: 49].")
                    st.write("**Zawody:** Grafik, Projektant mody, Muzyk, Architekt, Projektant gier, Animator [cite: 52-60].")
                else:
                    st.info("Zrównoważona dominacja obu półkul (5:5)")
                    st.write("**Charakterystyka:** Łączysz logikę z innowacyjnością[cite: 63].")
                    st.write("**Zawody:** Menedżer projektów, Psycholog, Przedsiębiorca, Konsultant strategii [cite: 65-74].")

    # --- LEKCJA 4 ---
    elif wybor == "Lekcja 4: Rola zmysłów w karierze":
        st.title("👁️👂🖐️ Lekcja 4: Rola zmysłów w karierze")
        st.subheader("Test na Wyodrębnienie Dominującego Zmysłu")
        st.info("Odkryj, czy Twoim dominującym zmysłem jest wzrok, słuch czy dotyk (kinestetyka).")
        q_data = [
            {"q": "1. Kiedy uczysz się czegoś nowego, najbardziej pomaga Ci:", "a": ("Eksperymentowanie i doświadczanie", "K"), "b": ("Słuchanie wykładów i podcastów", "S"), "c": ("Oglądanie obrazków i schematów", "W")},
            {"q": "2. Jak najchętniej spędzasz wolny czas?", "a": ("Słuchając muzyki lub podcastów", "S"), "b": ("Oglądając filmy lub internet", "W"), "c": ("Sport lub prace ręczne", "K")},
            {"q": "3. Jak najlepiej zapamiętujesz informacje?", "a": ("Widząc je napisane lub narysowane", "W"), "b": ("Powtarzając czynności", "K"), "c": ("Słysząc je kilkukrotnie", "S")},
            {"q": "4. Co Cię najbardziej irytuje?", "a": ("Głośne dźwięki lub hałas", "S"), "b": ("Bałagan lub nieestetyczne otoczenie", "W"), "c": ("Niewygodne ubranie", "K")},
            {"q": "5. Jak reagujesz na stres?", "a": ("Zajmujesz się czymś fizycznym", "K"), "b": ("Słuchasz ulubionej muzyki", "S"), "c": ("Zamyślasz się, patrząc na coś kojącego", "W")},
            {"q": "6. Co najczęściej przyciąga Twoją uwagę w nowym miejscu?", "a": ("Wystrój wnętrza i kolory", "W"), "b": ("Dźwięki i muzyka w tle", "S"), "c": ("Tekstura przedmiotów", "K")},
            {"q": "7. Jakie prezenty najbardziej Cię cieszą?", "a": ("Płyty CD, bilety na koncert", "S"), "b": ("Przytulne ubrania, narzędzia", "K"), "c": ("Piękne obrazy, dekoracje", "W")},
            {"q": "8. Jak najlepiej relaksujesz się po ciężkim dniu?", "a": ("Oglądając film lub czytając", "W"), "b": ("Rozciągając się lub biorąc kąpiel", "K"), "c": ("Słuchając muzyki", "S")},
            {"q": "9. Jak najczęściej wyrażasz swoje emocje?", "a": ("Poprzez dotyk (przytulanie)", "K"), "b": ("Opowiadając o uczuciach", "S"), "c": ("Rysując lub tworząc wizualnie", "W")},
            {"q": "10. Jak najczęściej uczysz się nowych rzeczy?", "a": ("Ćwiczenia praktyczne i ruch", "K"), "b": ("Patrząc na obrazy i schematy", "W"), "c": ("Słuchanie wyjaśnień i wykładów", "S")}
        ]
        with st.form("test_zmyslow"):
            user_choices = []
            for item in q_data:
                choice = st.radio(item["q"], [item["a"][0], item["b"][0], item["c"][0]])
                if choice == item["a"][0]: user_choices.append(item["a"][1])
                elif choice == item["b"][0]: user_choices.append(item["b"][1])
                else: user_choices.append(item["c"][1])
            submit_zmysly = st.form_submit_button("📊 Oblicz mój profil zmysłów")
        if submit_zmysly:
            count_w, count_s, count_k = user_choices.count("W"), user_choices.count("S"), user_choices.count("K")
            st.subheader("Twój rozkład zmysłów")
            st.bar_chart(pd.DataFrame({'Zmysł': ['Wzrok', 'Słuch', 'Dotyk'], 'Pkt': [count_w, count_s, count_k]}).set_index('Zmysł'))
            max_val = max(count_w, count_s, count_k)
            if count_w == max_val:
                st.success("Dominujący zmysł: WZROK [cite: 117]")
                st.write("**Styl uczenia się:** Obrazy, wykresy, mapy myśli [cite: 119-120].")
                st.write("**Zawody:** Grafik, Architekt, Projektant gier, Urbanista smart city [cite: 117-118].")
            elif count_s == max_val:
                st.success("Dominujący zmysł: SŁUCH [cite: 121]")
                st.write("**Styl uczenia się:** Wykłady, dyskusje, podcasty [cite: 123-124].")
                st.write("**Zawody:** Muzyk, Tłumacz, Psycholog, Specjalista AI (mowa) [cite: 121-122].")
            else:
                st.success("Dominujący zmysł: DOTYK / KINESTETYKA [cite: 125]")
                st.write("**Styl uczenia się:** Doświadczenie, ruch, modele 3D [cite: 128-129].")
                st.write("**Zawody:** Fizjoterapeuta, Chirurg, Technik robotyki, Terapeuta sensoryczny [cite: 126-127].")
