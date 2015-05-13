__author__ = 'Diego Reyes'

def create_crops_image(image, crop_x, crop_y):
    image_crops = []
    width, height = image.size
    x_crop = 0
    while x_crop < width:
        y_crop = 0
        list_crops = []
        while y_crop < height:
            list_crops.append(image.crop((x_crop, y_crop, x_crop + crop_x, y_crop + crop_y)))
            y_crop = y_crop + crop_y
        image_crops.append(list_crops)
        x_crop = x_crop + crop_x
    return image_crops