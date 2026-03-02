Python 3.13.12 (tags/v3.13.12:1cbe481, Feb  3 2026, 18:22:25) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> age = 28
>>> print ("อายุของผมคือ ") = age
SyntaxError: cannot assign to function call here. Maybe you meant '==' instead of '='?
>>> print ("อายุของผมคือ " , age)
อายุของผมคือ  28
>>> name = fahad dueramae
SyntaxError: invalid syntax
>>> name = "fahad dueramae"
>>> age = 28
>>> print(f"สวัสดี {name}, อายุ {age} ปี ")
สวัสดี fahad dueramae, อายุ 28 ปี 
>>> print("Python","Java","C++", sep="|")
Python|Java|C++
