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

    def test_unitnoise(self, tmp_path):
        """When unitnoise is invoked, `noisy.py` should write random
        pixel noise to the given file.
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
