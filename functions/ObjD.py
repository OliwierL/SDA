import cv2 as cv
import numpy as np


# define function to detect edges on the picture:
def detectEdges(frame):

  # Convert the frame to grayscale
  gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

  # Apply Gaussian blur to reduce noise and improve contour detection
  blurred = cv.GaussianBlur(gray, (5, 5), 0)

  # Perform edge detection
  edges = cv.Canny(blurred, 50, 150)

  return edges


# efine function to detect type of given shape
def detectShape(vertices):
  if len(vertices) == 3:
    return "Triangle"
  elif len(vertices) == 4:
    return "Rectangle"
  elif len(vertices) > 6:
    return "Circle"
  else:
    return "Unknown"


# define function to calculate avrage color of the area of the shape
def getColor(frame, contour):

  # Create a binary mask for the shape
  mask = np.zeros_like(frame)
  cv.drawContours(mask, [contour], -1, (255, 255, 255), thickness=cv.FILLED)
  mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)

  # Get the color of the shape (average color within the shape area)
  mean_color = cv.mean(frame, mask=mask)
  color = (int(mean_color[2]), int(mean_color[1]), int(mean_color[0]))

  return color


# define a function to detect objects in given image
def detectObjects(frame) -> list[dict]:

  # detect edges on the image
  edges = detectEdges(frame)

  # Find contours in the edge-detected image
  contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

  #define return array
  objects = []

  # Loop through each detected contour
  for contour in contours:
    # Approximate the contour to a polygon
    epsilon = 0.04 * cv.arcLength(contour, True)
    vertices = cv.approxPolyDP(contour, epsilon, True)

    x, y, w, h = cv.boundingRect(contour)

    # draw bounding boxes
    # cv.rectangle(frame, (x, y), (x + w, y + h), (20, 20, 20), 2)

    # Calculate the center point of the contour
    cPoint = (0, 0)
    M = cv.moments(contour)
    if M["m00"] != 0:
      cX = int(M["m10"] / M["m00"])
      cY = int(M["m01"] / M["m00"])
      cPoint = (cX, cY)
    else:
      cPoint = (0, 0)

    # Determine the shape
    shape = detectShape(vertices)

    color = getColor(frame, contour)

    x, y, w, h = cv.boundingRect(contour)

    # save data in dictionary
    obj = {
        'contour': contour,
        'center': cPoint,
        'shape': shape,
        'color': color,
        "bBox": {
            'x': x,
            'y': y,
            'w': w,
            'h': h
        }
    }
    objects.append(obj)

  return objects
