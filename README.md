# subwayGUI

### [beta version demo (1min)](https://drive.google.com/file/d/1UIVzM4W5C5yggjuARPqGQmIT5MTb1Pwq/view?usp=sharing)
Current:
-organize & track experiment files
TODO:
-launch processing steps by click
-visualize quality control metrics

### Initial design

<p float="left">
<img width="300" alt="overall schema" src="https://user-images.githubusercontent.com/80687346/214458451-e9af97db-cee1-4b37-9138-ee3697302777.png"/>
<img width="600" alt="schema builder design" src="https://user-images.githubusercontent.com/80687346/214458551-32c90746-8677-49a0-b5d6-3704d0ba8e72.png"/></p>

### Current Interface:

This is the first version in use - more bug fixes and updates coming soon

![image-20230331172117450](https://user-images.githubusercontent.com/80687346/229245566-d3425ada-3064-48c2-acdb-73962bb75228.png)

=======


How to package:

```shell
cd C:\Users\damao\PycharmProjects\subway # open project folder
pyinstaller main.py --windowed --paths C:\Users\damao\PycharmProjects\subway --onefile --add-data "static;static" # package exe
xcopy data dist\data /s/i/y # package program data
dist\main # run .exe
```



How to run:

1. Download dist.zip
2. unzip in local folder
3. click main.exe

