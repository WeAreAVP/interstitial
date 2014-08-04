# -*- mode: python -*-
a = Analysis(['Main.py'],
             pathex=['C:\\PyInstaller\\pyinstaller.py'],
             hiddenimports=[],
             hookspath=None)
for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break
a.datas += [('assets\\logo_sign_small.png', 'assets\\logo_sign_small.png','DATA')]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles, 
          a.datas,
          name=os.path.join('dist', 'Interstitail.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='assets\\icon.ico')
app = BUNDLE(exe,
             name=os.path.join('dist', 'Interstitail.exe.app'))



