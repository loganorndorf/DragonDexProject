import sys
import os
import re
import psycopg2

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# image path
PATH = "C:\\Users\\SirRunnerMan\\Desktop\\PythonProjects\\resources"

class DragonDex(QMainWindow):
    def __init__(self,windowSize):
        super().__init__()
        self.title  = 'DragonDex'
        self.windowSize = windowSize
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)

        self.setWindowIcon(QIcon('lorus_fire_03.png'))
        self.setFixedSize(self.windowSize)

        # set my central widget as the grid
        self.main_widget = MainGridWidget(self)
        self.setCentralWidget(self.main_widget)

        self.show()

class MainGridWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        # self.buttons = []
        self.create_grid()

        # Vertical BoxLayout
        vbox = QVBoxLayout()
        vbox.addWidget(self.scroll)
        self.setLayout(vbox)

    def create_grid(self):
        self.scroll = QScrollArea()
        self.groupBox = QGroupBox('Select A Dragon')
        self.gridLayout = QGridLayout()
        self.groupBox.setLayout(self.gridLayout)

        regex = ".*_03\.png"
        self.names = [file for file in os.listdir(PATH) if re.match(regex, file)]
        self.images = [os.path.join(PATH, file) for file in os.listdir(PATH) if re.match(regex, file)]

        hSize = int((len(self.images) / 13) * 80)
        wSize = int(13 * 80)

        self.groupBox.setMinimumSize(QSize(wSize, hSize))
        self.scroll.setWidget(self.groupBox)

        for i in range(len(self.images)):
            x = int(i / 13)
            y = int(i % 13)

            self.btn = QPushButton(QIcon(self.images[i]), "", self)
            self.btn.setIconSize(QSize(80, 80))
            self.btn.setMinimumSize(QSize(80, 80))
            self.btn.setMaximumSize(QSize(80, 80))
            self.btn.clicked.connect(self.create_popup)
            self.gridLayout.addWidget(self.btn, x, y)


    def create_popup(self):
        button = self.sender()
        idx = self.gridLayout.indexOf(button)
        name = self.names[idx]
        image = self.images[idx]
        self.poppy = character_popUp(name, image)
        # self.poppy.setGeometry(180,96,720,384)
        self.poppy.show()



class character_popUp(QMainWindow):
    def __init__(self, name, image):
        super().__init__()
        self.name = name
        self.windowSize = QSize(720, 384)
        self.initUI()

    def initUI(self):

        # connect to db - using for window title
        con = psycopg2.connect(
            host="localhost",
            database="DVMdb",
            user="postgres",
            password=""
        )

        cur = con.cursor()
        cur.execute("SELECT c_name, attri, base_star_count, unit_type FROM public.characters WHERE icon_ref LIKE '" + str(self.name) + "';")
        q = cur.fetchone()

        # set window title
        self.setWindowTitle(q[0])

        # regex for image resources
        regex = "(.*)_03\.png"
        m = re.match(regex, self.name)
        self.simple = m.group(1)

        image = PATH + "\\" + str(self.name)
        print(image)
        self.setWindowIcon(QIcon(image))
        self.setFixedSize(self.windowSize)
        # imageName = QLabel(self.name, self)

        self.pu = PopupGrid(self.simple, q[1], q[2], q[3])

        # don't forget to close your db's!!
        con.close()

        # set central widgets
        self.setCentralWidget(self.pu)
        self.show()


class PopupGrid(QWidget):
    def __init__(self, name, attri, baseStar, unitType):
        super().__init__()

        # input recieved from initial PopupGrid call
        self.simple = name
        self.cAttr = attri
        self.baseStar = baseStar
        self.unitType = unitType

        # info to remember
        self.currentStar = baseStar
        self.currentEvol = 0

        self.popup_grid()

        yeup = QVBoxLayout()
        yeup.addWidget(self.G)
        self.setLayout(yeup)

    def popup_grid(self):
        ###  dragon stats box setup  ###
        self.statsBox = QGroupBox("Dragon Stats")
        self.statsGrid = QGridLayout()
        self.statsBox.setLayout(self.statsGrid)

        # image QLabel instantiation
        self.BSImage = QLabel()
        UTImage = QLabel()
        AImage = QLabel()
        RImage = QLabel()

        # different image place holders
        self.role = None
        self.star = None
        self.attr = None
        self.rari = None

        # determine role image to display
        if(self.unitType == 1):
            self.role = PATH + "\\" + "role_dealer.png"
        elif(self.unitType == 2):
            self.role = PATH + "\\" + "role_tanker.png"
        elif(self.unitType == 3):
            self.role = PATH + "\\" + "role_healer.png"
        elif(self.unitType == 4):
            self.role = PATH + "\\" + "role_supporter"

        roleImg = QPixmap(self.role)
        roleImg.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        UTImage.setPixmap(roleImg)
        UTImage.setAlignment(Qt.AlignCenter)

        # determine attribute img to display
        if(self.cAttr == 1):
            self.attr = PATH + "\\" + "card_cha_attr_earth.png"
        elif(self.cAttr == 2):
            self.attr = PATH + "\\" + "card_cha_attr_fire.png"
        elif(self.cAttr == 3):
            self.attr = PATH + "\\" + "card_cha_attr_water.png"
        elif(self.cAttr == 4):
            self.attr = PATH + "\\" + "card_cha_attr_dark.png"
        elif(self.cAttr == 5):
            self.attr = PATH + "\\" + "card_cha_attr_light.png"

        attrImg = QPixmap(self.attr)
        attrImg.scaled(QSize(24, 24), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        AImage.setPixmap(attrImg)
        AImage.setAlignment(Qt.AlignCenter)

        if(self.baseStar == 2):
            self.star = PATH + "\\" + "card_star_yellow_0102.png"
            self.rari = PATH + "\\" + "gem_common.png"
        elif(self.baseStar == 3):
            self.star = PATH + "\\" + "card_star_yellow_0103.png"
            self.rari = PATH + "\\" + "gem_rare.png"
        elif(self.baseStar == 4):
            self.star = PATH + "\\" + "card_star_yellow_0104.png"
            self.rari = PATH + "\\" + "gem_hero.png"
        elif(self.baseStar == 5):
            self.star = PATH + "\\" + "card_star_yellow_0105.png"
            self.rari = PATH + "\\" + "gem_legend.png"

        # star Image
        self.starImg = QPixmap(self.star)
        self.starImg.scaled(QSize(20, 20), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.BSImage.setPixmap(self.starImg)
        self.BSImage.setAlignment(Qt.AlignCenter)
        self.plus = QPushButton(QIcon(PATH+"\\"+"plus.png"), "", self)
        self.plus.setIconSize(QSize(30, 30))
        self.plus.setMaximumSize(QSize(35, 35))
        # self.plus.setStyleSheet("margin: auto")
        self.plus.clicked.connect(self.add)

        self.minus = QPushButton(QIcon(PATH+"\\"+"minus.png"), "", self)
        self.minus.setIconSize(QSize(30, 30))
        self.minus.setMaximumSize(QSize(35, 35))
        # self.minus.setStyleSheet("margin: auto")
        self.minus.clicked.connect(self.subtract)

        # rarity Image
        rarityImg = QPixmap(self.rari)
        rarityImg.scaled(QSize(20, 20), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        RImage.setPixmap(rarityImg)
        RImage.setAlignment(Qt.AlignCenter)

        self.numberBox = QGroupBox("")
        self.numberGrid = QGridLayout()
        self.numberBox.setLayout(self.numberGrid)

        self.statsGrid.addWidget(UTImage, 0, 1)
        self.statsGrid.addWidget(AImage, 0, 0)
        self.statsGrid.addWidget(RImage, 0, 2)
        self.statsGrid.addWidget(self.BSImage, 1, 1)
        self.statsGrid.addWidget(self.minus, 1, 0)
        self.statsGrid.addWidget(self.plus, 1,2)

        self.statsGrid.addWidget(self.numberBox, 2, 0, 2, 3)
        ##############################

        ### dragon skill box setup ###
        self.skillBox = QGroupBox("Dragon Skills")

        self.skillGrid = QGridLayout()
        self.skillBox.setLayout(self.skillGrid)
        ##############################

        ### dragon evolution box setup ###
        self.imageBox = QGroupBox("Dragon Evolutions")
        self.imageGrid = QGridLayout()
        self.imageBox.setLayout(self.imageGrid)

        for i in range(1, 4):
            pictures = PATH + "\\" + self.simple + "_0"+ str(i) + str(".png")
            label = QPushButton(QIcon(pictures), "", self)
            label.setIconSize(QSize(110,110))
            label.clicked.connect(self.evo_selection_action)

            j = i-1
            self.imageGrid.addWidget(label, 0, j)
        ##############################

        # pop up window grid layout
        self.container = QGridLayout()
        self.G = QGroupBox("")
        self.G.setLayout(self.container)

        self.container.addWidget(self.imageBox, 0, 0)
        self.container.addWidget(self.statsBox, 0, 1, 2, 1)
        self.container.addWidget(self.skillBox, 1, 0)

    def evo_selection_action(self):
        parent = self.sender()
        pos = self.imageGrid.indexOf(parent)

        # starting with brute force option for checking what star image to put up
        if(self.currentEvol != 0 and pos == 0):
            self.update = None
            if(self.currentStar == 2):
                self.update = QPixmap(PATH + "\\" + "card_star_yellow_0102.png")
            elif(self.currentStar == 3):
                self.update = QPixmap(PATH + "\\" + "card_star_yellow_0103.png")
            elif(self.currentStar == 4):
                self.update = QPixmap(PATH + "\\" + "card_star_yellow_0104.png")
            elif(self.currentStar == 5):
                self.update = QPixmap(PATH + "\\" + "card_star_yellow_0105.png")
            elif(self.currentStar == 6):
                self.update = QPixmap(PATH + "\\" + "card_star_yellow_0106.png")

            self.update.scaled(QSize(20,20), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.BSImage.setPixmap(self.update)

            self.currentEvol = 0
        elif(self.currentEvol != 1 and pos == 1):
            self.update = None
            if (self.currentStar == 2):
                self.update = QPixmap(PATH + "\\" + "card_star_purple_0102.png")
            elif (self.currentStar == 3):
                self.update = QPixmap(PATH + "\\" + "card_star_purple_0103.png")
            elif (self.currentStar == 4):
                self.update = QPixmap(PATH + "\\" + "card_star_purple_0104.png")
            elif (self.currentStar == 5):
                self.update = QPixmap(PATH + "\\" + "card_star_purple_0105.png")
            elif (self.currentStar == 6):
                self.update = QPixmap(PATH + "\\" + "card_star_purple_0106.png")

            self.update.scaled(QSize(20, 20), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.BSImage.setPixmap(self.update)

            self.currentEvol = 1
        elif(self.currentEvol != 2 and pos == 2):

            if(self.baseStar == self.currentStar):
                self.currentStar += 1

            self.update = None
            if (self.currentStar == 3):
                self.update = QPixmap(PATH + "\\" + "card_star_red_0103.png")
            elif (self.currentStar == 4):
                self.update = QPixmap(PATH + "\\" + "card_star_red_0104.png")
            elif (self.currentStar == 5):
                self.update = QPixmap(PATH + "\\" + "card_star_red_0105.png")
            elif (self.currentStar == 6):
                self.update = QPixmap(PATH + "\\" + "card_star_red_0106.png")

            self.update.scaled(QSize(20, 20), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.BSImage.setPixmap(self.update)
            self.currentEvol = 2

    def subtract(self):
        self.word = None
        if(self.currentEvol == 2):
            # make sure by decreasing the star you are still above the
            temp = self.baseStar + 1
            if(self.currentStar - 1 >= temp):
                self.currentStar -= 1

            self.word = "red"
        elif(self.currentEvol == 1):
            if(self.currentStar - 1 >= self.baseStar):
                self.currentStar -= 1
            self.word = "purple"

        elif(self.currentEvol == 0):
            if(self.currentStar - 1 >= self.baseStar):
                self.currentStar -= 1
            self.word = "yellow"


        self.newGuy = None
        if (self.currentStar == 2):
            self.newGuy = QPixmap(PATH + "\\" + "card_star_"+self.word+"_0102.png")
        if (self.currentStar == 3):
            self.newGuy = QPixmap(PATH + "\\" + "card_star_"+self.word+"_0103.png")
        elif (self.currentStar == 4):
            self.newGuy = QPixmap(PATH + "\\" + "card_star_"+self.word+"_0104.png")
        elif (self.currentStar == 5):
            self.newGuy = QPixmap(PATH + "\\" + "card_star_"+self.word+"_0105.png")
        elif (self.currentStar == 6):
            self.newGuy = QPixmap(PATH + "\\" + "card_star_"+self.word+"_0106.png")

        self.newGuy.scaled(QSize(20, 20), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.BSImage.setPixmap(self.newGuy)

    def add(self):
        self.word = None
        temp = 6
        if (self.currentEvol == 2):
            # make sure by decreasing the star you are still above the
            temp = 6
            if (self.currentStar + 1 <= temp):
                self.currentStar += 1

            self.word = "red"
        elif (self.currentEvol == 1):
            if (self.currentStar + 1 <= temp):
                self.currentStar += 1
            self.word = "purple"

        elif (self.currentEvol == 0):
            if (self.currentStar + 1 <= temp):
                self.currentStar += 1
            self.word = "yellow"

        self.newGuy = None
        if (self.currentStar == 3):
            self.newGuy = QPixmap(PATH + "\\" + "card_star_" + self.word + "_0103.png")
        elif (self.currentStar == 4):
            self.newGuy = QPixmap(PATH + "\\" + "card_star_" + self.word + "_0104.png")
        elif (self.currentStar == 5):
            self.newGuy = QPixmap(PATH + "\\" + "card_star_" + self.word + "_0105.png")
        elif (self.currentStar == 6):
            self.newGuy = QPixmap(PATH + "\\" + "card_star_" + self.word + "_0106.png")

        self.newGuy.scaled(QSize(20, 20), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.BSImage.setPixmap(self.newGuy)
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screenSize = app.desktop().availableGeometry().size()/1.265
    ex = DragonDex(screenSize)
    sys.exit(app.exec_())


# cName; char[]
# iconRef; char[]
# baseStarCount; int
# attribute; int -> 1: Earth, 2: Fire, 3: Water, 4: Dark, 5: Light
# unitType; int -> 1: Attack, 2: Defense, 3: Recovery, 4: Support
