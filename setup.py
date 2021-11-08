import cx_Freeze

executables = [cx_Freeze.Executable("Graphics.py")]

cx_Freeze.setup(
    name="Casino Game",
    options = {"build_exe": {"packages": ["pygame", "pygame_widgets"]}},
    executables = executables
)