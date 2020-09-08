import os, sys, webbrowser
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class QWindow(QWidget):
    def __init__(self):
        super(QWindow, self).__init__()
        self.defaultContentOfSettingFile = \
            'button,Unset,Unset\n'+ \
            'button,Unset,Unset\n'+ \
            'button,Unset,Unset\n'+ \
            'button,Unset,Unset\n'+ \
            'button,Unset,Unset\n'+ \
            'screenLower,0.1,0.1,0.8,0.8\n'+ \
            'screenUpper,0,0,1,0.917\n'+ \
            'screenToTopHalf,0,0,1,0.865\n'+ \
            'screenToBottomHalf,0,555,1,0.865\n'+ \
           r'iconPath,D:\Desktop\Project\QText\QText.ico'+'\n'
                                    
        self.setWindowTitle('QText')
        self.maxLineNumber = 3001
        self.numOfQBton = 6
        self.push_btns = [QBton(self,i) for i in range(self.numOfQBton)]
        self.line_text = [QLine(self,i) for i in range(self.numOfQBton)]
        self.main_text = [QText(self,i) for i in range(self.numOfQBton)]
        self.highlight = [QHigh(QText.document()) for QText in self.main_text]
        self.showAllQBton = True
        self.isFullScreen = False
        self.screenUpperHalf = [0, 0, 1, 0.865]
        self.screenLowerHalf = [0, 555, 1, 0.865]
        self.screenLower = [0.1, 0.1, 0.8, 0.8]
        self.screenUpper = [0, 0, 1, 0.917]    
        self.eachLineInSettingFile = []
        self.settingFile = os.path.split(sys.argv[0])[0] + '\\SettingFile.txt'
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.getEachLineInSettingFile()
        self.setScreenSize()
        self.setIcon()
        self.setAllQBton()
        self.setLineNumberToTheQLine(0)
        self.show()
        
    def resetSettingFile(self):
        if os.path.isfile(self.settingFile):
            with open(self.settingFile, 'w+') as file:
                file.write(self.defaultContentOfSettingFile)
        
    def setScreenSize(self):
        # get latest arguments from settingFile
        self.getEachLineInSettingFile()
        
        # default arguments of screen
        screen = QApplication.desktop().screenGeometry()
        height = screen.height()
        width =  screen.width()
        
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
            # setMaximumSize can avoid screen become too big
            # if you do not this, you will get a warning
            X = int(self.screenUpper[0])
            Y = int(self.screenUpper[1]) + 45
            W = int(self.screenUpper[2]*width)
            H = int(self.screenUpper[3]*height)
            self.setGeometry(X, Y, W, H)
        else:
            X = int(self.screenLower[0] * width)
            Y = int(self.screenLower[1] * height)
            W = int(self.screenLower[2] * width)
            H = int(self.screenLower[3] * height)
            self.setGeometry(X, Y, W, H)
            
        self.isFullScreen = not self.isFullScreen
        
    def setScreenToUpperHalf(self):
        # get latest arguments from settingFile
        self.getEachLineInSettingFile()
        
        # default arguments of screen
        screen = QApplication.desktop().screenGeometry()
        height = screen.height()
        width =  screen.width()
        
        # try to update arguments from settingFile
        for line in self.eachLineInSettingFile:
            if line.startswith('screenToTopHalf'):
                s = line.split(',')[1:]
                for i in range(4):
                    self.screenUpperHalf[i] = float(s[i])
        
        X = int(self.screenUpperHalf[0])
        Y = int(self.screenUpperHalf[1]) + 45
        W = int(self.screenUpperHalf[2]*width)
        H = int(self.screenUpperHalf[3]*height) >> 1
        self.setGeometry(X, Y, W, H)
        
    def setScreenToLowerHalf(self):
        # get latest arguments from settingFile
        self.getEachLineInSettingFile()
        
        # default arguments of screen
        screen = QApplication.desktop().screenGeometry()
        height = screen.height()
        width =  screen.width()
        
        # try to update arguments from settingFile
        for line in self.eachLineInSettingFile:
            if line.startswith('screenToBottomHalf'):
                s = line.split(',')[1:]
                for i in range(4):
                    self.screenLowerHalf[i] = float(s[i])
        
        X = int(self.screenLowerHalf[0])
        Y = int(self.screenLowerHalf[1])
        W = int(self.screenLowerHalf[2]*width)
        H = int(self.screenLowerHalf[3]*height) >> 1
        self.setGeometry(X, Y, W, H)
        
    # The speed of open this app would be slow if you set all QLine when app start
    # so we just set one QLine when app start
    def setLineNumberToTheQLine(self, index):
        qline = self.line_text[index]
        if not qline.getFlagOfSetLineNumber():
            # set line_number and then move cursor to first line
            [qline.insertPlainText('%5d\n'%i) for i in range(1,self.maxLineNumber)]
            [qline.moveCursor(QTextCursor.Start)]
            [qline.setFlagOfSetLineNumber(True)]
        
    def setIcon(self):
        # default iconPath
        iconPath = r'D:\Desktop\Project\QText\QText.ico'   
        
        # try to update arguments from settingFile
        for line in self.eachLineInSettingFile:
            if line.startswith('iconPath'):
                iconPath = line.split(',')[1]
                
        # set icon
        self.setWindowIcon(QIcon(iconPath))
        
    def setAllQBton(self):
        # set QBton of the index = 0
        self.push_btns[0].setPath(self.main_text[0].getFilePath())
            
        # get latest arguments from settingFile
        self.getEachLineInSettingFile()
        
        # set QBton from index = 1
        index = 1
        for line in self.eachLineInSettingFile:
            if line.startswith('button'):
                btnSettingData = line.split(',')
                # set filePath and name to each button if path is valid
                if os.path.isfile(btnSettingData[2]):
                    self.push_btns[index].setName(btnSettingData[1])
                    self.push_btns[index].setPath(btnSettingData[2])
                else:
                    self.push_btns[index].setName('Unset')
                    self.push_btns[index].setPath('Unset')
                index += 1
            # support at most 5 QBton 
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
        return self.line_text
    
    def getAllQText(self):
        return self.main_text
    
    def getAllQBton(self):
        return self.push_btns
        
    def getTheQText(self, index):
        return self.main_text[index]
    
    def getTheQLine(self, index):
        return self.line_text[index]
        
    def getNumOfQBton(self):    
        return self.numOfQBton
        
    def showTheQText(self, index):
        self.main_text[index].show()
        
    def showTheQLine(self, index):
        self.line_text[index].show()
        
    def hideOtherQText(self, index):
        [self.main_text[i].hide() for i in range(self.numOfQBton) if i != index]    
        
    def hideOtherQLine(self, index):
        [self.line_text[i].hide() for i in range(self.numOfQBton) if i != index]
    
    def keyPressEvent(self, event):
        # set size of screen
        if event.key() == Qt.Key_F2:
            self.setScreenSize()
            
        # show or hide all QBton
        elif event.key() == Qt.Key_F1:
            if self.showAllQBton:
                [b.show() for b in self.push_btns]
            else:
                [b.hide() for b in self.push_btns]
            self.showAllQBton = not self.showAllQBton
            
        # create or open the settingFile
        elif event.key() == Qt.Key_F10:
            if not os.path.isfile(self.settingFile):
                with open(self.settingFile, 'w+') as file:
                    file.write(self.defaultContentOfSettingFile)
                os.startfile(self.settingFile)
            else:
                os.startfile(self.settingFile)
            
class QBton(QPushButton):
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
        # get the latest setting of all QBton
        self.parent.setAllQBton()
        
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
        self.parent.setLineNumberToTheQLine(self.index)
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
        self.hasSetLineNumber = False
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet((
            'color: #552a07;'
            'background-color: #FFFF99;'
            'border:1px solid black;')
        )
        
    def getFlagOfSetLineNumber(self):
        return self.hasSetLineNumber
        
    def setFlagOfSetLineNumber(self, flag):
        self.hasSetLineNumber = flag
                
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
        self.openFile()                # try to fetch filename and open file
        self.wrapMode = True
        self.setStyleSheet((
            'color: white;'
            'background-color: black;'
            'border:1px solid black;')
        )
        # synchronize line_number with Vbar_value of main_text 
        self.verticalScrollBar().valueChanged.connect(
            self.parent.getTheQLine(self.index).verticalScrollBar().setValue
        )
    
    def getFilePath(self):
        return self.filePath
    
    def setFilePath(self, filePath):
        self.filePath = filePath
        
    # fetch filePath -> open file -> load content into QPlainTextEdit 
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
                
        # open website
        elif event.key() == Qt.Key_F4:
            cursor = self.textCursor()
            cursor.select(QTextCursor.LineUnderCursor)
            if cursor.selectedText().startswith('http'):
                webbrowser.open_new_tab(cursor.selectedText())
                        
        # execute python script
        elif event.key() == Qt.Key_F5:
            if os.path.splitext(self.filePath)[1] in ['.pyw','.py']:
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
            
            # reset settingFile
            elif event.key() == Qt.Key_F10:
                self.parent.resetSettingFile() 
                
            # set Screen To UpperHalf 
            elif event.key() == Qt.Key_Up:
                self.parent.setScreenToUpperHalf()       
                
            # set Screen To LowerHalf 
            elif event.key() == Qt.Key_Down:
                self.parent.setScreenToLowerHalf() 
                
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
                
            # open new QText
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
            # do this for Python-Programming
            # rstrip can get rid off space_char that in back of :
            if line.rstrip().endswith(':'):
                self.insertPlainText('    ')
                    
        # find next pattern (this have to put after function of alt + F3)
        elif event.key() == Qt.Key_F3:
            if self.pattern:
                self.find(self.pattern)
        else:
            QPlainTextEdit.keyPressEvent(self, event)
        
        # synchronize line_number with KeyEvent
        self.parent.getTheQLine(self.index).verticalScrollBar().setValue(
            self.verticalScrollBar().value()
        )

class QHigh(QSyntaxHighlighter):
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
            
class QTextLayout(QGridLayout):
    def __init__(self, appWindow):
        QGridLayout.__init__(self)
        main_text = appWindow.getAllQText()
        line_text = appWindow.getAllQLine()
        push_btns = appWindow.getAllQBton()
        numOfQBton = appWindow.getNumOfQBton()
        [self.setColumnStretch(0,1)]
        [self.addWidget(btn,0,i+1) for i,btn in enumerate(push_btns)]
        [self.setColumnStretch(i,10) for i in range(1,numOfQBton+1)]
        [self.addWidget(line_text[i],1,0,1,1) for i in range(numOfQBton)]
        [self.addWidget(main_text[i],1,1,1,6) for i in range(numOfQBton)]
        [btn.hide() for btn in push_btns]
        [appWindow.setLayout(self)]
        
if __name__ == '__main__' :
    editorApp = QApplication(sys.argv)
    appWindow = QWindow()
    appLayout = QTextLayout(appWindow)
    appWindow.hideOtherQLine(0)
    appWindow.hideOtherQText(0)
    appWindow.getTheQText(0).setFocus()
    sys.exit(editorApp.exec_())
