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

    return paths


def add_execute_permissions(filename):

    if platform.system() != 'Linux':
        raise OSError("This method should only be used on Linux")

    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)


def create_init_all(current_os, paths):

    current_dir = os.getcwd()

    if current_os == 'Windows':
        with open('init_all.bat', 'w') as file_:
                
            for path in paths:
                module_path = f'{current_dir}\\{path}'
                
                file_.write(f'cd {module_path}\n')
                file_.write('python -m venv venv\n')
                file_.write(f'call {module_path}\\venv\\Scripts\\activate\n')
                file_.write('pip install -r requirements.txt\n')
                file_.write(f'python {module_path}\\init_script.py\n')
                file_.write(f'call {module_path}\\venv\\Scripts\\deactivate\n\n')

            file_.write('\nPAUSE')

    elif current_os == 'Linux':
        with open('init_all.sh', 'w') as file_:
            for path in paths:
                module_path = f'{current_dir}/{path}'
                
                file_.write(f'cd {module_path}\n')
                file_.write('python3 -m venv venv\n')
                file_.write(f'. ./venv/bin/activate\n')
                file_.write('pip install -r requirements.txt\n')
                file_.write(f'python ./init_script.py\n')
                file_.write(f'. ./venv/bin/deactivate\n\n')

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
