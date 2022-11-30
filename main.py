from tkinter import *
from tkinter import messagebox
import pyperclip
import re
import random

def generate_password():
    global password_input
    if password_input.get():
        password_input.delete(0,END)
    letters = [l for l in 'abcdefghijklmnopqrstuvwyxz']
    numbers = [0,1,2,3,4,5,6,7,8,9]
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    res = []
    n_letters = random.randint(8,10)
    n_symbols = random.randint(2,4)
    n_numbers = random.randint(2, 4)
    for i in range(n_letters):
        is_upper = random.randint(0,1)
        letter = random.choice(letters)
        if is_upper:
            res.append(letter.upper())
        else:
            res.append(letter)
    res.extend([str(random.choice(numbers)) for i in range(n_numbers)])
    res.extend([random.choice(symbols) for i in range(n_symbols)])
    random.shuffle(res)

    res = "".join(res)
    password_input.insert(0,res)
    pyperclip.copy(res)
    return res

window = Tk()

window.config(pady=50,padx=20)
window.title("Password Manager")
canvas = Canvas(height=200,width=200)


def validate_pw(password) -> bool:
    if len(password) < 5:
        return False
    return True

def validate_email(email) -> bool:
    email_pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if not re.fullmatch(email_pattern,email):
        return False
    return True




def clear_data() -> None:
    global password_input
    global email_input
    global web_input
    password_input.delete(0,END)
    email_input.delete(0,END)
    web_input.delete(0,END)

def save_data():
    global password_input
    global email_input
    global web_input
    password = password_input.get()
    email = email_input.get()
    site = web_input.get()
    is_valid_pw = validate_pw(password)
    is_valid_email = validate_email(email)

    if not is_valid_pw:
        messagebox.showerror(title='Invalid Password ', message='The password you entered is too short')
    if not is_valid_email:
        messagebox.showerror(title='Invalid Email ',message='The email you entered is invalid')
    if is_valid_pw and is_valid_email:
        is_ok = messagebox.askokcancel(title=site,message=f'Is this the correct details to save ?\n'
                                                  f'Email:{email}\n'
                                                  f'Password:{password}\n')
        # format_for_file = str(hashed)
        if is_ok:
            with open('passwords.txt','a') as pass_file:
                pass_file.write(f'{site} | {email} | {password}\n')
            clear_data()



pass_logo = PhotoImage(file='logo.png')
img = canvas.create_image(100,100,image=pass_logo)
canvas.grid(row=0,column=1)

web_label = Label(text='Website:')
web_label.grid(row=1)
email_label = Label(text='Email/Username:')
email_label.grid(row=2)
password_label = Label(text='Password:')
password_label.grid(row=3,column=0)

web_val = StringVar()
web_input = Entry(textvariable=web_val,width=35)
web_input.grid(row=1,column=1,columnspan=2)
web_input.focus()

email_var = StringVar()
email_input = Entry(textvariable=email_var,width=35)
email_input.grid(row=2,column=1,columnspan=2)
email_input.insert(0,'anthony@gmail.com')

password_var = StringVar()
password_input = Entry(textvariable=password_var)
password_input.grid(row=3,column=1)

gen_password = Button(text='Generate Password',command=generate_password)
gen_password.grid(row=3,column=2)

submit_btn = Button(text='Add',width=36,command=save_data)
submit_btn.grid(row=4,columnspan=2,column=1)


window.mainloop()