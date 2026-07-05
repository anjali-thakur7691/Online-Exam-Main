from student import Student
from auth import Auth

success , message = Student.register (
    2,
    "Rohit",
    "sharma@gmail.com",
    "4518"
)

print(message)

user = Auth.login(
    "sharma@gmail.com",
    "4518"

)

print(user)
