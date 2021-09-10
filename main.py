"""
Username : admin
Password : admin
"""
import datetime
from time import strftime
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from Admin_menu import Admin
from User_menu import User
from Userlogin import Login

TOP_NAV_COLOR = "#ffffff"
BG = "#ffffff"
FG = "#000000"


class Main(Login, Admin, User):

    def __init__(self):
        Login.__init__(self)
        self.loginw.mainloop()
        self.loginw.state('withdraw')  # LOGIN WINDOW EXITS
        self.main_window = Toplevel(bg="#FFFFFF")
        self.main_window.state('zoomed')

        # self.main_window.attributes('-fullscreen', True)

        self.main_window.iconbitmap("images/icon.ico")
        self.main_window.title("Business Application")
        self.main_window.protocol('WM_DELETE_WINDOW', self.__Main_del__)
        self.getdetails()

    # OVERRIDING CLOSE BUTTON && DESTRUCTOR FOR CLASS LOGIN AND MAIN WINDOW
    def __Main_del__(self):
        if messagebox.askyesno("Quit", " Leave Application?"):
            self.loginw.quit()
            self.main_window.quit()
            exit(0)
        else:
            pass

    # FETCH USER DETAILS FROM PRODUCTS,USERS AND INVENTORY TABLE
    def getdetails(self):
        self.cur.execute("CREATE TABLE if not exists products("
                         "product_id varchar (20),"
                         "product_name varchar (50) NOT NULL,"
                         "product_desc varchar (50) NOT NULL,"
                         "product_cat varchar (50),"
                         "product_price INTEGER NOT NULL,"
                         "stocks INTEGER NOT NULL,PRIMARY KEY(product_id));")

        self.cur.execute("CREATE TABLE if not exists sales ("
                         "Trans_id	INTEGER,"
                         "invoice	INTEGER NOT NULL,"
                         "Product_id	varchar (20),"
                         "Quantity INTEGER NOT NULL,"
                         "Date	varchar (20),"
                         "Time varchar (20),"
                         "PRIMARY KEY(Trans_id));")

        self.cur.execute("select * from products ")

        self.products = self.cur.fetchall()
        capuser = self.username.get()
        capuser = capuser.upper()
        self.cur.execute("select account_type from users where username= ? ", (capuser,))
        li = self.cur.fetchall()
        self.account_type = li[0][0]
        self.buildmain()

    #  ADD WIDGETS TO TOP OF MAIN WINDOW
    def buildmain(self):
        if self.account_type == 'ADMIN':
            super(Admin).__init__()
            self.admin_main_menu()
        else:
            super(User).__init__()
            self.user_mainmenu()

        self.logout.config(command=self.__Main_del__)
        self.changeuser.config(command=self.change_user)
        canvas_top = Canvas(self.main_window, bg=TOP_NAV_COLOR, width=700, height=70, highlightthickness=2)
        image = Image.open("images/crm.png")
        resize_image = image.resize((60, 60))
        self.logo = ImageTk.PhotoImage(resize_image)
        self.label = Label(self.main_window, image=self.logo, bg="#ffffff")
        self.label.image = self.logo
        self.label.grid(column=0, row=0, pady=(10, 15))

        title = Label(canvas_top, text="Easy Business", bg=TOP_NAV_COLOR, font=('Century', 30, 'normal'))
        title.place(x=220, y=10)

        canvas_top.place(x=200, y=10)

        self.canvas_user = Canvas(self.main_window, bg=TOP_NAV_COLOR, height=70, width=210)

        image = Image.open("images/employee man.png")
        resize_image = image.resize((50, 50))
        user = ImageTk.PhotoImage(resize_image)

        self.user_label = Label(self.canvas_user, image=user, bg=TOP_NAV_COLOR)
        self.user_label.image = user
        self.user_label.place(x=15, y=10)

        self.User_Name = Label(self.canvas_user, text=f"Hello, {(self.username.get()).capitalize()}",
                               font=("calibre", 15, "normal"), bg=TOP_NAV_COLOR)
        self.User_Name.place(x=75, y=25)

        self.canvas_user.place(x=1100, y=10)

        self.canvas_date = Canvas(self.main_window, bg=BG, height=60, width=210, highlightthickness=2)
        date = datetime.date.today()
        day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day = day_name[datetime.date.today().weekday()]
        self.date_lbl = Label(self.canvas_date, text=f'{day}, {datetime.date.strftime(date, "%d %b %y")}',
                              font=('calibri', 15, 'normal'),
                              fg=FG, bg=BG)
        self.date_lbl.place(x=10, y=7)
        wish = ['Morning', 'Afternoon', 'Evening']
        index = 0
        if 5 <= int(strftime('%H')) < 12:
            index = 0
        if 12 <= int(strftime('%H')) < 17:
            index = 1
        if int(strftime('%H')) >= 17:
            index = 2
        self.wish_lbl = Label(self.canvas_date, text=f"Good {wish[index]}, Team", bg=BG, fg=FG,
                              font=('calibri', 13, 'italic'))
        self.wish_lbl.place(x=10, y=35)
        self.canvas_date.place(x=1100, y=100)

    # METHODS FOR ITEMS AND CHANGE USER BUTTONS
    def change_user(self):
        if messagebox.askyesno("Alert!", "Do  you want to change user?"):
            self.base.commit()
            self.main_window.destroy()
            self.loginw.destroy()
            self.__init__()


if __name__ == '__main__':
    w = Main()
    w.base.commit()
    w.main_window.mainloop()
