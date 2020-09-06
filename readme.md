1# 此程式的用途  
自製的簡易編輯器，用來"編輯檔案"以及"撰寫&測試Python"  
  
# 使用到的技術  
GUI程式設計、物件導向(封裝、繼承、多型)  
  
# 開發環境 & 使用的套件  
win10(64bit) + Python3.8.5 + PyQt5  

# 此程式的功能說明  
1.語法高亮(Python的"Keyword"和"Operator"會有Highlight)  
2.各種功能鍵和組合鍵  
F1 : 顯示或隱藏[開啟其它檔案的按鈕]，按鈕需要到F10設定才能使用  
F2 : 放大或縮小視窗  
F3 : 往下搜尋字串(往上為Alt+F3)  
F4 : 開啟網址(網址必須完整，並且必須獨佔一行)  
F5 : 執行自己(副檔名必須為py或pyw)  
F10: 開啟設定檔(可以在此設定視窗大小、ICON路徑、按鈕的名稱和對應檔案的路徑)  
  
Ctrl + F : 搜尋字串  
Ctrl + S : 儲存檔案  
Ctrl + N : 開新檔案  
Ctrl + C : 複製游標所在的那一行  
Ctrl + X : 剪下游標所在的那一行  
Ctrl + ↑ : 讓APP的視窗占滿螢幕的上半部
Ctrl + ↓ : 讓APP的視窗占滿螢幕的下半部
  
Alt + W  : 關閉檔案  
Alt + X  : 刪除游標之前的該行字元  
Alt + C  : 刪除游標之後的該行字元  
Alt + 1  : 將括號後的字元移到當前游標所在的空括號  
  
Enter的效果  
1.插入新行，游標自動與上一行的第1個字元對齊  
2.如果上一行的最後有效字元(空白為無效字元)為':'，則游標還會進行縮進  
  
Enter + shift : 效果如一般編輯器的Enter  

Tab : 插入4個空白字元 or 將"被滑鼠選取到的那幾行"做縮排  
Tab + shitf : 將"被滑鼠選取到的那幾行"做反縮排  
  
Esc : 刪除游標所在的那一行，並將游標定位到上一行的尾端  
  
# 架設環境的步驟 & 此程式的執行方法  
1.下載並安裝 Python3.8.5 (此版本有內建pip)  
  
2.打開命令列，使用以下指令安裝各個套件  
pip install PyQt5  
pip install sip  

3.到以下網址下載"pygame-1.9.6-cp38-cp38-win_amd64.whl"  
http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame  

4.將命令列的路徑切換到該whl檔案所在的資料夾，然後輸入以下指令  
pip install pygame-1.9.6-cp38-cp38-win_amd64.whl  
  
5.架設好環境後，雙擊QText.pyw   

# 執行的結果1(編輯TXT檔)  
![image](https://github.com/Jacky20200711/QText/blob/master/DEMO1.PNG?raw=true)
&emsp;
&emsp;
&emsp;
# 執行的結果2(執行PY檔)  
![image](https://github.com/Jacky20200711/QText/blob/master/DEMO2.PNG?raw=true)
&emsp;
&emsp;
&emsp;
# 執行的結果3(用來編輯其它檔案的按鈕)  
![image](https://github.com/Jacky20200711/QText/blob/master/DEMO3.PNG?raw=true)
&emsp;
&emsp;
&emsp;
# 執行的結果4(方便比對兩個檔案的內容)  
![image](https://github.com/Jacky20200711/QText/blob/master/DEMO4.PNG?raw=true)
&emsp;
&emsp;