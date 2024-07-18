I write a python file to read the serial data from arduino into an excel on computer
## How to use?
1. make sure you have install python in your computer
2. run start.bat
3. do not turn on other serial moniter !!! once the file is running, it keep recording
4. the Arduino output should be in a line with commas to split them, different group should in different lines
5. any serial data is ok, you can change the serial output format into excel
## GUI version
get into the command line and enter
```python
pip install pyinstaller pyQt
```
then use pyinstaller to package the python file into exe
```python
pyinstaller --onefile --noconsole serialdata_withgui.py
```
then the exe file is in ./dst, it must in this dictionary to run
