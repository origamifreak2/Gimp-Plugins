#! /usr/bin/python

from gimpfu import *

# change aspect ratio of image with blurred background
def change_aspect_ratio(image, drawable, width_ratio, height_ratio, background_type, blur_radius = 100, background_color = (0, 0, 0, 255)):
    
    # if drawable is a channel, layer group, or mask, then return
    if(isinstance(drawable,gimp.Channel) or isinstance(drawable,gimp.GroupLayer)):
        gimp.message("Please select a layer")
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
        gimp.message("Image is already " + str(width_ratio) + " x " + str(height_ratio))
        return

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

    image.undo_group_start()
    gimp.context_push()

    # resize canvas and center foreground
    image.resize(canvas_new_width, canvas_new_height, fg_off_x, fg_off_y)

    if(background_type == 0): # blur background
        # create duplicate layer to use as background
        background = drawable.copy()
        image.add_layer(background, 1)

        # resize background
        bg_width = int(round(canvas_original_width * bg_scale))
        bg_height = int(round(canvas_original_height * bg_scale))
        background.scale(bg_width, bg_height, bg_width // 2)

        # blur background
        pdb.plug_in_gauss(image, background, blur_radius, blur_radius, 0)

        # merge foreground and background and clip to canvas size
        layer = image.merge_down(drawable, CLIP_TO_IMAGE)

    elif(background_type in [1,2,3]): # color background
        # create new layer to use as background
        background = gimp.Layer(image, "Background", canvas_new_width, canvas_new_height, RGB_IMAGE, 100, NORMAL_MODE)
        image.add_layer(background, 1)

        # Fill the background with the specified color
        color=[gimp.get_foreground(),gimp.get_background(),background_color][background_type-1]
        gimp.set_foreground(color)
        background.fill(FILL_FOREGROUND)

        # merge foreground and background and clip to canvas size
        layer = image.merge_down(drawable, CLIP_TO_IMAGE)

    else: # transparent background case: do nothing since resized canvas background is already transparent
        pass

    gimp.context_pop()
    image.undo_group_end()


# register functions
register(
          "change_aspect_ratio",
          "Change aspect ratio by adding padding of different types",
          "Change aspect ratio by adding padding of different types",
          "origamifreak",
          "Apache 2 license",
          "2024",
          "Change Aspect Ratio",
          "RGB*,GRAYSCALE*",
          [
              (PF_IMAGE, "image", "Input Image", None),
              (PF_DRAWABLE, "drawable", "Input Drawable", None),
              (PF_INT, "width_ratio", "Width Ratio", 16),
              (PF_INT, "height_ratio", "Height Ratio", 9),
              (PF_OPTION, "background_type", "Background Type", 0, ['blurred copy', 'active foreground color', 'active background color', 'other color', 'transparent']),
              (PF_SLIDER, "blur_radius", "Blur Radius", 100, (0, 500, 1)),
              (PF_COLOR, "background_color", "Other Color", (0, 0, 0, 255)),
          ],
          [],
          change_aspect_ratio, menu="<Image>/Image")
main()