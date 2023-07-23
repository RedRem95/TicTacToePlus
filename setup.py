import setuptools
import os

with open(os.path.join(os.path.dirname(__file__), "TicTacToePlus", "version.txt"), "r") as fv:
    __version__ = fv.read().strip()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fr:
    requirements = [x.strip() for x in fr.readlines() if len(x.strip()) > 0]

setuptools.setup(
    name="TicTacToePlus",
    version=__version__,
    author="RedRem95",
    description="An advanced game of tictactoe. With the possibility to train agents using reinforcement learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license_files=('LICENSE',),
    url="https://github.com/RedRem95/TicTacToePlus",
    project_urls={
        "Bug Tracker": "https://github.com/RedRem95/TicTacToePlus/issues",
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: GPL 3",
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        'console_scripts': [
            'play_tttp = TicTacToePlus.entries.play:main',
            'train_tttp = TicTacToePlus.entries.train:main',
        ],
    },
    keywords="reinforcement-learning-algorithms reinforcement-learning machine-learning "
             "gymnasium gym stable baselines toolbox python data-science",
    packages=setuptools.find_packages(include=['TicTacToePlus', 'TicTacToePlus.*']),
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    package_data={"TicTacToePlus": ["version.txt"]},
)
