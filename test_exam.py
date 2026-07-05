from test import Test

success, message = Test.create_test(
    102,
    "Java Basics",
    10,
    [1]

)

print(message)
print(Test.get_all_tests())





