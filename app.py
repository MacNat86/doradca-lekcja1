import streamlit as st
import pandas as pd

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Cyfrowy Doradca Zawodowy", layout="wide")

# --- PROSTY SYSTEM LOGOWANIA ---
if 'zalogowany' not in st.session_state:
    st.session_state['zalogowany'] = False

if not st.session_state['zalogowany']:
    st.title("🔐 Logowanie")
    login = st.text_input("Login")
    haslo = st.text_input("Hasło", type="password")
    if st.button("Zaloguj"):
        if login == "uczen1" and haslo == "123":
            st.session_state['zalogowany'] = True
            st.rerun()
        else:
            st.error("Błędne dane logowania.")
else:
    # --- MENU BOCZNE ---
    with st.sidebar:
        st.header("Twoje Lekcje")
        wybor = st.radio("Wybierz temat:", [
            "Lekcja 1: Poznaję Siebie", 
            "Lekcja 2: Mój Temperament", 
            "Lekcja 3: Różne mózgi - różne zawody"
        ])
        st.divider()
        if st.button("Wyloguj"):
            st.session_state['zalogowany'] = False
            st.rerun()

    # --- LEKCJA 1 ---
    if wybor == "Lekcja 1: Poznaję Siebie":
        st.title("🧩 Lekcja 1: Poznaję Siebie")
        st.write("Tu znajdują się Twoje umiejętności i cele zawodowe.")

    # --- LEKCJA 2 ---
    elif wybor == "Lekcja 2: Mój Temperament":
        st.title("⚖️ Lekcja 2: Mój Temperament")
        st.write("Tu znajduje się Twój wykres temperamentu.")

    # --- LEKCJA 3: RÓŻNE MÓZGI - RÓŻNE ZAWODY ---
    elif wybor == "Lekcja 3: Różne mózgi - różne zawody":
        st.title("🧠 Lekcja 3: Różne mózgi - różne zawody")
        st.subheader("Test Samooceny Dominacji Półkul Mózgowych")
        
        st.info("Instrukcja: Przeczytaj uważnie każde pytanie i wybierz odpowiedź, która najlepiej opisuje Ciebie.")

        with st.form("test_mozgu"):
            # Pytania z pliku PDF
            q1 = st.radio("1. Co robisz, gdy napotykasz problem?", 
                ["a) Analizuję problem krok po kroku i szukam logicznego rozwiązania.", 
                 "b) Staram się znaleźć twórcze, nietypowe rozwiązanie."])
            
            q2 = st.radio("2. Jak zazwyczaj zapamiętujesz nowe informacje?", 
                ["a) Lubię robić notatki i układać informacje w logiczną całość.", 
                 "b) Łatwiej zapamiętuję, gdy widzę obrazy lub schematy."])
            
            q3 = st.radio("3. Jakie przedmioty w szkole lubisz najbardziej?", 
                ["a) Matematyka, język polski, nauki ścisłe.", 
                 "b) Plastyka, muzyka, zajęcia techniczne."])
            
            q4 = st.radio("4. Jak podchodzisz do organizacji czasu?", 
                ["a) Zawsze planuję swój dzień i trzymam się ustalonego harmonogramu.", 
                 "b) Działam spontanicznie i lubię improwizować."])
            
            q5 = st.radio("5. Jak wyrażasz swoje emocje?", 
                ["a) Często werbalnie opisuję swoje uczucia.", 
                 "b) Wyrażam emocje przez sztukę, muzykę lub ruch."])
            
            q6 = st.radio("6. Jak lubisz pracować nad projektami?", 
                ["a) Skupiam się na szczegółach i analizie danych.", 
                 "b) Wolę podejście całościowe i twórcze, z naciskiem na wizję końcową."])
            
            q7 = st.radio("7. Co jest dla Ciebie łatwiejsze?", 
                ["a) Rozwiązywanie zadań logicznych i matematycznych.", 
                 "b) Tworzenie prac plastycznych lub muzycznych."])
            
            q8 = st.radio("8. Jak radzisz sobie z nauką nowych rzeczy?", 
                ["a) Wolę szczegółowe instrukcje i ścisłe wytyczne.", 
                 "b) Wolę uczyć się przez doświadczenie i eksperymenty."])
            
            q9 = st.radio("9. Co wolisz robić w wolnym czasie?", 
                ["a) Czytać książki, rozwiązywać krzyżówki lub uczyć się czegoś nowego.", 
                 "b) Rysować, grać na instrumencie, tworzyć coś własnymi rękami."])
            
            q10 = st.radio("10. Jak zazwyczaj rozwiązujesz konflikt?", 
                ["a) Rozmawiam i staram się znaleźć racjonalne rozwiązanie.", 
                 "b) Staram się zrozumieć emocje innych i szukam kreatywnych rozwiązań."])

            if st.form_submit_button("📊 Sprawdź mój wynik"):
                # Zliczanie punktów
                odpowiedzi = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
                count_a = sum(1 for x in odpowiedzi if x.startswith("a"))
                count_b = sum(1 for x in odpowiedzi if x.startswith("b"))
                
                st.divider()
                
                # Interpretacja wyników na podstawie klucza z PDF
                if count_a > count_b:
                    st.success(f"Twój wynik: {count_a} 'a' vs {count_b} 'b' - Dominacja LEWEJ półkuli")
                    st.write("**Charakterystyka:** Osoby z dominacją lewej półkuli mają tendencję do logicznego myślenia, są analityczne i systematyczne. Mają predyspozycje do rozwiązywania problemów przy pomocy logiki.")
                    st.write("**Przykładowe zawody:** Analityk finansowy, Programista, Inżynier, Nauczyciel matematyki, Prawnik, Data scientist, Inżynier robotyki, Specjalista ds. cyberbezpieczeństwa.")
                
                elif count_b > count_a:
                    st.success(f"Twój wynik: {count_b} 'b' vs {count_a} 'a' - Dominacja PRAWEJ półkuli")
                    st.write("**Charakterystyka:** Osoby z dominacją prawej półkuli są bardziej kreatywne, intuicyjne i wizualne. Mają predyspozycje do zadań artystycznych i innowacyjnych.")
                    st.write("**Przykładowe zawody:** Grafik komputerowy, Projektant mody, Muzyk, Architekt, Specjalista UX Designer, Projektant gier wideo, Animator komputerowy.")
                
                else:
                    st.info(f"Twój wynik: {count_a} 'a' i {count_b} 'b' - Zrównoważona dominacja")
                    st.write("**Charakterystyka:** Potrafisz łączyć logiczne myślenie z kreatywnością. Masz zdolność do rozwiązywania problemów zarówno w sposób analityczny, jak i innowacyjny.")
                    st.write("**Przykładowe zawody:** Menedżer projektów, Architekt systemów, Kreatywny specjalista ds. marketingu, Psycholog, Innowacyjny przedsiębiorca.")
