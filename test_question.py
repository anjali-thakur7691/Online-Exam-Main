from questions import Question

success , message = Question.add_question(
    2,
    "What is Java ?",
    "P L",
    "Coffee",
    "Browser",
    "Editor",
    "P L",
    1
)

print(message)

print(Question.get_all_questions())