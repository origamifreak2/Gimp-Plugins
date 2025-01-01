#! /usr/bin/python

from gimpfu import *

# convert image to 16 x 9 with blurred background
def sixteen_by_nine(image, drawable):

    # if drawable is a channel, layer group, or mask, then return
    if(isinstance(drawable,gimp.Channel) or isinstance(drawable,gimp.GroupLayer)):
        pdb.gimp_message("Please select a layer")
        return

    # get current/original canvas width and height
    canvas_original_width = image.width
    canvas_original_height = image.height

    # get potential 16:9 width based on height
    width_16_9 = int(round((canvas_original_height / 9.0) * 16))
    # get potential 16:9 height based on width
    height_16_9 = int(round((canvas_original_width / 16.0) * 9))

    # check if image is already 16:9
    if(canvas_original_width == width_16_9 and canvas_original_height == height_16_9):
        pdb.gimp_message("Image is already 16:9")
        return
    
    image.undo_group_start()

    # if image is in index color mode, convert to RGB
    if(image.base_type==INDEXED):
        pdb.gimp_image_convert_rgb(image)

    # create duplicate layer to use as background
    background = drawable.copy()
    image.add_layer(background, 1)

    # calculate new canvas width, height, background scale, and foreground offset, based on which dimension needs to be increased
    if(canvas_original_width < width_16_9): # canvas width needs to be increased
        canvas_new_width = width_16_9
        canvas_new_height = canvas_original_height
        bg_scale = float(width_16_9) / float(canvas_original_width)
        fg_off_x = (width_16_9 - canvas_original_width) / 2
        fg_off_y = 0
    elif(canvas_original_height < height_16_9): # canvas height needs to be increased
        canvas_new_width = canvas_original_width
        canvas_new_height = height_16_9
        bg_scale = float(height_16_9) / float(canvas_original_height)
        fg_off_x = 0
        fg_off_y = (height_16_9 - canvas_original_height) / 2

    # resize canvas and center foreground
    pdb.gimp_image_resize(image, canvas_new_width, canvas_new_height, fg_off_x, fg_off_y)

    # resize background
    bg_width = canvas_original_width * bg_scale
    bg_height = canvas_original_height * bg_scale
    pdb.gimp_layer_scale(background, bg_width, bg_height, True)

    # blur background
    blur_radius = min(500., bg_height * bg_width / 35000)
    pdb.plug_in_gauss(image, background, blur_radius, blur_radius, 0)

    # merge foreground and background and clip to canvas size
    layer = pdb.gimp_image_merge_down(image, drawable, 1)

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
