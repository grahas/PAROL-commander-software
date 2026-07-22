# -*- mode: python ; coding: utf-8 -*-
#
# Build the PAROL commander GUI into a standalone application.
#
#   pyinstaller PAROL-commander.spec
#
# Produces a onedir build in dist/PAROL-commander/ containing the
# executable plus all bundled images, program scripts, and third-party
# data files (roboticstoolbox meshes, customtkinter themes, etc).

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

GUI_DIR = "GUI/files"

# Image/icon/program assets the app loads relative to its own directory
# at runtime (see Image_path in GUI_PAROL_latest.py et al). These need to
# land next to the executable's _MEIPASS root, so destination "." is used.
asset_datas = [
    (f"{GUI_DIR}/{name}", ".")
    for name in [
        "logo.ico",
        "logo.png",
        "logo_krug_viri.png",
        "help.png",
        "button_arrow_1.png",
        "cart_x_down.png",
        "cart_x_up.png",
        "cart_y.png",
        "cart_y_left.png",
        "cart_y_right.png",
        "cart_z.png",
        "cart_z_down.png",
        "cart_z_up.png",
        "RX_MINUS.png",
        "RX_PLUS.png",
        "RY_MINUS.png",
        "RY_PLUS.png",
        "RZ_MINUS.png",
        "RZ_PLUS.png",
    ]
]
asset_datas.append((f"{GUI_DIR}/Programs", "Programs"))

# Data files bundled inside third-party packages that PyInstaller's static
# analysis can't discover on its own (meshes, themes, web assets, etc).
package_datas = []
for pkg in [
    "customtkinter",
    "roboticstoolbox",
    "rtbdata",
    "spatialgeometry",
    "swift",
    "s_visual_kinematics",
]:
    package_datas += collect_data_files(pkg)

hidden_imports = [
    # PIL.ImageTk looks this helper module up dynamically at runtime to
    # locate the _tkinter C extension; PyInstaller's static analysis
    # can't see that reference, so without this the app crashes as soon
    # as it tries to render its first PhotoImage-backed button.
    "PIL._tkinter_finder",
]
for pkg in ["roboticstoolbox", "spatialgeometry", "swift", "s_visual_kinematics"]:
    hidden_imports += collect_submodules(pkg)

a = Analysis(
    [f"{GUI_DIR}/Serial_sender_good_latest.py"],
    pathex=[GUI_DIR],
    binaries=[],
    datas=asset_datas + package_datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="PAROL-commander",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    # Keep a console window: the app logs connection/robot status via
    # `logging`/`print`, which is otherwise invisible to the user.
    console=True,
    icon=f"{GUI_DIR}/logo.ico" if sys.platform == "win32" else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="PAROL-commander",
)
