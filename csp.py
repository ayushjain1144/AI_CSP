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
#######################################

# Predefined CSP Problem
number_nodes = 0
default_m = 20
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
is_with_constraint_prop = 0
is_MRV = 0
is_Degree = 1

class CSP():

    def __init__(self, variables, domains, neighbors, constraints):

        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        self.current_domains = None
        self.number_assigned = 0

    def assign(self, var, val, assignment):
        """Assign variable to value"""

        assignment[var]  = val
        self.number_assigned += 1

    def unassign(self, var, val, assignment):
        """Deletes val from var"""

        if var in assignment:
            del assignment[var]

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

        assignment = self.backtrack_search()

        if assignment == None:
            print("No assignment possible")
        else:
            print(assignment)
        #print(self.mrv({10: 1, 20 : 2}))
        #print(self.ordered_variable_list)

        #self.show()

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
        """If B is a neighbour of A and a = b, then they are involved in constraint"""
        """a and b should be in respective domains"""

        try:
            assert(a in default_domains[A])
            assert(b in default_domains[B])
        except Exception:
            print("Values out of domains")
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

    def backtrack_search(self):
        """Implements backtrack search, returns assignment or None"""
        return self.backtrack({})

    def mrv(self, assignment):
        """Returns the variable with minimum valid moves"""

        min = float('Inf')
        min_var = None
        for var in self.adjacency_dict:
            if var not in assignment:
                if len(self.current_domains[var]) < min:
                    min = len(self.current_domains[var])
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


    def order_variable_list(self, assignment):
        """Returns the next variable to be chosen"""

        if is_MRV:
            return self.mrv(assignment)
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



    def backtrack(self, assignment):
        if self.is_complete_assignmnet(assignment):
            return assignment


        number_assigned = len(assignment)

        var = self.order_variable_list(assignment)

        #print(f"{var} returned by order_variable_list")
        if var is None:
            return None

        for value in self.current_domains[var]:

            global number_nodes
            number_nodes += 1
            if number_nodes % 100 == 0:
                print(assignment, number_nodes)
            #print(value)
            if self.is_consistent(assignment, var, value):
                #print("Returned True")
                assignment[var] = value

            #if is_with_constraint_prop == 1:
                #inference = self.ac3()
                #if inference
                result = self.backtrack(assignment)
                if result != None:
                    return result
            if var in assignment:
                del assignment[var]
        #print(assignment)
        return None



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
ex = MainWidget()
sys.exit(app.exec_())
