import sys
import math
import pygame
import cv2 as cv
import numpy as np
from pygame.locals import *
import dobotLib.DoBotArm as dbt
from serial.tools import list_ports
import shapes.Shape as shape
import shapes.Circle as circle
import shapes.Rectangle as rect
import shapes.Triangle as triangle

# define starting pos
sPos = {'x': 0, 'y': 0, 'z': 0}


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
  elif len(vertices) > 4:
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
def detectObjects(frame):

  #
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

    # Calculate the center point of the contour
    cPoint = (0, 0)
    M = cv.moments(contour)
    if M["m00"] != 0:
      cX = int(M["m10"] / M["m00"])
      cY = int(M["m01"] / M["m00"])
      cPoint(cX, cY)
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


# define a function that converts list[dict] -> list[obj]
def objectDef(screen, objects):

  newObjects = []
  # iterate through the provided list
  for obj in objects:
    if obj['shape'] == "Triangle":
      t = triangle(screen, obj['bBox']['x'], obj['bBox']['y'], obj['bBox']['w'],
                   obj['bBox']['h'], obj['color'])
      newObjects.append(t)

    elif obj['shape'] == "Rectangle":
      r = rect(screen, obj['bBox']['x'], obj['bBox']['y'], obj['bBox']['w'],
               obj['bBox']['h'], obj['color'])
      newObjects.append(r)

    elif obj['shape'] == "Circle":
      c = circle(screen, obj['bBox']['x'], obj['bBox']['y'],
                 (obj['bBox']['w'] + obj['bBox']['h']) / 2, obj['color'])
      newObjects.append(c)

  return newObjects


# define a function to draw the objects using pygame
def drawObjects(screen, objDict):
  objects = objectDef(screen, objDict)
  for obj in objects:
    obj.draw()


def main() -> None:

  # start the program
  print("program started")

  # init camera
  # 0 represents the default camera (you can change it if you have multiple cameras)
  cap = cv.VideoCapture(0)

  # get first camera frame
  ret, frame = cap.read()
  if not ret:
    return None  # Exit if there's an issue with the camera feed

  # init dobot obj
  dobot = dbt.DoBotArm(sPos['x'], sPos['y'], sPos['z'])

  # init pygame enviorment
  pygame.init()

  # create pygame window
  imgHeight, imgWidth, _ = frame.shape
  screen = pygame.display.set_mode((imgWidth, imgHeight))

  # loop forever:
  while True:

    #check if the user closed the window
    for event in pygame.event.get():
      #clicked the close button?
      #Quit pygame and end the program
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    # refresh the camera
    ret, frame = cap.read()
    if not ret:
      break  # Exit if there's an issue with the camera feed

    # detect objects on the image
    objects = detectObjects(frame)

    # draw the objects using pygame
    drawObjects(screen, objects)

    # wait for user to select the object

    # move selected object

    pass


# run the main function
if __name__ == "__main__":
  main()
