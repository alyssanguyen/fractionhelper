from tkinter import *
import tkinter as tk
import sqlite3
from fractions import Fraction
import fractions
import re
import random
import plotly.plotly as py
import plotly.graph_objs as go

#random fonts used throughout the code
TITLE_FONT = ("Helvetica", 14, "bold")
APP_FONT = ("Avenir", 18, "bold")
ANSWER = ("Helvetica", 14, "bold")
curruser = None

class login:
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.minsize(width=300, height=200)
        self.createContainer()
        
    def createContainer(self):
        try:
            self.container.destroy()
        except:
            pass
        
        self.container = Frame(self.parent)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.configure(background="lightblue")
        
        Label(self.container, text="The Fraction Helper", font=APP_FONT, fg='green', background="lightblue").pack()
        
        self.prompt = Label(self.container, text="Login Page", font=TITLE_FONT, background="lightblue")
        self.prompt.pack()

        #Labels and textbox for username and password
        Label(self.container, text="Username: ", background="lightblue").pack()
        self.username = Entry(self.container)
        self.username.pack()
        
        Label(self.container, text="Password: ", background="lightblue").pack()
        self.password = Entry(self.container, show="*")
        self.password.pack()

        #login button
        self.loginButton = Button(self.container, text="Login", fg='blue', command=lambda: self.navigateApp(mainMenu))
        self.loginButton.pack(side=RIGHT, padx=50)
        
        #create button
        self.createbutton = Button(self.container, text="Create New Account", command=lambda:self.navigateApp(createUser))
        self.createbutton.pack(side=LEFT, padx=30)

    def invalid(self):
        self.window = tk.Toplevel(self.parent)
        self.window.minsize(width=200, height=75)
        Label(self.window, fg='red', text="Error!").pack()
        Label(self.window, text="Invalid username or password \n Please try again").pack()

    def checkCredentials(self):
        """
        Takes in users input for: username and password
        and checks if the username and password matches with the database

        For: login container
        
        """
        with sqlite3.connect("Users.db") as conn:
            c = conn.cursor()

        c.execute('''
        CREATE TABLE IF NOT EXISTS newDatabase(
        userID INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(20) NOT NULL,
        password VARCHAR(20),
        operator VARCHAR(1) NOT NULL,
        score REAL(20) NOT NULL);
        ''')
        
        user = str(self.username.get())
        pw = str(self.password.get())
        success = False
        
        query = "SELECT * FROM newDatabase"
        c.execute(query)
        rows = c.fetchall()
        for row in rows:
            if row[1] == user and row[2] == pw:
                print('Login Success')
                success = True

                #checks for user that is currently logged in
                curruser = user
        
        if success == True:
            self.mainmenu()
        else:
            if len(user) == 0 and len(pw) == 0:
                self.noentry()
            else:
                print('Login Failed')
                self.login()
                self.invalid()
                

    def navigateApp(self, whereTo):
        root = Tk()
        app = whereTo(root)
        root.configure(background="lightblue")
        

#------------------------------------------------------------------------------------------------------------------------------

class createUser:

    def __init__(self, parent):
        self.parent = parent
        self.parent.minsize(width=300, height=200)
        self.createContainer()

    def createContainer(self):
        """
        Create New User
        Users enter new username and new password
        """
    
        self.container = Frame(self.parent)
        self.container.pack()
        self.container.configure(background="lightblue")
        
        Label(self.container, text="The Fraction Helper", font=APP_FONT, fg='green', background="lightblue").pack()
        Label(self.container, text="Create New User", font=TITLE_FONT, background="lightblue").pack()

        #entry box for new username
        Label(self.container, text="New Username: ", background="lightblue").pack()
        self.newusername = Entry(self.container)
        self.newusername.pack()

        #entry box for new password
        Label(self.container, text="New Password: ", background="lightblue").pack()
        self.newpassword = Entry(self.container, show="*")
        self.newpassword.pack()
        
        Label(self.container, text="", background="lightblue").pack()

        #button for create
        self.createbutton = Button(self.container, text="Create", fg='blue', command=lambda: self.createuser())
        self.createbutton.pack(side= RIGHT, padx=10)

        #button for going back to login
        self.loginButton1 = Button(self.container, text="Back to Login", command=lambda: self.navigateApp(login))
        self.loginButton1.pack(side=LEFT, padx=10)
        
    def createuser(self):
        
        """
        Takes in users input for: username and password
        and puts it into a database, as well as
        initialize operator and score with that user

        For: create container
        
        """
        username = self.newusername.get()
        password = self.newpassword.get()
        
        with sqlite3.connect("Users.db") as conn:
            c = conn.cursor()

        c.execute('''
        CREATE TABLE IF NOT EXISTS newDatabase(
        userID INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(20) NOT NULL,
        password VARCHAR(20),
        operator VARCHAR(1) NOT NULL,
        score REAL(20) NOT NULL);
        ''')
        
        try:
            
            c.execute("SELECT * FROM newDatabase WHERE username = '%s'" % username)
            results = c.fetchall()
        
        except Exception as e:
            print("Error:", e)
            conn.close()
        
        try:
            if results[0][0] == username:
                print("Username already taken, try again")
                conn.close()
            else:
                self.usernameError()
        except:
            try:
                #make sure that something is entered
                if len(username) != 0 and len(password) != 0:
                    c.execute("INSERT INTO newDatabase (username, password, operator, score) VALUES (?, ?, ?, ?)", (username, password, 0, 0))
                    conn.commit()
                    c.close()
                    conn.close()
                    print("Username: %s Created!" % (username))
                    Label(self.container, text="Success! User created").pack()
                else:
                    self.noentry()
            except Exception as e:
                print(e)
                conn.close()

    #--------------------------------------------------------------
    #Login and Create New Account Error Pop Up Windows
    #--------------------------------------------------------------
    def usernameError(self):
        self.window = tk.Toplevel(self.parent)
        self.window.minsize(width=200, height=75)
        Label(self.window, fg='red', text="Error!").pack()
        Label(self.window, text="Username already taken \n Please choose a different username \n and try again").pack()

    def noentry(self):
        self.window = tk.Toplevel(self.parent)
        self.window.minsize(width=200, height=75)
        Label(self.window, fg='red', text="Error!").pack()
        Label(self.window, text="Nothing was entered for \n Username or Password \n \n Please try again").pack()    

    def navigateApp(self, whereTo):
        root = Tk()
        app = whereTo(root)
        root.configure(background="lightblue")

        
#------------------------------------------------------------------------------------------------------------------------------

class mainMenu:
    def __init__(self, parent):
        self.parent = parent
        self.parent.minsize(width=300, height=200)
        self.createContainer()

    def createContainer(self):

        self.container = Frame(self.parent)
        self.container.pack()

        self.container.configure(background="lightblue")

        Label(self.container, text="Welcome to The Fraction Helper", font=APP_FONT, fg='green', background="lightblue").pack()
        
        Label(self.container, text="Main Menu", font=TITLE_FONT, background="lightblue").pack()
        Label(self.container, text="", background="lightblue").pack()
        
        self.solverbutton = Button(self.container, text="Solver", background="lightgoldenrod", command=lambda: self.navigateApp(solver))
        self.solverbutton.pack()
        
        Label(self.container, text="", background="lightblue").pack()
        
        self.solverbutton = Button(self.container, text="Quizzer",background="coral", command=lambda: self.navigateApp(quizzer))
        self.solverbutton.pack()
        
        Label(self.container, text="", background="lightblue").pack()

        self.solverbutton = Button(self.container, text="Results", background="lightgreen", command=lambda: self.navigateApp(results))
        self.solverbutton.pack()

        Label(self.container, text="", background="lightblue").pack()

        self.solverbutton = Button(self.container, text="Log Out", command=lambda: self.navigateApp(login))
        self.solverbutton.pack()

        Label(self.container, text="", background="lightblue").pack()

    def navigateApp(self, whereTo):
        root = Tk()
        app = whereTo(root)
        root.configure(background="lightblue")
    
#------------------------------------------------------------------------------------------------------------------------------

class solver:
    def __init__(self, parent):
        self.parent = parent
        self.parent.minsize(width=300, height=200)
        self.createContainer()

    def createContainer(self):
    
        self.container = Frame(self.parent)
        self.container.pack(expand=True)
        self.container.grid_rowconfigure(0, weight=0)
        self.container.grid_columnconfigure(0, weight=0)

        self.container.configure(background="lightgoldenrod")
        
        Label(self.container, text="The Fraction Helper", font=APP_FONT, fg='green', background="lightgoldenrod").grid(row=0, columnspan=6)
        
        Label(self.container, text="Solver", font=TITLE_FONT, background="lightgoldenrod").grid(row=1,columnspan=6)

        self.solverbutton = Button(self.container, text="Back to Main Menu", background="lightblue", command=lambda: self.navigateApp(mainMenu))
        self.solverbutton.grid(row=2, columnspan=6)

        Label(self.container, text="", font=TITLE_FONT, background="lightgoldenrod").grid(row=3,columnspan=6)
        
        self.tkvar = StringVar(self.container)

        Label(self.container, text="Type in a Fraction Problem you wish to solve \n (Type fraction with ""/""): \n ", fg="darkblue", font=("Avenir", 12, "bold"), background="lightgoldenrod").grid(row=4, columnspan=6)
        
        self.solve0 = Entry(self.container, width=7)
        self.solve0.grid(row=7, column=0)

        Label(self.container, text="Fraction", font=("Avenir", 11, "bold"), background="lightgoldenrod").grid(row=6, column=0)
        """
        self.solve1 = Entry(self.container, width=5)
        self.solve1.grid(row=6, column=0)
        """
        self.option = OptionMenu(self.container, self.tkvar, "+", "-", "*", "/")
        self.option.grid(row=7, column=1)

        Label(self.container, text="Operator", font=("Avenir", 11, "bold"), background="lightgoldenrod").grid(row=6, column=1)

        self.solve3 = Entry(self.container, width=7)
        self.solve3.grid(row=7, column=2)
        Label(self.container, text="Fraction", font=("Avenir", 11, "bold"), background="lightgoldenrod").grid(row=6, column=2)
        """
        self.solve4 = Entry(self.container, width=5)
        self.solve4.grid(row=6, column=2)
        """

        Label(self.container, text="=", background="lightgoldenrod").grid(row=7, column=3)
        
        Label(self.container, text="Answer:", font=("Avenir", 11, "bold"), background="lightgoldenrod").grid(row=6, column=4)
        
        self.solve = StringVar()
        #self.solve.set(str(self.solve0.get()) + "/" + str(self.solve1.get()) + str(self.tkvar.get()) + str(self.solve3.get()) + "/" + str(self.solve4.get()))

        self.solvebutton = Button(self.container, text="Solve", fg='white', background="blue", command=lambda: self.answer())
        self.solvebutton.grid(row=10, column=4)

        Label(self.container, text="", background="lightgoldenrod").grid(row=11, columnspan=1)
    #--------------------------------------------------------------
    #Solver Error Pop Up Windows
    #--------------------------------------------------------------
    def dividebyzero(self):
        self.window = tk.Toplevel(self.parent)
        self.window.minsize(width=200, height=75)
        Label(self.window, fg='red', text="Error!").pack()
        Label(self.window, text="Fractions are not allowed \n to be divided by zero").pack()

    def form(self):
        self.window = tk.Toplevel(self.parent)
        self.window.minsize(width=200, height=75)
        Label(self.window, fg='red', text="Error!").pack()
        Label(self.window, text="Must be in the form: \n <fraction> <operator> <fraction> \n Example: 1/2 + 1/2 \n Must be Fraction Form").pack()

    def fracform(self):
        self.window = tk.Toplevel(self.parent)
        self.window.minsize(width=200, height=75)
        Label(self.window, fg='red', text="Error!").pack()
        Label(self.window, text="Fraction must be entered as \n integer\integer").pack()
        
    def answer(self):
        """
        Takes in <fraction> <operator> <fraction> from user
        and solves that fraction problem

        (aka: a fraction calculator)

        For: solver container

        Raise Exception: KeyError, ZeroDivisionError, IndexError, ValueError
        
        """
        self.patt = r'\d+|^[-]\d+|\s.\s'

        self.prob = str(self.solve0.get()) + str(self.tkvar.get()) + str(self.solve3.get())
        print(self.prob)
        self.user = re.findall(self.patt,self.prob)
        oper = str(self.tkvar.get())
        self.user.insert(2, oper)
        
        try:    
            self.sign = self.user[2]
            self.frac1 = fractions.Fraction(self.user[0] + "/" + self.user[1])
            self.frac2 = fractions.Fraction(self.user[3] + "/" + self.user[4])
            
            self.op = {"+": self.frac1 + self.frac2,
                  "-": self.frac1 - self.frac2,
                  "*": self.frac1 * self.frac2,
                  "/": self.frac1 / self.frac2}
            
            self.R = self.op[self.sign]         
            self.userfract = self.user[0] + "/" + self.user[1] + " " + self.sign + " " + self.user[3] + "/" + self.user[4]
            
            solution = "{0}".format(self.R)
            
            try:
                self.theAnswer.destroy()
            except:
                pass
            self.theAnswer = Label(self.container, text=solution, fg='green', font=ANSWER)
            self.theAnswer.grid(row=7, column=4)
            
        except KeyError as e:
            try:
                self.theAnswer.destroy()
            except:
                pass
            Label(self.container, text="ERROR!" + solution, fg='green', bg='yellow', font=ANSWER)
            self.theAnswer.grid(row=7, columnspan=4)
        #has to be entered correctly
        except ZeroDivisionError as e:
            try:
                self.theAnswer.destroy()
            except:
                pass
            
            self.dividebyzero()
            
        except IndexError as e:
            try:
                self.theAnswer.destroy()
            except:
                pass
          
            self.form()
            
        except ValueError as e:
            try:
                self.theAnswer.destroy()
            except:
                pass

            self.fracform()

    def navigateApp(self, whereTo):
        root = Tk()
        app = whereTo(root)
        root.configure(background="lightblue")

#------------------------------------------------------------------------------------------------------------------------------

class quizzer:
    def __init__(self, parent):
        self.parent = parent
        self.parent.minsize(width=300, height=200)
        self.createContainer()

    def createContainer(self):
        """
        Gives users random fraction problem
        Takes users answers
        Grades the answers accordingly.
        
        """
        self.flag = StringVar()
        self.flag = False

        self.flag1=StringVar()
        self.flag1=False

        self.container = Frame(self.parent)
        self.container.pack(expand=True)
        self.container.grid_rowconfigure(0, weight=0)
        self.container.grid_columnconfigure(0, weight=0)
        self.container.configure(background="coral")
        Label(self.container, text="The Fraction Helper", font=APP_FONT, fg='green', background="coral").grid(row=0, columnspan=7)

        Label(self.container, text="Quizzer", fg='purple',font=TITLE_FONT, background="coral").grid(row=1,columnspan=7)

        #COMMAND IS THE FUNCTION TO BE CALL
        self.button1 = Button(self.container, text="Back to Main Menu", background="lightblue", command=lambda: self.mainmenu())
        self.button1.grid(row=3,columnspan=7)

        #space
        Label(self.container, text="", font=TITLE_FONT, background="coral").grid(row=4,columnspan=1)

        Label(self.container, text="Please choose an operator and then click generate.", fg="DarkBlue", font=("Avenir",12, "bold"), background="coral").grid(row=5,columnspan=7)
        Label(self.container, text="To check your answer click check." ,justify=LEFT, fg="DarkBlue", font=("Avenir",12, "bold"), background="coral").grid(row=6,columnspan=7)
        Label(self.container, text="To generate next question click next and start over.", fg="DarkBlue", font=("Avenir",12, "bold"), background="coral").grid(row=7,columnspan=7)

        Label(self.container, text="", font=TITLE_FONT, background="coral").grid(row=8,columnspan=1)

        self.num1 = StringVar()
        self.num2 = StringVar()
        self.tkvar1 = StringVar(self.container)
        self.tkvar1.set("+")
        self.num3 = StringVar() #input

        #box1
        self.box1 = Entry(self.container, width=5, text= self.num1, state = 'disabled', disabledforeground = 'darkblue', font=("Avenir", 12, "bold"))
        self.box1.grid(row=9, column=1)

        #box2
        self.box2 = Entry(self.container,width=5, text= self.num2, state = 'disabled', disabledforeground = 'darkblue', font=("Avenir", 12, "bold"))
        self.box2.grid(row=9, column=3)

        #operator
        self.option = OptionMenu(self.container, self.tkvar1, "+", "-", "*", "/")
        self.option.grid(row=9, column=2)

        Label(self.container, text="Enter your answer as a fraction ex: 3/4 or  whole number if apply.", background="coral", fg="DarkBlue", font=("Avenir",12, "bold")).grid(row=12,columnspan=6)

        Label(self.container, text="=", background="coral").grid(row=9, column=4)
        
        #box for user's answer
        Label(self.container, text="Your Answer:", background="coral", font=("Avenir", 12, "bold")).grid(row=8, column=5)

        self.box3 = Entry(self.container,width=8, text= self.num3, highlightbackground="LightBlue")
        self.box3.grid(row=9, column=5)

        Label(self.container, text="", font=TITLE_FONT, background="coral").grid(row=16,columnspan=1)#space

        #BUTTOMS
        self.button2 = Button(self.container, text="Generate",background="purple", fg="white", command=lambda: self.generateRandom(self.flag))
        self.button2.grid(row=17, column=1)

        self.button3 = Button(self.container, text="Check",background="lightseagreen", command=lambda: self.checkAnswer(self.box3))
        self.button3.grid(row=17, column=3)

        self.button4 = Button(self.container, text="Next" , background="springgreen2",command=lambda: self.navigateApp(quizzer))
        self.button4.grid(row=17, column=5)

        Label(self.container, text="", background="coral", font=TITLE_FONT).grid(row=18,columnspan=1)
    # quiz
    def generateRandom(self, other):
        """
        creates random fractions

        For: generate button
        
        """
        if self.flag is True:
            return
        self.flag = True

        a = random.randint(1, 10)
        b = random.randint(2, 10)
        c = random.randint(1, 10)
        d = random.randint(2, 10)

        n1 = str(a)
        d1 = str(b)
        n2 = str(c)
        d2 = str(d)

        r1 = n1 + "/" + d1
        r2 = n2 + "/" + d2
        
        if a != b and b > 1:
            self.num1.set(r1)
        if c != d and d > 1:
            self.num2.set(r2)
        return

    #--------------------------------------------------------------
    #Quizzer Error Pop Up
    #--------------------------------------------------------------
    def noquizentry(self):
        self.window = tk.Toplevel(self.parent)
        self.window.minsize(width=200, height=75)
        Label(self.window, fg='red', text="Error!").pack()
        Label(self.window, text="No answer was entered! \n Please click '\'Next'\' and try again").pack()

    #check quiz's answer 
    def checkAnswer(self, other):
        """
        Takes in fraction problem and user's answer and checks the answer

        1 point - Fully Correct Answer
        0.5 - Partially Correct
        0 - Wrong

        For: Quizzer Container

        Raise Exception: Index, UnboundLocalError, TypeError
        
        """
        if self.flag1 is True:
            return
        self.flag1 = True
        
        patt = re.compile(r'(-?\d+)/?(-?\d+)?([+\-*/])(-?\d+)/?(-?\d+)?')
        self.s = str(self.box1.get()) + str(self.tkvar1.get()) + str(self.box2.get())   
        
        if self.s is None:
            raise TypeError
        try:
            sm = re.findall(patt,self.s)[0]
            numerator1 = sm[0]
            denominator1 = sm[1]
            operator = sm[2]
            numerator2 = sm[3]
            denominator2 = sm[4]

            
            
            if not denominator1:
                denominator1 = 1
            if not denominator2:
                denominator2 = 1   
            #print(sm[0], sm[1], sm[2], sm[3], sm[4], "HERE1.1")

            print("n1", sm[0], "d1", sm[1], "o", sm[2], "n2", sm[3], "d2", sm[4])
               
        except IndexError:
            print("IndexError, try again.")
        except UnboundLocalError:
            print("Error: regex pattern didn't detect num1 or num2")
        #print(type(sm))
        #print(sm)
        if sm is None:
            raise TypeError
            print("TypeError, try again.")
        
        X = Fraction(int(numerator1), int(denominator1))
        Y = Fraction(int(numerator2), int(denominator2))
        global O
        O = operator

        
        try:
            if operator is '+':
                R = X + Y
                #R_decimal = float(X) + float(Y)
            if operator is '-':
                R = X - Y
                #R_decimal = float(X) - float(Y)
            if operator is '*':
                R = X * Y
                #R_decimal = float(X) * float(Y)
            if operator is '/':
                print("X", X)
                print("Y", Y)
                if int(denominator1) == 1:
                    num1 = X * int(denominator2)
                    R = Fraction(num1, numerator2)
                    print(R)
                    Y = float(numerator2)/float(denominator2)
                    R_decimal = X / Y
                    print("R den1", R)
                else:
                    R = X / Y
                    Y = float(numerator2)/float(denominator2)
                    R_decimal = X / Y
                    print("R", R)

            #R = Fraction(eval(str(X) + O + str(Y)))
            if operator is not '/':
                R_decimal = eval(str(X) + O + str(Y))
            
            print("R decimal", R_decimal)
            
        except TypeError:
            print("Error, try again.")
       
        #Getting user answer
        self.user = str(self.box3.get())
        #print("input:",self.user)
        patt2 = re.compile(r'(-?\d+)/?(-?\d+)?')
        try:
            userAnswer = re.findall(patt2,self.user)[0]
            numerator = userAnswer[0]
            denominator = userAnswer[1]
        except IndexError as e:
            self.noquizentry()
        
        if denominator:
            # print("split string:", numerator, denominator)
            Z = Fraction(int(numerator), int(denominator))
            Z_decimal = float(numerator)/int(denominator)
        else:
            Z = numerator
            Z_decimal = float(numerator)
        Zstr = self.user
        global Rstr
        Rstr = str(R)
        print("Z decimal", Z_decimal)
        if Zstr == Rstr and round(R_decimal, 3) == round(Z_decimal, 3):
            #print ("1 point: correct and reduced")
            #Label(self.container, text="Good job!  1 point: correct and reduced", fg='DarkOrchid2', bg='aquamarine2', font=("Times",17)).grid(row=19,column=2)
            self.correct()
            self.updatescore(curruser, O, 1.0)
            
        elif round(R_decimal, 3) == round(Z_decimal, 3):
            #print (".5 points: correct but not reduced. Correct Answer:", R)
            #Label(self.container, text=".5 points: correct but not reduced. Correct Answer: "+ Rstr , fg='DarkOrchid2', bg='aquamarine2', font=("Times",17)).grid(row=19,column=2)
            self.partiallycorrect()
            self.updatescore(curruser, O, 0.5)
            
        else:
            #print ("0 points: Incorrect answer. Correct Answer:", R) 
            #Label(self.container, text="0 points: Incorrect answer. Correct Answer: "+ str(R) , fg='VioletRed1', bg='azure', font=("Times",17)).grid(row=19,column=2)
            self.wrong()
            self.updatescore(curruser, O, 0)
            

            
    #--------------------------------------------------------------
    #Quizzer Pop Up Windows
    #--------------------------------------------------------------
    def correct(self):
        self.window = tk.Toplevel(self.parent)
        self.window.minsize(width=200, height=75)
        Label(self.window, fg='green', text="Correct!").pack()
        Label(self.window, text="Good job! You've earned 1 point for \n Correct and reduced fraction").pack()

    def partiallycorrect(self):
        self.window = tk.Toplevel(self.parent)
        self.window.minsize(width=200, height=75)
        Label(self.window, fg='blue', text="Partially Correct").pack()
        Label(self.window, text="You were close! You've earned 0.5 point for it.\n Fraction is equivalent to the correct answer \n But, fraction is not reduced. \n Correct Answer is: " + Rstr).pack()

    def wrong(self):
        self.window = tk.Toplevel(self.parent)
        self.window.minsize(width=200, height=75)
        Label(self.window, fg='red', text="Incorrect!").pack()
        Label(self.window, text="Incorrect! You've earned 0 point for \n Fraction is not equivalent to the correct answer \n Correct Answer is: " + Rstr).pack()

    def updatescore(self, username, operator, point):
        """
        Takes in username and the point earned from quizzer
        and puts it into the database into the score section

        For: quizzer

        Raise Exception: Exception
        
        """
        with sqlite3.connect("Users.db") as conn:
            c = conn.cursor()
        
        c.execute('''
        CREATE TABLE IF NOT EXISTS newDatabase(
        userID INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(20),
        password VARCHAR(20),
        operator VARCHAR(1),
        score REAL(20));
        ''')
        
        username = curruser
        
        
        query = "SELECT * FROM newDatabase WHERE username = '%s'" % username

        try:
            c.execute(query)
            results = c.fetchall()

        except Exception as e:
            print("DATABASE ERROR!", e)

        userresults = results[0][4]

        #query1 = "UPDATE newDatabase SET score='%d' WHERE username='%s'" %((userresults + point), username)
        #query1 = "INSERT INTO newDatabase VALUES(?, ?, ?, ?)", (username, None, operator, score)
        c.execute("INSERT INTO newDatabase (username, password, operator, score) VALUES (?, ?, ?, ?)", (username, None, operator, point))
        conn.commit()
        conn.close()

    def overallavg(self):
        """
        Takes in username and the point earned from quizzer
        and puts it into the database into the score section

        For: quizzer

        Raise Exception: Exception
        
        """
        with sqlite3.connect("Users.db") as conn:
            c = conn.cursor()
        
        c.execute('''
        CREATE TABLE IF NOT EXISTS newDatabase(
        userID INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(20),
        password VARCHAR(20),
        operator VARCHAR(1),
        score REAL(20));
        ''')
        
        username = curruser
        
        
        query = "SELECT AVG(score) FROM newDatabase WHERE operator = '+'" 

        try:
            c.execute(query)
            global overallplus
            overallplus = c.fetchall()
            
        except Exception as e:
            print("DATABASE ERROR!", e)

        c.execute("SELECT AVG(score) FROM newDatabase WHERE operator = '-'")
        global overallsub
        overallsub = c.fetchall()

        c.execute("SELECT AVG(score) FROM newDatabase WHERE operator = '*'")
        global overallmul
        overallmul = c.fetchall()

        c.execute("SELECT AVG(score) FROM newDatabase WHERE operator = '/'")
        global overalldiv
        overalldiv = c.fetchall()

        c.execute("SELECT AVG(score) FROM newDatabase")
        global overallall
        overallall = c.fetchall()

        conn.commit()
        conn.close()

    def useravg(self, username):
        """
        Takes in username and the point earned from quizzer
        and puts it into the database into the score section

        For: quizzer

        Raise Exception: Exception
        
        """
        with sqlite3.connect("Users.db") as conn:
            c = conn.cursor()
        
        c.execute('''
        CREATE TABLE IF NOT EXISTS newDatabase(
        userID INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(20),
        password VARCHAR(20),
        operator VARCHAR(1),
        score REAL(20));
        ''')
        
        username = curruser
        
        
        query = "SELECT AVG(score) FROM newDatabase WHERE username = '%s' AND operator = '+'" % username

        try:
            c.execute(query)
            global userplus
            userplus = c.fetchall()
            
        except Exception as e:
            print("DATABASE ERROR!", e)

        c.execute("SELECT AVG(score) FROM newDatabase WHERE username = '%s' AND operator = '-'" % username)
        global usersub
        usersub = c.fetchall()

        c.execute("SELECT AVG(score) FROM newDatabase WHERE username = '%s' AND operator = '*'" % username)
        global usermul
        usermul = c.fetchall()

        c.execute("SELECT AVG(score) FROM newDatabase WHERE username = '%s' AND operator = '/'" % username)
        global userdiv
        userdiv = c.fetchall()

        c.execute("SELECT AVG(score) FROM newDatabase WHERE username = '%s'" % username)
        global userall
        userall = c.fetchall()

        conn.commit()
        conn.close()

    def navigateApp(self, whereTo):
        root = Tk()
        app = whereTo(root)
        root.configure(background="lightblue")
        
#------------------------------------------------------------------------------------------------------------------------------
class results:

    def __init__(self, parent):
        self.parent = parent
        self.parent.minsize(width=300, height=200)
        self.createContainer()

    def createContainer(self):
        # Delete old container and create new one to display results
        self.container = Frame(self.parent)
        self.container.pack()
        self.container.configure(background="lightblue")
        # Display container Description        
        Label(self.container, text="The Fraction Helper", font=APP_FONT, fg='green', background="lightblue").pack()
        Label(self.container, text="Results", font=TITLE_FONT, background="lightblue").pack()
        
        # Plotly API - 
        # -----------------------------------------------------------------------------------------------
        self.useravg(curruser)
        self.overallavg()
        
        trace0 = go.Bar(
            x=['+', '-','*','/', 'all'],
            y=[userplus[0][0], usersub[0][0], usermul[0][0], userdiv[0][0], userall[0][0]],
            name='User',
            marker=dict(
                color='rgb(49,130,189)'
            )
        )
        trace1 = go.Bar(
            x=['+', '-','*','/', 'all'],
            y=[overallplus[0][0], overallsub[0][0], overallmul[0][0], overalldiv[0][0], overallall[0][0]],
            name='Overall',
            marker=dict(
                color='rgb(204,204,204)',
            )
        )

        data = [trace0, trace1]
        layout = go.Layout(
            xaxis=dict(tickangle=0),
            barmode='group',
        )

        fig = go.Figure(data=data, layout=layout)
        py.plot(fig, filename='angled-text-bar')

        # Main menu button
        self.new_button = Button(self.container, text="Back to Main Menu", command=lambda: navigateApp(mainMenu))
        self.new_button.pack()

    def overallavg(self):
        """
        Takes in username and the point earned from quizzer
        and puts it into the database into the score section

        For: quizzer

        Raise Exception: Exception
        
        """
        with sqlite3.connect("Users.db") as conn:
            c = conn.cursor()
        
        c.execute('''
        CREATE TABLE IF NOT EXISTS newDatabase(
        userID INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(20),
        password VARCHAR(20),
        operator VARCHAR(1),
        score REAL(20));
        ''')
        
        username = curruser
        
        
        query = "SELECT AVG(score) FROM newDatabase WHERE operator = '+'" 

        try:
            c.execute(query)
            global overallplus
            overallplus = c.fetchall()
            
        except Exception as e:
            print("DATABASE ERROR!", e)

        c.execute("SELECT AVG(score) FROM newDatabase WHERE operator = '-'")
        global overallsub
        overallsub = c.fetchall()

        c.execute("SELECT AVG(score) FROM newDatabase WHERE operator = '*'")
        global overallmul
        overallmul = c.fetchall()

        c.execute("SELECT AVG(score) FROM newDatabase WHERE operator = '/'")
        global overalldiv
        overalldiv = c.fetchall()

        c.execute("SELECT AVG(score) FROM newDatabase")
        global overallall
        overallall = c.fetchall()

        conn.commit()
        conn.close()

    def useravg(self, username):
        """
        Takes in username and the point earned from quizzer
        and puts it into the database into the score section

        For: quizzer

        Raise Exception: Exception
        
        """
        with sqlite3.connect("Users.db") as conn:
            c = conn.cursor()
        
        c.execute('''
        CREATE TABLE IF NOT EXISTS newDatabase(
        userID INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(20),
        password VARCHAR(20),
        operator VARCHAR(1),
        score REAL(20));
        ''')
        
        username = curruser
        
        query = "SELECT AVG(score) FROM newDatabase WHERE username = '%s' AND operator = '+'" % username

        try:
            c.execute(query)
            global userplus
            userplus = c.fetchall()
            
        except Exception as e:
            print("DATABASE ERROR!", e)

        c.execute("SELECT AVG(score) FROM newDatabase WHERE username = '%s' AND operator = '-'" % username)
        global usersub
        usersub = c.fetchall()

        c.execute("SELECT AVG(score) FROM newDatabase WHERE username = '%s' AND operator = '*'" % username)
        global usermul
        usermul = c.fetchall()

        c.execute("SELECT AVG(score) FROM newDatabase WHERE username = '%s' AND operator = '/'" % username)
        global userdiv
        userdiv = c.fetchall()

        c.execute("SELECT AVG(score) FROM newDatabase WHERE username = '%s'" % username)
        global userall
        userall = c.fetchall()

        conn.commit()
        conn.close()
        
    def navigateApp(self, whereTo):
        root = Tk()
        app = whereTo(root)
        root.configure(background="lightblue")


#------------------------------------------------------------------------------------------------------------------------------
        
if __name__ == "__main__":
    root = Tk()
    app = login(root)
    root.configure(background="lightblue")
    root,mainloop()
