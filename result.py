from database import Database
from questions import Question

class Result:
    FILE_NAME = "data/results.json"

    @classmethod
    def submit_test(cls, student_id, test, answers):
        questions = Question.get_all_questions() 
        score = 0
        total_marks = 0
        correct = 0
        wrong = 0
        answer_details = []

        for q_id in test["questions"]:
            question = next((q for q in questions if q["question_id"] == q_id), None)
            if question is None: continue    

            total_marks += question["marks"]
            student_answer = answers.get(str(q_id))
            is_correct = (student_answer == question["correct_answer"])

            if is_correct:
                score += question["marks"]
                correct += 1
            else:
                wrong += 1 

            answer_details.append({
                "question_id": q_id,
                "question": question["question"],
                "student_answer": student_answer,
                "correct_answer": question["correct_answer"],
                "marks": question["marks"],
                "status": "Correct" if is_correct else "Wrong"
            }) 

        percentage = round((score / total_marks) * 100, 2) if total_marks > 0 else 0

        result = {
            "id": f"{student_id}_{test['test_id']}", # Unique ID for result
            "student_id": student_id,
            "test_id": test["test_id"],
            "test_title": test["title"],
            "score": score,
            "total_marks": total_marks,
            "correct": correct,
            "wrong": wrong,
            "percentage": percentage,
            "answers": answer_details
        } 

        # Save logic loop ke bahar hona chahiye
        results = Database.load_data(cls.FILE_NAME)
        results.append(result) 
        Database.savedata(cls.FILE_NAME, results)

        return result

    @classmethod
    def get_all_results(cls):
        return Database.load_data(cls.FILE_NAME)

    @classmethod
    def get_student_result(cls, student_id):
        results = cls.get_all_results()
        return [r for r in results if r["student_id"] == student_id]

    @classmethod
    def delete_result(cls, result_id):
        results = cls.get_all_results()
        new_results = [r for r in results if r.get("id") != result_id]
        Database.savedata(cls.FILE_NAME, new_results)
        return True