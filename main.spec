# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\razan\\Desktop\\ING 3\\Compilation\\tp\\projet_compilation\\interface\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\razan\\Desktop\\ING 3\\Compilation\\tp\\projet_compilation\\interface', 'interface'), ('C:\\Users\\razan\\Desktop\\ING 3\\Compilation\\tp\\projet_compilation\\analyser', 'analyser'), ('C:\\Users\\razan\\Desktop\\ING 3\\Compilation\\tp\\projet_compilation\\docs', 'docs')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
