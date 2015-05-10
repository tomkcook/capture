# capture
Program for archival capture using a DSLR camera.

## Requirements
You will need installed:
* Python 3 (Python 2 may work but I have not tested it)
* Gtk3 (Not PyGTK but the new GObject introspection - `pip install gobject`)
* gphoto2 (`pip install gphoto2`)
* Also the libraries that these depend on (on Ubuntu 14.04, this is libgphoto2-dev - GTK3 is installed by default).

You will need a camera that is supported by gphoto2.  I use a Canon 600D.  It needs to have the following capabilities:
* Capture preview image.
* Capture image.
* Set ISO level (using the config /main/imgsettings/iso).
* Set capture mode (/main/settings/capture - this may be specific to Canon cameras and not necessary on others).

## Usage
Connect the camera by USB.  Run `capture.py`.  This shows a window with some file-related things at the left and a preview of what the camera sees.

Use the file chooser button at the top left to select the root of your image archive.

Select the folder you want images to go in from the tree at the left.

Position the camera.  Click the preview when you are ready and it will capture an image and save it in the selected folder.

Images are named 'imgXXXXX.jpg'.  XXXXX is a sequential number, starting at 00000.

Reposition the camera.  Click the preview to take the next image.

You can add folders using the text entry (for the new folder name) and add button at the bottom left.

## Tips
To get the best results, you need to have your camera set up correctly.

You should have it fixed to something so you don't have to hold it.  Capturing high quality images requires low ISO
numbers, which in turn typically require long exposure times to get enough light in the sort of conditions this
programme is intended for.  If you're holding the camera, you will blur it.  A tripod is fine; I don't have one, so
I've knocked up a frame from some old lumber.

You should have the subject in bright, indirect light.  As much light as possible, but without any light shining
directly onto the subject.  As many light sources as possible.  Large light sources are better than small ones (ie
a long flourescent tube is better than an incandescent bulb).  You want as much light shining indirectly as possible;
this gives even lighting and minimal 'shine' on the subject.  Using several lights minimises the amount of shadow
cast.
