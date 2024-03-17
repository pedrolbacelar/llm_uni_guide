import sqlite3
import os


class Student():
    def __init__(self,name, data = "", student_db_path = "databases\\nlp\\students_db.db", verbose = False):
        #self.id = id
        self.name = name
        self.data = data
        self.student_db_path = student_db_path
        self.verbose = verbose

    #--- Initiate DB
    def initiate(self):
        #--- check if there is a student database
        if not os.path.exists(self.student_db_path):
            #--- create a student database
            print("Creating a student database...")
            print(f"Path: {self.student_db_path}")
            conn = sqlite3.connect(self.student_db_path)
            c = conn.cursor()
            c.execute('''CREATE TABLE students_db (id INTEGER PRIMARY KEY, name TEXT, data TEXT)''')
            conn.commit()
            conn.close()
        else:
            print(" --- Student database already exists ---")
            if self.verbose:
                self.print_database()
    
    #--- Printing Student Database
    def print_database(self):
        conn = sqlite3.connect(self.student_db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM students_db")
        students = c.fetchall()
        print("Existing students:")
        for student in students:
            print(f"-- {student}")
        conn.close()

    #--- Updating DB
    def update(self):
        #--- check if the student is already in the database
        conn = sqlite3.connect(self.student_db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM students_db WHERE name=?", (self.name,))
        student = c.fetchone()
        conn.close()

        #--- if the student is not in the database, add it
        if student is None:
            conn = sqlite3.connect(self.student_db_path)
            c = conn.cursor()
            c.execute("INSERT INTO students_db (name, data) VALUES (?, ?)", (self.name, self.data))
            conn.commit()
            conn.close()
            if self.verbose:
                print(f"Student {self.name} added to the database.")
        else:
            #--- if the student is in the database, update its data
            conn = sqlite3.connect(self.student_db_path)
            c = conn.cursor()
            c.execute("UPDATE students_db SET data=? WHERE name=?", (self.data, self.name))
            conn.commit()
            conn.close()
            if self.verbose:
                print(f"Student {self.name} updated in the database.")

    #--- Adding Data    
    def add_data(self, new_data):
        self.data = self.data + " | " + (new_data)

    # --------- get methods ---------
    def get_id(self):
        return self.id
    def get_name(self):
        return self.name
    def get_data(self):
        return self.data

class University():
    def __init__(self, name= None, data="", universities_db= "databases\\nlp\\universities_db.db",raw_uni_db = "databases\\nlp\\raw_universities", verbose = False):
        self.name = name
        self.data = data
        self.universities_db = universities_db
        self.raw_uni_db = raw_uni_db
        self.verbose = verbose
        self.initiate()
    
    #--- Initiate University DB
    def initiate(self):
        #--- check if there is a university database
        if not os.path.exists(self.universities_db):
            #--- create a university database
            print("Creating a university database...")
            print(f"Path: {self.universities_db}")
            conn = sqlite3.connect(self.universities_db)
            c = conn.cursor()
            c.execute('''CREATE TABLE universities_db (id INTEGER PRIMARY KEY, name TEXT, data TEXT)''')
            conn.commit()
            conn.close()
        else:
            print(" --- University database already exists ---")
            if self.verbose:
                self.print_database()
   
    #--- Add new university from the raw data txt files
    def update(self):
        #--- Take all the names of universities already in the database
        conn = sqlite3.connect(self.universities_db)
        c = conn.cursor()
        c.execute("SELECT name FROM universities_db")
        universities = c.fetchall()
        conn.close()

        #--- Take all the names of universities from the raw data txt files
        # obs: the .txt file title is the name of the university
        raw_universities = os.listdir(self.raw_uni_db)

        #--- Check if it's missing any university
        for university in raw_universities:
            if university not in universities:
                #--- Get the data from the corresponding .txt file
                with open(f"{self.raw_uni_db}\\{university}", "r") as file:
                    data = file.read()

                #--- correct the name removing the .txt
                university = university.replace(".txt", "")

                #--- Add the university to the database
                conn = sqlite3.connect(self.universities_db)
                c = conn.cursor()
                c.execute("INSERT INTO universities_db (name, data) VALUES (?, ?)", (university, data))
                conn.commit()
                conn.close()
                print(f"-- University '{university}' added to the database.")

                if self.verbose:
                    print("University data:")
                    print(data)


    def print_database(self):
        conn = sqlite3.connect(self.universities_db)
        c = conn.cursor()
        c.execute("SELECT * FROM universities_db")
        universities = c.fetchall()
        print("Existing universities:")
        for university in universities:
            print(f"-- {university}")
        conn.close()

    # --------- get methods ---------
    def get_id(self):
        return self.id
    def get_name(self):
        return self.name
    def get_data(self):
        return self.data
    
class Chat():
    def __init__(self, id, requested_questions_path = "databases\\nlp\\questions_db.db"):
        self.id = id
        self.requested_questions_path = requested_questions_path
        self.standard_questions = [
            "What are your preferred subjects or fields of study?",
            "Are there any specific industries or roles you're targeting?",
            "Are you open to studying abroad, or do you prefer to stay in your home country?",
            "Are you looking for large universities with a wide range of programs or smaller, more specialized institutions?",
            "Are you involved in any extracurricular activities or hobbies?",
            "What are your financial constraints or considerations when choosing a university?",
            "Do you prefer a more structured learning environment or a more flexible one?",
            "What languages are you proficient in?"
        ]

        self.standard_messages = {
            "intro": "Hello! I'm a chatbot that can help you find the right university for you. I'll ask you a few questions to get started.",
            "name": "What's your name?",
            "end": "Thank you for chatting with me. I hope I was able to help you in your search for the right university."
        }
    
    def initiate(self):
        #--- check if there is a question database
        if not os.path.exists(self.requested_questions_path):
            
            #--- create a question database
            print(" Path to create the new question database:")
            print(self.requested_questions_path)
            print("Creating a question database...")
            
            conn = sqlite3.connect(self.requested_questions_path)
            c = conn.cursor()
            c.execute('''CREATE TABLE questions_db (id INTEGER PRIMARY KEY, question TEXT)''')
            
            print("Adding standard questions to the database...")
            #--- insert standard questions
            for question in self.standard_questions:
                c.execute("INSERT INTO questions_db (question) VALUES (?)", (question,))
                print(f"Added: {question}")

            conn.commit()
            conn.close()


        else:
            print(" --- Question database already exists ---")
            # print the existing questions
            conn = sqlite3.connect(self.requested_questions_path)
            c = conn.cursor()
            c.execute("SELECT * FROM questions_db")
            questions = c.fetchall()
            print("Existing questions:")
            for question in questions:
                print(f"-- {question}")
            conn.close()

    def print_std_message(self, message_type):
        print(self.standard_messages[message_type])

    def get_question(self, question_id):
        conn = sqlite3.connect(self.requested_questions_path)
        c = conn.cursor()
        c.execute("SELECT * FROM questions_db WHERE id=?", (question_id,))
        question = c.fetchone()
        conn.close()

        print(f"Question: {question[1]}")
        return question[1]
    
    def get_all_questions(self):
        conn = sqlite3.connect(self.requested_questions_path)
        c = conn.cursor()
        c.execute("SELECT * FROM questions_db")
        questions = c.fetchall()
        conn.close()

        return questions


    # --------- get methods ---------
    def get_id(self):
        return self.id
    def get_requested_questions_path(self):
        return self.requested_questions_path

class Translator():
    def __init__(self, raw_uni_db = "databases\\nlp\\raw_universities", universities_db = "databases\\nlp\\universities_db.db", raw_student_db = "databases\\nlp\\raw_students", student_db = "databases\\nlp\\students_db.db", verbose = False):
        self.raw_uni_db = raw_uni_db
        self.universities_db = universities_db
        self.raw_student_db = raw_student_db
        self.student_db = student_db
        self.verbose = verbose
        self.initiate()

    def initiate(self):
        #--- Check if the student_db exists
        if not os.path.exists(self.student_db):
            #--- create a student database
            print("Creating a student database...")
            print(f"Path: {self.student_db}")
            conn = sqlite3.connect(self.student_db)
            c = conn.cursor()
            c.execute('''CREATE TABLE students_db (id INTEGER PRIMARY KEY, name TEXT, data TEXT)''')
            conn.commit()
            conn.close()
        
        #--- Check if the universities_db exists
        if not os.path.exists(self.universities_db):
            #--- create a university database
            print("Creating a university database...")
            print(f"Path: {self.universities_db}")
            conn = sqlite3.connect(self.universities_db)
            c = conn.cursor()
            c.execute('''CREATE TABLE universities_db (id INTEGER PRIMARY KEY, name TEXT, data TEXT)''')
            conn.commit()
            conn.close()

    def translate_student_raw_data(self, name= None):
            #--- The raw student folder has txt files in which the name of the file is the name of the student and within the file
            # the data of student answers of questions. This function translates the raw data into the student database. If the 
            # name was not provided, it translates all the students in the raw student folder that are not in the student database. If 
            # the name was provided, it translates only the student with that name.

            #--- Take all the names of students already in the database
            conn = sqlite3.connect(self.student_db)
            c = conn.cursor()
            c.execute("SELECT name FROM students_db")
            students = c.fetchall()
            conn.close()

            #--- Take all the names of students from the raw data txt files
            # obs: the .txt file title is the name of the student
            raw_students = os.listdir(self.raw_student_db)

            #--- Check if it's missing any student
            if name is not None:
                if name not in students:
                    #--- Get the data from the corresponding .txt file
                    with open(f"{self.raw_student_db}\\{name}.txt", "r") as file:
                        data = file.read()

                    #--- Add the student to the database
                    conn = sqlite3.connect(self.student_db)
                    c = conn.cursor()
                    c.execute("INSERT INTO students_db (name, data) VALUES (?, ?)", (name, data))
                    conn.commit()
                    conn.close()
                    print(f"-- Student '{name}' added to the database.")

                    if self.verbose:
                        print("Student data:")
                        print(data)
            else:
                for student in raw_students:
                    if student not in students:
                        #--- Get the data from the corresponding .txt file
                        with open(f"{self.raw_student_db}\\{student}", "r") as file:
                            data = file.read()

                        #--- correct the name removing the .txt
                        student = student.replace(".txt", "")

                        #--- Add the student to the database
                        conn = sqlite3.connect(self.student_db)
                        c = conn.cursor()
                        c.execute("INSERT INTO students_db (name, data) VALUES (?, ?)", (student, data))
                        conn.commit()
                        conn.close()
                        print(f"-- Student '{student}' added to the database.")

                        if self.verbose:
                            print("Student data:")
                            print(data)