"""
build_data
~~~~~~~~~~

Build the expected data files for the example tests.
"""
import imggen as ig
import imgwriter as iw


def build_noisy():
    """Build the expected data for `examples/noisy.py`."""
    noise = ig.noise.Noise(seed='spam')
    a = noise.fill((1, 480, 640))
    iw.write('tests/data/__test_noisy_noise.jpg', a)


if __name__ == '__main__':
    build_noisy()
