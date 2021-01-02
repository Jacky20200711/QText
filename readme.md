# 程式用途  
自製的簡易編輯器，用來取代記事本 & 撰寫 Python 腳本。  
&emsp;  
# 開發環境  
Win10(64bit) + Python 3.8.5 + PyQt5  
&emsp;  
# 架構簡述  
總共有六個類別(QMain、QButton、QLine、QText、QGridLayout、QHighlighter)  
QMain 為主程式的視窗，也是其餘五個類別的 Parent  
QGridLayout 用來控制 QButton、QLine、QText 在 QMain 中的擺放位置  
QHighlighter 用來協助 QText 產生語法高亮  
&emsp;  
# 功能說明  
1.遇到 Python 的 "Keyword" 和 "Operator" 會產生語法高亮  
2.功能鍵和組合鍵  
F1 : 顯示或隱藏[開啟其它檔案的按鈕]，按鈕需要到F10設定有效的檔案路徑後才能使用  
F2 : 放大或縮小視窗  
F3 : 往下搜尋字串(往上為Alt+F3)  
F4 : 嘗試用 Chrome 開啟游標所在那一行的網址 or 檔案(路徑必須完整且獨佔一行)  
F5 : 執行自己(副檔名必須為py或pyw)  
F10: 開啟設定檔(可以在此設定視窗大小、視窗位置、ICON路徑、按鈕的名稱和對應檔案的路徑)  
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
Alt + L  : 延伸行數(預設的行數只有到3000，可用此功能來延伸行數)  
Enter : 插入新行並與上一行的第1個字元對齊  
Enter + shift : 效果如一般的 Enter  
Tab : 插入4個空白字元 or 將 "被選取到的那幾行" 做縮排  
Tab + shift : 將 "被選取到的那幾行" 做反縮排  
Esc : 刪除游標所在的那一行，並將游標定位到上一行的尾端  
&emsp;  
# 架設環境的步驟 & 此程式的執行方法  
1.下載並安裝 Python3.8.5 (此版本有內建pip)  
&emsp;  
2.打開命令列，使用以下指令安裝各個套件  
pip install PyQt5  
pip install sip  
&emsp;  
3.到以下網址下載"pygame-1.9.6-cp38-cp38-win_amd64.whl"  
http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame  
&emsp;  
4.將命令列的路徑切換到該whl檔案所在的資料夾，然後輸入以下指令  
pip install pygame-1.9.6-cp38-cp38-win_amd64.whl  
&emsp;  
5.架設好環境後，雙擊 QText.pyw  
&emsp;  
# 編輯TXT檔  
![image](https://github.com/Jacky20200711/QText/blob/master/DEMO_01.PNG?raw=true)  
&emsp;  
# 執行PY檔  
![image](https://github.com/Jacky20200711/QText/blob/master/DEMO_02.PNG?raw=true)  
&emsp;  
# 按F10開啟設定檔並設定按鈕  
![image](https://github.com/Jacky20200711/QText/blob/master/DEMO_03.PNG?raw=true)  
&emsp;  
