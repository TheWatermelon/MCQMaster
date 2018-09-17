import math
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


class MCQMaster:
    def __init__(self, file):
        with open(file, 'r', encoding = "ISO-8859-1") as xml_file:
            self.tree = ET.parse(xml_file)

    def get_mcq_by_element_tree(self, mcq_element):
        mcq = {}
        questions = []

        # get all the questions in a list
        for question_i in mcq_element.findall('question'):
            question = {}
            answers = ""
            for answer in question_i.findall('answer'):
                answers += answer.text
            # a question has a name and answers
            question['name'] = question_i.get('name')
            question['answers'] = answers
            # add the question to the questions list
            questions.append(question)
        # a mcq has a name and questions
        mcq['name'] = mcq_element.get('name')
        mcq['questions'] = questions

        return mcq

    def get_mcq_by_name(self, mcq_name):
        # search for the mcq by its name on the tree
        for mcq_i in self.tree.getroot():
            if mcq_i.get('name') not in mcq_name:
                continue
            # found
            else:
                return self.get_mcq_by_element_tree(mcq_i)

    def get_all_mcqs(self):
        mcqs = []
        # for all mcqs
        for mcq_i in self.tree.getroot():
            # get its info and add it to the list
            mcqs.append(self.get_mcq_by_element_tree(mcq_i))

        return mcqs

    def get_test_name(self):
        return self.tree.getroot().get('name')

    def evaluate_answer(self, to_check, answer):
        errors = 0
        # How many correct answers weren't provided
        for char in answer:
            if char.lower() not in to_check.lower():
                errors += 1
        # How many bad answers were provided
        for char in to_check:
            if not (char == ' ' or char == '\t' or char == '\r' or char == '\n'):
                if char.lower() not in answer.lower():
                    errors += 1

        # Detect whether the answer is SCQ or MCQ
        if len(answer) > 1:
            # MCQ : 0 error = 1; 1 error = 0.5; 2+ errors = 0
            if errors > 1:
                return 0
            elif errors > 0:
                return 0.5
            else:
                return 1
        else:
            # SCQ : 0 error = 1; 1+ error(s) = 0
            if errors > 0:
                return 0
            else:
                return 1


class MCQCreator:
    def __init__(self, filename, tree):
        self.filename = filename
        self.tree = tree

    def create_from_dict(self, d):
        self.tree.attrib['name'] = d['name']

        for mcq_i in range(len(d['mcqs'])):
            mcq = ET.SubElement(self.tree, 'mcq')
            mcq.attrib['name'] = d['mcqs'][mcq_i]['name']

            questions = d['mcqs'][mcq_i]['questions']
            for question_i in range(len(questions)):
                question = ET.SubElement(mcq, 'question')
                question.attrib['name'] = questions[question_i][0]
                for char in questions[question_i][1]:
                    answer = ET.SubElement(question, 'answer')
                    answer.text = char.upper()

        self.print_on_file()

    def print_on_file(self):
        pretty_xml = minidom.parseString(ET.tostring(self.tree,
                                                     'utf-8')).toprettyxml(indent="\t")
        f = open(self.filename, 'w')
        f.write(pretty_xml)

