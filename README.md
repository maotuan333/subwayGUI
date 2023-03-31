# subwayGUI

-organize & track experiment files


-launch processing steps by click


-databasing experimental progress


-visualize quality control metrics

### Initial design

<p float="left">
<img width="300" alt="overall schema" src="https://user-images.githubusercontent.com/80687346/214458451-e9af97db-cee1-4b37-9138-ee3697302777.png"/>
<img width="600" alt="schema builder design" src="https://user-images.githubusercontent.com/80687346/214458551-32c90746-8677-49a0-b5d6-3704d0ba8e72.png"/></p>

### Current Interface: 
This is the first version in daily use in our lab - more bug fixes and updates coming soon
![image](https://user-images.githubusercontent.com/80687346/229228642-bb0f1343-0e23-4da6-b287-1d9c3e6843b5.png)



How to package:

```
cd C:\Users\damao\PycharmProjects\subway 
pyinstaller main.py --windowed --paths C:\Users\damao\PycharmProjects\subway --onefile --add-data "static;static" --add-data "data;data" 
cp 
```



How to run:

1. Download dist.zip
2. unzip in local folder
3. click main.exe

