from bin import *
from passlib.hash import sha256_crypt
import json
from tkinter import *
import tkinter as tk
from tkinter import messagebox

class TikinterApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switchFrame(StartPage)


    def switchFrame(self, frameClass):
        newFrame = frameClass(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = newFrame
        self._frame.pack()


class StartPage(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master, width=250, height=250)
        self.master.title("Restaurant Towkay")
        startLabel = tk.Label(self, text="Welcome to Restaurant Towkay")
        pageLogin = tk.Button(self, text="Login", command=lambda: master.switchFrame(PageOne))
        pageRegister = tk.Button(self, text="Register", command=lambda: master.switchFrame(PageTwo))
        startLabel.place(x=40, y=50)
        pageLogin.place(x=110, y=160)
        pageRegister.place(x=108, y=200)

class PageOne(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master, width=250, height=250)

        pageLoginLabel = tk.Label(self, text="Login Page")
        startButton = tk.Button(self, text="Home", command=lambda: master.switchFrame(StartPage))
        enterButton = tk.Button(self, text="Enter", command=self.login)
        pageLoginLabel.place(x=100, y=10)

        Label(self, text="Username :").place(x=10, y=65)
        self.userEntry = Entry(self)
        self.userEntry.place(x=80, y=65)

        Label(self, text="Password :").place(x=10, y=100)
        self.passwordEntry = Entry(self, show="*")
        self.passwordEntry.place(x=80, y=100)

        enterButton.place(x=110, y=160)
        startButton.place(x=108, y=200)

    def login(self):

        user = self.userEntry.get()
        password = self.passwordEntry.get()

        with open('security/hash.json','r') as json_file:
            keyList = json.load(json_file)

        noUser = True

        for acc in keyList:
            if user == acc['user']:
                noUser = False
                account = acc
                hash1 = account['hashValue']
                if sha256_crypt.verify(password, hash1) is True:
                    messagebox.showinfo("Success!", "Login is successful.")
                    break
                else:
                    messagebox.showerror("Oops!", "Wrong password!")
                    break

        if noUser:
            messagebox.showerror("Oops!", "User is not registered!")

        json_file.close()

class PageTwo(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master, width=250, height=250)

        pageRegisterLabel = tk.Label(self, text="Register New User")
        startButton = tk.Button(self, text="Home", command=lambda: master.switchFrame(StartPage))
        enterButton = tk.Button(self, text="Enter", command=self.newUser)

        Label(self, text="Username :").place(x=10, y=65)
        self.userNewEntry = Entry(self)
        self.userNewEntry.place(x=80, y=65)

        Label(self, text="Password :").place(x=10, y=100)
        self.passwordNewEntry = Entry(self, show="*")
        self.passwordNewEntry.place(x=80, y=100)

        Label(self, text="Confirm :").place(x=10, y=135)
        self.passwordConfirmEntry = Entry(self, show="*")
        self.passwordConfirmEntry.place(x=80, y=135)

        pageRegisterLabel.place(x=85, y=10)
        enterButton.place(x=110, y=160)
        startButton.place(x=108, y=200)

    def newUser(self):

        userNew = self.userNewEntry.get()
        passwordNew = self.passwordNewEntry.get()
        passwordConfirm = self.passwordConfirmEntry.get()

        with open('security/hash.json', 'r') as json_file:
            keyList = json.load(json_file)
            json_file.close()

        redundantUser = False
        blankUser = False
        matchPassword = True

        for acc in keyList:
            if userNew == acc['user']:
                redundantUser = True
                messagebox.showerror("Oops!", "Username taken!")
                break

        if passwordNew != passwordConfirm:
            matchPassword = False
            messagebox.showerror("Oops!", "Password does not match!")

        if userNew == "":
            blankUser = True
            messagebox.showerror("Oops!", "Username blank!"
                                 )
        if not redundantUser and not blankUser and matchPassword:
            keys = {}
            keys['user'] = userNew
            keys['hashValue'] = sha256_crypt.encrypt(passwordNew)

            with open('security/hash.json', 'w') as json_file:
                keyList.append(keys)
                json.dump(keyList, json_file, indent=4)
            json_file.close()
            messagebox.showinfo("Success!", "Registration successful!")



if __name__ == "__main__":
    app = TikinterApp()
    app.geometry("350x250")
    app.mainloop()
