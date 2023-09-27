"""
test_examples
~~~~~~~~~~~~~

Unit tests for the example scripts for :mod:`imggen`.
"""
from subprocess import run


# Common test code.
def compare_files(a, b):
    """Compare the contents of two binary files."""
    with open(a, 'rb') as fh:
        a_content = fh.read()
    with open(b, 'rb') as fh:
        b_content = fh.read()
    assert a_content == b_content


# Test cases.
class TestNoisy:
    def test_coscurtains(self, tmp_path):
        """When coscurtains is invoked, `noisy.py` should write one-
        dimensional cosine unit noise (cosine curtains) to the given
        file.
        """
        fname = '__test_noisy_coscurtains.jpg'
        expected = f'tests/data/{fname}'
        actual = tmp_path / fname

        run([
            'python',
            'examples/noisy.py',
            'coscurtains',
            '-s', 'spam',
            '640', '480',
            actual
        ])
        compare_files(actual, expected)

    def test_curtains(self, tmp_path):
        """When curtains is invoked, `noisy.py` should write one-
        dimensional unit noise (curtains) to the given file.
        """
        fname = '__test_noisy_curtains.jpg'
        expected = f'tests/data/{fname}'
        actual = tmp_path / fname

        run([
            'python',
            'examples/noisy.py',
            'curtains',
            '-s', 'spam',
            '640', '480',
            actual
        ])
        compare_files(actual, expected)

    def test_noise(self, tmp_path):
        """When noise is invoked, `noisy.py` should write random pixel
        noise to the given file.
        """
        fname = '__test_noisy_noise.jpg'
        expected = f'tests/data/{fname}'
        actual = tmp_path / fname

        run([
            'python',
            'examples/noisy.py',
            'noise',
            '-s', 'spam',
            '640', '480',
            actual
        ])
        compare_files(actual, expected)

    def test_coscurtains(self, tmp_path):
        """When ocoscurtains is invoked, `noisy.py` should write
        octave one-dimensional cosine unit noise (cosine curtains)
        to the given file.
        """
        fname = '__test_noisy_ocoscurtains.jpg'
        expected = f'tests/data/{fname}'
        actual = tmp_path / fname

        run([
            'python',
            'examples/noisy.py',
            'ocoscurtains',
            '-s', 'spam',
            '640', '480',
            actual
        ])
        compare_files(actual, expected)

    def test_ocurtains(self, tmp_path):
        """When ocurtains is invoked, `noisy.py` should write octave
        one-dimensional unit noise (curtains) to the given file.
        """
        fname = '__test_noisy_ocurtains.jpg'
        expected = f'tests/data/{fname}'
        actual = tmp_path / fname

        run([
            'python',
            'examples/noisy.py',
            'ocurtains',
            '-s', 'spam',
            '640', '480',
            actual
        ])
        compare_files(actual, expected)

    def test_operlin(self, tmp_path):
        """When operlin is invoked, `noisy.py` should write octave
        perlin noise to the given file.
        """
        fname = '__test_noisy_operlin.jpg'
        expected = f'tests/data/{fname}'
        actual = tmp_path / fname

        run([
            'python',
            'examples/noisy.py',
            'operlin',
            '-s', 'spam',
            '640', '480',
            actual
        ])
        compare_files(actual, expected)

    def test_ounitnoise(self, tmp_path):
        """When ounitnoise is invoked, `noisy.py` should write octave
        unit noise to the given file.
        """
        fname = '__test_noisy_ounitnoise.jpg'
        expected = f'tests/data/{fname}'
        actual = tmp_path / fname

        run([
            'python',
            'examples/noisy.py',
            'ounitnoise',
            '-s', 'spam',
            '640', '480',
            actual
        ])
        compare_files(actual, expected)

    def test_perlin(self, tmp_path):
        """When perlin is invoked, `noisy.py` should write perlin
        noise to the given file.
        """
        fname = '__test_noisy_perlin.jpg'
        expected = f'tests/data/{fname}'
        actual = tmp_path / fname

        run([
            'python',
            'examples/noisy.py',
            'perlin',
            '-s', 'spam',
            '640', '480',
            actual
        ])
        compare_files(actual, expected)

    def test_unitnoise(self, tmp_path):
        """When unitnoise is invoked, `noisy.py` should write unit
        noise to the given file.
        """
        fname = '__test_noisy_unitnoise.jpg'
        expected = f'tests/data/{fname}'
        actual = tmp_path / fname

        run([
            'python',
            'examples/noisy.py',
            'unitnoise',
            '-s', 'spam',
            '640', '480',
            actual
        ])
        compare_files(actual, expected)

    def test_worley(self, tmp_path):
        """When worley is invoked, `noisy.py` should write worley
        noise to the given file.
        """
        fname = '__test_noisy_worley.jpg'
        expected = f'tests/data/{fname}'
        actual = tmp_path / fname

        run([
            'python',
            'examples/noisy.py',
            'worley',
            '-s', 'spam',
            '640', '480',
            actual
        ])
        compare_files(actual, expected)
