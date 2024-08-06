import sys
from setuptools import setup, find_packages, Command

# Platform-specific dependencies
if sys.platform.startswith('linux'):
    platform_dependencies = [
        "python-xlib",
        "opencv-python",
        "pytesseract",
        "pyautogui",
    ]
elif sys.platform == 'darwin':
    platform_dependencies = [
        "pyobjc",
    ]
elif sys.platform == 'win32':
    platform_dependencies = [
        "pywin32",
        "pyautogui",
    ]
else:
    platform_dependencies = []

# Social media related dependencies
social_media_dependencies = [
    "tweepy",
    # Add other social media related dependencies here
]

class InstallPlatformDependencies(Command):
    description = 'Install platform-specific dependencies'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess

        if sys.platform.startswith('linux'):
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements-linux.txt'])
        elif sys.platform == 'darwin':
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements-mac.txt'])
        elif sys.platform == 'win32':
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements-windows.txt'])

setup(
    name="autobyteus_community_tools",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=platform_dependencies + social_media_dependencies,
    extras_require={
        "dev": [
            "pytest",
            "flake8",
            "black",
        ],
    },
    python_requires=">=3.8",
    author="Ryan Zheng",
    author_email="ryan.zheng.work@example.com",
    description="Community tools including OS-specific and social media libraries for autobyteus",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/autobyteus_community_tools",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    package_data={
        "autobyteus_community_tools.social_media_poster.weibo": [
            "images/open_file_button_template.png",
            "images/downloads_folder_button.png"
        ],
    },
    cmdclass={
        'install_platform_deps': InstallPlatformDependencies,
    },
)