import getopt
import sys
from MCQMaster import *


class MCQRunConsole:
    def __init__(self, file):
        self.master = MCQMaster(file)
        mcqs = self.master.get_all_mcqs()
        # Print the test name
        self.beautify(self.master.get_test_name())
        print()
        # Print all the MCQs names in list-style
        str_mcqs = "This test contains these MCQs : "
        list_mcqs = []
        for mcq_i in mcqs:
            list_mcqs.append(mcq_i.get('name'))
        print(str_mcqs, list_mcqs, '\n')
        # Prompt to choose a MCQ (or all of them)
        mcq_choice = input("Enter the MCQ (only one) you want, or '*' for all : ")
        print()
        # Start the corresponding exam
        if mcq_choice in '*':
            self.start_all()
        else:
            for mcq_name in list_mcqs:
                if mcq_choice in mcq_name:
                    self.start_one_by_mcq_name(mcq_name)

    def beautify(self, string):
        line = ""
        for i in range(len(string) + 4):
            line += "#"
        print(line)
        print("# " + string + " #")
        print(line)

    def start_one_by_mcq_object(self, mcq_object):
        total = 0
        result = 0
        print("[ " + mcq_object.get('name') + " ]")
        print("Questions :")
        str_answers = "Answers :\n"
        for question in mcq_object.get('questions'):
            answers = question.get('answers')
            to_check = input(question.get('name') + " : ")
            question_result = self.master.evaluate_answer(to_check, answers)
            str_answers += question.get('name') + " : " + answers + " (" + str(question_result) + "/1)\n"

            result += question_result
            total += 1
        print(str_answers[:-1])
        print("Result : " + str(result) + "/" + str(total) + "\n")

    def start_one_by_mcq_name(self, mcq_name):
        mcq = self.master.get_mcq_by_name(mcq_name)
        self.start_one_by_mcq_object(mcq)

    def start_all(self):
        exam = self.master.get_all_mcqs()
        for mcq in exam:
            self.start_one_by_mcq_object(mcq)


class MCQCreateConsole:
    def __init__(self, filename):
        self.filename = filename


def main(argv):
    usage = "usage: MCQConsole.py <option>\n" + \
            "Options :\n" + \
            " -f <XML file> : Launch MCQConsole in test mode (read from file)\n" + \
            " -c <XML file> : Launch MCQConsole in create mode (write to file)"
    try:
        opts, args = getopt.getopt(argv, "hf:c:", ["file="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    if len(sys.argv) < 2:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-f", "--file"):
            m = MCQRunConsole(arg)
        elif opt in ("-c", "--file"):
            m = MCQCreator(arg)
            m.create()


if __name__ == "__main__":
    main(sys.argv[1:])