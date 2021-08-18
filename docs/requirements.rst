##################
rasty Requirements
##################

The purpose of this document is to detail the requirements for
rasty, a Python module procedurally create image data. This is an
initial take for the purposes of planning. There may be additional
requirements or non-required features added in the future that are
not covered in this document.


*******
Purpose
*******
The purpose of rasty is to make pretty pictures. More seriously, it is
to use procedurally generated patterns or pseudorandomness to create
image data that can be used in either image or video files. 


***********************
Functional Requirements
***********************
The following are the functional requirements for rasty:

*   rasty can create grayscale or color images.
*   rasty can generate still images or video.
*   rasty has image sources that generate image data.
*   rasty has distorters that modify image data.
*   rasty has eases that modify the color curve of image data.
*   rasty has blends that combine two sets of image data.
*   rasty blends have masks that can change how much blending occurs
    at each pixel in the image data.


**********************
Technical Requirements
**********************
The following are the technical requirements for rasty:

*   rasty outputs image data in array-like objects that can be saved
    by the imgwriter package.
