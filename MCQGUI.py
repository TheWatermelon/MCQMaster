from tkinter import *
from tkinter.filedialog import askopenfilename
from MCQMaster import *


class MCQRunGUI(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (MainMenu, MCQCreate1, MCQCreate2, MCQCreate3):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name].refresh()
        frame.tkraise()

    def set_MCQMaster(self, mcq_master):
        self.master = mcq_master


class MainMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        Label(self, text="MCQ GUI", borderwidth=1).pack(side="top")
        Button(self, text="Create MCQ").pack(side="top")
        Button(self, text="Load MCQ", command=self.loadFileCallBack).pack(side="top")
        Button(self, text="Quit", command=quit).pack(side="top")

    def loadFileCallBack(self):
        filename = askopenfilename()
        self.controller.set_MCQMaster(MCQMaster(filename))
        frame = MCQExam(parent=self.controller.container, controller=self.controller)
        frame.grid(row=0, column=0, sticky="nsew")
        self.controller.frames['MCQExam'] = frame
        self.controller.show_frame("MCQExam")

    def refresh(self):
        return self


class MCQExam(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.test_name_label = Label(self, text="")
        self.test_name_label.pack(side="top")
        Button(self, text="Quit Exam", command=lambda: self.controller.show_frame("MainMenu")).pack(side="bottom")

    def refresh(self):
        master = self.controller.master
        self.test_name_label['text'] = master.get_test_name()
        frame = Frame(self)
        frame.pack(side="top")
        for mcq_i in master.get_all_mcqs():
            Label(frame, text=mcq_i.get('name')).pack(side="top")

            for question_i in mcq_i.get('questions'):
                question_frame = Frame(frame)
                question_frame.pack(side="top")
                Label(question_frame, text=question_i.get('name')).pack(side="left")
                CA = Checkbutton(question_frame, text="A", variable=IntVar)
                CA.pack(side="left")
                CB = Checkbutton(question_frame, text="B", variable=IntVar)
                CB.pack(side="left")
                CC = Checkbutton(question_frame, text="C", variable=IntVar)
                CC.pack(side="left")
                CD = Checkbutton(question_frame, text="D", variable=IntVar)
                CD.pack(side="left")
                CE = Checkbutton(question_frame, text="E", variable=IntVar)
                CE.pack(side="left")


        return self


class MCQCreate1(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

    def refresh(self):
        return self

class MCQCreate2(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

    def refresh(self):
        return self

class MCQCreate3(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

    def refresh(self):
        return self

if __name__ == "__main__":
    gui = MCQRunGUI()
    gui.mainloop()