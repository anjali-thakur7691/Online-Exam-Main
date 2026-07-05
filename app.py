import streamlit as st
from auth import Auth
from student import Student
from questions import Question
from test import Test
from result import Result

# --- Utility Function ---
def get_value(data, key, default):
    return data.get(key, default) if isinstance(data, dict) else getattr(data, key, default)

st.set_page_config(page_title="Online Exam System", page_icon="📝", layout="wide")

# --- SESSION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user" not in st.session_state: st.session_state.user = None

def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()

# --- LOGIN / REGISTER ---
if not st.session_state.logged_in:
    st.title("📝 Online Exam System")
    option = st.sidebar.radio("Menu", ["Login", "Register"])
    if option == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = Auth.login(email, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
            else: st.error("Invalid Email or Password")
    else:
        st.subheader("Student Registration")
        s_id = st.number_input("Student ID", min_value=1)
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Register"):
            success, message = Student.register(s_id, name, email, password)
            if success: st.success(message)
            else: st.error(message)
    st.stop()

# --- AFTER LOGIN ---
user = st.session_state.user
st.sidebar.success(f"👋 {user['name']}")
if st.sidebar.button("Logout"): logout()

# --- ROUTING ---
if user["role"] == "admin":
    menu = st.sidebar.selectbox("Admin Menu", ["Dashboard", "Add Question", "View Question", "Create Test", "View Test", "View Results"])
else:
    menu = st.sidebar.selectbox("Student Menu", ["Dashboard", "Available Tests", "My Results"])

# --- PAGES ---
if menu == "Dashboard":
    st.title("Admin Dashboard")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Total Students", len(Student.get_all_students()))
        st.metric("Total Questions", len(Question.get_all_questions()))
    with c2:
        st.metric("Total Tests", len(Test.get_all_tests()))

elif menu == "Add Question":
    st.title("➕ Add Question")

    with st.form("q_form", clear_on_submit=True):

        q_id = st.number_input(
            "Question ID",
            min_value=1,
            step=1
        )

        q_text = st.text_area(
            "Question"
        )

        a = st.text_input("Option A")
        b = st.text_input("Option B")
        c = st.text_input("Option C")
        d = st.text_input("Option D")

        ans = st.selectbox(
            "Correct Answer",
            [
                "Select Correct Answer",
                "A",
                "B",
                "C",
                "D"
            ]
        )

        marks = st.number_input(
            "Marks",
            min_value=1,
            value=1
        )

        submit = st.form_submit_button("💾 Save Question")

        if submit:

            if q_text.strip() == "":
                st.error("Please enter the question.")
            elif a.strip() == "" or b.strip() == "" or c.strip() == "" or d.strip() == "":
                st.error("Please fill all four options.")
            elif ans == "Select Correct Answer":
                st.error("Please select the correct answer.")
            else:

                success, message = Question.add_question(
                    q_id,
                    q_text,
                    a,
                    b,
                    c,
                    d,
                    ans,
                    marks
                )

                if success:
                    st.success(message)
                else:
                    st.error(message)

elif menu == "View Question":
    st.title("View Questions")
    for q in Question.get_all_questions():
        with st.expander(f"ID: {get_value(q, 'question_id', 'N/A')}"):
            st.write(f"**Q:** {get_value(q, 'question', 'N/A')}")
            st.success(f"Ans: {get_value(q, 'correct_answer', 'N/A')}")
    
    st.subheader("🗑️ Delete Question")
    del_id = st.number_input("Enter ID", step=1, key="del_q")
    if st.button("Delete"):
        if Question.delete_question(del_id):
            st.success("Deleted"); st.rerun()
        else: st.error("Not Found")

elif menu == "Create Test":
    st.title("Create Test")
    questions = Question.get_all_questions()
    with st.form("t_form"):
        t_id = st.number_input("Test ID", min_value=1)
        title = st.text_input("Title")
        duration = st.number_input("Duration", min_value=1)
        sel = st.multiselect("Questions", [f"{get_value(q, 'question_id', '')} - {get_value(q, 'question', '')}" for q in questions])
        if st.form_submit_button("Create"):
            q_ids = [int(s.split(' - ')[0]) for s in sel]
            s, m = Test.create_test(t_id, title, duration, q_ids)
            if s: st.success(m)
            else: st.error(m)

elif menu == "View Test":
    st.title("View Tests")
    for t in Test.get_all_tests():
        with st.expander(f"Test: {get_value(t, 'title', 'N/A')}"):
            st.write(f"ID: {get_value(t, 'test_id', 'N/A')}")
            if st.button(f"Delete {get_value(t, 'test_id', '')}", key=f"d_{get_value(t, 'test_id', '')}"):
                Test.delete_test(get_value(t, 'test_id', 0))
                st.rerun()

elif menu == "View Results":
    st.title("📊 View Exam Results")
    results = Result.get_all_results()
    
    if not results:
        st.warning("No results found.")
    else:
        for r in results:
            # Status determine karne ka logic
            # Agar 'status' key pehle se result mein hai, to wo use karein, 
            # varna score ke basis par 'Pass' ya 'Fail' show karein
            score = get_value(r, 'score', 0)
            total = get_value(r, 'total_marks', 1)
            
            # Logic: Agar score total ka 40% ya usse zyada hai to Pass
            status = "Pass" if (score / total) >= 0.4 else "Fail"
            
            with st.expander(f"Student: {get_value(r, 'student_name', 'Student')}"):
                st.write(f"**Test ID:** {get_value(r, 'test_id', 'N/A')}")
                st.write(f"**Score:** {score} / {total}")
                st.write(f"**Status:** {status}") # Yahan ab 'Pass' ya 'Fail' dikhega
                
                # Delete Button
                if st.button(f"Delete Result {get_value(r, 'id', '')}", key=f"del_{get_value(r, 'id', '0')}"):
                    Result.delete_result(r.get('id'))
                    st.rerun()