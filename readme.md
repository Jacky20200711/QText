# 專案說明  
自製的簡易編輯器，用來取代記事本 & 撰寫 Python 腳本。  
&emsp;  
# 開發環境  
Win10(64bit) + Python 3.9.1 + PyQt5  
&emsp;  
# 架構簡述  
主要有四個類別(QMain、QLine、QText、QHighlighter)  
QMain 為程式的主視窗，也是其餘類別的 Parent  
QLine 用來顯示行數  
QText 用來編輯文本  
QHighlighter 用來令文本內容產生語法高亮  
&emsp;  
# 功能說明  
1.遇到 Python 的 "Keyword" 和 "Operator" 會產生語法高亮  
2.功能鍵和組合鍵  
F2 : 放大或縮小視窗  
F3 : 往下搜尋字串(往上為Alt+F3)  
F4 : 嘗試用 Chrome 開啟游標所在那一行的網址 or 檔案(路徑必須完整且獨佔一行)  
F5 : 執行自己(副檔名必須為py或pyw)  
F10: 開啟設定檔(可以在此設定視窗大小、視窗位置、ICON路徑)  
Ctrl + F10 : 嘗試開啟游標底下的檔案或目錄(路徑必須完整且獨佔一行)  
Ctrl + F : 搜尋字串，若搜尋失敗會顯示提示訊息  
Ctrl + S : 儲存檔案  
Ctrl + N : 開新檔案  
Ctrl + C : 複製游標所在的那一行  
Ctrl + X : 剪下游標所在的那一行  
Alt + W  : 關閉檔案  
Alt + X  : 刪除游標左邊的該行字元  
Alt + C  : 刪除游標右邊的該行字元  
Alt + 1  : 將括號後的字元移到當前游標所在的空括號  
Alt + L  : 延伸顯示的行數，一次延伸5000行  
Enter : 插入新行並與上一行的第1個字元對齊  
Enter + shift : 效果如一般的 Enter  
Tab : 插入4個空白字元 or 將 "被選取到的那幾行" 做縮排  
Tab + shift : 將 "被選取到的那幾行" 做反縮排  
Esc : 刪除游標所在的那一行，並將游標定位到上一行的尾端  
&emsp;  
# 架設環境的步驟 & 此程式的執行方法  
1.下載並安裝 Python 3.9.1 (此版本有內建pip)  
&emsp;  
2.打開命令列，輸入下列指令來安裝 PyQt5  
pip install PyQt5  
&emsp;  
3.架設好環境後，雙擊 QText.pyw  
&emsp;  
# 編輯TXT檔  
![image](https://github.com/Jacky20200711/QText/blob/master/DEMO_01.PNG?raw=true)  
&emsp;  
# 執行PY檔  
![image](https://github.com/Jacky20200711/QText/blob/master/DEMO_02.PNG?raw=true)  
&emsp;  

