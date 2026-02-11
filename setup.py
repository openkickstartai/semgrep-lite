from setuptools import setup, find_packages
setup(name='semgrep-lite', version='0.1.0', packages=find_packages(),
    install_requires=['click>=8.0','pyyaml>=6.0','rich>=13.0'],
    entry_points={'console_scripts':['semgrep-lite=semgrep_lite.cli:main']}, python_requires='>=3.9')
