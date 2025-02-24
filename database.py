from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL="sqlite:///database.db"

engine=create_engine(DATABASE_URL)

# Drops all tables
# Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)

Session=sessionmaker(bind=engine)

session=Session()

print("Database reset and recreated successfully.")


        # Create questions for HTML & CSS quiz
# html_css_quiz = [
#     {"question": "What does HTML stand for?", 
#     "option_A": "HyperText Markup Language", 
#     "option_B": "Hyperlink Text Markup Language", 
#     "option_C": "Home Tool Markup Language", 
#     "option_D": "None of the above", 
#     "answer": "HyperText Markup Language"
#     },
#     {"question": "Which HTML element is used to define the title of a web page?",
#     "option_A": "<h1>", 
#     "option_B": "<title>", 
#     "option_C": "<head>", 
#     "option_D": "<body>", 
#     "answer": "<title>"
#     },
#     {"question": "Which of the following is the correct syntax for linking an external CSS file?", 
#     "option_A": "<style src='style.css'>", 
#     "option_B": "<link rel='stylesheet' href='style.css'>", "option_C": "<css src='style.css'>", 
#     "option_D": "<link href='style.css'>", 
#     "answer": "<link rel='stylesheet' href='style.css'>"
#     },
#     {"question": "How do you make a list in HTML?", 
#     "option_A": "<list>", 
#     "option_B": "<ul>", 
#     "option_C": "<ol>", 
#     "option_D": "<dl>", 
#     "answer": "<ul>"
#     },
#     {"question": "Which CSS property is used to change the background color of an element?", 
#     "option_A": "bgcolor", 
#     "option_B": "background-color", 
#     "option_C": "color", 
#     "option_D": "background", 
#     "answer": "background-color"
#     },
#     {"question": "Which tag is used to create a hyperlink in HTML?", 
#     "option_A": "<a>", 
#     "option_B": "<link>", 
#     "option_C": "<url>", 
#     "option_D": "<hyperlink>", 
#     "answer": "<a>"
#     },
#     {"question": "What is the correct syntax for adding a comment in CSS?", 
#     "option_A": "// comment", 
#     "option_B": "/* comment */", 
#     "option_C": "<!-- comment -->", 
#     "option_D": "# comment", 
#     "answer": "/* comment */"
#     },
#     {"question": "Which property is used to change the text color in CSS?", 
#     "option_A": "font-color", 
#     "option_B": "color", 
#     "option_C": "text-color", 
#     "option_D": "text-style", "answer": "color"
#     },
#     {"question": "What does the <div> tag represent in HTML?", "option_A": "A division or section in a document", "option_B": "A paragraph of text", 
#     "option_C": "An image container", 
#     "option_D": "A table row", 
#     "answer": "A division or section in a document"
#     },
#     {"question": "How do you add a background image in CSS?", "option_A": "background-image: url('image.jpg');", "option_B": "image: url('image.jpg');", "option_C": "background: 'image.jpg';", "option_D": "image-background: url('image.jpg');", 
#     "answer": "background-image: url('image.jpg');"
#     }
# ]

# # Create questions for JavaScript quiz
# js_quiz = [
#     {"question": "What is the correct way to define a variable in JavaScript?", 
#     "option_A": "var x = 5;", 
#     "option_B": "variable x = 5;", 
#     "option_C": "define x = 5;", 
#     "option_D": "x = 5;", 
#     "answer": "var x = 5;"
#     },
#     {"question": "Which method is used to display an alert box in JavaScript?", 
#     "option_A": "alert()", 
#     "option_B": "popup()", 
#     "option_C": "msg()", 
#     "option_D": "show()", 
#     "answer": "alert()"
#     },
#     {"question": "How do you create a function in JavaScript?", "option_A": "function myFunction() { }", 
#     "option_B": "func myFunction() { }", 
#     "option_C": "function: myFunction() { }", 
#     "option_D": "create function myFunction() { }", 
#     "answer": "function myFunction() { }"
#     },
#     {"question": "Which of the following is NOT a valid JavaScript data type?", 
#     "option_A": "String", 
#     "option_B": "Integer", 
#     "option_C": "Boolean", 
#     "option_D": "Undefined", 
#     "answer": "Integer"
#     },
#     {"question": "How do you add a comment in JavaScript?", "option_A": "<!-- This is a comment -->", 
#     "option_B": "// This is a comment", 
#     "option_C": "/* This is a comment */", 
#     "option_D": "# This is a comment", 
#     "answer": "// This is a comment"
#     },
#     {"question": "What is the correct syntax to call a function named 'myFunction'?", "option_A": "call myFunction()", "option_B": "myFunction();", "option_C": "invoke myFunction()", "option_D": "execute myFunction()", "answer": "myFunction();"},
#     {"question": "Which of these is the correct way to declare an array in JavaScript?", 
#     "option_A": "let arr = [1, 2, 3];", 
#     "option_B": "let arr = (1, 2, 3);", 
#     "option_C": "let arr = {1, 2, 3};", 
#     "option_D": "let arr = 1, 2, 3;", 
#     "answer": "let arr = [1, 2, 3];"
#     },
#     {"question": "Which JavaScript method is used to find the length of an array?", 
#     "option_A": "length()", 
#     "option_B": "size()", 
#     "option_C": "arrayLength()", 
#     "option_D": ".length", 
#     "answer": ".length"
#     },
#     {"question": "Which of the following loops is used to execute a block of code while a condition is true?", "option_A": "for", 
#     "option_B": "while", 
#     "option_C": "do-while", 
#     "option_D": "All of the above", 
#     "answer": "All of the above"
#     },
#     {"question": "What is the result of '5' + 5 in JavaScript?", "option_A": "'55'", 
#     "option_B": "10", 
#     "option_C": "Error", 
#     "option_D": "'5' + '5'", 
#     "answer": "'55'"
#     }
# ]

# # Create questions for Python quiz
# python_quiz = [
#     {"question": "What is the correct syntax to print 'Hello, World!' in Python?", 
#     "option_A": "echo 'Hello, World!'", 
#     "option_B": "print('Hello, World!')", 
#     "option_C": "console.log('Hello, World!')", 
#     "option_D": "print(Hello, World!)", 
#     "answer": "print('Hello, World!')"
#     },
#     {"question": "Which of the following is a Python data type?", 
#     "option_A": "Integer", 
#     "option_B": "Boolean", 
#     "option_C": "List", 
#     "option_D": "All of the above", 
#     "answer": "All of the above"
#     },
#     {"question": "How do you define a function in Python?", "option_A": "function myFunction():", 
#     "option_B": "def myFunction():", 
#     "option_C": "func myFunction():", 
#     "option_D": "function: myFunction()", 
#     "answer": "def myFunction():"
#     },
#     {"question": "Which of the following is the correct way to create a list in Python?", 
#     "option_A": "list = (1, 2, 3)", 
#     "option_B": "list = [1, 2, 3]", 
#     "option_C": "list = {1, 2, 3}", 
#     "option_D": "list = <1, 2, 3>", 
#     "answer": "list = [1, 2, 3]"
#     },
#     {"question": "How do you add an item to a list in Python?", "option_A": "list.add(4)", "option_B": "list.append(4)", "option_C": "list.insert(4)", "option_D": "list.push(4)", "answer": "list.append(4)"},
#     {"question": "Which of the following is used to handle errors in Python?", 
#     "option_A": "try...catch", 
#     "option_B": "try...except", 
#     "option_C": "catch...finally", 
#     "option_D": "throw...catch", 
#     "answer": "try...except"
#     },
#     {"question": "What is the result of '3 == 3' in Python?", "option_A": "True", 
#     "option_B": "False", 
#     "option_C": "Error", 
#     "option_D": "None", 
#     "answer": "True"
#     },
#     {"question": "Which Python operator is used for exponentiation?", 
#     "option_A": "^", 
#     "option_B": "**", 
#     "option_C": "*", 
#     "option_D": "++", 
#     "answer": "**"
#     },
#     {"question": "What is the correct syntax to comment a single line in Python?", 
#     "option_A": "<!-- This is a comment -->", 
#     "option_B": "# This is a comment", 
#     "option_C": "/* This is a comment */", 
#     "option_D": "// This is a comment", 
#     "answer": "# This is a comment"
#     },
#     {"question": "Which function is used to get the length of a list in Python?", "option_A": "list.size()", "option_B": "list.length()", "option_C": "len(list)", "option_D": "list.length", "answer": "len(list)"
#     }
# ]
