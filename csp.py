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

#######################################

# Predefined CSP Problem

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
                'G12': [13, 11, 8, 18, 19, 20],
                'G13': [3, 8, 10, 12, 4, 20],
                'G14': [3, 5, 11, 9, 10, 17, 19, 20],
                'G15': [2, 8, 12, 18, 19, 20]}

default_domains = {'N1': [2, 5, 7],
           'N2': [1, 4, 6, 2],
           'N3': [2, 5, 6, 1],
           'N4': [2, 4, 6, 8],
           'N5': [2, 6, 5],
           'N6': [1, 5, 3],
           'N7': [2, 4, 6, 1, 8],
           'N8': [1, 3, 4],
           'N9': [4, 1, 5, 8, 6],
           'N10': [8],
           'N11': [2, 3],
           'N12': [1, 2, 3, 4, 7],
           'N13': [7, 1, 8],
           'N14': [5, 3, 6, 1],
           'N15': [2, 5],
           'N16': [2, 5, 1, 4],
           'N17': [1, 4, 5, 6],
           'N18': [5, 4],
           'N19': [1, 3, 6, 8],
           'N20': [6]}




#########################################
is_with_constraint_prop = 0
is_MRV = 0

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

        self.build_neighbours()

        self.show()

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
        print(adjacency_dict)





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
