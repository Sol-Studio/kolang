from setuptools import setup, find_packages
# build : python setup.py sdist bdist_wheel
# pip : python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
# test.pip : python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
setup(
      name='kolang',
      version=open("kolang/version.txt", "r", encoding="utf-8").read(),
      url='https://github.com/Sol-Studio/kolang',
      author='Sol-Studio', # 작성자
      author_email='dev.sol.studio@gmail.com', # 작성자 이메일
      description='코랭!', # 간단한 설명
      packages=find_packages(exclude=['']),
      keywords=[],
      long_description=open('README.md', encoding="utf-8").read(),
      install_requires=[],
      package_data={'': ['*.txt']},
      entry_points={
            'console_scripts': [
                  'kolang=kolang.main:main',
            ],
      },
      python_requires='==3.8.7',
)