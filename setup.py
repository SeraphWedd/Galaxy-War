#on cmd type: python setup.py build

from cx_Freeze import setup, Executable
includefiles = ['Resources', #Add Images and Music here
                'readme.md']

excludes = ['scipy', 'numpy']
packages = [#"Scripts", #Local Scripts
    "pygame", "math", "sys", "os", "threading"]#Python Packages

target = Executable(script='call_of_war_clone.py',
                    base='WIN32GUI', #None if console only
                    targetName='game',
                    shortcutName='Call of War Clone',
                    icon=None) #Place your path to the game's icon

setup(
    name = 'Game Name',#
    version = '1.0.0',#
    description = 'Description.',#
    author = 'Seraph Wedd', #
    author_email = 'seraphwedd18@gmail.com', #
    options = {'build_exe': {'zip_include_packages':packages,
                             'include_files':includefiles,
                             'excludes':excludes}},
    executables = [target]
    )
