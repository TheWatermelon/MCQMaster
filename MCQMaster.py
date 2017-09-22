import getopt
import sys
import math
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


class MCQMaster:
    def __init__(self, file):
        self.tree = ET.parse(file)

    def beautify(self, string):
        line = ""
        for i in range(len(string)+4):
            line += "#"
        print(line)
        print("# " + string + " #")
        print(line)

    def evaluate_answer(self, to_check, answer):
        result = 0
        if len(to_check) != len(answer):
            result -= int(math.fabs(len(to_check) - len(answer)))
        for char in to_check:
            if not (char == ' ' or char == '\t' or char == '\r' or char == '\n'):
                if char.lower() in answer.lower():
                    result += 1
                else:
                    result -= 1
        if result < 0:
            result = 0
        return result

    def start(self):
        root = self.tree.getroot()
        self.beautify(root.attrib['name'].upper())
        print()

        for mcq in root:
            print("[ " + mcq.attrib['name'] + " ]")
            print("Questions :")
            str_answers = "Answers : \n"
            result = 0
            total = 0
            for question in mcq.findall('question'):
                answers = ""
                for answer in question.findall('answer'):
                    answers += answer.text

                to_check = input(question.attrib['name'] + " : ")
                question_result = self.evaluate_answer(to_check, answers)
                str_answers += question.attrib['name'] + " : " + answers + " (" + str(question_result) + "/" + str(len(answers)) + ")\n"

                result += question_result
                total += len(answers)
            print(str_answers[:-1])
            print("Result : " + str(result) + "/" + str(total) + "\n")


class MCQCreator:
    def __init__(self, filename):
        self.filename = filename

    def create(self):
        root = ET.Element('test')

        test_name = input("Test name : ")
        root.attrib['name'] = test_name

        mcq_number = 0
        while True:
            try:
                mcq_number = int(input("Number of MCQs : "))
            except ValueError:
                print("Enter an integer !")
                continue
            else:
                break

        for mcq_i in range(mcq_number):
            print("MCQ [" + str(mcq_i+1) + "/" + str(mcq_number) + "]")

            mcq = ET.SubElement(root, 'mcq')
            mcq_name = input("MCQ name : ")
            mcq.attrib['name'] = mcq_name

            question_number = 0
            while True:
                try:
                    question_number = int(input("Number of questions : "))
                except ValueError:
                    print("Enter an integer !")
                    continue
                else:
                    break

            for question_i in range(question_number):
                print("Question [" + str(question_i+1) + "/" + str(question_number) + "]")

                question = ET.SubElement(mcq, 'question')
                question_name = input("Question name : ")
                question.attrib['name'] = question_name

                answers = input("Answers : ")
                for char in answers :
                    if not (char == ' ' or char == '\t' or char == '\r' or char == '\n'):
                        answer = ET.SubElement(question, 'answer')
                        answer.text = char.upper()

        pretty_xml = minidom.parseString(ET.tostring(root,
                'utf-8')).toprettyxml(indent="\t")
        f = open(self.filename, 'w')
        f.write(pretty_xml)
        print("\n" + self.filename + " succesfully created !")


def main(argv):
    usage = "usage: MCQMaster.py <option>\n" + \
        "Options :\n" + \
        " -f <XML file> : Launch MCQMaster in test mode (read from file)\n" + \
        " -c <XML file> : Launch MCQMaster in create mode (write to file)"
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
            m = MCQMaster(arg)
            m.start()
        elif opt in ("-c", "--file"):
            m = MCQCreator(arg)
            m.create()


if __name__ == "__main__":
    main(sys.argv[1:])