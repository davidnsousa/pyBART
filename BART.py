from tkinter import *
import datetime
import time
import random


def close(event):
    root.destroy()


class subject:

    def __init__(self):
        self.trials = 0
        self.cash = 0
        self.temp_cash = 0

        self.info = Label(root, text="'Esc' to exit at any time")
        self.info.pack()
        self.frame = Frame(root, bd=2, relief=GROOVE)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        id_label = Label(self.frame, text="Id")
        id_label.grid(row=0, column=0, sticky=E)
        self.id = Entry(self.frame)
        self.id.insert(END, 'test')
        self.id.grid(row=0, column=1)

        gender_label = Label(self.frame, text="Gender")
        gender_label.grid(row=1, column=0, sticky=E)
        self.gender = Entry(self.frame)
        self.gender.insert(END, 'F')
        self.gender.grid(row=1, column=1)

        age_label = Label(self.frame, text="Age")
        age_label.grid(row=2, column=0, sticky=E)
        self.age = Entry(self.frame)
        self.age.insert(END, '20')
        self.age.grid(row=2, column=1)

        condition_label = Label(self.frame, text="Condition")
        condition_label.grid(row=4, column=0, sticky=E)
        self.condition = Entry(self.frame)
        self.condition.insert(END, '0')
        self.condition.grid(row=4, column=1)

        submit_button = Button(self.frame, text="Submit")
        submit_button.bind('<ButtonPress-1>', self.submit)
        submit_button.grid(columnspan=2)
        submit_button.focus_set()

        self.DATE = datetime.datetime.now().strftime("%Y-%m-%d")
        self.CONDITION = self.condition.get()
        self.AGE = self.age.get()
        self.GENDER = self.gender.get()
        self.ID = self.id.get()

    def submit(self, event):
        self.frame.destroy()
        self.info.destroy()
        with open(self.ID + ".csv", "w") as F:
            F.write("Id,Gender,Age,Date,Condition,Trial,Explode,Collect,Total Cash,Temp Cash,Time\n")
        reset_canvas()
        message(input_[5].replace('\\n', '\n'))
        canvas.bind('<space>', setup)


class setup:

    def __init__(self, event):
        canvas.destroy()
        reset_canvas()

        bsize = int(input_[0])
        self.grate = int(input_[1])
        self.p = list(range(int(input_[2])))
        S.temp_cash = S.cash

        self.start_time = time.time()

        # put the circle at the center of the screen
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x0 = sw / 2 - bsize / 2
        y0 = sh / 2 - bsize / 2
        self.circle = canvas.create_oval(x0, y0, x0 + bsize, y0 + bsize, width=1, fill="black")

        # put cash label
        self.cash_label = canvas.create_text(sw - 40, sh - 40, fill="black", font="Times 40 bold",
                                             text=str(S.cash))

        # put collect cash label
        self.collect_cash_label = canvas.create_text(120, sh - 40, fill="black", font="Times 20 bold",
                                                     text="Click to collect")
        canvas.tag_bind(self.collect_cash_label, '<ButtonPress-1>', self.collect)

        # key bind the circle to run grow()
        canvas.bind('<space>', self.pump)

    def collect(self, event):
        S.cash = S.temp_cash
        # record collection
        record(0, 1, self.start_time)
        self.new_trial()

    def pump(self, event):

        # change radius and recenter circle
        x0, y0, x1, y1 = canvas.coords(self.circle)
        x1 += self.grate
        y1 += self.grate
        x0 -= self.grate
        y0 -= self.grate
        canvas.coords(self.circle, x0, y0, x1, y1)

        # explode?
        choice = random.choice(self.p)
        self.p.remove(choice)
        if choice == 1:
            canvas.itemconfig(self.circle, fill='red', outline='red')
            canvas.unbind('<space>')
            canvas.tag_unbind(self.collect_cash_label, '<ButtonPress-1>')
            canvas.after(1000, self.new_trial)
            # record explosion
            record(1, 0, self.start_time)
        else:
            # change cash
            S.temp_cash += int(input_[3])
            # record pump
            record(0, 0, self.start_time)

    def new_trial(self, event=None):
        canvas.destroy()
        reset_canvas()
        S.trials += 1
        if S.trials == int(input_[4]):
            message(input_[7].replace('\\n', '\n') + str(S.cash))
        else:
            message(input_[6].replace('\\n', '\n'))
            canvas.bind('<space>', setup)


def record(explode, collect, start_time):
    with open(S.ID + ".csv", "a") as F:
        F.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (S.ID, S.GENDER, S.AGE, S.DATE, S.CONDITION, S.trials, explode,
                                                        collect, S.cash, S.temp_cash, time.time() - start_time))


def message(msg):
    canvas.create_text(root.winfo_screenwidth() / 2, root.winfo_screenheight() / 2, fill="black", font="Times 16",
                       justify=CENTER, text=msg)


def reset_canvas():
    global canvas
    canvas = Canvas(root)
    canvas.delete("all")
    canvas.config(background="white")
    canvas.focus_set()
    canvas.pack(fill='both', expand=True)


root = Tk()
root.title("TMT")
root.attributes('-fullscreen', True)
root.bind('<Escape>', close)

with open('cfg') as f:
    input_ = f.read().splitlines()
    input_ = [x.split(' #', 1)[0] for x in input_]


S = subject()

root.mainloop()
