#! /usr/bin/python

from gimpfu import *

# convert image to 16 x 9 with blurred background
def sixteen_by_nine(image, drawable):

    # create duplicate layer to use as foreground
    forground = drawable.copy()
    image.add_layer(forground, 0)

    # get canvas width and height
    canvas_width = pdb.gimp_image_width(image)
    canvas_height = pdb.gimp_image_height(image)

    # get 16:9 width based on height
    width_16_9 = int(round((float(canvas_height) / 9) * 16))
    # get 16:9 height based on width
    height_16_9 = int(round((float(canvas_width) / 16) * 9))

    if(canvas_width < width_16_9): # canvas width needs to be increased
        # get new canvas width and offsets for centering the foreground
        canvas_width = width_16_9
        off_x = (width_16_9 - canvas_width) / 2
        off_y = 0
        # get new background width and height
        bg_scale = float(width_16_9) / float(canvas_width)
        bg_width = canvas_width * bg_scale
        bg_height = canvas_height * bg_scale
    elif(canvas_height < height_16_9): # canvas height needs to be increased
        # get new canvas height and offsets for centering the foreground
        canvas_height = height_16_9
        off_x = 0
        off_y = (height_16_9 - canvas_height) / 2
        # get new background width and height
        bg_scale = float(height_16_9) / float(canvas_height)
        bg_width = canvas_width * bg_scale
        bg_height = canvas_height * bg_scale

    # resize canvas and center foreground
    pdb.gimp_image_resize(image, canvas_width, canvas_height, off_x, off_y)

    # resize background
    pdb.gimp_layer_scale(drawable, bg_width, bg_height, True)

    # blur background
    pdb.plug_in_gauss(image, drawable, 90, 90, 0)


register(
          "sixteen_by_nine",
          "Convert image to 16 x 9 with blurred background",
          "Convert image to 16 x 9 with blurred background",
          "origamifreak",
          "Apache 2 license",
          "2024",
          "SixteenByNine",
          "*",
          [
              (PFimage, "image", "Input image", None),
              (PF_DRAWABLE, "drawable", "Input drawable", None),
          ],
          [],
          sixteen_by_nine, menu="<Image>/Image")
main()
