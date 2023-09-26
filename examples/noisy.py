"""
noisy
~~~~~

Generate an image containing visual noise.
"""
import argparse as ap
from pathlib import Path
from typing import Union

import imggen
from imgwriter import write


# Defaults.
OctaveNoiseDefaults = imggen.unitnoise.OctaveNoiseDefaults


# Noise generators.
def make_coscurtains(args: ap.Namespace) -> imggen.ImgAry:
    """Generate cosine curtains.
    
    :param args: The arguments passed from the command line.
    :return: The noise as a :class:`numpy.ndarray`.
    :rtype: numpy.ndarray
    """
    noise = imggen.unitnoise.CosineCurtains(
        unit=(1, *args.unit),
        min=args.min,
        max=args.max,
        repeats=args.repeats,
        seed=args.seed
    )
    size = (1, args.height, args.width)
    loc = (0, *args.location)
    return noise.fill(size, loc)


def make_curtains(args: ap.Namespace) -> imggen.ImgAry:
    """Generate curtains.
    
    :param args: The arguments passed from the command line.
    :return: The noise as a :class:`numpy.ndarray`.
    :rtype: numpy.ndarray
    """
    noise = imggen.unitnoise.Curtains(
        unit=(1, *args.unit),
        min=args.min,
        max=args.max,
        repeats=args.repeats,
        seed=args.seed
    )
    size = (1, args.height, args.width)
    loc = (0, *args.location)
    return noise.fill(size, loc)


def make_noise(args: ap.Namespace) -> imggen.ImgAry:
    """Generate random pixel value noise.
    
    :param args: The arguments passed from the command line.
    :return: The noise as a :class:`numpy.ndarray`.
    :rtype: numpy.ndarray
    """
    noise = imggen.noise.Noise(seed=args.seed)
    size = (1, args.height, args.width)
    loc = (0, *args.location)
    return noise.fill(size, loc)


def make_ocoscurtains(args: ap.Namespace) -> imggen.ImgAry:
    """Generate octaves cosine curtains.
    
    :param args: The arguments passed from the command line.
    :return: The noise as a :class:`numpy.ndarray`.
    :rtype: numpy.ndarray
    """
    noise = imggen.unitnoise.OctaveCosineCurtains(
        octaves=args.octaves,
        persistence=args.persistence,
        amplitude=args.amplitude,
        frequency=args.frequency,
        unit=(1, *args.unit),
        min=args.min,
        max=args.max,
        repeats=args.repeats,
        seed=args.seed
    )
    size = (1, args.height, args.width)
    loc = (0, *args.location)
    return noise.fill(size, loc)


def make_ocurtains(args: ap.Namespace) -> imggen.ImgAry:
    """Generate octave curtains.
    
    :param args: The arguments passed from the command line.
    :return: The noise as a :class:`numpy.ndarray`.
    :rtype: numpy.ndarray
    """
    noise = imggen.unitnoise.OctaveCurtains(
        octaves=args.octaves,
        persistence=args.persistence,
        amplitude=args.amplitude,
        frequency=args.frequency,
        unit=(1, *args.unit),
        min=args.min,
        max=args.max,
        repeats=args.repeats,
        seed=args.seed
    )
    size = (1, args.height, args.width)
    loc = (0, *args.location)
    return noise.fill(size, loc)


def make_operlin(args: ap.Namespace) -> imggen.ImgAry:
    """Generate octave perlin noise.
    
    :param args: The arguments passed from the command line.
    :return: The noise as a :class:`numpy.ndarray`.
    :rtype: numpy.ndarray
    """
    noise = imggen.perlin.OctavePerlin(
        octaves=args.octaves,
        persistence=args.persistence,
        amplitude=args.amplitude,
        frequency=args.frequency,
        unit=(1, *args.unit),
        min=args.min,
        max=args.max,
        repeats=args.repeats,
        seed=args.seed
    )
    size = (1, args.height, args.width)
    loc = (0, *args.location)
    return noise.fill(size, loc)


def make_ounitnoise(args: ap.Namespace) -> imggen.ImgAry:
    """Generate octave random blob noise.
    
    :param args: The arguments passed from the command line.
    :return: The noise as a :class:`numpy.ndarray`.
    :rtype: numpy.ndarray
    """
    noise = imggen.unitnoise.OctaveUnitNoise(
        octaves=args.octaves,
        persistence=args.persistence,
        amplitude=args.amplitude,
        frequency=args.frequency,
        unit=(1, *args.unit),
        min=args.min,
        max=args.max,
        repeats=args.repeats,
        seed=args.seed
    )
    size = (1, args.height, args.width)
    loc = (0, *args.location)
    return noise.fill(size, loc)


def make_perlin(args: ap.Namespace) -> imggen.ImgAry:
    """Generate perlin noise.
    
    :param args: The arguments passed from the command line.
    :return: The noise as a :class:`numpy.ndarray`.
    :rtype: numpy.ndarray
    """
    noise = imggen.perlin.Perlin(
        unit=(1, *args.unit),
        min=args.min,
        max=args.max,
        repeats=args.repeats,
        seed=args.seed
    )
    size = (1, args.height, args.width)
    loc = (0, *args.location)
    return noise.fill(size, loc)


def make_unitnoise(args: ap.Namespace) -> imggen.ImgAry:
    """Generate random blob noise.
    
    :param args: The arguments passed from the command line.
    :return: The noise as a :class:`numpy.ndarray`.
    :rtype: numpy.ndarray
    """
    noise = imggen.unitnoise.UnitNoise(
        unit=(1, *args.unit),
        min=args.min,
        max=args.max,
        repeats=args.repeats,
        seed=args.seed
    )
    size = (1, args.height, args.width)
    loc = (0, *args.location)
    return noise.fill(size, loc)


# Command line interface.
def parse_invocation() -> ap.ArgumentParser:
    """Build a CLI parser."""
    p = ap.ArgumentParser(
        description='Generate an image containing visual noise.',
        prog='noisy'
    )
    spa = p.add_subparsers(help='The type of noise.', required=True)
    parse_coscurtains(spa)
    parse_curtains(spa)
    parse_noise(spa)
    parse_ocoscurtains(spa)
    parse_ocurtains(spa)
    parse_operlin(spa)
    parse_ounitnoise(spa)
    parse_perlin(spa)
    parse_unitnoise(spa)
    
    p.add_argument(
        'width',
        action='store',
        help='The width of the image.',
        type=int
    )
    p.add_argument(
        'height',
        action='store',
        help='The height of the image.',
        type=int
    )
    p.add_argument(
        'path',
        action='store',
        help='Where to save the image.',
        type=str
    )
    p.add_argument(
        '-l', '--location',
        action='store',
        default=(0, 0),
        help='Location within the noise to sample for image.',
        nargs=2,
        type=int
    )
    
    return p.parse_args()


def parse_coscurtains(spa: ap._SubParsersAction) -> None:
    """Parse arguments for coscurtains.
    
    :param spa: The subparser.
    :return: None.
    :rtype: NoneType
    """
    sp = spa.add_parser(
        'coscurtains',
        description='Generate cosine curtains.'
    )
    add_unitnoise_arguments(sp)
    add_noise_arguments(sp)
    sp.set_defaults(func=make_coscurtains)


def parse_curtains(spa: ap._SubParsersAction) -> None:
    """Parse arguments for curtains.
    
    :param spa: The subparser.
    :return: None.
    :rtype: NoneType
    """
    sp = spa.add_parser(
        'curtains',
        description='Generate curtains.'
    )
    add_unitnoise_arguments(sp)
    add_noise_arguments(sp)
    sp.set_defaults(func=make_curtains)


def parse_noise(spa: ap._SubParsersAction) -> None:
    """Parser for noise.
    
    :param spa: The subparser.
    :return: None.
    :rtype: NoneType
    """
    sp = spa.add_parser(
        'noise',
        description='Generate randomized pixel noise.'
    )
    add_noise_arguments(sp)
    sp.set_defaults(func=make_noise)


def parse_ocoscurtains(spa: ap._SubParsersAction) -> None:
    """Parse arguments for ocoscurtains.
    
    :param spa: The subparser.
    :return: None.
    :rtype: NoneType
    """
    sp = spa.add_parser(
        'ocoscurtains',
        description='Generate octave cosine curtains.'
    )
    add_octave_arguments(sp)
    add_unitnoise_arguments(sp)
    add_noise_arguments(sp)
    sp.set_defaults(func=make_ocoscurtains)


def parse_ocurtains(spa: ap._SubParsersAction) -> None:
    """Parse arguments for octave curtains.
    
    :param spa: The subparser.
    :return: None.
    :rtype: NoneType
    """
    sp = spa.add_parser(
        'ocurtains',
        description='Generate octave curtains.'
    )
    add_octave_arguments(sp)
    add_unitnoise_arguments(sp)
    add_noise_arguments(sp)
    sp.set_defaults(func=make_ocurtains)


def parse_operlin(spa: ap._SubParsersAction) -> None:
    """Parse arguments for operlin.
    
    :param spa: The subparser.
    :return: None.
    :rtype: NoneType
    """
    sp = spa.add_parser(
        'operlin',
        description='Generate octave perlin noise.'
    )
    add_octave_arguments(sp, imggen.perlin.defaults)
    add_unitnoise_arguments(sp)
    add_noise_arguments(sp)
    sp.set_defaults(func=make_operlin)


def parse_ounitnoise(spa: ap._SubParsersAction) -> None:
    """Parse arguments for octave unit noise.
    
    :param spa: The subparser.
    :return: None.
    :rtype: NoneType
    """
    sp = spa.add_parser(
        'ounitnoise',
        description='Generate unit noise.'
    )
    add_unitnoise_arguments(sp)
    add_octave_arguments(sp)
    add_noise_arguments(sp)
    sp.set_defaults(func=make_ounitnoise)


def parse_perlin(spa: ap._SubParsersAction) -> None:
    """Parse arguments for perlin.
    
    :param spa: The subparser.
    :return: None.
    :rtype: NoneType
    """
    sp = spa.add_parser(
        'perlin',
        description='Generate perlin noise.'
    )
    add_unitnoise_arguments(sp)
    add_noise_arguments(sp)
    sp.set_defaults(func=make_perlin)


def parse_unitnoise(spa: ap._SubParsersAction) -> None:
    """Parse arguments for unit noise.
    
    :param spa: The subparser.
    :return: None.
    :rtype: NoneType
    """
    sp = spa.add_parser(
        'unitnoise',
        description='Generate unit noise.'
    )
    add_unitnoise_arguments(sp)
    add_noise_arguments(sp)
    sp.set_defaults(func=make_unitnoise)


def add_noise_arguments(sp: ap.ArgumentParser) -> None:
    """Add noise arguments to a subparser.
    
    :param sp: A subparser that accepts noise arguments.
    :return: None.
    :rtype: NoneType
    """
    sp.add_argument(
        '-s', '--seed',
        action='store',
        default=None,
        help='A seed for the random number generation.'
    )


def add_octave_arguments(
    sp: ap.ArgumentParser,
    d: OctaveNoiseDefaults = OctaveNoiseDefaults()
) -> None:
    """Add octave noise arguments to a subparser.
    
    :param sp: A subparser that accepts noise arguments.
    :param d: Default settings for the noise arguments.
    :return: None.
    :rtype: NoneType
    """
    sp.add_argument(
        '-o', '--octaves',
        action='store',
        default=d.octaves,
        help='The number of octaves.',
        type=int
    )
    sp.add_argument(
        '-p', '--persistence',
        action='store',
        default=d.persistence,
        help='The persistence of octaves.',
        type=int
    )
    sp.add_argument(
        '-a', '--amplitude',
        action='store',
        default=d.amplitude,
        help='The amplitude of octaves.',
        type=int
    )
    sp.add_argument(
        '-f', '--frequency',
        action='store',
        default=d.frequency,
        help='The frequency of octaves.',
        type=int
    )


def add_unitnoise_arguments(sp: ap.ArgumentParser) -> None:
    """Add unit noise arguments to a subparser.
    
    :param sp: A subparser that accepts noise arguments.
    :return: None.
    :rtype: NoneType
    """
    sp.add_argument(
        '-u', '--unit',
        action='store',
        default=(1024, 1024),
        help='The size of a unit within the noise.',
        nargs=2,
        type=int
    )
    sp.add_argument(
        '-m', '--min',
        action='store',
        default=0x00,
        help='The minimum brightness of the noise.',
        type=int
    )
    sp.add_argument(
        '-M', '--max',
        action='store',
        default=0xff,
        help='The maximum brightness of the noise.',
        type=int
    )
    sp.add_argument(
        '-r', '--repeats',
        action='store',
        default=1,
        help='The how often the values can be repeated within the noise.',
        type=int
    )


# Mainline.
if __name__ == '__main__':
    args = parse_invocation()
    a = args.func(args)
    write(args.path, a)
