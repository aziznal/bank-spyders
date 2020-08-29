import platform
import os
import stat


paths = [
    "./isbank-spyder",
    "./kuveytturk-spyder",
    "./vakifbank-spyder",
    "./yapikredi-spyder",
    "./ziraat-spyder"
]

current_os = platform.system()


def add_execute_permissions(filename):

    if platform.system() != 'Linux':
        raise OSError("This method should only be used on Linux")

    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)


def create_exec_file(os, commands):
    if os == 'Windows':
        with open('exec.bat', 'w') as exec_file:
            [exec_file.write(line + "\n") for line in commands]

    elif os == 'Linux':
        with open('exec.sh', 'w') as exec_file:
            [exec_file.write(line + "\n") for line in commands]

        add_execute_permissions('exec.sh')


def get_commands(os):
    if os == 'Windows':

        # TODO: set these up while in a windows os
        # IDEA: use multithreading to launch all exec.bat files at once?
        commands = []

        for path in paths:
            subcommands = [
                f"cd {path}",
                "call venv/Scripts/activate",
                "python init_script.py",
                "call exec.bat"
            ]

            commands.append(subcommands)

    elif os == 'Linux':
        commands = []

        for path in paths:
            pass


def init_windows():

    commands = get_commands('Windows')

    create_exec_file('Windows', commands)


def init_linux():

    commands = get_commands('Linux')

    create_exec_file('Linux', commands)


if __name__ == "__main__":

    if current_os == 'Windows':
        init_windows()

    elif current_os == 'Linux':
        init_linux()

    else:
        raise OSError('Unsupported OS')
