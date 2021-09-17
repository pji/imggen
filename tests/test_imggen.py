"""
test_imggen
~~~~~~~~~~~

Unit tests for the imggen.imggen module.
"""
import unittest as ut

from imggen import imggen as r


# Test cases.
class SerializableTestCase(ut.TestCase):
    def test_asdict(self):
        """The Serializable.asdict method should return the class's
        public attributes as a dictionary that can be used as keyword
        arguments to initialize a new instance of the class.
        """
        # Expected values.
        exp = {
            'spam': 1,
            'eggs': 2,
        }

        # Test data and state.
        class Bacon(r.Serializable):
            def __init__(self, spam, eggs):
                self.spam = spam
                self.eggs = eggs

        # Run test.
        bacon = Bacon(**exp)
        act = bacon.asdict()

        # Determine test results.
        self.assertDictEqual(exp, act)

    def test_asargs(self):
        """The Serializable.asargs method should return the class's
        public attributes as a tuple that can be used as positional
        arguments to initialize a new instance of the class.
        """
        # Expected values.
        exp = (1, 2)

        # Test data and state.
        class Bacon(r.Serializable):
            def __init__(self, spam, eggs):
                self.spam = spam
                self.eggs = eggs

        # Run test.
        bacon = Bacon(*exp)
        act = bacon.asargs()

        # Determine test results.
        self.assertTupleEqual(exp, act)

    def test_equal(self):
        """Two instances of Serializable with the same parameter
        values should evaluate as equal when compared.
        """
        # Test data and state.
        class Bacon(r.Serializable):
            def __init__(self, spam, eggs):
                self.spam = spam
                self.eggs = eggs

        kwargs = {
            'spam': 1,
            'eggs': 2,
        }
        a = Bacon(**kwargs)
        b = Bacon(**kwargs)

        # Run test and determine result.
        self.assertTrue(a == b)

    def test_equal_not_equal(self):
        """Two instances of Serializable with the different parameter
        values should evaluate as not equal when compared.
        """
        # Test data and state.
        class Bacon(r.Serializable):
            def __init__(self, spam, eggs):
                self.spam = spam
                self.eggs = eggs

        a = Bacon(1, 2)
        b = Bacon(1, 3)

        # Run test and determine result.
        self.assertFalse(a == b)

    def test_equal_with_other_class(self):
        """When comparing the equality of a Serializable subclass
        with a different class, the Serializable should return
        NotImplemented.
        """
        # Expected value.

        # Test data and state.
        class Bacon(r.Serializable):
            was_tested = False

            def __eq__(self, other):
                self.was_tested = True
                return super().__eq__(other)

            def __init__(self, spam, eggs):
                self.spam = spam
                self.eggs = eggs

        class Sausage:
            was_tested = False

            def __eq__(self, other):
                self.was_tested = True
                return False

        kwargs = {
            'spam': 1,
            'eggs': 2,
        }
        a = Bacon(**kwargs)
        b = Sausage()

        # Run test and determine result.
        _ = a == b

        # Determine test results.
        self.assertTrue(a.was_tested)
        self.assertTrue(b.was_tested)

    def test_repr(self):
        """Serializable objects should return a string useful for
        troubleshooting when coerced into a string.
        """
        # Expected value.
        exp = 'Bacon(spam=1, eggs=2)'

        # Test data and state.
        class Bacon(r.Serializable):
            def __init__(self, spam, eggs):
                self.spam = spam
                self.eggs = eggs

        bacon = Bacon(1, 2)

        # Run test.
        act = repr(bacon)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_repr_with_many_parameters(self):
        """Serializable objects with a large number of parameters
        should truncate the parameter list when creating a
        representative string.
        """
        # Expected value.
        exp = "Bacon(spam='0123...556575859')"

        # Test data and state.
        class Bacon(r.Serializable):
            def __init__(self, spam):
                self.spam = spam

        spam = ''.join(str(n) for n in range(60))
        bacon = Bacon(spam)

        # Run test.
        act = repr(bacon)

        # Determine test result.
        self.assertEqual(exp, act)

    def test_repr_with_string_value(self):
        """Serializable objects should return a string useful for
        troubleshooting when coerced into a string. String values
        in the arguments should be properly quoted.
        """
        # Expected value.
        exp = "Bacon(spam=1, eggs='2', sausage=b'3')"

        # Test data and state.
        class Bacon(r.Serializable):
            def __init__(self, spam, eggs, sausage):
                self.spam = spam
                self.eggs = eggs
                self.sausage = sausage

        bacon = Bacon(1, '2', b'3')

        # Run test.
        act = repr(bacon)

        # Determine test result.
        self.assertEqual(exp, act)


class SourceTestCase(ut.TestCase):
    def test_fill_required(self):
        """Subclasses of Source must implement the fill method."""
        # Expected values.
        exp_ex = TypeError
        exp_msg = ("Can't instantiate abstract class Spam "
                   "with abstract method fill")

        # Test data and state.
        class Spam(r.Source):
            pass

        # Run test and determine result.
        with self.assertRaisesRegex(exp_ex, exp_msg):
            spam = Spam()
