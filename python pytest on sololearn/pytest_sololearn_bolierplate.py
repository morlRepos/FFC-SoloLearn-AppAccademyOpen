import subprocess,sys

DEBUG_ON = False
if(DEBUG_ON):
    print(dir(subprocess))
    print(dir(sys))

    import pip
    help(pip)

    def ignoreWarning():
        pass
        #version not high enough.
        ##subprocess.call([sys.executable, "-m","pip","--root-user-action=ignore", "install"])
        ##pip install --root-user-action=ignore
    ignoreWarning()

def install(package):
    subprocess.call([sys.executable, "-m","pip","--disable-pip-version-check","-q", "install", package])
install('pytest')

import pytest
from pytest import mark

############################################################
#Tests Go Here.
class TestClass:
    def setup_function(fn):
        """The setup_function function runs before each test."""
        pass

    def teardown_function(fn):
        """The teardown_function function runs after each test."""
        pass

    #def testWhateverYouWant(self):
    #    """This is a unit test because it beings with "test"."""
    #    pass

    #def test_whatever_you_want(self):
    #    """This is a unit test because it beings with "test"."""
    #    pass

    def test_reverso_basic(self):
        result = reverso("ABCD")
        assert result == "DCBA"

    @mark.parametrize("s,expected", [("ABCD", "DCBZ"), ("ABC", "CBA"), ("", "")])
    def test_reverso(self, s, expected):
        result = reverso(s)
        assert result == expected

    def test_for_3(self):
        result = 3
        assert True == True

class MyPlugin:
    def pytest_sessionfinish(self):
        print("\n*** test run reporting finishing")

#Functions To Test Etc.
def reverso(a_string):
    return a_string[::-1]
#print(reverso("abcd"))
############################################################

if(DEBUG_ON):
    import os
    print(os.path.dirname(os.path.abspath(__file__)))
    print(os.path.abspath(os.getcwd()))
    import pathlib
    print(pathlib.Path(__file__).parent.resolve())
    print(pathlib.Path().resolve())
    print(os.path.basename(__file__))
    print(__file__)

if __name__ == "__main__":
    pytest_args = ['./file0.py']  #['-x','./file0.py']

    print("In Main:")
    retcode = pytest.main(pytest_args, plugins=[MyPlugin()])

############################################################
