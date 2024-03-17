import matcher
import importlib
importlib.reload(matcher)

matcher = matcher.Matcher(student_name= "Pedro")
matcher.match()
matcher.show_similarities()