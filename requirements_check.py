from importlib.metadata import version, PackageNotFoundError

REQUIRED_PACKAGES = [
    'camelot-py==0.11.0',
    'customtkinter==5.1.3',
    'ghostscript==0.7',
    'matplotlib==3.7.1',
    'numpy==1.24.3',
    'openpyxl==3.1.2',
    'pandas==2.0.2',
    'Pillow==9.5.0',
    'PyMuPDF==1.22.3',
    'python-dateutil==2.8.2',
    'pywin32==306',
]


def check_requirements():
    all_requirements_met = True
    for package_version in REQUIRED_PACKAGES:
        package, required_version = package_version.split('==')
        try:
            installed_version = version(package)
            if installed_version != required_version:
                print(
                    f'{package} has a different version installed: {installed_version}. Required version: {required_version}')
                all_requirements_met = False
            else:
                print(f'{package} ({installed_version}) is installed')
        except PackageNotFoundError:
            print(f'{package} is NOT installed')
            all_requirements_met = False

    if not all_requirements_met:
        print("Please install the missing packages and run the script again.")
        exit(1)

