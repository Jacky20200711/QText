import os, sys, webbrowser
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class QWindow(QWidget):
    def __init__(self):
        super(QWindow, self).__init__()
        self.magnifyFlag = False
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle('QText')
        self.setQTextIcon()
        self.setScreen()
        self.show()
        
    def setScreen(self):
        screen = QApplication.desktop().screenGeometry()
        height = screen.height()
        width =  screen.width()
        Y = int(height * 0.1)
        H = int(height * 0.8)
        X = int(width  * 0.1)
        W = int(width  * 0.8)
        if not self.magnifyFlag:
            self.setGeometry(X, Y, W, H)
        else:
            # set MaximumSize to avoid screen become too big
            # if you do not this, you will get a warning
            self.setMaximumSize(1920, 1080) 
            self.setGeometry(0, 40, width, height)
            
    def setQTextIcon(self):
        # iconPath is depend on yourself
        iconPath = r'D:\Desktop\Project\QText\QText.ico'
        if os.path.isfile(iconPath):
            self.setWindowIcon(QIcon(iconPath))
    
    # Magnify or minify main_window
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F2:
            # reverse the flag after pressing F2
            self.magnifyFlag = not self.magnifyFlag
            self.setScreen()
            
class QLine(QPlainTextEdit):
    def __init__(self, parent):
        QPlainTextEdit.__init__(self, parent)
        self.verticalScrollBar().setEnabled(False)
        self.setFont(QFont('consolas', 14, 0, False))
        self.setReadOnly(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet((
            'color: #552a07;'
            'background-color: #FFFF99;'
            'border:1px solid black;')
        )
        # set line_number and then move cursor to first line
        [self.insertPlainText('%5d\n'%i) for i in range(1,1000)]
        self.moveCursor(QTextCursor.Start)
                
class QText(QPlainTextEdit):
    def __init__(self, parent, line_text):
        QPlainTextEdit.__init__(self, parent)
        self.qline = line_text
        self.parentWindow = parent
        self.clipboard = QApplication.clipboard()
        self.setFont(QFont('consolas', 14, 0, False))
        self.setCursorWidth(3)
        self.fileName = ''             # keep filename
        self.pattern = ''              # keep the string you want to find
        self.openFile()                # try to fetch filename and open file
        self.setFocus()                # make cursor in position
        self.wrapMode = True
        self.setStyleSheet((
            'color: white;'
            'background-color: black;'
            'border:1px solid black;')
        )
        # synchronize line_number with Vbar_value of main_text 
        self.verticalScrollBar().valueChanged.connect(
            self.qline.verticalScrollBar().setValue
        )

    # fetch fileName -> open file -> load content into QPlainTextEdit 
    def openFile(self):
        if len(sys.argv) > 1:
            fname = ' '.join(sys.argv[1:]) # solve filename with space_char
            if os.path.isfile(fname):
                try:
                    with open(fname, 'r', encoding='utf-8') as file:
                        self.setPlainText(file.read().replace('\t', '    '))
                except:
                    with open(fname, 'rb') as file:
                        self.setPlainText(file.read().decode('cp950', 'ignore'))
                # set filename and WindowTitle after open_success
                self.fileName = fname              
                self.parentWindow.setWindowTitle(fname)
                
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
            if os.path.splitext(self.fileName)[1] in ['.pyw','.py']:
                os.system('python "%s" & pause'%(self.fileName))
            
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
                        
            # save file
            elif event.key() == Qt.Key_S:
                if not self.fileName:
                    self.fileName = QFileDialog.getSaveFileName(None, 
                        'Save File', 
                        'D:\\Desktop',
                        '(*.txt);;(*.py);;(*.pyw)'
                    )[0]
                    # make sure fileName cannot be empty
                    if self.fileName:
                        self.parentWindow.setWindowTitle(self.fileName)
                        with open(self.fileName, 'w+', encoding='utf-8') as file:
                            file.write(self.toPlainText())
                else:
                    with open(self.fileName, 'w+', encoding='utf-8') as file:
                        file.write(self.toPlainText())
                
            # open new QText
            elif event.key() == Qt.Key_N:
                os.startfile(sys.argv[0])
                
            # search string
            elif event.key() == Qt.Key_F:
                text, ok = QInputDialog.getText(
                    self.parentWindow,
                    'Search String', 
                    '<h3>Input</h3>', 
                    QLineEdit.Normal
                )
                if text and ok:
                    self.pattern = text
                    self.find(self.pattern)
                
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
        self.qline.verticalScrollBar().setValue(self.verticalScrollBar().value())

class QTextLighter(QSyntaxHighlighter):
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
            'open','list','dict','True','pass','type','None',
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
    def __init__(self, widget, line_text, main_text):
        super(QTextLayout, self).__init__()
        self.setSpacing(10)
        self.setColumnStretch(0,1)
        self.addWidget(line_text,0,0) # put this in row=0 col=0
        self.addWidget(main_text,0,1) # put this in row=0 col=1
        self.setColumnStretch(0,1)    # Grid[0] colSpan=1   
        self.setColumnStretch(1,18)   # Grid[1] colSpan=18
        widget.setLayout(self)
        
if __name__ == '__main__' :
    app = QApplication(sys.argv)
    appWindow = QWindow()
    line_text = QLine(appWindow)             # for displaying line number
    main_text = QText(appWindow, line_text)  # for editing file content
    appLayout = QTextLayout(appWindow, line_text, main_text)
    highlight = QTextLighter(main_text.document())
    sys.exit(app.exec_())
