
kivy程序打包成exe
===

该打包方案仅用于1.9.1及以上版本，打包成的exe是32位还是64位取决于Python的位数。
<font color=red>打包务必在administrator权限下进行，打包路径以及文件名都不能出现中文，否则在一些情况下会出现访问拒绝、编码错误导致打包失败。</font>


## 0x01要求环境

>kivy 1.9.1+
>pyinstaller 3.1+


## 0x02打包步骤

### 安装必要的包

>```pip install pyinstaller```

>```pip install pycrypto```		#这可能会提示编译错误，要先安装vcforPython27 (<http://aka.ms/vcpython27>)


### 打包命令

>```pyi-makespec –F main.py```	
>
>\#生成spec文件，这里注意一点，要根据入口代码所在的文件名来生成spec，不过这条命令并不会检查当前目录下到底是否存在main.py文件，-F表示生成单一exe文件的spec，与多文件exe的spec不同的是没有collect段，生成的spec文件如下：

```
    # -*- mode: python -*-
    
    block_cipher = None
    
    a = Analysis(['main.py'],
                	pathex=['E:\\NEW\\gardenproj\\mapviewtest'],
                	binaries=[],
                	datas=[],
                	hiddenimports=[],
                	hookspath=[],
                	runtime_hooks=[],
                	excludes=[],
                	win_no_prefer_redirects=False,
                	win_private_assemblies=False,
                	cipher=block_cipher)
    pyz = PYZ(a.pure, a.zipped_data,
    	              cipher=block_cipher)
    exe = EXE(pyz,
                  a.scripts,
                  a.binaries,
                  a.zipfiles,
                  a.datas,
                  name='main',
                  debug=False,
                  strip=False,
                  upx=True,
                  console=True )
```
>spec事实上是个py文件，所以可以使用import等py语法，为了让pyinstaller正确的打包kivy，需要做些修改，这些修改来自kivy官方文档：(<https://kivy.org/docs/guide/packaging-windows.html> )，修改后的完整spec如下：

```    
    from kivy.deps import sdl2, glew
    from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal,hookspath
    from PyInstaller.utils.hooks import collect_submodules
    
    block_cipher = None
    
    excludekivy = get_deps_minimal(video=None, audio=None,spelling=None,camera=None)['excludes']
    
    a = Analysis(['main.py'],
                pathex=[r'E:\NEW\gardenproj\mapviewtest'],
                binaries=[],
                hiddenimports=collect_submodules('kivy.garden'),
                hookspath=[],
                runtime_hooks=[],
                win_no_prefer_redirects=False,
                win_private_assemblies=False,
                cipher=block_cipher,
                excludes = excludekivy)
    
     
    pyz = PYZ(a.pure, a.zipped_data,
                cipher=block_cipher)
     
    exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
            name='main',
            debug=False,
            strip=False,
            upx=True,
            console=False )
```
修改包括三个部分

- 第一是`from kivy.deps import sdl2, glew`，在EXE类参数中添加`*[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)]`。
- 第二是导入get_deps_minimal，使用该函数获取可以排除的kivy模块列表，这个函数返回一个字典，传给Analysis类的excludes参数后就可以把指定的模块排除掉，减小exe体积。get_deps_minimal的具体参数可以参考kivy 1.9.1及以上版本的文档。
- 第三是导入collect_submodules，这个函数可以自动解析Python包并返回包里所包含的模块，将无法被pyinstaller自动识别打包的模块通过这种方法获取模块并传给Analysis类的hiddenimports参数即可。

注意：kivy.garden的模块必须使用命令`garden install –kivy mapview`来安装，加上—kivy参数garden.mapview才会安装在Python安装目录下，否则默认是安装在C:\Users\用户名\.kivy\garden下。

>```pyinstaller main.spec```

将会在当前目录下生成build、dist两个目录，打包成的exe位于dist下，build\main下有个warnmain.txt文件，记录了打包过程中出现的警告和错误，可以看到哪些模块没有被打包进去。


### 调试exe

>```pyi-archive_viewer -b main.exe```

会输出所有exe中存在的模块，可以方便查看是否包含了想要打包进的模块，可以排除程序不能正常运行时的原因。


# 0x03总结
kivy打包exe的完整命令是这样的

>```pyi-makespec –F main.py```
>```pyinstaller main.spec```

如果你想让这个过程自动化点，可以把上面的命令写入bat文件，pyinstaller打包的输出比较长，为了方便查看可以输出到txt中，可以把如下命令保存为packet.bat：

>```pyinstaller main.spec > package.txt 2>&1```
>```pause```

这样就会在当前目录生成一个package.txt包含了打包命令输出内容。同样可以在dist目录下建立一个调试批处理debug.bat：

>```pyi-archive_viewer -b main.exe > 1.txt```


我已经把例子代码和spec上传到当前版本库（看上面↑），大家可以直接下载测试，有任何问题欢迎issue，如果你觉得我写的好的话，可以给我star哦。
