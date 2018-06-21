# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QLabel,QGroupBox, QVBoxLayout,QHBoxLayout, QLineEdit,QTableWidget,QComboBox,QTableWidgetItem
import sys

UserDefineReactantList = ['Himic2095','Stearic']
UserDefineReactantParam = ['    h,kj/mol=-1315.2 C 44 H 90' ,'    h,kj/mol=-948.3 C 18 H 36 O 2']

class Reactant(object):
  def __init__(self,ident, name, amount, temp):
    self.ident = ident
    self.name = name
    self.amount = amount
    self.temp = temp

class View(QWidget): 
  def __init__(self, model):
    super().__init__()

    self.model = model

  def register(self,controller):
    self.controller = controller
    self.initUI() 
  
  def initUI(self):
    self.setGeometry(200,200,500,400)

    rocketGroupBox = QGroupBox('Rocket Problem')
    rocketVBox = QVBoxLayout()
    
    initPresHBox = QHBoxLayout()
    initPresLabel = QLabel('Initial Pres[bar]')
    self.initPresTextBox = QLineEdit()
    initPresHBox.addWidget(initPresLabel)
    initPresHBox.addWidget(self.initPresTextBox)

    ofRatiosHBox = QHBoxLayout()
    ofRatiosLabel = QLabel('O/F')
    self.ofRatiosTextBox = QLineEdit()
    ofRatiosHBox.addWidget(ofRatiosLabel)
    ofRatiosHBox.addWidget(self.ofRatiosTextBox)
    identValues = ['','fuel','oxid']
    nameValues = ['','N2O','Himic2095','Stearic']
    self.reactTable = QTableWidget()
    self.reactTable.setColumnCount(4)
    self.reactTable.setRowCount(4)
    self.reactTable.setHorizontalHeaderLabels(["Ident","Name","Amount","Temp"])
    for i in range(4):
      identCombo = QComboBox()
      nameCombo = QComboBox()
      
      for j in range(3):
        identCombo.addItem(identValues[j])
      for j in range(4):
        nameCombo.addItem(nameValues[j])
      self.reactTable.setCellWidget(i,0,identCombo)
      self.reactTable.setCellWidget(i,1,nameCombo)

    calculationButton = QPushButton('Calculation', self)
    calculationButton.clicked.connect(self.calculationButtonClicked)
    
    showButton = QPushButton('show', self)
    showButton.clicked.connect(self.controller.showList)

    rocketVBox.addLayout(ofRatiosHBox)
    rocketVBox.addLayout(initPresHBox)
    rocketVBox.addWidget(self.reactTable)
    rocketVBox.addWidget(calculationButton)
    rocketVBox.addWidget(showButton)

    rocketGroupBox.setLayout(rocketVBox) 
		
    VBox = QVBoxLayout()
    VBox.addWidget(rocketGroupBox)

    self.setLayout(VBox)

  def updateUI(self):
    #self.label.setText(model.word)
    pass

  def calculationButtonClicked(self):
    indexReactIdent = 0
    indexReactName = 1
    indexReactAmount = 2
    indexReactTemp = 3
  
    reactants = []    
    
    ofRatios = self.ofRatiosTextBox.text() 
    initPres = self.initPresTextBox.text()

    for column in range(0,self.reactTable.columnCount()):
      print(column)
      reactIdent = self.reactTable.cellWidget(column,indexReactIdent).currentText()
      reactName = self.reactTable.cellWidget(column,indexReactName).currentText()
      if(reactIdent == ''): continue
      reactAmount = self.reactTable.item(column,indexReactAmount).text()
      reactTemp = self.reactTable.item(column,indexReactTemp).text()

      reactants.append(Reactant(reactIdent,reactName,reactAmount,reactTemp))

    self.controller.calculation(ofRatios,initPres,reactants)


class Model(object):
  def __init__(self):
    self._ofRatios = []
    self._initPres = 0
    self._reactants = []
 
  def setParam(self,ofRatios, initPres, reactants):
    self._ofRatios = ofRatios.split(',') 
    self._initPres = initPres
    self._reactants = reactants

  def generateInp(self):
    inpFileName = 'sample'#input('Input File Name: ')
    inpFileName += '.inp'
    inpFile = open(inpFileName,'w')

    string = 'problem	o/f='
    for value in self._ofRatios:
      string += value+','
    string += '\n    rocket  frozen  nfz=2\n'
    string += '  p,bar=' + self._initPres + ',\nreact\n'
    for reactant in self._reactants:
      string += "  " + reactant.ident + "=" + reactant.name + " wt=" + reactant.amount + " t,k=" + reactant.temp + "\n" 
      string = self.checkUserDefineReactant(string,reactant)
    string += "end"
    inpFile.write(string)
    inpFile.close()

  def checkUserDefineReactant(self,string,reactant):
    print(UserDefineReactantList[0])
    print(reactant.name)
    print(reactant.name in UserDefineReactantList)
    if(reactant.name in UserDefineReactantList):
      string += UserDefineReactantParam[UserDefineReactantList.index(reactant.name)] + "\n"
    return string
    

  def showList(self):
    for data in self._reactants:
      print("-------------------------------")
      print("initPres: " + self._initPres)
      print("Ident: "+data.ident+", name: "+data.name+", Amount: "+str(data.amount)+", Temp: "+str(data.temp))


class Controller(object):
  def __init__(self, view, model):
    self.view = view
    self.model = model

    self.view.register(self)
  
  def calculation(self, ofRatios, initPres, reactants):
    self.model.setParam(ofRatios, initPres, reactants)
    self.model.generateInp()
    self.view.updateUI()

  def showList(self):
    self.model.showList() 


if __name__ == '__main__':
  app = QApplication(sys.argv)

  model = Model()
  view = View(model)
  controller = Controller(view,model)

  view.show()
  sys.exit(app.exec_())

