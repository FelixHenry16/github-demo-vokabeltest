from dataclasses import dataclass


@dataclass
class QuizResult:
    total: int
    correct: int
    errors: list 


    @property
    def wrong(self):
        return self.total - self.correct

    @property
    def percentage(self):
        if self.total == 0:
            return 0
        return round((self.correct / self.total) * 100)


def normalize_answer(text: str) -> str:
    return text.strip().lower()


def is_correct(user_answer: str, expected_answer: str) -> bool:
    return normalize_answer(user_answer) == normalize_answer(expected_answer)


def evaluate_answers(quiz_records):
    total = len(quiz_records)
    correct = 0
    errors = []  # Temporäre Liste für die Fehler

    # Wir packen hier das gefragte Wort (question) direkt mit aus
    for question, user_answer, expected_answer in quiz_records:
        if is_correct(user_answer, expected_answer):
            correct += 1
        else:
            # Falls falsch: Speicher Frage, falsche und richtige Antwort ab
            errors.append({
                "question": question,
                "user_answer": user_answer,
                "expected_answer": expected_answer
            })
            
    return QuizResult(total=total, correct=correct, errors=errors)


def run_quiz(entries):
    print("\nQuiz startet. Bitte Übersetzungen eingeben.\n")
    quiz_records = []  # Umbenannt von given_answers, da wir jetzt mehr Infos speichern

    for item in entries:
        user_answer = input(f"{item['question']}: ")
        # WICHTIG: Wir speichern jetzt ein Tuple mit (Frage, User-Antwort, Erwartete Antwort)
        quiz_records.append((item['question'], user_answer, item['answer']))

    result = evaluate_answers(quiz_records)
    
    print("\nErgebnis")
    print("-" * 20)
    print(f"Richtig: {result.correct} von {result.total}")
    print(f"Falsch : {result.wrong}")
    print(f"Quote  : {result.percentage} %")

    # Fehlerliste am Ende der Runde ausgeben
    if result.errors:
        print("\nDeine Fehlerliste:")
        print("-" * 20)
        for fehler in result.errors:
            print(f" X Gesucht war: '{fehler['question']}'")
            print(f"   Deine Eingabe: '{fehler['user_answer']}'")
            print(f"   Richtige Lösung: '{fehler['expected_answer']}'")
            print("-" * 20)
    else:
        print("\n Du hast keine Fehler gemacht!")


def ask_yes_no(prompt):
    return input(f"\n{prompt}")
