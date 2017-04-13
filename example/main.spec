# -*- mode: python -*-
from kivy.deps import sdl2, glew
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal
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
