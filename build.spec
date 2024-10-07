from PyInstaller.utils.hooks import collect_all, collect_submodules, collect_dynamic_libs

# Collect all necessary files and dependencies
datas = collect_all('mediapipe')[0]
hiddenimports = []
binaries = []

# Collect submodules for third-party packages
hiddenimports += collect_submodules('mediapipe')
hiddenimports += collect_submodules('pygame')
hiddenimports += collect_submodules('pymunk')
hiddenimports += collect_submodules('torch')
hiddenimports += collect_submodules('numpy')

# Collect dynamic libraries for third-party packages
binaries += collect_dynamic_libs('mediapipe')
binaries += collect_dynamic_libs('pygame')
binaries += collect_dynamic_libs('pymunk')
binaries += collect_dynamic_libs('torch')
binaries += collect_dynamic_libs('numpy')

# Define the Analysis, PYZ, EXE, and COLLECT classes
a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Physis Reality',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Physis Reality',
)
