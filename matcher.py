from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import sqlite3

import importlib
import components
importlib.reload(components)


class Matcher():
    def __init__(self, student_id = None, student_name = None, student= None, student_db_path= "databases\\nlp\\students_db.db", universities_db_path= "databases\\nlp\\universities_db.db", verbose = False):
        self.student_db_path = student_db_path
        self.universities_db_path = universities_db_path
        self.verbose = verbose
        self.student = student #--- student object
        self.student_id = student_id
        self.student_name = student_name
        self.initiate()
        self.universities_similarities = None


    def initiate(self):
        #--- check to create the student or extract data
        if self.student is None:
            if self.student_name is not None:
                self.student = components.Student(self.student_name)
                self.student.initiate()

                #--- search student on the database to extract data
                conn = sqlite3.connect(self.student_db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT data FROM students_db WHERE name=?", (self.student_name,))
                data = cursor.fetchone()
                conn.close()

                if data is not None:
                    self.student.add_data(data[0])
                    if self.verbose:
                        print(f"Student {self.student_name} found in the database.")
                else:
                    print(f"Student {self.student_name} not found in the database.")

            elif self.student_id is not None:
                conn = sqlite3.connect(self.student_db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name, data FROM students_db WHERE id=?", (self.student_id,))
                data = cursor.fetchone()
                conn.close()

                if data is not None:
                    self.student = components.Student(data[0])
                    self.student.add_data(data[1])
                    if self.verbose:
                        print(f"Student {self.student_id} found in the database.")
                else:
                    print(f"Student {self.student_id} not found in the database.")
            else:
                print("No student provided.")


    def match(self):
        # Load the student data and universities data from the databases
        student_data = self.load_student_data()
        universities_data, universities_names = self.load_universities_data()

        # Vectorize the student data and universities data
        vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
        student_vector = vectorizer.fit_transform([student_data])
        universities_vectors = vectorizer.transform(universities_data)

        # Calculate the cosine similarity between the student vector and universities vectors
        similarities = cosine_similarity(student_vector, universities_vectors)

        # ---- Correlate the university similarity with the appropriate name in a dictionary
        universities_similarities = {}
        for i in range(len(universities_names)):
            universities_similarities[universities_names[i]] = similarities[0][i]

        #--- Store the similarities
        self.universities_similarities = universities_similarities
    
        return universities_similarities
    
    def show_similarities(self):
        if self.universities_similarities is not None:
            print("-------------------- SHOWING SIMILARITIES --------------------")
            print("| UNIVERSITY   |   SIMILARITY |")
            for university in self.universities_similarities:
                print(f"|-- {university}: {round(self.universities_similarities[university]*1000000)/10000}%")
        else:
            print("No similarities found.")

    def load_student_data(self):
        # Load the student data from the student database
        # Implement the code to load the student data from the database
        student_data = self.student.get_data()
        return student_data

    def load_universities_data(self):
        # Connect to the universities database
        conn = sqlite3.connect(self.universities_db_path)
        cursor = conn.cursor()

        # Execute a query to fetch the universities data
        cursor.execute("SELECT  data FROM universities_db")

        # Fetch all the rows from the query result
        rows = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Extrat the data from the rows and add it to a list
        universities_data = [row[0] for row in rows]

        #--- Get universities names
        conn = sqlite3.connect(self.universities_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM universities_db")
        names = cursor.fetchall()
        conn.close()

        #--- Store the names
        self.universities_names = [name[0] for name in names]

        return universities_data, self.universities_names
    

