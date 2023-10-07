###################
imggen Requirements
###################

The purpose of this document is to detail the requirements for
imggen, a Python module procedurally create image data. This is an
initial take for the purposes of planning. There may be additional
requirements or non-required features added in the future that are
not covered in this document.


*******
Purpose
*******
The purpose of imggen is to make pretty pictures. More seriously, it is
to use procedurally generated patterns or pseudorandomness to create
image data that can be used in either image or video files. 


***********************
Functional Requirements
***********************
The following are the functional requirements for imggen:

*   imggen can create grayscale or color images.
*   imggen can generate still images or video.
*   imggen has image sources that generate image data.
*   imggen has distorters that modify image data.
*   imggen has eases that modify the color curve of image data.
*   imggen has blends that combine two sets of image data.
*   imggen blends have masks that can change how much blending occurs
    at each pixel in the image data.


**********************
Technical Requirements
**********************
The following are the technical requirements for imggen:

*   imggen outputs image data in array-like objects that can be saved
    by the imgwriter package.
