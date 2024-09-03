导出依赖
pip freeze > requests.txt
下载依赖
pip3 install -r requests.txt

pip freeze > requests.txt
pip3 install -r requests.txt
将Python脚本打包为Windows可执行文件（.exe）可以使用PyInstaller等工具。PyInstaller允许您从Python脚本创建独立的可执行文件，包括所有必要的依赖项。

以下是使用PyInstaller将您的脚本打包的步骤：

1. 在命令提示符或终端中运行以下命令安装PyInstaller：
   ```
   pip install pyinstaller
   ```

2. 安装完PyInstaller后，进入存放您的脚本（`bilibili_album.py`）的目录。

3. 运行以下命令创建可执行文件：
   ```
   pyinstaller --onefile bilibili_album.py
   ```

   这个命令告诉PyInstaller从您的脚本（`bilibili_album.py`）创建一个单独的可执行文件（`--onefile`）。

4. 命令完成后，您会在与脚本相同的位置找到一个名为`dist`的目录。在`dist`目录中，您会找到打包好的可执行文件（`bilibili_album.exe`）。

现在，您可以将`bilibili_album.exe`文件分发给其他人，在他们的Windows计算机上运行，而无需安装Python或任何依赖项。

注意：PyInstaller将您的脚本及其依赖项打包到一个可执行文件中，但由于包含了Python解释器和库，生成的文件可能仍然相对较大。