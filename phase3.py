from tkinter import*
import pymysql
from re import findall
import tkinter.messagebox #Dan had to include this for the messageboxes to show up
import datetime

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
        b1 = Button(f3,text="Login",command=self.LoginCheck)
        b1.grid(row=3,column=2,padx=2,pady=2)
        b2 = Button(f3,text="Create Account",command=self.ToRegister)
        b2.grid(row=3,column=3,padx=2,pady=2)

    def ToLogin(self):
        self.mainwin.deiconify()
        self.fourthwin.withdraw()

    def ToRegister(self):
        self.secondwin.deiconify()
        self.mainwin.withdraw()

    def ToSearchFromHome(self):
        self.fourthwin.deiconify()
        self.Homewin.withdraw()

    def ToSearchFromHoldRequest(self):
        self.fourthwin.deiconify()
        self.fifthwin.withdraw()

    def ToRequestExtension(self):
        self.RequestExtension()
        #self.sixthwin.deiconify()
        self.Homewin.withdraw()

    def ToHomeFromReqExtension(self):
        self.Homewin.deiconify()
        self.sixthwin.withdraw()

    def ToFutureHoldRequest(self):
        
        self.Homewin.withdraw()
        self.FutureHoldRequest()

    def ToHomeFromPenalty(self):
        self.Homewin.deiconify()
        self.LostDamagedBookPenalty.withdraw()

    def ToTrackBookLocation(self):
        self.Homewin.withdraw()
        self.TrackBookLocation()

    def ToHomeFromTrackLoc(self):
        self.Homewin.deiconify()
        self.eighthwin.withdraw()

    def ToBookCheckout(self):
        self.Homewin.withdraw()
        self.BookCheckout()

    def ToReturnBook(self):
        self.ReturnBook()
        self.Homewin.withdraw()

    def ToHomeFromReturnBook(self):
        self.Homewin.deiconify()
        self.tenthwin.withdraw()
        
    def Connect(self):
        try:
            db = pymysql.connect(host="academic-mysql.cc.gatech.edu",passwd="DC5xMas8",
                                 user="cs4400_Group_18",db="cs4400_Group_18")

            return db
        except:
            info = tkinter.messagebox.showinfo("Problem!", "Cannot connect to the database! Please check your internet connection.")
            return None 

    def LoginCheck(self):
        self.database = self.Connect()
        c = self.database.cursor()
        
        self.username = self.sv.get()
        password = self.sv2.get()

        #check to see if username and password is in the database
        #sql = "SELECT Username,Password FROM User"
        #c.execute(sql)
        sql = "SELECT COUNT(*) FROM User WHERE Username = %s AND Password = %s"
        c.execute(sql,(self.username,password))
        data = c.fetchall()
        #print(data)

        user = (1,)

        if user in data:
            info2 = tkinter.messagebox.showinfo("","You logged in successfully.")
            c.close()
            self.SearchBooks()
            self.mainwin.withdraw()
        else:
            info3 = tkinter.messagebox.showinfo("","You entered an unrecognizable username/password combination")

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
        b2 = Button(f3,text="Register",command=self.RegistrationCheck)#,command=self.CreateProfile)
        b2.grid(row=4,column=3,padx=2,pady=2)

    def RegistrationCheck(self):
        try:
            #check to see if username has not already been registered
            self.username = self.e.get()

            db = self.Connect()
            c = db.cursor()

            sql = "SELECT Username FROM User"
            c.execute(sql)
            data = c.fetchall()

            username = (self.username)
            # username is valid
            if username not in data:
                #check if password and confirm password are the same
                if self.e2.get() != self.e3.get():
                     error = tkinter.messagebox.showinfo("Problem!","Password and Confirm Password do not match.")
                #password and confirm password are the same, continue
                else:
                    password = self.e2.get()
                    
                    sql = "INSERT INTO User (Username, Password) VALUES (%s,%s)"
                    c.execute(sql, (username, password))
                    c.close()
                    db.commit()
                    db.close()
                    self.secondwin.withdraw()
                    self.CreateProfile()
            else:
                error4 = tkinter.messagebox.showinfo("Problem","The username already exists.")
        except:
            error4 = tkinter.messagebox.showinfo("Problem","The username already exists.")

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
        #Gender
        self.var = StringVar(f3)
        self.var.set("")
        choices = ['M', 'F']
        self.g = OptionMenu(f3,self.var,*choices)
        self.g.grid(row=2,column=1,sticky=E)
        #isFaculty
        self.iv = IntVar(f3)
        self.iv.set(5)
        c = Checkbutton(f3, text="Yes", variable=self.iv,bg="white", command=self.checkIsFaculty)
        c.grid(row=3,column=1)
##        v = StringVar()
##        combobox = Combobox(f3,textvariable=v)
##        combobox.grid(row=4,column=1)
        #Department
##        self.var2 = StringVar(f3)
##        self.var2.set("")
##        option = OptionMenu(f3,self.var2,"M","F")
##        option.grid(row=4,column=1)
        # dept
        self.e6 = Entry(f3, state="readonly")
        self.e6.grid(row=4, column=1)
        b = Button(f3,text="Submit",command=self.Create)#command=self.HomeScreen)
        b.grid(row=5,column=1,padx=2,pady=2)

    def checkIsFaculty(self):
        if self.iv.get() == 1:
            self.e6.config(state=NORMAL)

    def Create(self):
        import time

        firstName = self.e.get()
        lastName = self.e5.get()
##        date = self.e2.get()
##        dob = time.strftime(date,"%m/%d/%Y")
##        print(dob)
##        dob = datetime.datetime.strptime(date,"%m/%d/%Y")
        gender = self.var.get()
        isDebarred = True
        email = self.e3.get()
        address = self.e4.get()
        if self.iv.get() == 1:
            isFaculty = True
            dept = self.e6.get()
        else:
            isFaculty = False
            dept = ""

        db = self.Connect()
        c = db.cursor()

        #NEED TO ADD DOB
        sql = "INSERT INTO StudentFaculty (Username, F_Name, L_Name,Gender,isDebarred,Email,Address,isFaculty,Dept) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        c.execute(sql,(self.username,firstName,lastName,gender,isDebarred,email,address,isFaculty,dept))

        c.close()
        db.commit()
        db.close()

        self.thirdwin.withdraw()
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

        #ISBN
        self.e = Entry(f)
        self.e.grid(row=1,column=1,padx=2,pady=2)
        #Title
        self.e2 = Entry(f)
        self.e2.grid(row=2,column=1,padx=2,pady=2)
        #Author
        self.e3 = Entry(f)
        self.e3.grid(row=3,column=1,padx=2,pady=2)

        f2 = Frame(self.fourthwin)
        f2.config(bg="white")
        f2.grid(row=2,column=0)
        b = Button(f2,text="Home", command=self.ToHomeFromSearch)
        b.grid(row=4,column=0)
        b2 = Button(f2,text="Search",command=self.Search)
        b2.grid(row=4,column=1)
        b3 = Button(f2,text="Close", command=self.ToLogin)
        b3.grid(row=4,column=2)

        #self.fourthwin.withdraw()
        #self.RequestExtension()

    def ToHomeFromSearch(self):
        self.HomeScreen()
        self.fourthwin.withdraw()

    def ToHomeFromHoldRequest(self):
        self.HomeScreen()
        self.fifthwin.withdraw()

    def Search(self):
        self.isbn = self.e.get()
        self.title = self.e2.get()
        self.author = self.e3.get()

        print(self.title)

        db = self.Connect()
        c = db.cursor()

        print("searching for books")

        sql1 = "UPDATE BookCopy a SET isOnHold=false WHERE (ISBN,CopyNum) in (SELECT ISBN, CopyNum FROM Issues b "\
        "WHERE a.ISBN = b.ISBN AND a.CopyNum = b.CopyNum AND a.isOnHold = true AND isCheckedOut =false "\
        "AND datediff(sysdate(),dateofissue)>3 AND ReturnDate>=sysdate())"
        c.execute(sql1)
        db.commit()

        print("done updating in search")

    #for books available
        #search title only
        if self.isbn == "" and self.title != "" and self.author == "":
            print("search with title")
            sql = "SELECT Book.ISBN, Title, Edition, COUNT(*) FROM Book,BookCopy WHERE Book.ISBN = BookCopy.ISBN AND isBookOnReserve=false AND "\
            "isOnHold=false AND isCheckedOut=false AND isDamaged=false AND LOWER(Title) LIKE LOWER(%s) GROUP BY Book.ISBN, Title, Edition"
            c.execute(sql,('%' + self.title + '%'))
            #c.execute(sql)
            print(('%' + self.title + '%'))
        #search isbn only
        elif self.isbn != "" and self.title == "" and self.author == "":
            sql = "SELECT Book.ISBN,Title, Edition, COUNT(*) FROM Book,BookCopy WHERE Book.ISBN = BookCopy.ISBN AND isBookOnReserve=false AND "\
            "isCheckedOut=false AND isOnHold=false AND isDamaged=false AND Book.ISBN LIKE %s GROUP BY Book.ISBN, Title, Edition"
            c.execute(sql,('%' + self.isbn + '%'))
        #search author only
        elif self.isbn == "" and self.title == "" and self.author != "":
            sql = "SELECT ISBN, Title, Edition, COUNT(*) "\
            "FROM ( SELECT DISTINCT BookCopy.ISBN, BookCopy.CopyNum, Title, Edition FROM Book, BookCopy, Author "\
            "WHERE Book.ISBN = BookCopy.ISBN AND isBookOnReserve = false AND isCheckedOut = False AND isOnHold=false AND "\
            "isDamaged=FALSE AND Book.ISBN =Author.ISBN AND Lower(Authors) LIKE Lower(%s)) a "\
            "GROUP BY ISBN, Title, Edition"
            c.execute(sql,('%' + self.author + '%'))
        #search title and isbn only
        elif self.isbn != "" and self.title != "" and self.author == "":
            sql = "SELECT Book.ISBN, Title, Edition, COUNT(*) FROM Book,BookCopy WHERE Book.ISBN = BookCopy.ISBN AND isBookOnReserve=false AND "\
            "isCheckedOut=false AND isOnHold=false AND isDamaged=false AND "\
            "LOWER(Title) LIKE LOWER(%s) AND Book.ISBN LIKE %s GROUP BY Book.ISBN, Title, Edition"
            c.execute(sql,(('%' + self.title + '%'),('%' + self.isbn + '%')))
        #search title and author only
        elif self.isbn == "" and self.title != "" and self.author != "":
            sql = "SELECT ISBN, Title, Edition, COUNT(*) "\
            "FROM ( SELECT DISTINCT BookCopy.ISBN, BookCopy.CopyNum, Title, Edition FROM Book, BookCopy, Author "\
            "WHERE Book.ISBN = BookCopy.ISBN AND isBookOnReserve = false AND isCheckedOut = False AND isOnHold=false AND "\
            "isDamaged=FALSE AND Book.ISBN =Author.ISBN AND LOWER(Title) LIKE LOWER(%s) AND Lower(Authors) LIKE Lower(%s)) a "\
            "GROUP BY ISBN, Title, Edition"
            c.execute(sql,(('%' + self.title + '%'),('%' + self.author + '%')))
        #search isbn and author only
        elif self.isbn != "" and self.title == "" and self.author != "":
            sql = "SELECT ISBN, Title, Edition, COUNT(*) "\
            "FROM ( SELECT DISTINCT BookCopy.ISBN, BookCopy.CopyNum, Title, Edition FROM Book, BookCopy, Author "\
            "WHERE Book.ISBN = BookCopy.ISBN AND isBookOnReserve = false AND isCheckedOut = False AND isOnHold=false AND "\
            "isDamaged=FALSE AND Book.ISBN =Author.ISBN AND Book.ISBN LIKE %s AND Lower(Authors) LIKE Lower(%s)) a "\
            "GROUP BY ISBN, Title, Edition"
            c.execute(sql,(('%' + self.isbn + '%'),('%' + self.author + '%')))
        #search isbn, title, and author
        elif self.isbn != "" and self.title != "" and self.author != "":
            sql = "SELECT ISBN, Title, Edition, COUNT(*) "\
            "FROM ( SELECT DISTINCT BookCopy.ISBN, BookCopy.CopyNum, Title, Edition FROM Book, BookCopy, Author "\
            "WHERE Book.ISBN = BookCopy.ISBN AND isBookOnReserve = false AND isCheckedOut = False AND isOnHold=false AND "\
            "isDamaged=FALSE AND Book.ISBN =Author.ISBN AND LOWER(Title) LIKE LOWER(%s) AND Book.ISBN LIKE %s AND Lower(Authors) LIKE Lower(%s)) a "\
            "GROUP BY ISBN, Title, Edition"
            c.execute(sql,(('%' + self.title + '%'),('%' + self.isbn + '%'),('%' + self.author + '%')))
        else:
            error = tkinter.messagebox.showinfo("Problem","You have to fill in at least one field.")

        self.data = c.fetchall()
        print(self.data)
        print(self.data== ())
        print(len(self.data))

        for book in self.data:
            print(book)

        print(self.data[0][0])

    #for books on reserve
        #search title only
        if self.isbn == "" and self.title != "" and self.author == "":
            sql = "SELECT Book.ISBN, Title, Edition, COUNT(*) FROM Book,BookCopy WHERE Book.ISBN = BookCopy.ISBN AND isBookOnReserve=true AND "\
            "isDamaged=false AND LOWER(Title) LIKE LOWER(%s) GROUP BY Book.ISBN, Title, Edition"
            c.execute(sql,('%' + self.title + '%'))
            print(('%' + self.title + '%'))
        #search isbn only
        elif self.isbn != "" and self.title == "" and self.author == "":
            sql = "SELECT Book.ISBN, Title, Edition, COUNT(*) FROM Book,BookCopy WHERE Book.ISBN = BookCopy.ISBN AND isBookOnReserve=true AND "\
            "isDamaged=false AND Book.ISBN LIKE %s GROUP BY Book.ISBN, Title, Edition"
            c.execute(sql,('%' + self.isbn + '%'))
        #search author only
        elif self.isbn == "" and self.title == "" and self.author != "":
            sql = "SELECT ISBN, Title, Edition, COUNT(*) "\
            "FROM ( SELECT DISTINCT BookCopy.ISBN, BookCopy.CopyNum, Title, Edition FROM Book, BookCopy, Author "\
            "WHERE Book.ISBN = BookCopy.ISBN AND isBookOnReserve = true AND "\
            "isDamaged=FALSE AND Book.ISBN =Author.ISBN AND Lower(Authors) LIKE Lower(%s)) a "\
            "GROUP BY ISBN, Title, Edition"
            c.execute(sql,('%' + self.author + '%'))
        #search title and isbn only
        elif self.isbn != "" and self.title != "" and self.author == "":
            sql = "SELECT Book.ISBN, Title, Edition, COUNT(*) FROM Book,BookCopy WHERE Book.ISBN = BookCopy.ISBN AND isBookOnReserve=true AND "\
            "isDamaged=false AND LOWER(Title) LIKE LOWER(%s) AND Book.ISBN LIKE %s GROUP BY Book.ISBN, Title, Edition"
            c.execute(sql,(('%' + self.title + '%'),('%' + self.isbn + '%')))
        #search title and author only
        elif self.isbn == "" and self.title != "" and self.author != "":
            sql = "SELECT ISBN, Title, Edition, COUNT(*) "\
            "FROM ( SELECT DISTINCT BookCopy.ISBN, BookCopy.CopyNum, Title, Edition FROM Book, BookCopy, Author "\
            "WHERE Book.ISBN = BookCopy.ISBN AND isBookOnReserve =true AND "\
            "isDamaged=FALSE AND Book.ISBN =Author.ISBN AND LOWER(Title) LIKE LOWER(%s) AND Lower(Authors) LIKE Lower(%s)) a "\
            "GROUP BY ISBN, Title, Edition"
            c.execute(sql,(('%' + self.title + '%'),('%' + self.author + '%')))
        #search isbn and author only
        elif self.isbn != "" and self.title == "" and self.author != "":
            sql = "SELECT ISBN, Title, Edition, COUNT(*) "\
            "FROM ( SELECT DISTINCT BookCopy.ISBN, BookCopy.CopyNum, Title, Edition FROM Book, BookCopy, Author "\
            "WHERE Book.ISBN = BookCopy.ISBN AND isBookOnReserve = true AND "\
            "isDamaged=FALSE AND Book.ISBN =Author.ISBN AND Book.ISBN LIKE %s AND Lower(Authors) LIKE Lower(%s)) a "\
            "GROUP BY ISBN, Title, Edition"
            c.execute(sql,(('%' + self.isbn + '%'),('%' + self.author + '%')))
        #search isbn, title, and author
        elif self.isbn != "" and self.title != "" and self.author != "":
            sql = "SELECT ISBN, Title, Edition, COUNT(*) "\
            "FROM ( SELECT DISTINCT BookCopy.ISBN, BookCopy.CopyNum, Title, Edition FROM Book, BookCopy, Author "\
            "WHERE Book.ISBN = BookCopy.ISBN AND isBookOnReserve = true AND "\
            "isDamaged=FALSE AND Book.ISBN =Author.ISBN AND LOWER(Title) LIKE LOWER(%s) AND Book.ISBN LIKE %s AND Lower(Authors) LIKE Lower(%s)) a "\
            "GROUP BY ISBN, Title, Edition"
            c.execute(sql,(('%' + self.title + '%'),('%' + self.isbn + '%'),('%' + self.author + '%')))
        else:
            error = tkinter.messagebox.showinfo("Problem","You have to fill in at least one field.")

        self.data2 = c.fetchall()
        print(self.data2)

        self.fourthwin.withdraw()
        self.RequestHold()        

        c.close()
        db.close()

    def RequestHold(self):
        self.fifthwin = Toplevel()
        self.fifthwin.config(bg="white")
        self.fifthwin.title("Hold Request for a Book")

        f = Frame(self.fifthwin)
        f.grid(row=0,column=0)
        l = Label(f,text="Books Available Summary",bg="white")
        l.grid(row=0,column=0)

        f2 = Frame(self.fifthwin, bg="white")
        f2.grid(row=1,column=0)
        l2 = Label(f2,text="Select",bg="white")
        l2.grid(row=0,column=0)
        l3 = Label(f2,text="ISBN",bg="white",relief=GROOVE,width=15)
        l3.grid(row=0,column=1)
        l4 = Label(f2,text="Title of the Book",bg="white",relief=GROOVE,width=40)
        l4.grid(row=0,column=2)
        l5 = Label(f2,text="Edition",bg="white",relief=GROOVE,width=15)
        l5.grid(row=0,column=3)
        l6 = Label(f2,text="#copies available",bg="white",relief=GROOVE,width=15)
        l6.grid(row=0,column=4)

        self.sv3 = StringVar()
        self.sv3.set("a")
        if self.data != () :
            for x in range(len(self.data)):
                r = Radiobutton(f2,text="",bg="white",variable=self.sv3,value=self.data[x][0])
                r.grid(row=x+1,column=0)
                l = Label(f2,text=self.data[x][0],bg="white",relief=GROOVE,width=15)
                l.grid(row=x+1, column=1)
                l2 = Label(f2,text=self.data[x][1],bg="white",relief=GROOVE,width=40)
                l2.grid(row=x+1, column=2)
                l3 = Label(f2,text=self.data[x][2],bg="white",relief=GROOVE,width=15)
                l3.grid(row=x+1, column=3)
                l4 = Label(f2,text=self.data[x][3],bg="white",relief=GROOVE,width=15)
                l4.grid(row=x+1, column=4)

        self.sv = StringVar()
        self.sv2 = StringVar()

        f3 = Frame(self.fifthwin,bg="white")
        f3.grid(row=2,column=0)
        l7 = Label(f3,text="Hold Request Date",bg="white")
        l7.grid(row=0,column=0)
        e = Entry(f3,state="readonly",textvariable=self.sv)
        e.grid(row=0,column=1)
        l8 = Label(f3,text="Estimated Return Date",bg="white")
        l8.grid(row=0,column=2)
        e2 = Entry(f3,state="readonly",textvariable=self.sv2)
        e2.grid(row=0,column=3)

        b = Button(f3,text="Back",command=self.ToSearchFromHoldRequest)
        b.grid(row=1,column=1)
        b2 = Button(f3,text="Submit",command=self.Hold)
        b2.grid(row=1,column=2)
        b3 = Button(f3,text="Close",command=self.ToHomeFromHoldRequest)
        b3.grid(row=1,column=3)

        f4 = Frame(self.fifthwin,bg="white")
        f4.grid(row=3,column=0)
        l9 = Label(f4,text="Books on Reserve",bg="white")
        l9.grid(row=0,column=0)

        f5 = Frame(self.fifthwin,bg="gray")
        f5.grid(row=4,column=0)

        l10 = Label(f5,text="ISBN",bg="gray",relief=GROOVE,width=15)
        l10.grid(row=0,column=1)
        l11 = Label(f5,text="Title of the Book",bg="gray",relief=GROOVE,width=40)
        l11.grid(row=0,column=2)
        l12 = Label(f5,text="Edition",bg="gray",relief=GROOVE,width=15)
        l12.grid(row=0,column=3)
        l13 = Label(f5,text="#copies available",bg="gray",relief=GROOVE,width=15)
        l13.grid(row=0,column=4)

        if self.data2 != ():
            for i in range(len(self.data2)):
                l = Label(f5,text=self.data2[i][0],bg="gray",relief=GROOVE,width=15)
                l.grid(row=i+1, column=1)
                l2 = Label(f5,text=self.data2[i][1],bg="gray",relief=GROOVE,width=40)
                l2.grid(row=i+1, column=2)
                l3 = Label(f5,text=self.data2[i][2],bg="gray",relief=GROOVE,width=15)
                l3.grid(row=i+1, column=3)
                l4 = Label(f5,text=self.data2[i][3],bg="gray",relief=GROOVE,width=15)
                l4.grid(row=i+1, column=4)
            
    def Hold(self):
        print(self.sv3.get())
        isbn = self.sv3.get()

        db = self.Connect()
        c = db.cursor()

        sql = "SELECT MIN(CopyNum) FROM BookCopy WHERE ISBN=%s AND "\
              "isCheckedOut=false AND isOnHold=false AND isDamaged=false"

        c.execute(sql,isbn)
        copynum = c.fetchone()

        print(copynum)

        sql1 = "UPDATE BookCopy SET isOnHold=true WHERE ISBN=%s AND CopyNum=%s"
        c.execute(sql1,(isbn,copynum))
        db.commit()

        sql2 = "SELECT MAX(Issue_ID)+1 FROM Issues"
        c.execute(sql2)
        ID = c.fetchone()
        print(ID)
        issueID = findall("\d+",str(ID))
        print(int(issueID[0]))

        sql3 = "INSERT INTO Issues (ISBN,Username,CopyNum,Issue_ID,DateofIssue,"\
               "ExtensionDate,ReturnDate,CountOfExtensions) VALUES "\
               "(%s,%s,%s,%s,sysdate(),sysdate(),date_add(sysdate(),INTERVAL 17 DAY),0)"
        c.execute(sql3,(isbn,self.username,copynum,ID))
        db.commit()

        sql4 = "SELECT DateOfIssue,ReturnDate FROM Issues WHERE Issue_ID=%s"
        c.execute(sql4,ID)

        dates = c.fetchone()
        dateofissue = dates[0]
        returndate = dates[1]

        self.sv.set(dateofissue)
        self.sv2.set(returndate)
        
        showID = tkinter.messagebox.showinfo("Issue_ID","Your Issue_ID is " + issueID[0])
        
        c.close()
        db.close()
        

    def RequestExtension(self):

        self.sixthwin = Toplevel() #CHANGE TO --> Toplevel()
        self.sixthwin.config(bg="white")
        self.sixthwin.title("Request extension on a book")
        
        f = Frame(self.sixthwin)
        f.config(bg="white")
        f.grid(row=1,column=0)
        l=Label(f,text="Enter your issue_id",bg="white")
        l.grid(row=1,column=0,sticky=W)
        self.e = Entry(f,width=40) #to enter ISSUEID
        self.e.grid(row=1,column=1,padx=50,pady=10)
        
        b = Button(f,text="Submit", command=self.RequestExtensionSubmit1)
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

        self.sv2 = StringVar()
        self.sv3 = StringVar()
        self.sv4 = StringVar()
        self.sv5 = StringVar()
        self.sv6 = StringVar()

        self.e2 = Entry(f2,state="readonly",textvariable=self.sv2)
        self.e2.grid(row=1,column=1)#OriginalCheckoutDate
        self.e3 = Entry(f2,state="readonly",textvariable=self.sv3)
        self.e3.grid(row=2,column=1)#CurrentExtensionDate
        self.e4 = Entry(f2,state="readonly",textvariable=self.sv4)
        self.e4.grid(row=3,column=1)#NewExtensionDate

        l4 = Label(f2,text="Current Return Date",bg="white")
        l4.grid(row=2,column=2,sticky=W) 
        l5 = Label(f2,text="New Estimated Return Date",bg="white")
        l5.grid(row=3,column=2,sticky=W)

        self.e5 = Entry(f2,state="readonly",textvariable=self.sv5)
        self.e5.grid(row=2,column=3)#CurrentReturnDate
        self.e6 = Entry(f2,state="readonly",textvariable=self.sv6)
        self.e6.grid(row=3,column=3)#NewtReturnDate
        
        b2 = Button(f2,text="Submit", command=self.RequestExtensionSubmit2)
        b2.grid(row=4,column=3)
        b3 = Button(f2,text="Cancel", command=self.ToHomeFromReqExtension)
        b3.grid(row=4,column=2)

        #self.BookCheckout()


    def RequestExtensionSubmit1(self): 
        self.IssueId=self.e.get()
        self.IssueId=int(self.IssueId)
        c=self.Connect().cursor()
        c.execute("SELECT DateofIssue,ExtensionDate,ReturnDate FROM Issues WHERE Issue_ID='{}'".format(self.IssueId))
        info=c.fetchone()
        #print(info)          
        if info is not None:
            
           self.sv2.set(info[0])
           self.sv3.set(info[1])
           self.sv5.set(info[2])
        else:
            messagebox.showerror("ERROR","You cannot request an extension without a valid Issue ID")           
        self.Connect().commit()
        c.close()
        self.Connect().close()

    def RequestExtensionSubmit2(self): #Secondsubmit
        db=self.Connect()
        c=db.cursor()
        
        c.execute("SELECT COUNT(*)FROM StudentFaculty WHERE USERNAME=%s AND isFaculty=FALSE",(self.username))  ####TO TEST-->HARDCODE THE USERNAME
        a=c.fetchone()
        if a[0]==1:#if a=1 then is a student
            print("Is a student")
            c.execute("SELECT COUNT(*)FROM Issues a WHERE Issue_ID=%s AND EXISTS(SELECT* FROM BookCopy b "\
                      "WHERE a.ISBN=b.ISBN AND a.CopyNum=b.CopyNum AND b.isCheckedOut=TRUE AND b.isOnHold=FALSE AND "\
                      "b.FutureRequester is NULL)AND CountOfExtensions<2 AND DATEDIFF(DateofIssue,ReturnDate)<=28",(self.IssueId))
            b=c.fetchone()#if b=1 then student qualifies 
            if b[0]==1:
                print("student qualifies")
                sql="update Issues set countofextensions =countofextensions+1, extensiondate = sysdate(), "\
                     "returndate = least(date_add(sysdate(),INTERVAL 14 DAY),date_add(dateofissue,INTERVAL 28 DAY))"\
                     "where issue_ID = %s"
                c.execute(sql,(self.IssueId))

                db.commit()
                c.execute("SELECT ExtensionDate,ReturnDate FROM Issues WHERE Issue_ID=%s",(self.IssueId))
                d=c.fetchone()
                self.sv4.set(d[0])
                self.sv6.set(d[1])                
            else:
                messagebox.showerror("ERROR", "You don't qualify for an extension")         


        else:#is a faculty
            print("is a faculty")
            c.execute("SELECT COUNT(*)FROM Issues a WHERE Issue_ID=%s AND EXISTS(SELECT* FROM BookCopy b "\
                      "WHERE a.ISBN=b.ISBN AND a.CopyNum=b.CopyNum AND b.isCheckedOut=TRUE AND b.isOnHold=FALSE AND "\
                      "b.FutureRequester is NULL)AND CountOfExtensions<5 AND DATEDIFF(DateofIssue,ReturnDate)<=56",(self.IssueId))   
            e=c.fetchone()#if e=1 faculty qualifies
            if e[0]==1:
                print("faculty qualifies")

                sql="update Issues set countofextensions =countofextensions+1, extensiondate = sysdate(), "\
                     "returndate = least(date_add(sysdate(),INTERVAL 14 DAY),date_add(dateofissue,INTERVAL 56 DAY)) "\
                     "where issue_ID = %s"
                c.execute(sql,(self.IssueId))              
                db.commit()
                c.execute("SELECT ExtensionDate,ReturnDate FROM Issues WHERE Issue_ID=%s",(self.IssueId))
                f=c.fetchone()
                self.sv4.set(f[0])
                self.sv6.set(f[1])
            else:
                messagebox.showerror("ERROR", "You don't qualify for an extension")
        db.commit()
        c.close()
        db.close()

    def FutureHoldRequest(self): #ADD TO CLARISSA
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
        self.e = Entry(f,bg="white",textvariable=self.sv) #isbn
        self.e.grid(row=1,column=1,sticky=W,padx=20,pady=20)
        b = Button(f,text="Request",command=self.FutureRequest) #**********************add this button command
        b.grid(row=1,column=2)

        f2 = Frame(self.seventhwin)
        f2.config(bg="white")
        f2.grid(row=2,column=0)
        l2=Label(f2,text="Copy Number",bg="white")
        l2.grid(row=1,column=0,sticky=W)
        self.e2 = Entry(f2,bg="white",state = "readonly", textvariable=self.sv2) #Copy Number
        self.e2.grid(row=1,column=1,sticky=W,padx=2,pady=5)
        l3=Label(f2,text="Expect Available Date",bg="white")
        l3.grid(row=2,column=0,sticky=W)
        self.e3 = Entry(f2,bg="white",state = "readonly", textvariable=self.sv3) #ExpectedAvailableDate
        self.e3.grid(row=2,column=1,sticky=W,padx=2,pady=5)


        b2 = Button(f2,text="Ok",command = self.InsertFutureRequest)#command=self.HomeScreen
        b2.grid(row=3,column=1,sticky=E,padx=2,pady=10)

    def FutureRequest (self): #ADD TO CLARISSA
        self.isbn = self.e.get()

        db = self.Connect()
        c = db.cursor()

        print("Attempting to create future hold")
        check1 = "SELECT count(*) FROM BookCopy WHERE ISBN = %s AND (isOnHold=TRUE OR isCheckedOut = True OR isDamaged = True)"
        c.execute(check1,(self.isbn))
        clause1 = c.fetchone()
        check2 = "SELECT count(*) FROM BookCopy WHERE ISBN = %s"
        c.execute(check1,(self.isbn))
        clause2 = c.fetchone()

        if (clause1 == clause2):
            #search title only
            sql = "SELECT a.ReturnDate, a.CopyNum FROM Issues a,BookCopy b WHERE (a.ISBN = b.ISBN) AND (a.CopyNum = b.CopyNum) AND (a.ISBN = %s) AND ReturnDate in (SELECT MIN(ReturnDate) FROM Issues c, BookCopy d WHERE c.ISBN = %s AND c.ISBN = d.ISBN AND c.copyNum = d.copyNum AND(d.isOnHold = true OR d.isCheckedOut = true) AND isDamaged = false and ReturnDate >= sysdate()) AND (b.isOnHold = TRUE OR b.isCheckedOut = TRUE)"
            c.execute(sql,(self.isbn,self.isbn))
            data = c.fetchone()
            if data: #if the data exists
                retDate = data[0]
                cNum = data[1]

                print(retDate)
                print(cNum)

                #for next avail date update
                self.e3.config(state=NORMAL) #quotation marks?
                print("changed to normal")
                self.sv3.set(retDate)
                #self.e3.config(text =self.sv2)
                self.e3.config(state="readonly")
                #for copynumber update
                self.e2.config(state=NORMAL) #quotation marks?
                self.sv2.set(cNum)
                #self.e2.config(text = self.sv3)
                self.e2.config(state="readonly")
            else:
                pass
            print(data)
        else:
            avail = tkinter.messagebox.showinfo("","There are available books. No need for a future hold request!")

        c.close()
        db.close()

    def InsertFutureRequest (self): #ADD TO CLARISSA
        db = self.Connect()
        c = db.cursor()
        self.isbn = self.e.get()
        self.cNum = self.e2.get()
        print("Inserting future hold request")
        print(self.isbn)
        print(self.cNum)
        sql = "UPDATE BookCopy SET FutureRequester = %s WHERE ISBN = %s AND CopyNum = %s"
        c.execute(sql,(self.username,self.isbn,self.cNum)) # how to retreive the name
        print("executed")
        c.close()
        db.commit()
        db.close()
        self.seventhwin.withdraw()
        self.Homewin.deiconify()

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
        self.e = Entry(f,bg="white",textvariable=self.sv) #
        self.e.grid(row=1,column=1,sticky=W,padx=20,pady=20)
        b = Button(f,text="Locate",command=self.FindLocation)
        b.grid(row=1,column=2)

        f2 = Frame(self.eighthwin)
        f2.config(bg="white")
        f2.grid(row=2,column=0)
        l=Label(f2,text="Floor Number",bg="white")
        l.grid(row=1,column=0,sticky=W)
        e1 = Entry(f2,bg="white",state = "readonly", textvariable=self.sv2) #
        e1.grid(row=1,column=1,sticky=W,padx=2,pady=5)
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
        f3 = Frame(self.eighthwin)
        f3.config(bg="white")
        f3.grid(row=3,column=0)
        b2 = Button(f3,text="Home",command=self.ToHomeFromTrackLoc)
        b2.grid(row=0,column=0)

    def FindLocation(self):
        #self.ISBN = self.e.get()
        isbn = (str(self.e.get()))
        self.ISBN = (isbn,)
        db = self.Connect()
        c = db.cursor()
        sql = "SELECT ISBN FROM Book"
        c.execute(sql)
        data = c.fetchall()
        print("wanted ISBN: " + self.e.get())
        print(isbn)
        print(data)
        if (self.ISBN) not in data:
            error = messagebox.showinfo("Error!", "ISBN not in library.")
        else:
            #sql1 = "SELECT Book.FloorNum, Book.ShelfNum, Shelf.AisleNum, Book.Subject_Name FROM Book, Shelf, Subject WHERE Book.Subject_Name = Subject.Name AND Book.ShelfNum = Shelf.ShelfNum AND ISBN =self.ISBN"
            sql1 = ("SELECT Book.FloorNum, Book.ShelfNum, Shelf.AisleNum, Book.Subject_Name FROM Book, Shelf, Subject WHERE Book.ShelfNum = Shelf.ShelfNum AND Book.Subject_Name = Subject.Name AND ISBN = (%s)")
            c.execute(sql1, (isbn))
            data = c.fetchone()
            print(self.ISBN)
            print(data)
            self.sv2.set(str(data[0]))
            self.sv4.set(str(data[1]))
            self.sv3.set(str(data[2]))
            self.sv5.set(str(data[3]))

    def BookCheckout(self):
         self.ninthwin = Toplevel()
         self.ninthwin.config(bg="white")
         self.ninthwin.title("Book Checkout")

         self.sv = StringVar()  #issueid
         self.sv2 = StringVar() #ISBN
         self.sv3 = StringVar() #checkout date
         self.sv4 = StringVar() #username
         self.sv5 = StringVar() #copyNum
         self.sv6 = StringVar() #estimated return
        
         f = Frame(self.ninthwin)
         f.config(bg="white")
         f.grid(row=1,column=0)
         l=Label(f,text="Issue Id",bg="white") #ISSUE ID IS THE ONLY GET
         l.grid(row=1,column=0,sticky=W)
         l2=Label(f,text="ISBN",bg="white")
         l2.grid(row=2,column=0,sticky=W)
         l3=Label(f,text="Check out Date",bg="white")
         l3.grid(row=3,column=0,sticky=W)
         self.e = Entry(f, bg="white",textvariable=self.sv)
         self.e.grid(row=1,column=1,padx=10,pady=15)
         self.e2 = Entry(f,state="readonly", textvariable=self.sv2)
         self.e2.grid(row=2,column=1,padx=10,pady=15)
         self.e3 = Entry(f,state="readonly", textvariable=self.sv3)
         self.e3.grid(row=3,column=1,padx=10,pady=15)
        
         l4=Label(f,text="User Name",bg="white")
         l4.grid(row=1,column=2,sticky=W)
         l5=Label(f,text="Copy #",bg="white")
         l5.grid(row=2,column=2,sticky=W)
         l6=Label(f,text="Estimated Return Date",bg="white")
         l6.grid(row=3,column=2,sticky=W)
         self.e4 = Entry(f,state="readonly", textvariable=self.sv4)
         self.e4.grid(row=1,column=3,padx=10,pady=15)
         self.e5 = Entry(f,state="readonly", textvariable=self.sv5)
         self.e5.grid(row=2,column=3,padx=10,pady=15)
         self.e6 = Entry(f,state="readonly", textvariable=self.sv6)
         self.e6.grid(row=3,column=3,padx=10,pady=15)

         b = Button(f,text="Confirm",width=15, command=self.ConfirmCheckout)
         b.grid(row=4,column=2)
         b1 = Button(f, text="Submit Issue ID", width=15, command=self.Checkout)
         b1.grid(row=4, column=1)
        
    def Checkout(self):
        #issue id is an int
         issueID = int(self.e.get())
         self.issueID = (issueID,)
         db = self.Connect()
         c = db.cursor()
         sql = "SELECT Issue_ID FROM Issues"
         c.execute(sql)
         data = c.fetchall()
         print(issueID)
         print(data)
         print(self.issueID)
         if (self.issueID) not in data:
             error = messagebox.showinfo("Error!", "Issue ID not in library.")
         else:
             sql1 = ("SELECT Username, ISBN, CopyNum FROM Issues WHERE Issue_ID = (%s)")
             c.execute(sql1, (issueID))
             data = c.fetchall()
             #now have the data with which to populate
             print(data)
             self.username = data[0][0]
             self.ISBN = data[0][1]
             self.CopyNum = data[0][2]
             sql2 = ("SELECT COUNT(*) FROM StudentFaculty WHERE Username = (%s) AND isDebarred = 0")
             c.execute(sql2, (self.username))
             data = c.fetchall()
             print(data)
             if (data[0][0])==0: #if debarred, error message
                 error = messagebox.showinfo("Error!", "This user is debarred.")
             else: # if not debarred, check hold
                 #sysDate = time.strftime
                 sql3 = ("SELECT COUNT(*) FROM Issues WHERE DATEDIFF(sysdate(), DateofIssue)>3 AND Issue_ID = (%s)")
                 c.execute(sql3, (issueID))
                 data = c.fetchall()
                 if data==1: #throw error, hold has been dropped
                     error = messagebox.showinfo("Error!", "This user's hold has been dropped.")
                 else: #user is allowed to continue process now
                     self.sv2.set(str(self.ISBN))
                     self.sv4.set(str(self.username))
                     self.sv5.set(str(self.CopyNum))
##                     self.sv3.set(str(sysdate()))
                     sql4 = ("UPDATE Issues SET DateOfIssue = sysdate(), ReturnDate = DATE_ADD(sysdate(), INTERVAL 14 DAY), ExtensionDate=sysdate() WHERE Issue_ID = (%s)")
                     c.execute(sql4, (issueID))
                     db.commit()
                     data = c.fetchall()

                     c.close()
                     db.close()
##                     self.sv6.set(str(data))

    def ConfirmCheckout(self):
         db = self.Connect()
         c = db.cursor()
         issueID = self.issueID[0]
         sql5 = ("UPDATE BookCopy SET isOnHold = 0, isCheckedOut = 1 WHERE (ISBN, CopyNum) IN (SELECT ISBN, CopyNum FROM Issues WHERE Issue_ID = (%s))")
         c.execute(sql5, issueID)
         db.commit()

         sql6 = "SELECT DateOfIssue,ReturnDate FROM Issues WHERE Issue_ID=%s"
         c.execute(sql6,issueID)
         data = c.fetchone()

         dataofissue = data[0]
         returndate = data[1]

         self.sv3.set(dataofissue)
         self.sv6.set(returndate)

         c.close()
         db.close()

    def ReturnBook(self):
        self.tenthwin = Toplevel()
        self.tenthwin.config(bg="white")
        self.tenthwin.title("Return Book")

        self.sv1 = StringVar()
        self.sv2 = StringVar()
        self.sv3 = StringVar()#is ther DateVar
        self.sv5 = StringVar()


        f2 = Frame(self.tenthwin)
        f2.config(bg="white")
        f2.grid(row=1,column=0)
        l1=Label(f2,text="Issue Id",bg="white")
        l1.grid(row=0,column=0,sticky=W)
        self.e1 = Entry(f2,bg="white", textvariable=self.sv1) #IssueId
        self.e1.grid(row=0,column=1,sticky=W,padx=2,pady=5)
        l2=Label(f2,text="ISBN",bg="white")
        l2.grid(row=1,column=0,sticky=W)
        e2 = Entry(f2,bg="white",state = "readonly", textvariable=self.sv2) #ISBN
        e2.grid(row=1,column=1,sticky=W,padx=2,pady=5)
        
        b1=Button(f2,text="Search", command=self.ReturnBook2)
        b1.grid(row=0,column=2, sticky=W)
        
        l3=Label(f2,text="Copy Number",bg="white")
        l3.grid(row=1,column=2,sticky=W)
        e3 = Entry(f2,bg="white",state = "readonly", textvariable=self.sv3) #CopyNumber
        e3.grid(row=1,column=3,sticky=W,padx=2,pady=5)
        l4=Label(f2,text="Return in Damaged Condition",bg="white")
        l4.grid(row=2,column=0,sticky=W)
        #e4 = Entry(f2,bg="white",state = "readonly", textvariable=self.sv5) #
        #e4.grid(row=2,column=3,sticky=W,padx=2,pady=5)
        self.var = StringVar(f2)
        self.var.set("N")
        choices = ['N', 'Y']
        self.lb = OptionMenu(f2,self.var,*choices)
        self.lb.grid(row=2,column=1,sticky=E)
        
        l5=Label(f2,text="User Name",bg="white")
        l5.grid(row=2,column=2,sticky=W)
        e5 = Entry(f2,bg="white",state = "readonly", textvariable=self.sv5) #Username
        e5.grid(row=2,column=3,sticky=W,padx=2,pady=5)
        b2 = Button(f2,text="Return", command=self.ReturnBook3)
        b2.grid(row=3,column=3,padx=2,pady=10)

    def ReturnBook2(self): #Search Button
        self.ReturnIssueId=self.e1.get()
        c=self.Connect().cursor()
        c.execute("SELECT ISBN,CopyNum,Username FROM Issues WHERE Issue_ID='{}'".format(self.ReturnIssueId))
        a=c.fetchone()
        print (a)
        self.sv2.set(a[0])#ISBN
        self.sv3.set(a[1])#Copynum
        self.sv5.set(a[2])#Username
        self.Connect().commit()
        c.close()
        self.Connect().close()
        
    def ReturnBook3(self): #ReturnButton        
        if self.var.get()=='Y': #damagebook            
            db=self.Connect()
            c=db.cursor()
            sql3 = "UPDATE BookCopy SET IsDamaged = TRUE, isCheckedOut = FALSE WHERE (isbn,copynum) in (select isbn,copynum from Issues where issue_id = %s)"
            c.execute(sql3,(self.ReturnIssueId))
            db.commit()      
        if self.var.get()=='N':
            db=self.Connect()
            c=db.cursor()
            sql3="UPDATE BookCopy SET IsCheckedOut = FALSE WHERE (ISBN,CopyNum) in (SELECT ISBN,CopyNum from Issues where Issue_Id = %s)"
            c.execute(sql3,(self.ReturnIssueId))
            db.commit()

        db=self.Connect()
        c=db.cursor()
        sql="UPDATE StudentFaculty SET Penalty = Penalty + ifnull((SELECT 0.5*(DATEDIFF(sysdate(), ReturnDate)) "\
                  "FROM Issues WHERE issue_id = %s and returndate < sysdate()),0) "\
                  "WHERE Username in (select username from Issues where issue_id = %s)"
        c.execute(sql,(self.ReturnIssueId, self.ReturnIssueId))
        sql4 = "update Issues Set ReturnDate = sysdate() where issue_id= %s"
        c.execute(sql4,(self.e1.get()))#issueid
        db.commit()
        c.close()
        db.close()
        self.ToHomeFromReturnBook()
 
    def LostDamagedBookPenalty(self): #ADD TO CLARISSA
        self.LostDamagedBookPenalty = Toplevel()
        self.LostDamagedBookPenalty.title("Penalty Fees")
        self.LostDamagedBookPenalty.config(bg="white")
        
        self.ISBN = StringVar()
        self.cNum = StringVar()
        self.curTime = datetime.datetime.now()
        self.amtCharge = StringVar()
        self.lastUser = StringVar()


        f = Frame(self.LostDamagedBookPenalty)
        f.config(bg="white")
        f.grid(row=0,column=0)
        l=Label(f,text="ISBN",bg="white")
        l.grid(row=0,column=0,sticky=W)
        self.e = Entry(f,bg="white", textvariable=self.ISBN) #
        self.e.grid(row=0,column=1,sticky=W,padx=2,pady=5)
        l2=Label(f,text="Book Copy #",bg="white")
        l2.grid(row=0,column=2,sticky=W)
        self.e2 = Entry(f,bg="white", textvariable=self.cNum) #
        self.e2.grid(row=0,column=3,sticky=W,padx=2,pady=5)
        l3=Label(f,text="Current Time",bg="white")
        l3.grid(row=1,column=0,sticky=W)
        l4=Label(f,text=self.curTime,bg="gray")
        l4.grid(row=1,column=1,sticky=W,padx=2,pady=5)
        #self.e = Entry(f,bg="white", textvariable=datetime.datetime.now()) #WHAT TYPE OF TIME
        #self.e.grid(row=1,column=1,sticky=W,padx=2,pady=5)
        f2 = Frame(self.LostDamagedBookPenalty)
        f2.config(bg="white")
        f2.grid(row=1,column=0)
        b2 = Button(f2,text="Look for the last user", command = self.FindLastUser)#command=self.HomeScreen
        b2.grid(row=0,column=0,padx=2,pady=10)

        f3 = Frame(self.LostDamagedBookPenalty)
        f3.config(bg="white")
        f3.grid(row=2,column=0)
        l5=Label(f3,text="Last User of the Book",bg="white")
        l5.grid(row=0,column=0,sticky=W)
        self.e3 = Entry(f3,bg="white", textvariable=self.lastUser, state = "readonly")
        self.e3.grid(row=0,column=1,sticky=W,padx=2,pady=5)
        #l6=Label(f3,text="                   ",bg="gray")
        #l6.grid(row=0,column=1,sticky=W,padx=2,pady=5)
        l6=Label(f3,text="Amount to be charged",bg="white")
        l6.grid(row=1,column=0,sticky=W)
        self.e4 = Entry(f3,bg="white", textvariable=self.amtCharge) #
        self.e4.grid(row=1,column=1,sticky=W,padx=2,pady=5)

        f4 = Frame(self.LostDamagedBookPenalty)
        f4.config(bg="white")
        f4.grid(row=3,column=0)
        b3 = Button(f4,text="Submit", command = self.ChargeUser)#command=self.HomeScreen
        b3.grid(row=0,column=0,padx=2,pady=10)
        b4 = Button(f4,text="Cancel", command = self.ToHomeFromPenalty)#command=self.HomeScreen
        b4.grid(row=0,column=1,padx=2,pady=10)

    def FindLastUser(self): #add to clarissa
        db = self.Connect()
        c = db.cursor()

        self.isbn = self.e.get()
        self.cNum = self.e2.get()

        sql = "SELECT Username FROM Issues WHERE ISBN = %s AND CopyNum = %s ORDER BY DateOfIssue DESC Limit 1"
        c.execute(sql,(self.isbn,self.cNum))
        lastUser = c.fetchone()

        if lastUser:
            lastUserName = lastUser[0]
            self.e3.config(state=NORMAL) #quotation marks?
            self.lastUser.set(lastUserName)
            #self.e2.config(text = self.sv3)
            self.e3.config(state="readonly")
        else: 
            pass

        c.close()
        db.commit()
        db.close()

    def ChargeUser(self): #add to clarissa
        db = self.Connect()
        c = db.cursor()

        self.amtPenalized = self.e4.get()
        self.victim = self.e3.get()
        print(self.amtPenalized)

        sql = "UPDATE StudentFaculty SET Penalty = Penalty + (%s) WHERE Username = %s"
        c.execute(sql,(self.amtPenalized, self.victim))
        #lastUser = c.fetchone()
        debarredCheck = "UPDATE StudentFaculty SET isDebarred = TRUE WHERE Penalty > 100 AND Username= %s"
        c.execute(debarredCheck,(self.victim))
        print("done charging")

        c.close()
        db.commit()
        db.close()

    def DamBooksReport(self): #ADD TO CLARISSA
        self.DamBooksReport = Toplevel()
        self.DamBooksReport.title("Damaged Books Report")
        self.DamBooksReport.config(bg="white")
        
        f = Frame(self.DamBooksReport)
        f.config(bg="white")
        f.grid(row=0,column=0)
        #months
        self.var = StringVar(f)
        self.var.set("Month")
        choices = ['January','February','March','April','May','June','July','August','September','October','November','December']
        self.g = OptionMenu(f,self.var,*choices)
        self.g.grid(row=0,column=0,sticky=E)
        #subject1
        self.sub1 = StringVar(f)
        self.sub1.set("Subject 1")
        subjectOne = ['Alchemy','Creatures','Divination','General Education','History','Potions']
        self.g = OptionMenu(f,self.sub1,*subjectOne)
        self.g.grid(row=0,column=1,sticky=E)
        #subject2
        self.sub2 = StringVar(f)
        self.sub2.set("Subject 2")
        subjectTwo = ['Alchemy','Creatures','Divination','General Education','History','Potions']
        self.g = OptionMenu(f,self.sub2,*subjectTwo)
        self.g.grid(row=1,column=1,sticky=E)
        #subject3
        self.sub3 = StringVar(f)
        self.sub3.set("Subject 3")
        subjectThree = ['Alchemy','Creatures','Divination','General Education','History','Potions']
        self.g = OptionMenu(f,self.sub3,*subjectThree)
        self.g.grid(row=2,column=1,sticky=E)

        f2 = Frame(self.DamBooksReport)
        f2.config(bg="white")
        f2.grid(row=1,column=0)
        b = Button(f2,text="Show Report", command = self.genDamBookReport)#command=self.SearchBooks)#command=self.HomeScreen
        b.grid(row=0,column=0,padx=80,pady=10)

    def genDamBookReport(self): #ADD TO CLARISSA
        self.month = self.var.get()
        self.subj1 = self.sub1.get()
        self.subj2 = self.sub2.get()
        self.subj3 = self.sub3.get()

        db = self.Connect()
        c = db.cursor()

        sql1 = "SELECT DISTINCT %s FROM Subject"
        c.execute(sql1,(self.subj1))
        data1 = c.fetchone()
        sql2 = "SELECT DISTINCT %s FROM Subject"
        c.execute(sql2,(self.subj2))
        data2 = c.fetchone()
        sql3 = "SELECT DISTINCT %s FROM Subject"
        c.execute(sql3,(self.subj3))
        data3 = c.fetchone()

        if data1: #if the data exists
            sub1 = data1[0]
        else:
            pass
        if data2: #if the data exists
            sub2 = data2[0]
        else:
            pass
        if data3: #if the data exists
            sub3 = data3[0]
        else:
            pass

        f3 = Frame(self.DamBooksReport)
        f3.config(bg="white")
        f3.grid(row=2,column=0)

        l = Label(f3,text='Month',bg="blue",relief=GROOVE,width=15)
        l.grid(row=0, column=1)
        l2 = Label(f3,text='Subject',bg="blue",relief=GROOVE,width=40)
        l2.grid(row=0, column=2)
        l3 = Label(f3,text='# Damaged Books',bg="blue",relief=GROOVE,width=15)
        l3.grid(row=0, column=3)

        sql ="select month, Subject_Name, count(*) num_damaged_books From ( SELECT DISTINCT monthname(returnDate) month, Book.Subject_name, BookCopy.ISBN, BookCopy.CopyNum from Book, BookCopy, Issues WHERE Book.ISBN = BookCopy.ISBN AND Issues.ISBN = BookCopy.ISBN AND Issues.CopyNum = BookCopy.CopyNum AND isDamaged = TRUE AND (Subject_Name = %s OR Subject_Name = %s OR Subject_Name = %s) AND monthname(returndate) = %s and year(returndate) = (select year(max(returndate)) from Issues where monthname(returndate) = %s)) a group by month, Subject_Name"
        c.execute(sql,(self.subj1,self.subj2,self.subj3,self.month,self.month))
        self.data = c.fetchall()

        f4 = Frame(self.DamBooksReport)
        f4.config(bg="white")
        f4.grid(row=3,column=0)

        for i in range(len(self.data)):
            l = Label(f4,text=self.data[i][0],bg="gray",relief=GROOVE,width=15)
            l.grid(row=i+1, column=1)
            l2 = Label(f4,text=self.data[i][1],bg="gray",relief=GROOVE,width=40)
            l2.grid(row=i+1, column=2)
            l3 = Label(f4,text=self.data[i][2],bg="gray",relief=GROOVE,width=15)
            l3.grid(row=i+1, column=3)

        c.close()
        db.close()


    def PopBooksReport(self): #ADD TO CLARISSA
        db = self.Connect()
        c = db.cursor()

        self.PopBooksReport = Toplevel()
        self.PopBooksReport.title("Popular Books Report")
        self.PopBooksReport.config(bg="white")
        
        
        f = Frame(self.PopBooksReport)
        f.config(bg="white")
        f.grid(row=0,column=0)

        l = Label(f,text='Month',bg="blue",relief=GROOVE,width=15)
        l.grid(row=0, column=1)
        l2 = Label(f,text='Title',bg="blue",relief=GROOVE,width=40)
        l2.grid(row=0, column=2)
        l3 = Label(f,text='# Checkouts',bg="blue",relief=GROOVE,width=15)
        l3.grid(row=0, column=3)

        sql = "select * from (SELECT monthname(DateOfIssue) month,Title, COUNT(*) num_checkouts FROM Issues, Book WHERE MonthName(DateOfIssue) = 'January' AND Book.ISBN = Issues.ISBN GROUP BY MONTHName(DateOfIssue),Title ORDER BY COUNT(*) LIMIT 3) a UNION select * from (SELECT MONTHname(DateOfIssue) month,Title, COUNT(*) num_checkouts FROM Issues, Book WHERE Monthname(DateOfIssue) =  'February' AND Book.ISBN = Issues.ISBN GROUP BY Monthname(DateOfIssue),Title ORDER BY COUNT(*) LIMIT 3) b"
        c.execute(sql)
        self.data = c.fetchall()

        f2 = Frame(self.PopBooksReport)
        f2.config(bg="white")
        f2.grid(row=3,column=0)

        for i in range(len(self.data)):
            l = Label(f2,text=self.data[i][0],bg="gray",relief=GROOVE,width=15)
            l.grid(row=i+1, column=1)
            l2 = Label(f2,text=self.data[i][1],bg="gray",relief=GROOVE,width=40)
            l2.grid(row=i+1, column=2)
            l3 = Label(f2,text=self.data[i][2],bg="gray",relief=GROOVE,width=15)
            l3.grid(row=i+1, column=3)

        c.close()
        db.close()

    def FrequentUsersReport(self): #ADD TO CLARISSA
        db = self.Connect()
        c = db.cursor()

        self.FrequentUsersReport = Toplevel()
        self.FrequentUsersReport.title("Frequent Users Report")
        self.FrequentUsersReport.config(bg="white")
        
        
        f = Frame(self.FrequentUsersReport)
        f.config(bg="white")
        f.grid(row=0,column=0)

        l = Label(f,text='Month',bg="blue",relief=GROOVE,width=15)
        l.grid(row=0, column=1)
        l2 = Label(f,text='User Name',bg="blue",relief=GROOVE,width=40)
        l2.grid(row=0, column=2)
        l3 = Label(f,text='# Checkouts',bg="blue",relief=GROOVE,width=15)
        l3.grid(row=0, column=3)

        sql = "select * from (SELECT Monthname(DateOfIssue) month, Username, COUNT(*) num_checkouts FROM Issues WHERE Monthname(DateOfIssue) = 'January' GROUP BY Monthname(DateOfIssue),Username HAVING COUNT(*) > 10 ORDER BY COUNT(*) DESC LIMIT 5) a UNION select * from ( SELECT Monthname(DateOfIssue) month, Username, COUNT(*) num_checkouts FROM Issues WHERE Monthname(DateOfIssue) = 'February' GROUP BY Monthname(DateOfIssue),Username HAVING COUNT(*) > 10 ORDER BY COUNT(*) DESC LIMIT 5) b"
        c.execute(sql)
        self.data = c.fetchall()

        f2 = Frame(self.FrequentUsersReport)
        f2.config(bg="white")
        f2.grid(row=3,column=0)

        for i in range(len(self.data)):
            l = Label(f2,text=self.data[i][0],bg="gray",relief=GROOVE,width=15)
            l.grid(row=i+1, column=1)
            l2 = Label(f2,text=self.data[i][1],bg="gray",relief=GROOVE,width=40)
            l2.grid(row=i+1, column=2)
            l3 = Label(f2,text=self.data[i][2],bg="gray",relief=GROOVE,width=15)
            l3.grid(row=i+1, column=3)

        c.close()
        db.close()

    def PopularSubjectReport(self): #ADD TO CLARISSA
        db = self.Connect()
        c = db.cursor()

        self.PopularSubjectReport = Toplevel()
        self.PopularSubjectReport.title("Popular Subject Report")
        self.PopularSubjectReport.config(bg="white")
        
        
        f = Frame(self.PopularSubjectReport)
        f.config(bg="white")
        f.grid(row=0,column=0)

        l = Label(f,text='Month',bg="blue",relief=GROOVE,width=15)
        l.grid(row=0, column=1)
        l2 = Label(f,text='Top Subject',bg="blue",relief=GROOVE,width=40)
        l2.grid(row=0, column=2)
        l3 = Label(f,text='# Checkouts',bg="blue",relief=GROOVE,width=15)
        l3.grid(row=0, column=3)

        sql = "select * from (SELECT MonthName(DateOfIssue) month,Subject_Name, COUNT(*) num_checkouts FROM Book, Issues WHERE Book.ISBN = Issues.ISBN AND MonthName(DateOfIssue) = 'January' GROUP BY MonthName(DateOfIssue),Subject_Name ORDER BY COUNT(*) DESC) a UNION select * from (SELECT MonthName(DateOfIssue) month,Subject_Name, COUNT(*) num_checkouts FROM Book, Issues WHERE Book.ISBN = Issues.ISBN AND MonthName(DateOfIssue) = 'February' GROUP BY MonthName(DateOfIssue),Subject_Name ORDER BY COUNT(*) DESC) b"
        c.execute(sql)
        self.data = c.fetchall()

        f2 = Frame(self.PopularSubjectReport)
        f2.config(bg="white")
        f2.grid(row=3,column=0)

        for i in range(len(self.data)):
            l = Label(f2,text=self.data[i][0],bg="gray",relief=GROOVE,width=15)
            l.grid(row=i+1, column=1)
            l2 = Label(f2,text=self.data[i][1],bg="gray",relief=GROOVE,width=40)
            l2.grid(row=i+1, column=2)
            l3 = Label(f2,text=self.data[i][2],bg="gray",relief=GROOVE,width=15)
            l3.grid(row=i+1, column=3)

        c.close()
        db.close()


    def HomeScreen(self): #ADD TO CLARISSA/UPDATE WITH MORE BUTTONS
        self.Homewin = Toplevel()
        self.Homewin.title("Home Page")
        self.Homewin.config(bg="white")
        

        f = Frame(self.Homewin)
        f.config(bg="white")
        f.grid(row=0,column=0)
        b = Button(f,text="Seach Books",command=self.ToSearchFromHome)#self.SearchBooks)
        b.grid(row=0,column=0,padx=80,pady=10)
        b2 = Button(f,text="Request Extension",command=self.ToRequestExtension)#self.RequestExtension)
        b2.grid(row=1,column=0,padx=80,pady=10)
        b3 = Button(f,text="Future Hold Request",command=self.ToFutureHoldRequest)#self.FutureHoldRequest)
        b3.grid(row=2,column=0,padx=80,pady=10)
        b4 = Button(f,text="Track Book Location",command=self.ToTrackBookLocation)#self.TrackBookLocation)
        b4.grid(row=3,column=0,padx=80,pady=10)
        b5 = Button(f,text="Book Checkout",command=self.ToBookCheckout)#self.BookCheckout)
        b5.grid(row=4,column=0,padx=80,pady=10)
        b6 = Button(f,text="Return Book",command=self.ToReturnBook)#self.ReturnBook)
        b6.grid(row=5,column=0,padx=80,pady=10)
        b7 = Button(f,text="Penalty Charges",command=self.LostDamagedBookPenalty)#command=self.HomeScreen
        b7.grid(row=6,column=0,padx=80,pady=10)
        b8 = Button(f,text="Reports",command=self.Reports)#command=self.HomeScreen
        b8.grid(row=7,column=0,padx=80,pady=10)

    def Reports(self): #ADD TO CLARISSA
        self.Reports = Toplevel()
        self.Reports.title("Reports Page")
        self.Reports.config(bg="white") 

        f = Frame(self.Reports)
        f.config(bg="white")
        f.grid(row=0,column=0)

        b = Button(f,text="Damaged Books Report", command = self.DamBooksReport)#,command=self.SearchBooks)#command=self.HomeScreen
        b.grid(row=0,column=0,padx=80,pady=10)
        b2 = Button(f,text="Popular Books Report", command = self.PopBooksReport)#,command=self.RequestExtension)#command=self.HomeScreen
        b2.grid(row=1,column=0,padx=80,pady=10)
        b3 = Button(f,text="Frequent User Report", command = self.FrequentUsersReport)#,command=self.FutureHoldRequest)#command=self.HomeScreen
        b3.grid(row=2,column=0,padx=80,pady=10)
        b3 = Button(f,text="Frequent Subject Report", command = self.PopularSubjectReport)#,command=self.FutureHoldRequest)#command=self.HomeScreen
        b3.grid(row=3,column=0,padx=80,pady=10)

win = Tk()
app = GUI(win)
win.mainloop()        
