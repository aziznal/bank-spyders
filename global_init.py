import platform
import os
import stat


def get_paths(current_os):

    current_dir = os.getcwd()

    paths = [
        "isbank-spyder",
        "kuveytturk-spyder",
        "vakifbank-spyder",
        "yapikredi-spyder",
        "ziraat-spyder"
    ]

    if current_os == 'Windows':
        paths = [f'{current_dir}\\{path}\\init_script.py' for path in paths]

    elif current_os == 'Linux':
        paths = [f'{current_dir}/{path}/init_script.py' for path in paths]

    return paths


def add_execute_permissions(filename):

    if platform.system() != 'Linux':
        raise OSError("This method should only be used on Linux")

    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)


def create_init_all(os, paths):
    if os == 'Windows':
        with open('init_all.bat', 'w') as file_:
            for path in paths:
                file_.write(f'call {path}\n')

    elif os == 'Linux':
        with open('init_all.sh', 'w') as file_:
            for path in paths:
                file_.write(f'sh -x {path}\n')

        add_execute_permissions("init_all.sh")


def init_windows(paths):
    create_init_all('Windows', paths)


def init_linux(paths):
    create_init_all('Linux', paths)


if __name__ == "__main__":

    current_os = platform.system()

    if current_os == 'Windows':
        paths = get_paths('Windows')
        init_windows(paths)

    elif current_os == 'Linux':
        paths = get_paths('Linux')
        init_linux(paths)

    else:
        raise OSError('Unsupported OS')
