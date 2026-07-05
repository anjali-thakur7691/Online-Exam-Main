from test import Test
from result import Result

test = Test.get_test(101)

answers = {
    "1":"Programming Language"
}

result = Result.submit_test (
    student_id=2,
    test = test,
    answers=answers
)

print(result)