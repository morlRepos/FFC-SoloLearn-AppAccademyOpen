import unittest;

class TestSomeStuff(unittest.TestCase):
    """
    This is a test case, something run by both unittest
    and pytest.
    """

    def setUp(self):
        """The setUp method runs before each test."""
        pass

    def tearDown(self):
        """The tearDown method runs after each test."""
        pass

    def test_some_thing(self):
        """
        All methods that begin with "test_" are run as
        unit tests. Do your assertions in here so that
        the test runner will capture them.
        """
        pass
    def test_returns_3(self):
        result = 3
        self.assertEqual(result, 3)

suite_loader = unittest.TestLoader()
suite = suite_loader.loadTestsFromTestCase(TestSomeStuff)
runner = unittest.TextTestRunner()
runner.run(suite)

"""
assertEqual(a, b)	        a == b
assertNotEqual(a, b)	    a != b
assertTrue(x)	            bool(x) is True
assertFalse(x)	            bool(x) is False
assertIs(a, b)	            a is b
assertIsNot(a, b)	        a is not b
assertIsNone(x)	            x is None
assertIsNotNone(x)	        x is not None
assertIn(a, b)	            a in b
assertNotIn(a, b)	        a not in b
assertIsInstance(a, b)	    isinstance(a, b)
assertNotIsInstance(a, b)	not isinstance(a, b)
"""
