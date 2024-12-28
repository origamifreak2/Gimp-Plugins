#! /usr/bin/python

from gimpfu import *

# convert image to 16 x 9 with blurred background
def sixteen_by_nine(image, drawable):

    # make sure drawable is a layer
    drawable_type = pdb.gimp_drawable_type(drawable)
    if drawable_type != 0:
        pdb.gimp_message("Please select a layer")
        return
    
    image.undo_group_start()

    # create duplicate layer to use as background
    background = drawable.copy()
    image.add_layer(background, 1)

    # get canvas width and height
    canvas_width = image.width
    canvas_height = image.height

    # get 16:9 width based on height
    width_16_9 = int(round(canvas_height / 9.0) * 16)
    # get 16:9 height based on width
    height_16_9 = int(round(canvas_width / 16.0) * 9)

    if(canvas_width < width_16_9): # canvas width needs to be increased
        bg_scale = float(width_16_9) / float(canvas_width)
        bg_width = canvas_width * bg_scale
        bg_height = canvas_height * bg_scale
        off_x = (width_16_9 - canvas_width) / 2
        off_y = 0
        canvas_width = width_16_9
    elif(canvas_height < height_16_9): # canvas height needs to be increased
        bg_scale = float(height_16_9) / float(canvas_height)
        bg_width = canvas_width * bg_scale
        bg_height = canvas_height * bg_scale
        off_x = 0
        off_y = (height_16_9 - canvas_height) / 2
        canvas_height = height_16_9
    else: # canvas is already 16:9
        pdb.gimp_message("Image is already 16:9")
        return

    # resize canvas and center foreground
    pdb.gimp_image_resize(image, canvas_width, canvas_height, off_x, off_y)

    # resize background
    pdb.gimp_layer_scale(background, bg_width, bg_height, True)

    # blur background
    blur_radius = canvas_height * canvas_width / 15000
    pdb.plug_in_gauss(image, background, blur_radius, blur_radius, 0)

    image.undo_group_end()

register(
          "sixteen_by_nine",
          "Convert image to 16 x 9 with blurred background",
          "Convert image to 16 x 9 with blurred background",
          "origamifreak",
          "Apache 2 license",
          "2024",
          "Sixteen By Nine",
          "*",
          [
              (PF_IMAGE, "image", "Input image", None),
              (PF_DRAWABLE, "drawable", "Input drawable", None),
          ],
          [],
          sixteen_by_nine, menu="<Image>/Image")
main()
