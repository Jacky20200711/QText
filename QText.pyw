import os, sys, subprocess, linecache, getpass
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
        
class QMain(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.settingFile = os.path.split(sys.argv[0])[0] + '\\SettingFile.txt'
        self.setWindowTitle('QText')
        self.QLine = None
        self.QText = None
        self.QHighlighter = None
        self.QLayout = None
        self.isFullScreen = False
        self.screenSize = QApplication.desktop().screenGeometry()
        self.screenLower = [0.1, 0.1, 0.78, 0.8]
        self.screenUpper = [0, 45, 1, 0.917]
        self.eachLineInSettingFile = []
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.getEachLineInSettingFile()
        self.setScreenSize()
        self.setIcon()
        self.show()
        self.defaultContentOfSettingFile = \
            'screenLower,0.1,0.1,0.78,0.8\n'+ \
            'screenUpper,0,45,1,0.917\n'+ \
           r'iconPath,D:\Desktop\Project\QText\QText.ico' + '\n'
        
    def createQLine(self):
        self.QLine = QLine(self)
        
    def createQText(self):
        self.QText = QText(self)
        
    def createQHighlighter(self):
        self.QHighlighter = QHighlighter(self.QText.document())
        
    def arrangeElement(self):
        self.QLayout = QGridLayout()
        self.QLayout.addWidget(self.QLine,0,0) # pos : row = 0 & col = 0
        self.QLayout.addWidget(self.QText,0,1) # pos : row = 0 & col = 1
        self.QLayout.setColumnStretch(0,1)
        self.QLayout.setColumnStretch(1,16)
        self.setLayout(self.QLayout)
        
    def setScreenSize(self):
        # check arguments in settingFile
        self.getEachLineInSettingFile()
        for line in self.eachLineInSettingFile:
            if line.startswith('screenLower'):
                s = line.split(',')[1:]
                for i in range(4):
                    self.screenLower[i] = float(s[i])
            elif line.startswith('screenUpper'):
                s = line.split(',')[1:]
                for i in range(4):
                    self.screenUpper[i] = float(s[i])
        # resize the screen
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
        # reverse the flag    
        self.isFullScreen = not self.isFullScreen
        
    def setIcon(self):
        # default iconPath
        iconPath = r'D:\Desktop\Project\QText\QText.ico'   
        # check path in SettingFile
        for line in self.eachLineInSettingFile:
            if line.startswith('iconPath'):
                iconPath = line.split(',')[1]
        # set icon
        self.setWindowIcon(QIcon(iconPath))
                
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
        
    def getQText(self):
        return self.QText
    
    def getQLine(self):
        return self.QLine
    
    def keyPressEvent(self, event):
        # set screenSize
        if event.key() == Qt.Key_F2:
            self.setScreenSize()
        # open the settingFile
        elif event.key() == Qt.Key_F10:
            if not os.path.isfile(self.settingFile):
                with open(self.settingFile, 'w+') as file:
                    file.write(self.defaultContentOfSettingFile)
            os.startfile(self.settingFile)
                    
class QLine(QPlainTextEdit):
    def __init__(self, parent):
        QPlainTextEdit.__init__(self, parent)
        self.verticalScrollBar().setEnabled(False)
        self.setFont(QFont('細明體', 14, 0, False))
        self.setReadOnly(True)
        self.maxLineNumber = 2000
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet((
            'color: #552a07;'
            'background-color: #FFFF99;'
            'border:1px solid black;')
        )
    
    def setLineNumber(self, lineOfTheOpenFile=0):
        self.maxLineNumber = lineOfTheOpenFile + 2000
        [self.insertPlainText('%5d\n'%i) for i in range(1, self.maxLineNumber+1)]
        self.moveCursor(QTextCursor.Start)
    
    def extendLineNumber(self):
        self.moveCursor(QTextCursor.End)
        starLineNumber = self.maxLineNumber + 1
        numOfNewLine = 5000
        rightBound = starLineNumber + numOfNewLine
        [self.insertPlainText('%5d\n'%i) for i in range(starLineNumber, rightBound)]
        self.maxLineNumber = rightBound - 1
            
class QText(QPlainTextEdit):
    def __init__(self, parent):
        QPlainTextEdit.__init__(self, parent)
        self.lineOfTheOpenFile = 0
        self.parent = parent
        self.clipboard = QApplication.clipboard()
        self.setFont(QFont('細明體', 14, 0, False))
        self.setCursorWidth(3)
        self.filePath = ''            
        self.pattern = ''              # keep the string you want to find
        self.openFile()                # try to get ths filename and open this file
        self.wrapMode = False
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setStyleSheet((
            'color: white;'
            'background-color: black;'
            'border:1px solid black;')
        )
        # synchronize verticalScrollBar to the QLine and the QText
        self.verticalScrollBar().valueChanged.connect(
            self.parent.getQLine().verticalScrollBar().setValue
        )
    
    def getLineOfTheOpenFile(self):
        return self.lineOfTheOpenFile
        
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
                
                # Get line number of the file
                try:
                    self.lineOfTheOpenFile += len(linecache.getlines(filePath))
                except:
                    pass
                
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
                
        # open the dir, or open the file or url using chrome
        elif event.key() == Qt.Key_F4:
            # get the path or url under the cursor
            cursor = self.textCursor()
            cursor.select(QTextCursor.LineUnderCursor)
            underPath = cursor.selectedText()
            # 如果沒有D槽，則將桌面指到 C 槽某處
            if not os.path.isdir('D:'):
                underPath = underPath.lower()
                underPath = underPath.replace(r'd:\desktop',r'C:\Users\JackyChen\Desktop')
            # try to open the dir and then return
            if os.path.isdir(underPath):
                os.startfile(underPath)
                return
            # detect the path of chrome
            chromePath = r'C:/Program Files (x86)/Google/Chrome/Application/Chrome.exe'
            if not os.path.exists(chromePath):
                chromePath = r'C:/Program Files/Google/Chrome/Application/Chrome.exe'
            if not os.path.exists(chromePath):
                chromePath = r'C:/Users/%s/AppData/Local/Google/Chrome/Application/Chrome.exe'%(getpass.getuser())
            # get the flag whether we can open it by chrome
            underPathExtension = os.path.splitext(underPath)[1].lower()
            SupportedExtension = set(['.cs', '.cshtml', '.html', '.txt', '.json', '.config', '.md', '.js', '.py', '.pyw'])
            openThisByChrome = False
            if os.path.exists(underPath) and underPathExtension in SupportedExtension:
                openThisByChrome = True
            elif underPath.startswith('http'):
                openThisByChrome = True
            # check the flag whether we can open it by chrome            
            if openThisByChrome:
                command = '"%s" "%s"'%(chromePath, underPath)
                result = subprocess.Popen(
                    command, 
                    shell=True, 
                    stdin=subprocess.PIPE, 
                    stdout=subprocess.PIPE, 
                )
            
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
                    line_lstrip = line_origin.lstrip().lstrip('\t')
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
                self.setLineWrapMode(QPlainTextEdit.NoWrap if self.wrapMode else QPlainTextEdit.WidgetWidth)
                self.wrapMode = not self.wrapMode
                
            # save file
            elif event.key() == Qt.Key_S:
                if not self.filePath or self.filePath == 'QText':
                    # 如果沒有D槽，則將預設的儲存路徑指到 C:\Users\ycgis\Desktop
                    defaultPath = r'D:\Desktop'
                    if not os.path.isdir('D:'):
                        defaultPath = r'C:\Users\ycgis\Desktop'
                    # 設定彈窗
                    self.filePath = QFileDialog.getSaveFileName(None, 
                        'Save File', 
                        defaultPath,
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
                
            # copy the line to clipboard
            elif event.key() == Qt.Key_C:
                cursor = self.textCursor()
                if not cursor.hasSelection():
                    cursor.select(QTextCursor.LineUnderCursor)
                    self.clipboard.setText(cursor.selectedText().strip())
                else:
                    QPlainTextEdit.keyPressEvent(self, event)
                
            # copy the line to clipboard and then delete this line
            elif event.key() == Qt.Key_X:
                cursor = self.textCursor()
                if not cursor.hasSelection():
                    # copy the line to clipboard
                    cursor.select(QTextCursor.LineUnderCursor)
                    self.clipboard.setText(cursor.selectedText().strip())
                    # delete this line
                    cursor.movePosition(QTextCursor.EndOfLine)
                    colNum = cursor.columnNumber() + 1
                    [cursor.deletePreviousChar() for i in range(colNum)]
                else:
                    QPlainTextEdit.keyPressEvent(self, event)
                    
            # open the file by QText
            elif event.key() == Qt.Key_F10:
                cursor = self.textCursor()
                cursor.select(QTextCursor.LineUnderCursor)
                underPath = cursor.selectedText()
                # 如果沒有D槽，則將桌面指到 C:\Users\ycgis\Desktop
                if not os.path.isdir('D:'):
                    underPath = underPath.lower()
                    underPath = underPath.replace(r'd:\desktop',r'C:\Users\ycgis\Desktop')
                # 提取副檔名
                underPathExtension = os.path.splitext(underPath)[1].lower()
                SupportExtension = set(['.cs', '.cshtml', '.html', '.txt', '.json', '.config', '.md'])
                if os.path.isfile(underPath) and underPathExtension in SupportExtension:
                    command = '"%s" "%s"'%(sys.argv[0], underPath)
                    result = subprocess.Popen(
                        command, 
                        shell=True, 
                        stdin=subprocess.PIPE, 
                        stdout=subprocess.PIPE, 
                    )
            else:
                QPlainTextEdit.keyPressEvent(self, event)
            
        # key_combine(Alt)
        elif QApplication.keyboardModifiers() == Qt.AltModifier:
            # exit
            if event.key() == Qt.Key_W:
                QCoreApplication.quit()
                
            # extend line number
            elif event.key() == Qt.Key_L:
                self.parent.getQLine().extendLineNumber()
                
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
                # do the work as general key_Return
                cursor = self.textCursor()
                cursor.select(QTextCursor.LineUnderCursor)
                line = cursor.selectedText()
                self.insertPlainText('\n')
                # make cursor align to previous line
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
            # auto indent when last chr of previous line in the set
            line = line.rstrip()
            charSet = set([':','{','['])
            for c in charSet:
                if line.endswith(c):
                    self.insertPlainText('    ')
                    break
                    
        # find next pattern (this action should put after alt + F3)
        elif event.key() == Qt.Key_F3:
            if self.pattern:
                self.find(self.pattern)
        else:
            QPlainTextEdit.keyPressEvent(self, event)
        
        # synchronize KeyEvent with QLine
        self.parent.getQLine().verticalScrollBar().setValue(
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
            '='  , '==', '!=' , '<' , '<=', '>' , '\^' , '\|', '\&',
            '\+' , '-' , '\*' , '\%', '/' , '>=', 
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
            'open','list','dict','True','pass','type','None','sort', 'exit',
            'False','print','input','super','range','float','bytes',
            'format', 'sys.exit','bytearray','enumerate'
        ]
        
        rules += [(r'\b%s\b'%w , 0, self.STYLES['keyword1']) for w in keywords1]
        rules += [(r'\b%s\b'%w , 0, self.STYLES['keyword2']) for w in keywords2]
        rules += [(r'\bclass\b\s*(\w+)', 1, self.STYLES['defclass'])]
        rules += [(r'\bdef\b\s*(\w+)'  , 1, self.STYLES['defclass'])]
        rules += [(r'\bself\b'         , 0, self.STYLES['defclass'])]
        rules += [(r'#[^\n\'\"]*'      , 0, self.STYLES['comment' ])]
        rules += [(r'[^:]//[^\n\'\"]*' , 0, self.STYLES['comment' ])]
        rules += [(r'"[^"\\]*(\\.[^"\\]*)*"', 0, self.STYLES['string'])]
        rules += [(r"'[^'\\]*(\\.[^'\\]*)*'", 0, self.STYLES['string'])]

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
    # create ui and set layout
    editorApp = QApplication(sys.argv)
    appWindow = QMain()
    appWindow.createQLine()
    appWindow.createQText()
    appWindow.createQHighlighter()
    appWindow.arrangeElement()
    appWindow.getQText().setFocus()
    # set line Number to QLine
    numOfline = appWindow.getQText().getLineOfTheOpenFile()
    appWindow.getQLine().setLineNumber(numOfline)
    sys.exit(editorApp.exec_())
