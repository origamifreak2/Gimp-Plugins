#! /usr/bin/python

from gimpfu import *

# change aspect ratio of image with blurred background
def change_aspect_ratio(image, drawable, width_ratio, height_ratio):
    
    # if drawable is a channel, layer group, or mask, then return
    if(isinstance(drawable,gimp.Channel) or isinstance(drawable,gimp.GroupLayer)):
        pdb.gimp_message("Please select a layer")
        return

    # get current/original canvas width and height
    canvas_original_width = image.width
    canvas_original_height = image.height

    # get potential new canvas width based on height and aspect ratio
    width_aspect_ratio = int(round((canvas_original_height / float(height_ratio)) * width_ratio))
    # get potential new canvas height based on width and aspect ratio
    height_aspect_ratio = int(round((canvas_original_width / float(width_ratio)) * height_ratio))

    # check if image is already at desired aspect ratio
    if(canvas_original_width == width_aspect_ratio and canvas_original_height == height_aspect_ratio):
        pdb.gimp_message("Image is already " + str(width_ratio) + " x " + str(height_ratio))
        return
    
    image.undo_group_start()

    # create duplicate layer to use as background
    background = drawable.copy()
    image.add_layer(background, 1)

    # calculate new canvas width, height, background scale, and foreground offset, based on which dimension needs to be increased
    if(canvas_original_width < width_aspect_ratio): # canvas width needs to be increased
        canvas_new_width = width_aspect_ratio
        canvas_new_height = canvas_original_height
        bg_scale = width_aspect_ratio / float(canvas_original_width)
        fg_off_x = (width_aspect_ratio - canvas_original_width) / 2
        fg_off_y = 0
    elif(canvas_original_height < height_aspect_ratio): # canvas height needs to be increased
        canvas_new_width = canvas_original_width
        canvas_new_height = height_aspect_ratio
        bg_scale = height_aspect_ratio / float(canvas_original_height)
        fg_off_x = 0
        fg_off_y = (height_aspect_ratio - canvas_original_height) / 2

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


# convert image to 16 x 9 with blurred background
def sixteen_by_nine(image, drawable):
    change_aspect_ratio(image, drawable, 16, 9)


# convert image to 4 x 3 with blurred background
def four_by_three(image, drawable):
    change_aspect_ratio(image, drawable, 4, 3)


# convert image to 3 x 2 with blurred background
def three_by_two(image, drawable):
    change_aspect_ratio(image, drawable, 3, 2)


# convert image to 1 x 1 with blurred background
def one_by_one(image, drawable):
    change_aspect_ratio(image, drawable, 1, 1)


# register functions
register(
          "change_aspect_ratio",
          "Convert image to new aspect ratio with blurred background",
          "Convert image to new aspect ratio with blurred background",
          "origamifreak",
          "Apache 2 license",
          "2024",
          "Custom Aspect Ratio",
          "RGB*,GRAYSCALE*",
          [
              (PF_IMAGE, "image", "Input image", None),
              (PF_DRAWABLE, "drawable", "Input drawable", None),
              (PF_INT, "width_ratio", "Width ratio", 16),
              (PF_INT, "height_ratio", "Height ratio", 9),
          ],
          [],
          change_aspect_ratio, menu="<Image>/Image/Change Aspect Ratio")

register(
          "sixteen_by_nine",
          "Convert image to 16 x 9 with blurred background",
          "Convert image to 16 x 9 with blurred background",
          "origamifreak",
          "Apache 2 license",
          "2024",
          "Sixteen By Nine",
          "RGB*,GRAYSCALE*",
          [
              (PF_IMAGE, "image", "Input image", None),
              (PF_DRAWABLE, "drawable", "Input drawable", None),
          ],
          [],
          sixteen_by_nine, menu="<Image>/Image/Change Aspect Ratio")

register(
          "four_by_three",
          "Convert image to 4 x 3 with blurred background",
          "Convert image to 4 x 3 with blurred background",
          "origamifreak",
          "Apache 2 license",
          "2024",
          "Four By Three",
          "RGB*,GRAYSCALE*",
          [
              (PF_IMAGE, "image", "Input image", None),
              (PF_DRAWABLE, "drawable", "Input drawable", None),
          ],
          [],
          four_by_three, menu="<Image>/Image/Change Aspect Ratio")

register(
          "three_by_two",
          "Convert image to 3 x 2 with blurred background",
          "Convert image to 3 x 2 with blurred background",
          "origamifreak",
          "Apache 2 license",
          "2024",
          "Three By Two",
          "RGB*,GRAYSCALE*",
          [
              (PF_IMAGE, "image", "Input image", None),
              (PF_DRAWABLE, "drawable", "Input drawable", None),
          ],
          [],
          three_by_two, menu="<Image>/Image/Change Aspect Ratio")

register(
          "one_by_one",
          "Convert image to 1 x 1 with blurred background",
          "Convert image to 1 x 1 with blurred background",
          "origamifreak",
          "Apache 2 license",
          "2024",
          "One By One",
          "RGB*,GRAYSCALE*",
          [
              (PF_IMAGE, "image", "Input image", None),
              (PF_DRAWABLE, "drawable", "Input drawable", None),
          ],
          [],
          one_by_one, menu="<Image>/Image/Change Aspect Ratio")
main()