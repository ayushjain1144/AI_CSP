"""
#######################
NAME: AYUSH JAIN
ID: 2017A7PS0093P
######################
"""

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from functools import partial
import re
from copy import deepcopy
from collections import deque
import time
#######################################

# Predefined CSP Problem
number_nodes = 0
default_m = 20

num_groups = 0
num_novels = 0
limit = 0

input_groups = {}
input_domains = {}
default_groups = {'G1': [3, 5, 8, 9, 12, 18, 19],
                'G2': [8, 9, 12, 19, 2],
                'G3': [3, 5, 4, 16, 8, 9, 19],
                'G4': [8, 9, 12, 15],
                'G5': [15, 16, 17, 18, 19, 20],
                'G6': [3, 5, 7, 11, 14, 20],
                'G7': [3, 5, 12, 2, 18, 19, 20, 1],
                'G8': [3, 5, 8, 9, 10, 18, 19, 20],
                'G9': [3, 13, 8, 9, 7, 19, 20],
                'G10': [1, 8, 9, 13, 20],
                'G11': [18, 19, 20],
                'G12': [3, 11, 8, 18, 19, 20],
                'G13': [3, 8, 10, 12, 4, 20],
                'G14': [3, 5, 11, 9, 10, 17, 19, 20],
                'G15': [2, 8, 12, 18, 19, 20]}

default_domains = {1: [2, 5, 7],
           2: [1, 4, 6, 2],
           3: [2, 5, 6, 1],
           4: [2, 4, 6, 8],
           5: [2, 6, 5],
           6: [1, 5, 3],
           7: [2, 4, 6, 1, 8],
           8: [1, 3, 4],
           9: [4, 1, 5, 8, 6],
           10: [8],
           11: [2, 3],
           12: [1, 2, 3, 4, 7],
           13: [7, 1, 8],
           14: [5, 3, 6, 1],
           15: [2, 5],
           16: [2, 5, 1, 4],
           17: [1, 4, 5, 6],
           18: [5, 4],
           19: [1, 3, 6, 8],
           20: [6]}

default_m1 = 4
default_groups1 = {'G1': [1, 2],
                    'G2': [1, 3, 4],
                    'G3': [1, 3, 2]}
default_domains1 = {1: [2, 3],
                    2: [2, 4, 5],
                    3: [2, 3, 4],
                    4: [3, 4]}





#########################################
is_with_constraint_prop = 1
is_MRV = 0
is_Degree = 0
is_default_input = 1

class MainWidget(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"AI Game")
        window = QWidget()

        self.setCentralWidget(window)
        self.resize(1800, 950)
        self.center()

        self.current_domains = default_domains
        self.adjacency_dict = self.build_neighbours()
        self.ordered_variable_list = self.build_variable_list()
        self.number_assigned = 0
        self.assignment = {}

        #print(self.current_domains)
        print(self.adjacency_dict)
        #print(self.order_variable_list)



        self.show()
        assignment = self.backtrack_search(self.current_domains)

        if assignment == None:
            print("No assignment possible")
        else:
            global number_nodes
            print("Assignment Successful")
            print(assignment)
        print(f"Total nodes produced: {number_nodes}")
        #print(self.mrv({10: 1, 20 : 2}))
        #print(self.ordered_variable_list)



    def center(self):

        qr = self.frameGeometry()
        cp  = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def  build_neighbours(self, group = default_groups, m = default_m):
        """Returns the adjacency dict"""

        adjacency_dict = {}
        for var in range(m):
            neighbors = []
            for g in group.values():

                if var + 1 in g:
                    neighbors.extend(g)
                    neighbors.remove(var + 1)
                    #print(neighbors)


            neighbors = list(set(neighbors))
            adjacency_dict[var + 1] = neighbors
        #print(adjacency_dict)
        return adjacency_dict

    def is_neighbor(self, A, B):
        """Returns true if A and B are neighbors"""


        if A in self.adjacency_dict[B]:
            return True
        else:
            return False


    def constraint(self, A, a, B, b):
        """If B is a neighbour of A and a = b, then they are voilatind constraint"""
        """a and b should be in respective domains"""

        try:
            assert(a in default_domains[A])
            assert(b in default_domains[B])
        except Exception:
            print("Values out of domains")
            print(default_domains)
            print(A, a, B, b)
            print("Exiting")
            sys.exit()
        if self.is_neighbor(A, B) and a == b:
            return True
        return False

    def build_variable_list(self, m = default_m):
        """Returns list of variables"""

        var_list = [i + 1 for i in range(m)]
        return var_list

    def is_complete_assignmnet(self, assignment, m = default_m):
        """Returns true if assignment is complete"""

        count = 0
        for var in assignment:
            count += 1
        if count == m:
            return True
        else:
            return False

    def backtrack_search(self, current_domains):
        """Implements backtrack search, returns assignment or None"""
        return self.backtrack({}, current_domains)

    def mrv(self, assignment, current_domains):
        """Returns the variable with minimum valid moves"""

        min = float('Inf')
        min_var = None
        for var in self.adjacency_dict:
            if var not in assignment:
                if len(current_domains[var]) < min:
                    min = len(current_domains[var])
                    min_var = var
        if min == 0:
            return None
        else:
            return min_var


    def degree_heurestic(self, assignment):
        """Returns the variable involved in highest number of constraints"""

        min = -float('Inf')
        min_var = None
        for var in self.adjacency_dict:
            if var not in assignment:
                count1 = len([v for v in self.adjacency_dict[var] if v not in assignment])
                #print(count1)
                if count1 > min:
                    min = count1
                    min_var = var
        return min_var


    def order_variable_list(self, assignment, current_domains):
        """Returns the next variable to be chosen"""

        if is_MRV:
            return self.mrv(assignment, current_domains)
        elif is_Degree:
            return self.degree_heurestic(assignment)
        else:
            #print(len(assignment))
            #print(self.ordered_variable_list)
            return self.ordered_variable_list[len(assignment)]

    def is_consistent(self, assignment, var, val):
        """Tests if var = val is consistent or not"""

        for A, a in assignment.items():
            if self.constraint(A, a, var, val):
                return False
        return True

    def ac3(self, assignment, current_domains, var):
        """Returns False if domain of some variable becomes empty"""

        list = deque()

        # Forms the initial queue of constraints to be mantained
        for neighbor in self.adjacency_dict[var]:
            if neighbor not in assignment:
                list.append((var, neighbor))

        while list:
            (A, B) = list.popleft()

            for  a in current_domains[A]:
                flag = False
                for b in current_domains[B]:
                    if self.constraint(A, a, B, b) == False:
                        flag = True
                        break
                if flag == False:
                    current_domains[A].remove(a)
                    if not current_domains[A]:
                        return False

                    for neighbor1 in self.adjacency_dict[A]:
                        if neighbor1 not in assignment and neighbor1 != B:
                            list.append((A, neighbor1))
        return True




    def backtrack(self, assignment, current_domains):

        current_domain_local = deepcopy(current_domains)
        if self.is_complete_assignmnet(assignment):
            return assignment


        number_assigned = len(assignment)

        var = self.order_variable_list(assignment, current_domain_local)

        #print(f"{var} returned by order_variable_list")
        if var is None:
            return None

        print(f"var = {var}")
        for value in current_domain_local[var]:

            global number_nodes
            number_nodes += 1
            if number_nodes % 100 == 0:
                print(assignment, number_nodes)
                #time.sleep(2)
            #print(value)
            if self.is_consistent(assignment, var, value):
                #print("Returned True")
                assignment[var] = value

                if is_with_constraint_prop == 1:
                    inference = self.ac3(assignment, current_domain_local, var)
                    if inference == True:

                        result = self.backtrack(assignment, current_domain_local)

                        if result != None:
                            return result
                else:
                    result = self.backtrack(assignment, current_domain_local)

                    if result != None:
                        return result

            #If the execution comes here, it means we failed somewhere, we need to restore
            #undo assignment
            if var in assignment:
                del assignment[var]
            #restore domain
            current_domain_local = deepcopy(current_domains)
        #print(assignment)
        return None

class InputWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"AI Game")
        window = QWidget()

        self.normal_button = QPushButton()
        self.normal_button.setFixedSize(QSize(200, 100))
        self.normal_button.setText("Yes")
        self.normal_button.pressed.connect(partial(self.open_game, 1))

        self.ab_button = QPushButton()
        self.ab_button.setFixedSize(QSize(200, 100))
        self.ab_button.setText("No")
        self.ab_button.pressed.connect(partial(self.open_game, 0))
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.label.setText("Do you want to use default inputs?")
        font = self.label.font()
        font.setPointSize(20)
        font.setWeight(65)
        self.label.setFont(font)

        layout =QHBoxLayout()
        layout.addWidget(self.normal_button)
        layout.addWidget(self.ab_button)

        vert_layout = QVBoxLayout()
        vert_layout.addWidget(self.label)
        vert_layout.addLayout(layout)

        window.setLayout(vert_layout)
        self.setCentralWidget(window)
        self.resize(600, 600)
        self.center()
        self.show()

    def open_game(self, val):

        global is_default_input
        is_default_input = val
        if is_default_input:
            self.win = PrintWidget()
        else:
            self.win = AskWidget()
        self.win.show()
        self.close()

    def center(self):

        qr = self.frameGeometry()
        cp  = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class AskWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Inputs")
        window = QWidget()

        self.normal_button = QPushButton()
        #self.normal_button.setFixedSize(QSize(200, 100))
        self.normal_button.setText("Start Taking Input")
        self.normal_button.pressed.connect(partial(self.open_game, 1))



        self.label1 = QLabel()
        #self.label1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        font = self.label1.font()
        font.setPointSize(20)
        font.setWeight(65)
        self.label1.setFont(font)
        self.label1.setText("INPUT: \n")

        self.add1 = QLineEdit()
        self.add2 = QLineEdit()
        self.add3 = QLineEdit()
        fbox = QFormLayout()
        fbox.addRow(QLabel("Number of groups"), self.add1)
        fbox.addRow(QLabel("Number of Laureates"), self.add2)
        fbox.addRow(QLabel("Largest value of Time Slot"), self.add3)
        fbox.addRow(self.normal_button)

        #layout =QHBoxLayout()
        #layout.addWidget(self.normal_button)
        #layout.addWidget(self.ab_button)

        vert_layout = QVBoxLayout()
        #vert_layout.addWidget(self.label1)
        vert_layout.addLayout(fbox)
        #vert_layout.addLayout(layout)

        window.setLayout(vert_layout)
        self.setCentralWidget(window)
        #self.resize(400, 400)
        self.center()
    #self.get_num_groups()
        #self.get_num_novels()
        #self.showMaximized()
        self.show()

    def createWidgets(self):
        self.formGroupBox = QGroupBox("Inputs")
        layout = QFormLayout()
        layout.addRow(QLabel("number groups"), QLineEdit())
        layout.addRow(QLabel("number Laureates"), QLineEdit())
        self.formGroupBox.setLayout(layout)

    def get_num_novels(self):
        global num_novels
        num_novels, ok_pressed = QInputDialog.getInt(self, "Get Laureates", "Number of Laureates:", 1, 1, 15, 1)
        if not ok_pressed:
            sys.exit()

    def get_num_groups(self):
        global num_groups
        num_groups, ok_pressed = QInputDialog.getInt(self, "Get Groups", "Number of Groups:", 1, 1, 25, 1)
        if not ok_pressed:
            sys.exit()

    def open_game(self, val):
        global num_groups
        global num_novels
        global limit

        num_groups = int(self.add1.text())
        num_novels = int(self.add2.text())
        limit = int(self.add3.text())
        #print(num_groups, num_laureates)
        self.win = FormWidget1()
        self.win.show()
        self.close()

    def center(self):

        qr = self.frameGeometry()
        cp  = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



class FormWidget1(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"INPUT")
        window = QWidget()

        self.normal_button = QPushButton()
        #self.normal_button.setFixedSize(QSize(200, 100))
        self.normal_button.setText("Take further input")
        self.normal_button.pressed.connect(partial(self.open_game, 1))



        global num_groups
        global num_novels
        self.group_var_list = []


        fbox = QFormLayout()

        for i in range(num_groups):
            take_group_box = QHBoxLayout()
            for j in range(num_novels):
                q1 = QCheckBox("N" + str(j + 1))
                #q1.toggle()
                q1.stateChanged.connect(partial(self.fillDomain, i, j))
                take_group_box.addWidget(q1)

            take_group_box.addStretch()
            fbox.addRow(QLabel("G" + str(i + 1)), take_group_box)

        fbox.addRow(self.normal_button)

        #layout =QHBoxLayout()
        #layout.addWidget(self.normal_button)
        #layout.addWidget(self.ab_button)

        vert_layout = QVBoxLayout()
        #vert_layout.addWidget(self.label1)
        vert_layout.addLayout(fbox)
        #vert_layout.addLayout(layout)

        window.setLayout(vert_layout)
        self.setCentralWidget(window)
        #self.resize(400, 400)
        self.center()
    #self.get_num_groups()
        #self.get_num_novels()
        #self.showMaximized()
        self.show()



    def open_game(self, val):

        global input_groups
        print(input_groups)
        self.win = FormWidget2()
        self.win.show()
        self.close()

    def fillDomain(self, i, j):
        global input_groups

        if i + 1 in input_groups:
            if j + 1 not in input_groups[i + 1]:
                input_groups[i + 1].append(j + 1)
            else:
                input_groups[i+1].remove(j+1)
        else:
            input_groups[i + 1] = [j + 1]


    def center(self):

        qr = self.frameGeometry()
        cp  = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class FormWidget2(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"INPUT")
        window = QWidget()

        self.normal_button = QPushButton()
        #self.normal_button.setFixedSize(QSize(200, 100))
        self.normal_button.setText("Display my inputs")
        self.normal_button.pressed.connect(partial(self.open_game, 1))

        global num_groups
        global num_novels
        global limit

        fbox = QFormLayout()

        for i in range(num_novels):
            take_group_box = QHBoxLayout()
            for j in range(limit):
                q1 = QCheckBox(str(j + 1))
                #q1.toggle()
                q1.stateChanged.connect(partial(self.fillDomain, i, j))
                take_group_box.addWidget(q1)

            take_group_box.addStretch()
            fbox.addRow(QLabel("N" + str(i + 1)), take_group_box)

        fbox.addRow(self.normal_button)

        #layout =QHBoxLayout()
        #layout.addWidget(self.normal_button)
        #layout.addWidget(self.ab_button)

        vert_layout = QVBoxLayout()
        #vert_layout.addWidget(self.label1)
        vert_layout.addLayout(fbox)
        #vert_layout.addLayout(layout)

        window.setLayout(vert_layout)
        self.setCentralWidget(window)
        #self.resize(400, 400)
        self.center()
    #self.get_num_groups()
        #self.get_num_novels()
        #self.showMaximized()
        self.show()



    def open_game(self, val):

        global input_domains
        print(input_domains)
        self.win = PrintWidget1()
        self.win.show()
        self.close()

    def fillDomain(self, i, j):
        global input_domains

        if i + 1 in input_domains:
            if j + 1 not in input_domains[i + 1]:
                input_domains[i + 1].append(j + 1)
            else:
                input_domains[i + 1].remove(j + 1)
        else:
            input_domains[i + 1] = [j + 1]


    def center(self):

        qr = self.frameGeometry()
        cp  = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class PrintWidget1(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"AI Game")
        window = QWidget()

        self.normal_button = QPushButton()
        self.normal_button.setFixedSize(QSize(200, 100))
        self.normal_button.setText("Start Scheduling")
        self.normal_button.pressed.connect(partial(self.open_game, 1))

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        font = self.label.font()
        font.setPointSize(20)
        font.setWeight(65)
        self.label.setFont(font)
        self.label.setText("The values\n\n")

        self.label1 = QLabel()
        #self.label1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        font = self.label1.font()
        font.setPointSize(20)
        font.setWeight(65)
        self.label1.setFont(font)
        self.label1.setText("Groups: \n")

        self.label2 = QLabel()
        #self.label2.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        font = self.label2.font()
        font.setPointSize(10)
        self.label2.setFont(font)
        self.label2.setText(" 'G1': [3, 5, 8, 9, 12, 18, 19] \n \
'G2': [8, 9, 12, 19, 2], \n \
'G3': [3, 5, 4, 16, 8, 9, 19], \n \
'G4': [8, 9, 12, 15], \n \
'G5': [15, 16, 17, 18, 19, 20], \n \
'G6': [3, 5, 7, 11, 14, 20], \n \
'G7': [3, 5, 12, 2, 18, 19, 20, 1], \n \
'G8': [3, 5, 8, 9, 10, 18, 19, 20], \n \
'G9': [3, 13, 8, 9, 7, 19, 20], \n \
'G10': [1, 8, 9, 13, 20], \n \
'G11': [18, 19, 20],\n \
'G12': [3, 11, 8, 18, 19, 20], \n \
'G13': [3, 8, 10, 12, 4, 20], \n \
'G14': [3, 5, 11, 9, 10, 17, 19, 20], \n \
'G15': [2, 8, 12, 18, 19, 20] \n\n")

        self.label3 = QLabel()
        #self.label3.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        font = self.label3.font()
        font.setPointSize(20)
        font.setWeight(65)
        self.label3.setFont(font)
        self.label3.setText("Domains: \n")

        self.label4 = QLabel()
        #self.label4.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        font = self.label4.font()
        font.setPointSize(10)
        self.label4.setFont(font)


        self.label4.setText(" N1: [2, 5, 7],  \n \
N2: [1, 4, 6, 2], \n \
N3: [2, 5, 6, 1], \n \
N4: [2, 4, 6, 8], \n \
N5: [2, 6, 5], \n \
N6: [1, 5, 3], \n \
N7: [2, 4, 6, 1, 8], \n \
N8: [1, 3, 4], \n \
N9: [4, 1, 5, 8, 6], \n \
N10: [8], \n \
N11: [2, 3], \n \
N12: [1, 2, 3, 4, 7], \n \
N13: [7, 1, 8], \n \
N14: [5, 3, 6, 1], \n \
N15: [2, 5], \n \
N16: [2, 5, 1, 4], \n \
N17: [1, 4, 5, 6], \n \
N18: [5, 4], \n \
N19: [1, 3, 6, 8], \n N20: [6]")


        layout =QHBoxLayout()
        layout.addWidget(self.normal_button)
        #layout.addWidget(self.ab_button)

        vert_layout = QVBoxLayout()
        vert_layout.addWidget(self.label)
        vert_layout.addWidget(self.label1)
        vert_layout.addWidget(self.label2)
        vert_layout.addWidget(self.label3)
        vert_layout.addWidget(self.label4)
        vert_layout.addLayout(layout)

        window.setLayout(vert_layout)
        self.setCentralWidget(window)
        #self.resize(600, 600)
        #self.center()
        self.showMaximized()
        self.show()

    def open_game(self, val):

        self.win = FirstWidget()
        self.win.show()
        self.close()

    def center(self):

        qr = self.frameGeometry()
        cp  = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class PrintWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"AI Game")
        window = QWidget()

        self.normal_button = QPushButton()
        self.normal_button.setFixedSize(QSize(200, 100))
        self.normal_button.setText("Start Scheduling")
        self.normal_button.pressed.connect(partial(self.open_game, 1))

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        font = self.label.font()
        font.setPointSize(20)
        font.setWeight(65)
        self.label.setFont(font)
        self.label.setText("The values\n\n")

        self.label1 = QLabel()
        #self.label1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        font = self.label1.font()
        font.setPointSize(20)
        font.setWeight(65)
        self.label1.setFont(font)
        self.label1.setText("Groups: \n")

        self.label2 = QLabel()
        #self.label2.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        font = self.label2.font()
        font.setPointSize(10)
        self.label2.setFont(font)
        self.label2.setText(" 'G1': [3, 5, 8, 9, 12, 18, 19] \n \
'G2': [8, 9, 12, 19, 2], \n \
'G3': [3, 5, 4, 16, 8, 9, 19], \n \
'G4': [8, 9, 12, 15], \n \
'G5': [15, 16, 17, 18, 19, 20], \n \
'G6': [3, 5, 7, 11, 14, 20], \n \
'G7': [3, 5, 12, 2, 18, 19, 20, 1], \n \
'G8': [3, 5, 8, 9, 10, 18, 19, 20], \n \
'G9': [3, 13, 8, 9, 7, 19, 20], \n \
'G10': [1, 8, 9, 13, 20], \n \
'G11': [18, 19, 20],\n \
'G12': [3, 11, 8, 18, 19, 20], \n \
'G13': [3, 8, 10, 12, 4, 20], \n \
'G14': [3, 5, 11, 9, 10, 17, 19, 20], \n \
'G15': [2, 8, 12, 18, 19, 20] \n\n")

        self.label3 = QLabel()
        #self.label3.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        font = self.label3.font()
        font.setPointSize(20)
        font.setWeight(65)
        self.label3.setFont(font)
        self.label3.setText("Domains: \n")

        self.label4 = QLabel()
        #self.label4.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        font = self.label4.font()
        font.setPointSize(10)
        self.label4.setFont(font)


        self.label4.setText(" N1: [2, 5, 7],  \n \
N2: [1, 4, 6, 2], \n \
N3: [2, 5, 6, 1], \n \
N4: [2, 4, 6, 8], \n \
N5: [2, 6, 5], \n \
N6: [1, 5, 3], \n \
N7: [2, 4, 6, 1, 8], \n \
N8: [1, 3, 4], \n \
N9: [4, 1, 5, 8, 6], \n \
N10: [8], \n \
N11: [2, 3], \n \
N12: [1, 2, 3, 4, 7], \n \
N13: [7, 1, 8], \n \
N14: [5, 3, 6, 1], \n \
N15: [2, 5], \n \
N16: [2, 5, 1, 4], \n \
N17: [1, 4, 5, 6], \n \
N18: [5, 4], \n \
N19: [1, 3, 6, 8], \n N20: [6]")


        layout =QHBoxLayout()
        layout.addWidget(self.normal_button)
        #layout.addWidget(self.ab_button)

        vert_layout = QVBoxLayout()
        vert_layout.addWidget(self.label)
        vert_layout.addWidget(self.label1)
        vert_layout.addWidget(self.label2)
        vert_layout.addWidget(self.label3)
        vert_layout.addWidget(self.label4)
        vert_layout.addLayout(layout)

        window.setLayout(vert_layout)
        self.setCentralWidget(window)
        #self.resize(600, 600)
        #self.center()
        self.showMaximized()
        self.show()

    def open_game(self, val):

        self.win = FirstWidget()
        self.win.show()
        self.close()

    def center(self):

        qr = self.frameGeometry()
        cp  = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class FirstWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"AI Game")
        window = QWidget()

        self.normal_button = QPushButton()
        self.normal_button.setFixedSize(QSize(200, 100))
        self.normal_button.setText("With Constraint_Prop")
        self.normal_button.pressed.connect(partial(self.open_game, 1))

        self.ab_button = QPushButton()
        self.ab_button.setFixedSize(QSize(200, 100))
        self.ab_button.setText("Without Constraint_Prop")
        self.ab_button.pressed.connect(partial(self.open_game, 0))
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.label.setText("Choose Algorithm")
        font = self.label.font()
        font.setPointSize(20)
        font.setWeight(65)
        self.label.setFont(font)

        layout =QHBoxLayout()
        layout.addWidget(self.normal_button)
        layout.addWidget(self.ab_button)

        vert_layout = QVBoxLayout()
        vert_layout.addWidget(self.label)
        vert_layout.addLayout(layout)

        window.setLayout(vert_layout)
        self.setCentralWidget(window)
        self.resize(600, 600)
        self.center()
        self.show()

    def open_game(self, val):

        global is_with_constraint_prop
        is_with_constraint_prop = val
        self.win = SecondWidget()
        self.win.show()
        self.close()

    def center(self):

        qr = self.frameGeometry()
        cp  = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class SecondWidget(QMainWindow):

    def __init__(self):
        super().__init__()


        self.setWindowTitle(f"AI Game")
        window = QWidget()




        self.normal_button = QPushButton()
        self.normal_button.setFixedSize(QSize(100, 100))
        self.normal_button.setText("Degree")
        self.normal_button.pressed.connect(partial(self.open_game, 0))

        self.ab_button = QPushButton()
        self.ab_button.setFixedSize(QSize(100, 100))
        self.ab_button.setText("MRV")
        self.ab_button.pressed.connect(partial(self.open_game, 1))
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.label.setText("Choose Heurestic")
        font = self.label.font()
        font.setPointSize(20)
        font.setWeight(65)
        self.label.setFont(font)

        layout =QHBoxLayout()
        layout.addWidget(self.normal_button)
        layout.addWidget(self.ab_button)

        vert_layout = QVBoxLayout()
        vert_layout.addWidget(self.label)
        vert_layout.addLayout(layout)

        window.setLayout(vert_layout)

        self.setCentralWidget(window)
        self.resize(600, 600)
        self.center()
        self.show()

    def open_game(self, val):

        global is_MRV
        is_MRV = val
        self.win = MainWidget()
        self.win.show()
        self.close()

    def center(self):

        qr = self.frameGeometry()
        cp  = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())




app = QApplication(sys.argv)
ex = InputWidget()
sys.exit(app.exec_())
