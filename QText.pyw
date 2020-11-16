import os, sys, webbrowser
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
        
class QMain(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.settingFile = os.path.split(sys.argv[0])[0] + '\\SettingFile.txt'
        self.defaultContentOfSettingFile = \
            'button,Unset,Unset\n'+ \
            'button,Unset,Unset\n'+ \
            'button,Unset,Unset\n'+ \
            'button,Unset,Unset\n'+ \
            'button,Unset,Unset\n'+ \
            'screenLower,0.1,0.1,0.85,0.8\n'+ \
            'screenUpper,0,45,1,0.917\n'+ \
            'screenToTopHalf,0,45,1,0.865\n'+ \
            'screenToBottomHalf,0,555,1,0.865\n'+ \
           r'iconPath,D:\Desktop\Project\QText\QText.ico'+'\n'
                                    
        self.setWindowTitle('QText')
        self.numOfQButton = 6
        self.QButtonList = None
        self.QLineList = None
        self.QTextList = None
        self.highlight = None
        self.showAllQButton = True
        self.isFullScreen = False
        self.layout = None
        self.screenSize = QApplication.desktop().screenGeometry()
        self.screenUpperHalf = [0, 45, 1, 0.865]
        self.screenLowerHalf = [0, 555, 1, 0.865]
        self.screenLower = [0.1, 0.1, 0.85, 0.8]
        self.screenUpper = [0, 45, 1, 0.917]
        self.eachLineInSettingFile = []
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.getEachLineInSettingFile()
        self.setScreenSize()
        self.setIcon()
        self.show()
        
    def createQButtons(self):
        self.QButtonList = [QButton(self,i) for i in range(self.numOfQButton)]
        
    def createQLines(self):
        self.QLineList = [QLine(self,i) for i in range(self.numOfQButton)]
        
    def createQTexts(self):
        self.QTextList = [QText(self,i) for i in range(self.numOfQButton)]
        
    def createQHighlighterToAllQText(self):
        self.highlight = [QHighlighter(QText.document()) for QText in self.QTextList]
        
    def setLayoutOfUI(self):
        self.layout = QGridLayout()
        self.layout.setColumnStretch(0,1)
        [self.layout.addWidget(btn,0,i+1) for i,btn in enumerate(self.QButtonList)]
        [self.layout.setColumnStretch(i,10) for i in range(1, self.numOfQButton+1)]
        [self.layout.addWidget(self.QLineList[i],1,0,1,1) for i in range(self.numOfQButton)]
        [self.layout.addWidget(self.QTextList[i],1,1,1,6) for i in range(self.numOfQButton)]
        [btn.hide() for btn in self.QButtonList]
        self.setLayout(self.layout)
        
    def setScreenSize(self):
        # get latest arguments from settingFile
        self.getEachLineInSettingFile()
        
        # try to update arguments from settingFile
        for line in self.eachLineInSettingFile:
            if line.startswith('screenLower'):
                s = line.split(',')[1:]
                for i in range(4):
                    self.screenLower[i] = float(s[i])
            elif line.startswith('screenUpper'):
                s = line.split(',')[1:]
                for i in range(4):
                    self.screenUpper[i] = float(s[i])
        
        if self.isFullScreen:
            X = int(self.screenUpper[0])
            Y = int(self.screenUpper[1])
            W = int(self.screenUpper[2] * self.screenSize.width())
            H = int(self.screenUpper[3] * self.screenSize.height())
            self.setGeometry(X, Y, W, H)
        else:
            X = int(self.screenLower[0] * self.screenSize.width())
            Y = int(self.screenLower[1] * self.screenSize.height())
            W = int(self.screenLower[2] * self.screenSize.width())
            H = int(self.screenLower[3] * self.screenSize.height())
            self.setGeometry(X, Y, W, H)
            
        self.isFullScreen = not self.isFullScreen
        
    def setScreenToUpperHalf(self):
        # get latest arguments from settingFile
        self.getEachLineInSettingFile()
        
        # try to update arguments from settingFile
        for line in self.eachLineInSettingFile:
            if line.startswith('screenToTopHalf'):
                s = line.split(',')[1:]
                for i in range(4):
                    self.screenUpperHalf[i] = float(s[i])
        
        X = int(self.screenUpperHalf[0])
        Y = int(self.screenUpperHalf[1])
        W = int(self.screenUpperHalf[2] * self.screenSize.width())
        H = int(self.screenUpperHalf[3] * self.screenSize.height()) >> 1
        self.setGeometry(X, Y, W, H)
        
    def setScreenToLowerHalf(self):
        # get latest arguments from settingFile
        self.getEachLineInSettingFile()
        
        # try to update arguments from settingFile
        for line in self.eachLineInSettingFile:
            if line.startswith('screenToBottomHalf'):
                s = line.split(',')[1:]
                for i in range(4):
                    self.screenLowerHalf[i] = float(s[i])
        
        X = int(self.screenLowerHalf[0])
        Y = int(self.screenLowerHalf[1])
        W = int(self.screenLowerHalf[2] * self.screenSize.width())
        H = int(self.screenLowerHalf[3] * self.screenSize.height()) >> 1
        self.setGeometry(X, Y, W, H)
        
    def setScreenToRightHalf(self):
        # get latest arguments from settingFile
        self.getEachLineInSettingFile()
        
        # try to update arguments from settingFile
        for line in self.eachLineInSettingFile:
            if line.startswith('screenUpper'):
                s = line.split(',')[1:]
                for i in range(4):
                    self.screenUpper[i] = float(s[i])
        
        X = int(self.screenUpper[0]) + (self.screenSize.width() >> 1)
        Y = int(self.screenUpper[1])
        W = int(self.screenUpper[2] * self.screenSize.width()) >> 1
        H = int(self.screenUpper[3] * self.screenSize.height()) 
        self.setGeometry(X, Y, W, H)
    
    def setScreenToLeftHalf(self):
        # get latest arguments from settingFile
        self.getEachLineInSettingFile()
        
        # try to update arguments from settingFile
        for line in self.eachLineInSettingFile:
            if line.startswith('screenUpper'):
                s = line.split(',')[1:]
                for i in range(4):
                    self.screenUpper[i] = float(s[i])
        
        X = int(self.screenUpper[0])
        Y = int(self.screenUpper[1])
        W = int(self.screenUpper[2] * self.screenSize.width()) >> 1
        H = int(self.screenUpper[3] * self.screenSize.height()) 
        self.setGeometry(X, Y, W, H)
        
    def setIcon(self):
        # default iconPath
        iconPath = r'D:\Desktop\Project\QText\QText.ico'   
        
        # try to update arguments from settingFile
        for line in self.eachLineInSettingFile:
            if line.startswith('iconPath'):
                iconPath = line.split(',')[1]
                
        # set icon
        self.setWindowIcon(QIcon(iconPath))
        
    def setNameAndPathToAllQButton(self):
        # set QButton of the index = 0
        firstQTextFilePath = self.QTextList[0].getFilePath()
        self.QButtonList[0].setPath(firstQTextFilePath if firstQTextFilePath else 'QText')
            
        # get latest arguments from settingFile
        self.getEachLineInSettingFile()
        
        # set QButton from index = 1
        index = 1
        for line in self.eachLineInSettingFile:
            if line.startswith('button'):
                btnSettingData = line.split(',')
                # set filePath and name to each button if path is valid
                if os.path.isfile(btnSettingData[2]):
                    self.QButtonList[index].setName(btnSettingData[1])
                    self.QButtonList[index].setPath(btnSettingData[2])
                else:
                    self.QButtonList[index].setName('Unset')
                    self.QButtonList[index].setPath('Unset')
                index += 1
            # support at most 5 QButton 
            if index == 6:
                break
                
    def getEachLineInSettingFile(self):
        if os.path.isfile(self.settingFile):
            try:
                with open(self.settingFile, 'r', encoding='utf-8') as file:
                    content = file.read().split('\n')
                    self.eachLineInSettingFile = content
            except:
                with open(self.settingFile, 'rb') as file:
                    content = file.read().decode('cp950', 'ignore').split('\n')
                    self.eachLineInSettingFile = content
        
    def getAllQLine(self):
        return self.QLineList
    
    def getAllQText(self):
        return self.QTextList
    
    def getAllQButton(self):
        return self.QButtonList
        
    def getTheQText(self, index):
        return self.QTextList[index]
    
    def getTheQLine(self, index):
        return self.QLineList[index]
        
    def getNumOfQButton(self):    
        return self.numOfQButton
        
    def showTheQText(self, index):
        self.QTextList[index].show()
        
    def showTheQLine(self, index):
        self.QLineList[index].show()
        
    def hideOtherQText(self, index):
        [self.QTextList[i].hide() for i in range(self.numOfQButton) if i != index]    
        
    def hideOtherQLine(self, index):
        [self.QLineList[i].hide() for i in range(self.numOfQButton) if i != index]
    
    def keyPressEvent(self, event):
        # set screenSize
        if event.key() == Qt.Key_F2:
            self.setScreenSize()
            
        # show or hide all QButton
        elif event.key() == Qt.Key_F1:
            if self.showAllQButton:
                [b.show() for b in self.QButtonList]
            else:
                [b.hide() for b in self.QButtonList]
            self.showAllQButton = not self.showAllQButton
            
        # create or open the settingFile
        elif event.key() == Qt.Key_F10:
            if not os.path.isfile(self.settingFile):
                with open(self.settingFile, 'w+') as file:
                    file.write(self.defaultContentOfSettingFile)
                os.startfile(self.settingFile)
            else:
                os.startfile(self.settingFile)
                
class QButton(QPushButton):
    def __init__(self, parent, index):
        QPushButton.__init__(self, parent)
        self.isEmptyQText = True    # avoid reload content of the file
        self.parent = parent
        self.index = index
        self.name = ''
        self.filePath = ''
        self.setName('QText' if index == 0 else 'Unset')
        self.setPath('QText' if index == 0 else 'Unset')
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFont(QFont('Consolas', 14, 0, False))
        self.setStyleSheet((
            'border:5px outset blue;'
            'background-color: blue;'
            'color: #FFFF0A;'
        ))
        
    def getPath(self):    
        return self.filePath
        
    def setPath(self, filePath):
        self.filePath = filePath
    
    def getName(self):    
        return self.name
        
    def setName(self, name):
        self.name = name
        self.setText(name)
    
    def mousePressEvent(self, event):
        # get the latest setting of all QButton
        self.parent.setNameAndPathToAllQButton()
        
        # check whether the btn has path-setting 
        if self.filePath == 'Unset':
            QMessageBox.warning(
                self.parent, 
                'Message', 
                'The setting of the button is incorrect.'
            )
            return
            
        # hide QLine and QText of other index
        self.parent.hideOtherQLine(self.index)
        self.parent.hideOtherQText(self.index)
        
        # show QLine and QText of the index
        self.parent.showTheQLine(self.index)
        self.parent.showTheQText(self.index)
        
        # set lineNumber of the QLine
        # set filePath of the QText
        # set focus on the QText
        # set WindowTitle 
        self.parent.QLineList[self.index].setLineNumber()
        self.parent.getTheQText(self.index).setFilePath(self.getPath())
        self.parent.getTheQText(self.index).setFocus()
        self.parent.setWindowTitle(self.filePath)
        
        # update content of the QText (if this is the default QText, ignore it)
        if self.index != 0 and self.isEmptyQText and os.path.isfile(self.filePath):
            try:
                with open(self.filePath, 'r', encoding='utf-8') as file:
                    content = file.read().replace('\t', '    ')
                    self.parent.getTheQText(self.index).setPlainText(content)
                    self.isEmptyQText = False
            except:
                with open(self.filePath, 'rb') as file:
                    content = file.read().decode('cp950', 'ignore')
                    self.parent.getTheQText(self.index).setPlainText(content)
                    self.isEmptyQText = False
                    
class QLine(QPlainTextEdit):
    def __init__(self, parent, index):
        QPlainTextEdit.__init__(self, parent)
        self.verticalScrollBar().setEnabled(False)
        self.setFont(QFont('consolas', 14, 0, False))
        self.setReadOnly(True)
        self.maxLineNumber = 3000
        self.hasSetLineNumber = False
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet((
            'color: #552a07;'
            'background-color: #FFFF99;'
            'border:1px solid black;')
        )
    
    # The speed of open this app would be slow if you set all QLine at first
    # Just set the first QLine when app start and set other QLine when other QButton is clicked
    def setLineNumber(self):
        if not self.hasSetLineNumber:
            self.hasSetLineNumber = True
            # set line_number and then move cursor to first line
            [self.insertPlainText('%5d\n'%i) for i in range(1, self.maxLineNumber+1)]
            [self.moveCursor(QTextCursor.Start)]
    
    def ExtendLineNumber(self):
        [self.moveCursor(QTextCursor.End)]
        starLineNumber = self.maxLineNumber + 1
        number_addNewLine = 3000
        rightBound = starLineNumber + number_addNewLine
        [self.insertPlainText('%5d\n'%i) for i in range(starLineNumber, rightBound)]
        self.maxLineNumber = rightBound - 1
            
class QText(QPlainTextEdit):
    def __init__(self, parent, index):
        QPlainTextEdit.__init__(self, parent)
        self.index = index
        self.parent = parent
        self.clipboard = QApplication.clipboard()
        self.setFont(QFont('consolas', 14, 0, False))
        self.setCursorWidth(3)
        self.filePath = ''            
        self.pattern = ''              # keep the string you want to find
        self.openFile()                # try to get ths filename and open this file
        self.wrapMode = True
        self.setStyleSheet((
            'color: white;'
            'background-color: black;'
            'border:1px solid black;')
        )
        # synchronize verticalScrollBar to the QLine and the QText
        self.verticalScrollBar().valueChanged.connect(
            self.parent.getTheQLine(self.index).verticalScrollBar().setValue
        )
    
    def getFilePath(self):
        return self.filePath
    
    def setFilePath(self, filePath):
        self.filePath = filePath
        
    def openFile(self):
        if len(sys.argv) > 1:
            filePath = ' '.join(sys.argv[1:]) # solve filePath with space_char
            if os.path.isfile(filePath):
                try:
                    with open(filePath, 'r+', encoding='utf-8') as file:
                        self.setPlainText(file.read().replace('\t', '    '))
                except:
                    with open(filePath, 'rb+') as file:
                        self.setPlainText(file.read().decode('cp950', 'ignore'))
                # set filePath and WindowTitle after open_success
                self.filePath = filePath              
                self.parent.setWindowTitle(filePath)
                
    def keyPressEvent(self, event):
        # del a line and set cursor to end of last line
        if event.key() == Qt.Key_Escape:
            cursor = self.textCursor()
            cursor.insertText(' ') # avoid no char lead to bug occur
            cursor.select(QTextCursor.LineUnderCursor)
            cursor.deleteChar()    # delete all char    
            cursor.deleteChar()    # delete the empty line 
            self.moveCursor(QTextCursor.Up)
            self.moveCursor(QTextCursor.EndOfLine)
                
        # open website by chrome
        elif event.key() == Qt.Key_F4:
            cursor = self.textCursor()
            cursor.select(QTextCursor.LineUnderCursor)
            underPath = cursor.selectedText()
            underPathExtension = os.path.splitext(underPath)[1].lower()
            SupportExtension = set(['.cs', '.cshtml', '.html', '.txt', '.json', '.config'])
            if underPath.startswith('http') or underPathExtension in SupportExtension:
                Chrome = r'C:\Program Files (x86)\Google\Chrome\Application\Chrome.exe '
                os.popen('"%s" "%s"'%(Chrome, underPath))
                        
        # execute python script
        elif event.key() == Qt.Key_F5:
            if os.path.splitext(self.filePath)[1].lower() in ['.pyw','.py']:
                os.system('python "%s" & pause'%(self.filePath))
            
        # indent
        elif event.key() == Qt.Key_Tab:
            cursor = self.textCursor()
            if cursor.hasSelection():
                curS = cursor.selectionStart()
                curE = cursor.selectionEnd()
                    
                # get diff from row_start to row_end
                cursor.setPosition(curE)
                rowE = cursor.blockNumber()
                cursor.setPosition(curS)
                rowS = cursor.blockNumber()
                insertNum = rowE - rowS + 1
                    
                # add four space-char to start of line which was selected
                cursor.setPosition(curS)
                cursor.movePosition(cursor.StartOfLine)
                for i in range(insertNum):
                    cursor.insertText('    ')
                    cursor.movePosition(cursor.Down)
                    cursor.movePosition(cursor.StartOfLine)
            else:
                cursor.insertText('    ')
            
        # de-indent lines which has char selected
        elif event.key() == Qt.Key_Backtab:
            cursor = self.textCursor()
            if cursor.hasSelection():
                curS = cursor.selectionStart()
                curE = cursor.selectionEnd()
                cursor.setPosition(curE)
                rowE = cursor.blockNumber()
                cursor.setPosition(curS)
                rowS = cursor.blockNumber()
                insertNum = rowE - rowS + 1
                for i in range(insertNum):
                    cursor.select(QTextCursor.LineUnderCursor)
                    # get number that we can do step back
                    line_origin = cursor.selectedText()
                    line_lstrip = line_origin.strip().strip('\t')
                    # we can do at most 4 step back 
                    delNum = min(4, len(line_origin) - len(line_lstrip))
                    cursor.movePosition(QTextCursor.StartOfLine)
                    [cursor.deleteChar() for i in range(delNum)]
                    # action of next line as above 
                    cursor.movePosition(cursor.Down)
            
        # key_combine(Control)
        elif QApplication.keyboardModifiers() == Qt.ControlModifier:
            # change WrapMode 
            if event.key() == Qt.Key_L:
                if self.wrapMode:
                    self.setLineWrapMode(QPlainTextEdit.NoWrap)
                else:
                    self.setLineWrapMode(QPlainTextEdit.WidgetWidth)
                # reverse the flag
                self.wrapMode = not self.wrapMode
                
            # set Screen To UpperHalf 
            elif event.key() == Qt.Key_Up:
                self.parent.setScreenToUpperHalf()       
                
            # set Screen To LowerHalf 
            elif event.key() == Qt.Key_Down:
                self.parent.setScreenToLowerHalf() 
            
            # set Screen To RightHalf 
            elif event.key() == Qt.Key_Right:
                self.parent.setScreenToRightHalf()
            
            # set Screen To LeftHalf 
            elif event.key() == Qt.Key_Left:
                self.parent.setScreenToLeftHalf()
            
            # extend line number
            elif event.key() == Qt.Key_P:
                self.parent.getTheQLine(self.index).ExtendLineNumber()
                
            # save file
            elif event.key() == Qt.Key_S:
                if not self.filePath or self.filePath == 'QText':
                    self.filePath = QFileDialog.getSaveFileName(None, 
                        'Save File', 
                        'D:\\Desktop',
                        '(*.txt);;(*.py);;(*.pyw)'
                    )[0].replace('/', '\\')
                    # make sure filePath cannot be empty
                    if self.filePath:
                        self.parent.setWindowTitle(self.filePath)
                        with open(self.filePath, 'w+', encoding='utf-8') as file:
                            file.write(self.toPlainText())
                else:
                    with open(self.filePath, 'w+', encoding='utf-8') as file:
                        file.write(self.toPlainText())
                
            # open a new App
            elif event.key() == Qt.Key_N:
                os.startfile(sys.argv[0])
                
            # search string
            elif event.key() == Qt.Key_F:
                text, clickOk = QInputDialog.getText(
                    self.parent,
                    'Search String', 
                    '<h3>Input</h3>', 
                    QLineEdit.Normal
                )
                if text and clickOk:
                    self.pattern = text
                    if not self.find(self.pattern):
                        QMessageBox.warning(
                            self.parent, 
                            'Message', 
                            'Can\'t find the string...'
                        )
                
            # copy the line
            elif event.key() == Qt.Key_C:
                cursor = self.textCursor()
                if not cursor.hasSelection():
                    # copy all line except front space_chars
                    cursor.select(QTextCursor.LineUnderCursor)
                    self.clipboard.setText(cursor.selectedText().strip())
                else:
                    QPlainTextEdit.keyPressEvent(self, event)
                
            # cut the line
            elif event.key() == Qt.Key_X:
                cursor = self.textCursor()
                if not cursor.hasSelection():
                    # copy to clipboard
                    cursor.select(QTextCursor.LineUnderCursor)
                    self.clipboard.setText(cursor.selectedText().strip())
                    # delete all chars in this line
                    cursor.movePosition(QTextCursor.EndOfLine)
                    colNum = cursor.columnNumber() + 1
                    [cursor.deletePreviousChar() for i in range(colNum)]
                else:
                    QPlainTextEdit.keyPressEvent(self, event)
                    
            # open the file 
            elif event.key() == Qt.Key_F10:
                cursor = self.textCursor()
                cursor.select(QTextCursor.LineUnderCursor)
                underPath = cursor.selectedText()
                underPathExtension = os.path.splitext(underPath)[1].lower()
                SupportExtension = set(['.cs', '.cshtml', '.html', '.txt', '.json', '.config'])
                if underPathExtension in SupportExtension:
                    if os.path.exists(underPath):
                        os.startfile(underPath)
            else:
                QPlainTextEdit.keyPressEvent(self, event)
            
        # key_combine(Alt)
        elif QApplication.keyboardModifiers() == Qt.AltModifier:
            # exit
            if event.key() == Qt.Key_W:
                QCoreApplication.quit()
                
            # find previous pattern
            elif event.key() == Qt.Key_F3:
                if self.pattern:
                    self.find(self.pattern, QTextDocument.FindBackward)
                
            # delete chars in front of cursor
            elif event.key() == Qt.Key_X:
                cursor = self.textCursor()
                delNum = cursor.columnNumber()
                [cursor.deletePreviousChar() for i in range(delNum)]
                
            # delete chars in back of cursor
            elif event.key() == Qt.Key_C:
                cursor = self.textCursor()
                col_now = cursor.columnNumber()
                cursor.movePosition(QTextCursor.EndOfLine)
                delNum = cursor.columnNumber() - col_now
                [cursor.deletePreviousChar() for i in range(delNum)]
                        
            # move text which in back of cursor into the bracket
            # this action occur when cursor in () or []
            elif event.key() == Qt.Key_1:
                # get current colume of cursor
                cursor = self.textCursor()
                curcol = cursor.columnNumber()
                # get line string
                cursor.select(QTextCursor.LineUnderCursor)
                line = cursor.selectedText()
                # check cursor whether between () or []
                if len(line) > 1 and line[curcol-1:curcol+1] in ["()","[]"]:
                    # del chars that in back of cursor
                    cursor.movePosition(QTextCursor.EndOfLine)
                    delNum = cursor.columnNumber() - curcol
                    [cursor.deletePreviousChar() for i in range(delNum)]
                    # add chars which in back of right-bracket
                    # if last char in (;:) , do not include it
                    rbracket = ')' if line[curcol-1] == '(' else ']'
                    if line[-1] == ':':
                        cursor.insertText(line[curcol+1:-1] + '%c:'%rbracket)
                    elif line[-1] == ';':
                        cursor.insertText(line[curcol+1:-1] + '%c;'%rbracket)
                    else:
                        cursor.insertText(line[curcol+1:] + '%c'%rbracket)
            
        # key_combine(Shift)
        elif QApplication.keyboardModifiers() == Qt.ShiftModifier:
            if event.key() == Qt.Key_ParenLeft:
                self.insertPlainText('()')
                self.moveCursor(QTextCursor.PreviousCharacter)
                    
            elif event.key() == Qt.Key_Return:
                cursor = self.textCursor()
                cursor.select(QTextCursor.LineUnderCursor)
                line = cursor.selectedText()
                self.insertPlainText('\n')
                # make cursor align to first char of previous line
                space = len(line) - len(line.strip())
                [self.insertPlainText(' ') for i in range(space)]
            else:
                QPlainTextEdit.keyPressEvent(self, event)
            
        # make key_Return more smart
        elif event.key() == Qt.Key_Return:
            cursor = self.textCursor()
            cursor.select(QTextCursor.LineUnderCursor)
            line = cursor.selectedText()
            self.moveCursor(QTextCursor.EndOfLine)
            self.insertPlainText('\n')
            # make cursor align to first char of previous line
            space = len(line) - len(line.lstrip())
            [self.insertPlainText(' ') for i in range(space)]
            # make Python-Programming more easily
            if line.rstrip().endswith(':'):
                self.insertPlainText('    ')
                    
        # find next pattern (this have to put after function of alt + F3)
        elif event.key() == Qt.Key_F3:
            if self.pattern:
                self.find(self.pattern)
        else:
            QPlainTextEdit.keyPressEvent(self, event)
        
        # synchronize KeyEvent with QLine
        self.parent.getTheQLine(self.index).verticalScrollBar().setValue(
            self.verticalScrollBar().value()
        )

class QHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)
        self.STYLES = {
            'keyword1': self._setFormat('#FFCC33'),
            'keyword2': self._setFormat('#FF66FF'),
            'comment' : self._setFormat('#66FF33'),
            'operator': self._setFormat('#FF0000'),
            'defclass': self._setFormat('#85FFFF'),
            'string'  : self._setFormat('yellow')
        }
        
        self.operators = [
            '='  , '==', '!=' , '<' , '<=', '>' , 
            '\+' , '-' , '\*' , '\%', '/' , '>=', 
            '\^' , '\|', '\&'
        ]
        
        self.tri_single = (QRegExp('\'\'\''), 1, self.STYLES['string'])
        self.tri_double = (QRegExp('\"\"\"'), 2, self.STYLES['string'])
        rules = [(r'%s' % o, 0, self.STYLES['operator']) for o in self.operators]
        
        keywords1 = [
            'and',  'class' , 'lambda' , 'elif', 'else', 'break' , 'for', 'def', 
            'from' , 'if' ,  'import', 'global' , 'with', 'try' , 'except', 'not', 
            'or' , 'while', 'in' ,'continue', 'return' , '__init__'
        ]
            
        keywords2 = [
            'as' ,
            'abs','min','max','bin','len','set','zip','del','str','ord','chr','int',
            'oct','hex','sum','map',
            'open','list','dict','True','pass','type','None','sort',
            'False','print','input','super','range','float','bytes',
            'format', 'sys.exit','bytearray','enumerate'
        ]
        
        rules += [(r'\b%s\b'%w , 0, self.STYLES['keyword1']) for w in keywords1]
        rules += [(r'\b%s\b'%w , 0, self.STYLES['keyword2']) for w in keywords2]
        rules += [(r'\bself\b'         , 0, self.STYLES['defclass'])]
        rules += [(r'#[^\n\'\"]*'      , 0, self.STYLES['comment' ])]
        rules += [(r'[^:]//[^\n\'\"]*' , 0, self.STYLES['comment' ])]
        rules += [(r'\bdef\b\s*(\w+)'  , 1, self.STYLES['defclass'])]
        rules += [
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, self.STYLES['string']),
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, self.STYLES['string']),
            (r'\bclass\b\s*(\w+)'     , 1, self.STYLES['defclass'])
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt) for (pat, index, fmt) in rules]
    
    def _setFormat(self, color):
        _color = QColor()
        _color.setNamedColor(color)
        _Format = QTextCharFormat()
        _Format.setForeground(_color)
        return _Format
    
    def highlightBlock(self, text):
        for expression, nth, FORMAT in self.rules:
            index = expression.indexIn(text, 0)
            while index >= 0:
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, FORMAT)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        else:
            start = delimiter.indexIn(text)
            add = delimiter.matchedLength()

        # As long as there is a delimiter match
        while start >= 0:
            end = delimiter.indexIn(text, start + add)
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            
            self.setFormat(start, length, style)               # Apply formatting
            start = delimiter.indexIn(text, start + length)    # next match

        # Return True if still inside a multi-line string, False otherwise
        return True if self.currentBlockState() == in_state else False
        
if __name__ == '__main__' :
    editorApp = QApplication(sys.argv)
    appWindow = QMain()
    # create UI and set layout 
    appWindow.createQButtons()
    appWindow.createQLines()
    appWindow.createQTexts()
    appWindow.setLayoutOfUI()
    
    # set data to all QButton
    # set line number to QLine which index = 0
    # set focus to QText which index = 0
    # create Highlighter for all QText
    appWindow.setNameAndPathToAllQButton()
    appWindow.getTheQLine(0).setLineNumber()
    appWindow.getTheQText(0).setFocus()
    appWindow.createQHighlighterToAllQText()
    
    # Just show default UI which index = 0
    appWindow.hideOtherQLine(0)
    appWindow.hideOtherQText(0)
    
    sys.exit(editorApp.exec_())
