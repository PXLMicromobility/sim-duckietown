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
  
  
def stop_line(view, output_image):
    # Change the image to HSV (better for color detection)
    img = cv2.cvtColor(view, cv2.COLOR_RGB2HSV)
    # Create a mask for the red-ish color of the stop-lines (this will take too much, but we will filter)
    upper_mask = cv2.inRange(img, np.array([160,100,100]), np.array([179,255,255]))
    lower_mask = cv2.inRange(img, np.array([0,100,100]), np.array([5,255,255]))

    mask = upper_mask + lower_mask

    # Kernel that will be used to clean up the mask
    kernel = np.ones((3, 3), np.uint8)

    # Filter out all the small detections it has (by having a range in our mask)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # To make sure the stop-lines are pretty accurate, we first expand the mask (the field where it detects something will be expanded in area)
    # Then we shrink it again by the same amount, having no effect on loose detects (noise), but filling gaps in good detects (stop-line)
    mask = cv2.dilate(mask, kernel, iterations=5)
    mask_filtered = cv2.erode(mask, kernel, iterations=5)

    # Apply the mask we just cropped to this bgr view, only showing what the mask detects, but in the real colors
    img_filtered = cv2.bitwise_and(output_image, output_image, mask=mask)
    
    # We crop the area where we can actually detect things, making sure we can't see too far away, and not too far left and right
    mask_cropped = mask_filtered.copy()

    h, w, *_ = mask_cropped.shape
    mask_cropped[0:h - 50, 0:w] = 0
    mask_cropped[0:h, 0:w-400] = 0
    mask_cropped[0:h, 750:w] = 0

    # Contours, we want pretty lines around everything we detect
    # Find Canny edges 
    edged = cv2.Canny(mask_cropped, 30, 200) 
    
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Draw all contours 
    # -1 signifies drawing all contours, (0,255,0) signifies a green line, 2 signifies the width of the line used
    cv2.drawContours(output_image, contours, -1, (0, 255, 0), 2)

    # Show
    # cv2.imshow('mask', mask)  # Everthing that is red-ish
    # cv2.imshow('filtered', mask_filtered)  # Clean stop-lines (black-white)
    # cv2.imshow('filtered image', img_filtered)  # Only the stop-lines (color)
    # cv2.imshow('cropped mask', mask_cropped)

    return len(contours) > 0, output_image
