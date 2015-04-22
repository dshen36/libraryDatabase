from tkinter import*
import pymysql
from re import findall

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
        self.sixthwin.deiconify()
        self.Homewin.withdraw()

    def ToFutureHoldRequest(self):
        self.seventhwin.deiconify()
        self.Homewin.withdraw()

    def ToTrackBookLocation(self):
        self.eighthwin.deiconify()
        self.Homewin.withdraw()

    def ToBookCheckout(self):
        self.ninthwin.deiconify()
        self.Homewin.withdraw()

    def ToReturnBook(self):
        self.tenthwin.deiconify()
        self.Homewin.withdraw()
        
    def Connect(self):
        try:
            db = pymysql.connect(host="academic-mysql.cc.gatech.edu",passwd="DC5xMas8",
                                 user="cs4400_Group_18",db="cs4400_Group_18")

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
        #sql = "SELECT Username,Password FROM User"
        #c.execute(sql)
        sql = "SELECT COUNT(*) FROM User WHERE Username = %s AND Password = %s"
        c.execute(sql,(self.username,password))
        data = c.fetchall()
        #print(data)

        user = (1,)

        if user in data:
            info2 = messagebox.showinfo("","You logged in successfully.")
            c.close()
            self.SearchBooks()
            self.mainwin.withdraw()
        else:
            info3 = messagebox.showinfo("","You entered an unrecognizable username/password combination")

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
                     error = messagebox.showinfo("Problem!","Password and Confirm Password do not match.")
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
            error = messagebox.showinfo("Problem","You have to fill in at least one field.")

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
            error = messagebox.showinfo("Problem","You have to fill in at least one field.")

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
        
        showID = messagebox.showinfo("Issue_ID","Your Issue_ID is " + issueID[0])
        
        c.close()
        db.close()
        

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

        #self.BookCheckout()

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
        b = Button(f,text="Seach Books",command=self.ToSearchFromHome)
        b.grid(row=0,column=0,padx=80,pady=10)
        b2 = Button(f,text="Request Extension",command=self.ToRequestExtension)#command=self.HomeScreen
        b2.grid(row=1,column=0,padx=80,pady=10)
        b3 = Button(f,text="Future Hold Request",command=self.ToFutureHoldRequest)#command=self.HomeScreen
        b3.grid(row=2,column=0,padx=80,pady=10)
        b4 = Button(f,text="Track Book Location",command=self.ToTrackBookLocation)#command=self.HomeScreen
        b4.grid(row=3,column=0,padx=80,pady=10)
        b5 = Button(f,text="Book Checkout",command=self.ToBookCheckout)#command=self.HomeScreen
        b5.grid(row=4,column=0,padx=80,pady=10)
        b6 = Button(f,text="Return Book",command=self.ToReturnBook)#command=self.HomeScreen
        b6.grid(row=5,column=0,padx=80,pady=10)

win = Tk()
app = GUI(win)
win.mainloop()        
