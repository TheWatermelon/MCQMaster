from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from MCQMaster import *
import os

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

    def run_tests(self, cb_list):
        for cb in cb_list:
            if cb.instate(['selected']):
                # create a test view for the selected test and add it to the frames
                print(cb.cget("text"))

        # goto the first test selected to start 


class MainMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        Label(self, text="MCQ GUI", borderwidth=1).pack(side="top")
        Button(self, text="Create MCQ").pack(side="top")
        Button(self, text="Load MCQ", command=self.loadFileCallBack).pack(side="top")
        Button(self, text="Quit", command=quit).pack(side="top")

    def loadFileCallBack(self):
        filename = askopenfilename(initialdir=(os.path.expanduser('~/')))
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
        
        mcqs_frame = Frame(frame)
        mcqs_frame.pack(side="top")
        Label(mcqs_frame, text="Choose the MCQs you want").pack(side="top")
        cb_list = []
        for mcq_i in master.get_all_mcqs():
            cb = ttk.Checkbutton(mcqs_frame, text=mcq_i.get('name'))
            cb.pack(side="left")
            cb_list.append(cb)

        Button(mcqs_frame, text="Run test(s)", command=lambda: self.controller.run_tests(cb_list)).pack(side="bottom")

        return self


class MCQTest(Frame):
    def __init__(self, parent, controller, mcq_name):
        Frame.__init__(self, parent)
        self.controller = controller
        self.mcq = controller.master.get_mcq_by_name(mcq_name)


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
