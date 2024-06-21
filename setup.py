from setuptools import setup

setup(
    name='Testy',
    version='0.1',
    py_modules=['Application', 'dbConnection', 'server'],
    install_requires=[
        'mysql-connector-python',
    ],
    entry_points={
        'console_scripts': [
            'Testy=Application:main',
        ],
    },
    author="APU UCDF2208ICT(SE) SDP Team 17",
    author_email='zokeyot2004@gmail.com',
    description='Gamification E-Learning System',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ZokeYot/APU_SDP_BE',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)