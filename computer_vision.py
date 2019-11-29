import cv2
import numpy as np


def trafficlight(view, output_image):
    # We crop the area where we can actually detect things
    # This way we are making sure we can't see too far away, and not too far left and right
    image_cropped = view.copy()

    h, w, *_ = image_cropped.shape
    image_cropped[60:h, 0:w] = 0

    # Use this new cropped image to detect if we see a green or red light

    # Change the image to HSV (better for color detection)
    img = cv2.cvtColor(image_cropped, cv2.COLOR_RGB2HSV)
    # Create a mask for the yellow-ish color of the traffic light (this will take too much, but we will filter)
    red_upper_mask = cv2.inRange(img, np.array([160, 100, 100]), np.array([180, 255, 255]))
    red_lower_mask = cv2.inRange(img, np.array([0, 100, 100]), np.array([5, 255, 255]))

    red_mask = red_upper_mask + red_lower_mask

    green_mask = cv2.inRange(img, np.array([55, 100, 100]), np.array([65, 255, 255]))

    # Kernel that will be used to clean up the mask
    kernel = np.ones((3, 3), np.uint8)
    
    # Filter out all the small detections it has (by having a range in our mask)
    red_mask = cv2.erode(red_mask, kernel, iterations=1)
    red_mask = cv2.dilate(red_mask, kernel, iterations=10)

    green_mask = cv2.erode(green_mask, kernel, iterations=1)
    green_mask = cv2.dilate(green_mask, kernel, iterations=10)

    # Contours, we want pretty lines around everything we detect
    # Find Canny edges 
    red_edged = cv2.Canny(red_mask, 30, 200) 
    green_edged = cv2.Canny(green_mask, 30, 200) 
    
    # Finding Contours 
    # Use a copy of the image e.g. edged.copy() if you want to keep edged
    # since findContours alters the image
    red_contours, _ = cv2.findContours(red_edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    green_contours, _ = cv2.findContours(green_edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Draw all contours
    # -1 signifies drawing all contours, (0,255,0) signifies a green line, 2 signifies the width of the line used
    # We can draw a red contour for red light and same for green because we dilated a bit extra
    cv2.drawContours(output_image, red_contours, -1, (0, 0, 255), 2)
    cv2.drawContours(output_image, green_contours, -1, (0, 255, 0), 2)

    # Show
    # cv2.imshow('red', red_mask)
    # cv2.imshow('green', green_mask)

    red_detected = len(red_contours) > 0 
    green_detected = len(green_contours) > 0

    out = False

    # We assume we can't see both at the same time :/
    if red_detected:
        out = 'red'
    elif green_detected:
        out = 'green'

    # We return the color we have detected and the output image
    return out, output_image
