import cv2

def augment(input_image):
    '''
    This fucntion is used for augmenting image using rotation and flipping and mirroring techniques. The final results contain 7 images including the original input image as well.
    :param input_image >>  Is the input image.
    :return >> is a list of different augmented form of input image in grayscale and uint8 format.
    
    Note: The inpout_image can be either in single channel format or in 3-channel format.

    Created augment_list consists of the following image types:

        1- Original Image (input image)
        2- rotated by 90 degrees clockwise
        3- rotated by 180 degrees clockwise
        4- rotated by 270 degress clockwise
        5- flipped vertically 
        6- flipped horizontally 
        7- flipped vertically & horizontally
        
    '''
    flip_h  = cv2.flip(input_image, 1)               # Mirror can be done with horizontal flipping.
    flip_v  = cv2.flip(input_image, 0)               # Flipping vertically.
    flip_vh = cv2.flip(input_image,-1)               # Flipping vertically & horizontally.
    rotate_90  = cv2.rotate(input_image, cv2.ROTATE_90_CLOCKWISE)
    rotate_180 = cv2.rotate(rotate_90, cv2.ROTATE_90_CLOCKWISE)
    rotate_270 = cv2.rotate(rotate_180, cv2.ROTATE_90_CLOCKWISE)

    augment_list = []                                # augment_list is the list of 7 augmented results of the input image.
    augment_list.append(input_image)
    augment_list.append(rotate_90)
    augment_list.append(rotate_180)
    augment_list.append(rotate_270)
    augment_list.append(flip_v)
    augment_list.append(flip_h)
    augment_list.append(flip_vh)

    return augment_list
