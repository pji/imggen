######
imggen
######

A Python module for the procedural generation of image data. Or, to
put it another way: it makes pretty pictures.


***********************
Why did you write this?
***********************
I've been working on some code to procedurally generate images and
video. It is getting pretty bloated, and it seemed like a good idea
to peel off the image generators into their own modules. Because of
that, this is probably pretty niche. But, hey, maybe there is someone
else who can benefit from this somehow.


************************************
Can I install this package from pip?
************************************
Yes, but imggen is not currently available through PyPI. You will
need to clone the repository to the system you want to install
imggen on and run the following::

    pip install path/to/local/copy

Replace `path/to/local/copy` with the path for your local clone of
this repository.


***********************
How do I run the tests?
***********************
The `precommit.py` script in the root of the repository will run the
unit tests and a few other tests beside. Otherwise, the unit tests
are written with the standard unittest module, so you can run the
tests with::

    python -m unittest discover tests


********************
How do I contribute?
********************
At this time, this is code is really just me exploring and learning.
I've made it available in case it helps anyone else, but I'm not really
intending to turn this into anything other than a personal project.

That said, if other people do find it useful and start using it, I'll
reconsider. If you do use it and see something you want changed or
added, go ahead and open an issue. If anyone ever does that, I'll
figure out how to handle it.
