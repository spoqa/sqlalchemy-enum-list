import ast
import os.path
import sys

from setuptools import setup, __version__ as setuptools_version


def readme():
    try:
        with open('README.rst') as f:
            readme = f.read()
    except IOError:
        pass
    return readme


def get_version():
    module_path = os.path.join(os.path.dirname(__file__),
                               'sqlalchemy_enum_list.py')
    module_file = open(module_path)
    try:
        module_code = module_file.read()
    finally:
        module_file.close()
    tree = ast.parse(module_code, module_path)
    for node in ast.iter_child_nodes(tree):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target, = node.targets
        if isinstance(target, ast.Name) and target.id == '__version__':
            return node.value.s


setup_requires = []
install_requires = ['six', 'SQLAlchemy >= 0.8.0']
tests_require = ['tox', 'pytest']
below34_requires = ['enum34 >= 1.1.6']
extras_require = {'tests': tests_require}


if 'bdist_wheel' not in sys.argv and sys.version_info < (3, 5):
    install_requires.extend(below34_requires)
if tuple(map(int, setuptools_version.split('.'))) < (17, 1):
    setup_requires = ['setuptools >= 17.1']
    extras_require.update({
        ":python_version=='3.4'": below34_requires,
        ":python_version=='3.3'": below34_requires,
        ":python_version=='3.2'": below34_requires,
        ":python_version=='2.7'": below34_requires,
    })
else:
    extras_require.update({":python_version<'3.5'": below34_requires})


setup(
    name='SQLAlchemy-Enum-List',
    description='',
    long_description=readme(),
    version=get_version(),
    setup_requires=setup_requires,
    url='https://github.com/spoqa/sqlalchemy-enum-list',
    author='Kang Hyojun',
    author_email='iam.kanghyojun' '@' 'gmail.com',
    license='MIT License',
    py_modules=['sqlalchemy_enum_list'],
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: SQL',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development',
    ]
)
