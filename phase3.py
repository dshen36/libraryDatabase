from tkinter import*
import pymysql
import urllib.request

class GUI:
    def __init__(self,win):
        self.LoginPage()
        self.RegisterPage()
        self.secondwin.withdraw()

    def LoginPage(self):
        self.mainwin = win
        self.mainwin.title("Login")
        self.mainwin.config(bg="white")

        self.sv=StringVar()
        self.sv2=StringVar()
        
        l = Label(self.mainwin,text = "Username:",bg="white")
        l.grid(row=1,column=0)
        l2 = Label(self.mainwin,text="Password:",bg="white")
        l2.grid(row=2,column=0)

        f=Frame(self.mainwin)
        f.config(bg="white")
        f.grid(row=1,column=1)
        
        f2=Frame(self.mainwin)
        f2.config(bg="white")
        f2.grid(row=2,column=1)

        e = Entry(f,textvariable=self.sv)
        e.grid(row=0,column=0,padx=2,pady=2)
        e2 = Entry(f2,textvariable=self.sv2)
        e2.grid(row=0,column=0,padx=2,pady=2)

        f3=Frame(self.mainwin)
        f3.config(bg="white")
        f3.grid(row=3,column=2)
        b1 = Button(f3,text="Login")#,command=self.LoginCheck)
        b1.grid(row=3,column=2,padx=2,pady=2)
        b2 = Button(f3,text="Create Account",command=self.ToRegister)
        b2.grid(row=3,column=3,padx=2,pady=2)

    def ToRegister(self):
        self.secondwin.deiconify()
        self.mainwin.withdraw()

    def Connect(self):
        try:
            db = pymysql.connect(host="academic-mysql.cc.gatech.edu",passwd="am4uNpz1",
                                 user="cchan61",db="cs2316db")
            
            return db
        except:
            info = messagebox.showinfo("Problem!", "Cannot connect to the database! Please check your internet connection.")            
            return None

    def LoginCheck(self):
        self.database = self.Connect()
        c = self.database.cursor()
        
        self.username = self.sv.get()
        password = self.sv2.get()

        #check to see if username and password is in the database
        sql = "SELECT Username,Password FROM User"
        c.execute(sql)
        sql1 = "SELECT Username FROM User WHERE Username=%s AND Password=%s"
        c.execute(sql1,self.username,password)
        data = c.fetchall()

        user = (self.username,password)
        if user in data:
            c.close()
            self.SearchBooks()
            self.mainwin.withdraw()
        else:
            info2 = messagebox.showinfo("","You entered an unrecognizable username/password combination")

    def RegisterPage(self):
        self.secondwin = Toplevel()
        self.secondwin.title("New User Registration")
        self.secondwin.config(bg="white")

        f = Frame(self.secondwin)
        f.config(bg="white")
        f.grid(row=1,column=0)
        l2=Label(f,text="Username:",bg="white")
        l2.grid(row=1,column=0,sticky=W)
        l3=Label(f,text="Password:",bg="white")
        l3.grid(row=2,column=0,sticky=W)
        l4=Label(f,text="Confirm Password:",bg="white")
        l4.grid(row=3,column=0,sticky=W)

        f2 = Frame(self.secondwin)
        f2.config(bg="white")
        f2.grid(row=1,column=1)
        self.e = Entry(f2)
        self.e.grid(row=0,column=0,padx=2,pady=2)
        self.e2 = Entry(f2)
        self.e2.grid(row=1,column=0,padx=2,pady=2)
        self.e3 = Entry(f2)
        self.e3.grid(row=2,column=0,padx=2,pady=2)

        f3 = Frame(self.secondwin)
        f3.config(bg="white")
        f3.grid(row=2,column=2)
        b2 = Button(f3,text="Register",command=self.RegistrationCheck)
        b2.grid(row=4,column=3,padx=2,pady=2)

    def RegistrationCheck(self):
        try:
            #check to see if username has not already been registered
            username = self.e2.get()

            db = self.Connect()
            c = db.cursor()

            sql = "SELECT Username FROM User"
            c.execute(sql)
            data = c.fetchall()

            # username is valid
            if username not in data:
                #check if password and confirm password are the same
                if self.e3.get() != self.e4.get():
                     error = messagebox.showinfo("Problem!","Password and Confirm Password do not match.")
                #password and confirm password are the same, continue
                else:
                    password = self.e3.get()

                    sql = "INSERT INTO User (Username, Password) VALUES (%s,%s)"
                    c.execute(sql, (username, password))
                    c.close()
                    db.commit()
                    db.close()
                    self.secondwin.withdraw()
                    self.CreateProfile()
            else:
                error4 = messagebox.showinfo("Problem","The username already exists.")
        except:
            error4 = messagebox.showinfo("Problem","The username already exists.")
                    

    def CreateProfile(self):
        self.thirdwin = Toplevel()
        self.thirdwin.config(bg="white")
        self.thirdwin.title("Create Profile")

        f = Frame(self.thirdwin)
        f.config(bg="white")
        f.grid(row=1,column=0)
        l=Label(f,text="First Name",bg="white")
        l.grid(row=1,column=0,sticky=W)
        l2=Label(f,text="D.O.B",bg="white")
        l2.grid(row=2,column=0,sticky=W)
        l3=Label(f,text="Email",bg="white")
        l3.grid(row=3,column=0,sticky=W)
        l4=Label(f,text="Address",bg="white")
        l4.grid(row=4,column=0,sticky=W)

        f2 = Frame(self.thirdwin)
        f2.config(bg="white")
        f2.grid(row=1,column=1)
        self.e = Entry(f2)
        self.e.grid(row=0,column=0,padx=2,pady=2)
        self.e2 = Entry(f2)
        self.e2.grid(row=1,column=0,padx=2,pady=2)
        self.e3 = Entry(f2)
        self.e3.grid(row=2,column=0,padx=2,pady=2)
        self.e4 = Entry(f2)
        self.e4.grid(row=3,column=0,padx=2,pady=2)

        f3 = Frame(self.thirdwin)
        f3.config(bg="white")
        f3.grid(row=1,column=2)
        l=Label(f3,text="Last Name",bg="white")
        l.grid(row=1,column=0,sticky=W)
        l2=Label(f3,text="Gender",bg="white")
        l2.grid(row=2,column=0,sticky=W)
        l3=Label(f3,text="Are you a faculty member?",bg="white")
        l3.grid(row=3,column=0,sticky=W)
        l4=Label(f3,text="Associated Department",bg="white")
        l4.grid(row=4,column=0,sticky=W)
        self.e5 = Entry(f3)
        self.e5.grid(row=1,column=1,padx=2,pady=2)
        var = StringVar(f3)
        var.set("")
        choices = ['M', 'F']
        self.lb = OptionMenu(f3,var,*choices)
        self.lb.grid(row=2,column=1,sticky=E)
        c = Checkbutton(f3, text="Yes", variable=var,bg="white")
        c.grid(row=3,column=1)
##        v = StringVar()
##        combobox = Combobox(f3,textvariable=v)
##        combobox.grid(row=4,column=1)
        var2 = StringVar(f3)
        var2.set("")
        option = OptionMenu(f3,var2,"M","F")
        option.grid(row=4,column=1)
        
        b = Button(f3,text="Submit")
        b.grid(row=5,column=1,padx=2,pady=2)

        self.SearchBooks()
        
    def SearchBooks(self):

        self.fourthwin = Toplevel()
        self.fourthwin.config(bg="white")
        self.fourthwin.title("Search Books")
    
        f = Frame(self.fourthwin)
        f.config(bg="white")
        f.grid(row=1,column=0)
        l=Label(f,text="ISBN",bg="white")
        l.grid(row=1,column=0,sticky=W)
        l2=Label(f,text="Title",bg="white")
        l2.grid(row=2,column=0,sticky=W)
        l3=Label(f,text="Author",bg="white")
        l3.grid(row=3,column=0,sticky=W)

        self.e = Entry(f)
        self.e.grid(row=1,column=1,padx=2,pady=2)
        self.e2 = Entry(f)
        self.e2.grid(row=2,column=1,padx=2,pady=2)
        self.e3 = Entry(f)
        self.e3.grid(row=3,column=1,padx=2,pady=2)

        f2 = Frame(self.fourthwin)
        f2.config(bg="white")
        f2.grid(row=2,column=0)
        b = Button(f2,text="Back")
        b.grid(row=4,column=0)
        b2 = Button(f2,text="Search")
        b2.grid(row=4,column=1)
        b3 = Button(f2,text="Close")
        b3.grid(row=4,column=2)

        self.fourthwin.withdraw()
        self.RequestExtension()

    def RequestExtension(self):

        self.sixthwin = Toplevel()
        self.sixthwin.config(bg="white")
        self.sixthwin.title("Request extension on a book")
        
        f = Frame(self.sixthwin)
        f.config(bg="white")
        f.grid(row=1,column=0)
        l=Label(f,text="Enter your issue_id",bg="white")
        l.grid(row=1,column=0,sticky=W)
        self.e = Entry(f,width=40)
        self.e.grid(row=1,column=1,padx=50,pady=10)
        
        b = Button(f,text="Submit")
        b.grid(row=1,column=2)

        f2= Frame(self.sixthwin)
        f2.config(bg="white")
        f2.grid(row=2,column=0)
        l = Label(f2,text="Original Checkout Date",bg="white")
        l.grid(row=1,column=0,sticky=W)
        l2 = Label(f2,text="Current Extension Date",bg="white")
        l2.grid(row=2,column=0,sticky=W)
        l3 = Label(f2,text="New Extension Date",bg="white")
        l3.grid(row=3,column=0,sticky=W)

        self.sv = StringVar()
        

        self.e2 = Entry(f2,state="readonly",textvariable=self.sv)
        self.e2.grid(row=1,column=1)
        self.e3 = Entry(f2,state="readonly")
        self.e3.grid(row=2,column=1)
        self.e4 = Entry(f2,state="readonly")
        self.e4.grid(row=3,column=1)

        l4 = Label(f2,text="Current Return Date",bg="white")
        l4.grid(row=2,column=2,sticky=W)
        l5 = Label(f2,text="New Estimated Return Date",bg="white")
        l5.grid(row=3,column=2,sticky=W)

        self.e5 = Entry(f2,state="readonly",textvariable=self.sv)
        self.e5.grid(row=2,column=3)
        self.e6 = Entry(f2,state="readonly")
        self.e6.grid(row=3,column=3)
        
        b2 = Button(f2,text="Submit")
        b2.grid(row=4,column=3)

        self.BookCheckout()

    def FutureHoldRequest(self):
        self.seventhwin = Toplevel()
        self.seventhwin.config(bg="white")
        self.seventhwin.title("Future Hold Request for a Book")

        self.sv = StringVar()
        self.sv2 = StringVar()
        self.sv3 = StringVar()#is ther DateVar

        f = Frame(self.seventhwin)
        f.config(bg="white")
        f.grid(row=1,column=0)
        l=Label(f,text="ISBN",bg="white")
        l.grid(row=1,column=0,sticky=W)
        e = Entry(f,bg="white",textvariable=self.sv) #
        e.grid(row=1,column=1,sticky=W,padx=20,pady=20)
        b = Button(f,text="Request")
        b.grid(row=1,column=2)

        f2 = Frame(self.seventhwin)
        f2.config(bg="white")
        f2.grid(row=2,column=0)
        l=Label(f2,text="Copy Number",bg="white")
        l.grid(row=1,column=0,sticky=W)
        e = Entry(f2,bg="white",state = "readonly", textvariable=self.sv2) #
        e.grid(row=1,column=1,sticky=W,padx=2,pady=5)
        l2=Label(f2,text="Expect Available Date",bg="white")
        l2.grid(row=2,column=0,sticky=W)
        e2 = Entry(f2,bg="white",state = "readonly", textvariable=self.sv3) #
        e2.grid(row=2,column=1,sticky=W,padx=2,pady=5)


        b2 = Button(f2,text="Return")#command=self.HomeScreen
        b2.grid(row=3,column=1,sticky=E,padx=2,pady=10)

    def TrackBookLocation(self):
        self.eighthwin = Toplevel()
        self.eighthwin.config(bg="white")
        self.eighthwin.title("Track Book Location")

        self.sv = StringVar()
        self.sv2 = StringVar()
        self.sv3 = StringVar()#is ther DateVar
        self.sv4 = StringVar()
        self.sv5 = StringVar()

        f = Frame(self.eighthwin)
        f.config(bg="white")
        f.grid(row=1,column=0)
        l=Label(f,text="ISBN",bg="white")
        l.grid(row=1,column=0,sticky=W)
        e = Entry(f,bg="white",textvariable=self.sv) #
        e.grid(row=1,column=1,sticky=W,padx=20,pady=20)
        b = Button(f,text="Locate")
        b.grid(row=1,column=2)

        f2 = Frame(self.eighthwin)
        f2.config(bg="white")
        f2.grid(row=2,column=0)
        l=Label(f2,text="Floor Number",bg="white")
        l.grid(row=1,column=0,sticky=W)
        e = Entry(f2,bg="white",state = "readonly", textvariable=self.sv2) #
        e.grid(row=1,column=1,sticky=W,padx=2,pady=5)
        l2=Label(f2,text="Aisle Number",bg="white")
        l2.grid(row=2,column=0,sticky=W)
        e2 = Entry(f2,bg="white",state = "readonly", textvariable=self.sv3) #
        e2.grid(row=2,column=1,sticky=W,padx=2,pady=5)
        l3=Label(f2,text="Shelf Number",bg="white")
        l3.grid(row=1,column=2,sticky=W)
        e3 = Entry(f2,bg="white",state = "readonly", textvariable=self.sv4) #
        e3.grid(row=1,column=3,sticky=W,padx=2,pady=5)
        l4=Label(f2,text="Subject",bg="white")
        l4.grid(row=2,column=2,sticky=W)
        e4 = Entry(f2,bg="white",state = "readonly", textvariable=self.sv5) #
        e4.grid(row=2,column=3,sticky=W,padx=2,pady=5)
        #b2 = Button(f3,text="Register",command=self.CreateProfile)
        #self.secondwin.withdraw()
        #self.mainwin.deiconify()

    def BookCheckout(self):
        
        self.ninthwin = Toplevel()
        self.ninthwin.config(bg="white")
        self.ninthwin.title("Book Checkout")
        
        f = Frame(self.ninthwin)
        f.config(bg="white")
        f.grid(row=1,column=0)
        l=Label(f,text="Issue Id",bg="white")
        l.grid(row=1,column=0,sticky=W)
        l2=Label(f,text="ISBN",bg="white")
        l2.grid(row=2,column=0,sticky=W)
        l3=Label(f,text="Check out Date",bg="white")
        l3.grid(row=3,column=0,sticky=W)
        self.e = Entry(f)
        self.e.grid(row=1,column=1,padx=10,pady=15)
        self.e2 = Entry(f,state="readonly")
        self.e2.grid(row=2,column=1,padx=10,pady=15)
        self.e3 = Entry(f,state="readonly")
        self.e3.grid(row=3,column=1,padx=10,pady=15)
        
        l4=Label(f,text="User Name",bg="white")
        l4.grid(row=1,column=2,sticky=W)
        l5=Label(f,text="Copy #",bg="white")
        l5.grid(row=2,column=2,sticky=W)
        l6=Label(f,text="Estimated Return Date",bg="white")
        l6.grid(row=3,column=2,sticky=W)
        self.e = Entry(f,state="readonly")
        self.e.grid(row=1,column=3,padx=10,pady=15)
        self.e2 = Entry(f,state="readonly")
        self.e2.grid(row=2,column=3,padx=10,pady=15)
        self.e3 = Entry(f,state="readonly")
        self.e3.grid(row=3,column=3,padx=10,pady=15)

        b = Button(f,text="Confirm",width=15)
        b.grid(row=4,column=2)



    def ReturnBook(self):
        self.tenthwin = Toplevel()
        self.tenthwin.config(bg="white")
        self.tenthwin.title("Return Book")

        self.sv = StringVar()
        self.sv2 = StringVar()
        self.sv3 = StringVar()#is ther DateVar
        self.sv4 = StringVar()
        self.sv5 = StringVar()


        f2 = Frame(self.tenthwin)
        f2.config(bg="white")
        f2.grid(row=1,column=0)
        l=Label(f2,text="Issue Id",bg="white")
        l.grid(row=0,column=0,sticky=W)
        e = Entry(f2,bg="white", textvariable=self.sv2) #
        e.grid(row=0,column=1,sticky=W,padx=2,pady=5)
        l2=Label(f2,text="ISBN",bg="white")
        l2.grid(row=1,column=0,sticky=W)
        e2 = Entry(f2,bg="white",state = "readonly", textvariable=self.sv3) #
        e2.grid(row=1,column=1,sticky=W,padx=2,pady=5)
        l3=Label(f2,text="Copy Number",bg="white")
        l3.grid(row=1,column=2,sticky=W)
        e3 = Entry(f2,bg="white",state = "readonly", textvariable=self.sv4) #
        e3.grid(row=1,column=3,sticky=W,padx=2,pady=5)
        l4=Label(f2,text="Return in Damaged Condition",bg="white")
        l4.grid(row=2,column=0,sticky=W)
        #e4 = Entry(f2,bg="white",state = "readonly", textvariable=self.sv5) #
        #e4.grid(row=2,column=3,sticky=W,padx=2,pady=5)
        var = StringVar(f2)
        var.set("N")
        choices = ['N', 'Y']
        self.lb = OptionMenu(f2,var,*choices)
        self.lb.grid(row=2,column=1,sticky=E)
        l3=Label(f2,text="User Name",bg="white")
        l3.grid(row=2,column=2,sticky=W)
        e3 = Entry(f2,bg="white",state = "readonly", textvariable=self.sv4) #
        e3.grid(row=2,column=3,sticky=W,padx=2,pady=5)
        b2 = Button(f2,text="Return")#command=self.HomeScreen
        b2.grid(row=3,column=3,padx=2,pady=10)
 
    def HomeScreen(self):
        self.Homewin = Toplevel()
        self.Homewin.title("Home Page")
        self.Homewin.config(bg="white")
        

        f = Frame(self.Homewin)
        f.config(bg="white")
        f.grid(row=0,column=0)
        b = Button(f,text="Seach Books",command=self.SearchBooks)#command=self.HomeScreen
        b.grid(row=0,column=0,padx=80,pady=10)
        b2 = Button(f,text="Request Extension",command=self.RequestExtension)#command=self.HomeScreen
        b2.grid(row=2,column=0,padx=80,pady=10)
        b3 = Button(f,text="Future Hold Request",command=self.FutureHoldRequest)#command=self.HomeScreen
        b3.grid(row=2,column=0,padx=80,pady=10)
        b4 = Button(f,text="Track Book Location",command=self.TrackBookLocation)#command=self.HomeScreen
        b4.grid(row=3,column=0,padx=80,pady=10)
        #b5 = Button(f,text="Book Checkout",command=self.BookCheckout)#command=self.HomeScreen
        #b5.grid(row=4,column=0,padx=80,pady=10)
        b6 = Button(f,text="Return Book",command=self.ReturnBook)#command=self.HomeScreen
        b6.grid(row=5,column=0,padx=80,pady=10)

win = Tk()
app = GUI(win)
win.mainloop()        
