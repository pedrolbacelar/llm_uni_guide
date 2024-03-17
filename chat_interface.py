import importlib
import components
import matcher
from components import Chat
from components import Student
importlib.reload(components)
importlib.reload(matcher)

#---- Check to re-train databases ----
university_check = components.University()
translator = components.Translator()

#--- Check Uni
university_check.update()

#--- Check Students
translator.translate_student_raw_data()

# ------------------------------------ CHAT Interaction ------------------------------------

#--- create a chat object
chatbot = Chat(1)

#--- chat initiation
chatbot.initiate()

#--- Intro Start
print()
print("--------------------------------------------------------------")
chatbot.print_std_message("intro")
chatbot.print_std_message("name")
name = input("Answer: ")

#--- create a student object
student = Student(name)
student.initiate()

#--- Get questions
number_of_questions = len(chatbot.get_all_questions())

# ------------------ Main Loop Through the Questions ------------------
for i in range(1, number_of_questions+1):
    print(f"-- Question {i}/{number_of_questions}")
    
    #-- Take the next question
    question = chatbot.get_question(i)
    answer = input(f"Answer: ")

    #--- Save the answer into the data of the student
    # obs: structuring this data migh be crucial for the next steps and we might change it
    # should we add the question or it's just overlapping?
    student.add_data(answer)

#--- Update the student database
student.update()

#-------------------------- MATCHING --------------------------
#--- create a matcher object
matcher = matcher.Matcher(student=student, verbose=True)
most_similar_university = matcher.match()
print(most_similar_university)

#--- End
chatbot.print_std_message("end")
