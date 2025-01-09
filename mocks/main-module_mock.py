from typing import List, Dict, Optional

# Моковые данные для тестов
mock_tests = [
    {"id": 1, "name": "Тест по математике", "description": "Проверьте свои знания по математике."},
    {"id": 2, "name": "Тест по истории", "description": "Проверьте свои знания по истории."},
]

mock_questions = {
    1: [
        {"id": 1, "text": "Сколько будет 2 + 2?", "options": ["3", "4", "5"], "correct_option": 1},
        {"id": 2, "text": "Сколько будет 3 * 3?", "options": ["6", "9", "12"], "correct_option": 1},
    ],
    2: [
        {"id": 3, "text": "В каком году началась Вторая мировая война?", "options": ["1939", "1941", "1945"], "correct_option": 0},
        {"id": 4, "text": "Кто был первым президентом США?", "options": ["Джордж Вашингтон", "Авраам Линкольн", "Томас Джефферсон"], "correct_option": 0},
    ],
}

mock_attempts = {}
mock_answers = {}

# Функции для моков

def get_tests() -> List[Dict]:
    """Возвращает список тестов."""
    return mock_tests

def get_test_details(test_id: int) -> Optional[Dict]:
    """Возвращает детали теста по его ID."""
    for test in mock_tests:
        if test["id"] == test_id:
            return test
    return None

def get_test_questions(test_id: int) -> List[Dict]:
    """Возвращает список вопросов для теста."""
    return mock_questions.get(test_id, [])

def create_attempt(test_id: int, user_id: int) -> Dict:
    """Создаёт попытку прохождения теста."""
    attempt_id = len(mock_attempts) + 1
    attempt = {
        "id": attempt_id,
        "test_id": test_id,
        "user_id": user_id,
        "status": "in_progress",
    }
    mock_attempts[attempt_id] = attempt
    return attempt

def submit_answer(attempt_id: int, question_id: int, answer: int) -> Dict:
    """Отправляет ответ на вопрос."""
    if attempt_id not in mock_attempts:
        return {"status": "error", "message": "Попытка не найдена."}

    if question_id not in [q["id"] for q in mock_questions[mock_attempts[attempt_id]["test_id"]]]:
        return {"status": "error", "message": "Вопрос не найден."}

    mock_answers[(attempt_id, question_id)] = answer
    return {"status": "success"}

def get_attempt_results(attempt_id: int) -> Dict:
    """Возвращает результаты попытки."""
    if attempt_id not in mock_attempts:
        return {"status": "error", "message": "Попытка не найдена."}

    test_id = mock_attempts[attempt_id]["test_id"]
    questions = mock_questions[test_id]
    results = []
    total_correct = 0

    for question in questions:
        answer = mock_answers.get((attempt_id, question["id"]), -1)
        is_correct = answer == question["correct_option"]
        if is_correct:
            total_correct += 1
        results.append({
            "question_id": question["id"],
            "question_text": question["text"],
            "user_answer": answer,
            "correct_answer": question["correct_option"],
            "is_correct": is_correct,
        })

    return {
        "status": "success",
        "results": results,
        "total_correct": total_correct,
        "total_questions": len(questions),
    }