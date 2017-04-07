from tkinter import *
from tkinter import ttk
import re
import random
import operator
import fractions
from collections import OrderedDict
from fractions import Fraction

TITLE_FONT = ("Helvetica", 18, "bold")


class FractionApp:
    #container
    def __init__(self, parent):
        self.master = ""
        self.display = 0

        self.parent = parent

        self.parent.minsize(width=300, height=200)
        self.login()
        
    def login(self):
        try:
            self.container.destroy()
        except:
            pass
        
        self.container = Frame(self.parent)
        self.container.pack(side="top", fill="both", expand=True)
        
        self.prompt = Label(self.container, text="Login Page", font=TITLE_FONT)
        self.prompt.pack()

        #Labels and textbox for username and password
        Label(self.container, text="Username: ").pack()
        self.username = Entry(self.container).pack()
        
        Label(self.container, text="Password: ").pack()
        self.password = Entry(self.container, show="*").pack()

        #login button
        self.loginButton = Button(self.container, text="Login", fg='blue', command=lambda: self.checkCredentials())
        self.loginButton.pack(side=RIGHT, padx=50)
        
        #create button
        self.createbutton = Button(self.container, text="Create New Account", command=lambda:self.create())
        self.createbutton.pack(side=LEFT, padx=30)
        
    #containera
    def create(self):
        self.container.destroy()

        self.container = Frame(self.parent)
        self.container.pack()

        Label(self.container, text="Create New User", font=TITLE_FONT).pack()
        
        Label(self.container, text="New Username: ").pack()
        self.username = Entry(self.container).pack()
        
        Label(self.container, text="New Password: ").pack()
        self.password = Entry(self.container, show="*").pack()

    #container
    def mainmenu(self):
        self.container.destroy()

        self.container = Frame(self.parent)
        self.container.pack()
        
        Label(self.container, text="Main Menu", font=TITLE_FONT).pack()
        Label(self.container, text="").pack()
        
        self.solverbutton = Button(self.container, text="Solver", command=lambda: self.solver())
        self.solverbutton.pack()
        
        Label(self.container, text="").pack()
        
        self.solverbutton = Button(self.container, text="Quizzer", command=lambda: self.quizzer())
        self.solverbutton.pack()
        
        Label(self.container, text="").pack()

        self.solverbutton = Button(self.container, text="Results", command=lambda: self.results())
        self.solverbutton.pack()

        Label(self.container, text="").pack()

        self.solverbutton = Button(self.container, text="Log Out", command=lambda: self.login())
        self.solverbutton.pack()

        Label(self.container, text="").pack()
        
        
    def checkCredentials(self):
        self.mainmenu()

    #container
    def solver(self):
        self.container.destroy()
        
        self.container = Frame(self.parent)
        self.container.pack()
        
        Label(self.container, text="Solver", font=TITLE_FONT).pack()

        self.solverbutton = Button(self.container, text="Back to Main Menu", command=lambda: self.mainmenu())
        self.solverbutton.pack()
        

        Label(self.container, text="Type in a Fraction you want to solve: ").pack()
        self.solve = Entry(self.container)
        self.solve.pack()

        self.solvebutton = Button(self.container, text="Solve", command=lambda: self.answer(self.solve))
        self.solvebutton.pack()
        
    #working on
    
    def answer(self, other):
        self.prob = self.solve.get()

        self.patt = "(.*.)/(.) *(.) *(.*.)/(.)"

        try:
            self.user = re.findall(self.patt, self.prob)[0]
            self.sign = self.user[2]
            self.frac1 = Fraction(int(self.user[0]), int(self.user[1]))
            self.frac2 = Fraction(int(self.user[3]), int(self.user[4]))
            
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
            self.theAnswer = Label(self.container, text="Answer: \n" + solution)
            self.theAnswer.pack()
            

        except KeyError as e:
            print("Error: ", e)
            print("Operator must be either: + - * /")
            print()
            
        except IndexError as e:
            print("Error: ", e)
            print("You've entered too little or too many numbers")
            print("Please enter ONLY two fractions in the form: fraction operator fraction")
            print()
        
    #container
    def quizzer(self):
        self.container.destroy()
        
        self.container = Frame(self.parent)
        self.container.pack()

        Label(self.container, text="Results", font=TITLE_FONT).pack()
        """
        self.solverbutton = Button(self.container, text="Back to Main Menu", command=lambda: self.mainmenu())
        self.solverbutton.pack()
        """

    #container
    def results(self):
        self.container.destroy()
        
        self.container = Frame(self.parent)
        self.container.pack()
        
        Label(self.container, text="Results", font=TITLE_FONT).pack()
        """
        self.solverbutton = Button(self.container, text="Back to Main Menu", command=lambda: self.mainmenu())
        self.solverbutton.pack()
        """
        
        

root = Tk()

text = Label(root, text="Fraction Helper Application\n")
text.pack()
myapp = FractionApp(root)

root.mainloop()
