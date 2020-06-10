from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import cv2
from typing import List, Tuple
from functools import wraps
import os

# import collections


time = 0
dt = 0  # will change after readFile
image_x, image_y = [], []
pathXY = "../imagexy/"
pathIMG = "../img/"
imgFile = "dog.jpg"
txtFile = "dog.txt"


def readFile(x: List[int], y: List[int]) -> Tuple[int, int, int, int]:
    '''
    REQUIRES: emtpy list(namely x,y)
    ENSURES: the x,y coordinates of {filename}, and
    also returns the xmin, xmax, ymin, ymax of all
    of the coordinates to create a boundary
    '''

    with open(pathXY + txtFile, "r") as f:
        for pos in f:
            x1, y1 = pos.split(",")
            x.append(float(x1))
            y.append(float(y1))

    xmin, xmax = min(x), max(x)
    ymin, ymax = min(y), max(y)
    return (xmin, xmax, ymin, ymax)


def writeFile() -> None:
    '''
    REQUIRES: Nothing
    ENSURES: writes to a {filename}.txt with the coordinates, also returns
    the image with edges
    '''

    # 0 = gray scale
    try:
        img = cv2.imread(pathIMG + imgFile, 0)
    except:
        print("File not found or accepted")
        exit(1)

    edges = cv2.Canny(img, 100, 200)

    x, y = [], []

    for row in range(len(edges)):
        for col in range(len(edges[0])):
            if edges[row][col]:
                x.append(col)
                y.append(row)

    x, y = reOrganize(pos=zip(x, y))

    with open(pathXY + txtFile, "w") as f:
        for i, j in zip(x, y):
            f.write(f'{i},{j}\n')

    return edges


def transform(x: List[int], y: List[int]):
    '''
    REQUIRES: x,y coordinates of the image
    ENSURES: returns a list initial magnitudes and
    starting angles for each vector
    '''

    assert(len(x) == len(y))
    num_of_points = len(x)
    reals, imags, mag, phase, freq = [], [], [], [], []

    for k in range(-(num_of_points//2), (num_of_points+1)//2):
        freq.append(k)
        attri = 0
        for t in range(num_of_points):

            z = complex(x[t], y[t])
            re = np.cos(-2*np.pi*t*k / num_of_points)
            im = np.sin(-2*np.pi*t*k / num_of_points)
            offset = complex(re, im)
            attri += z * offset

        dt = 1 / num_of_points
        attri *= dt

        reals.append(np.real(attri))
        imags.append(np.imag(attri))
        phase.append(np.angle(attri))
        mag.append(np.sqrt(reals[-1]**2 + imags[-1]**2))

    return (reals, imags, mag, phase, freq)


def animate(t: float, dt: float, attributes, boundaries: List[int]):
    '''
    REQUIRES: A time varibale to keep track of total time,
    dt, and the drawn image_x, image_y.
    ENSURES: After each call, image_x, and image_y gets
    updated with one more coordinate, and increments time 
    by dt
    '''

    global time, image_x, image_y
    x, y = [0], [0]

    xCoeffs, yCoeffs, mags, phases, freqs = attributes

    for re, im, mag, phase, freq in zip(xCoeffs, yCoeffs, mags, phases, freqs):
        x.append(mag * np.cos(2*np.pi*freq*time + phase) + x[-1])
        y.append(mag * np.sin(2*np.pi*freq*time + phase) + y[-1])

    # update outline by one more coordinate
    image_x.append(x[-1])
    image_y.append(y[-1])

    # draw vectors
    xmin, xmax, ymin, ymax = boundaries
    plt.cla()
    xdiff, ydiff = .5*(xmax - xmin), .5*(ymax - ymin)
    plt.xlim(xmin-xdiff, xmax+xdiff)
    plt.ylim(ymin-ydiff, ymax+ydiff)
    plt.plot(x, y, color='blue', alpha=.5)
    plt.plot(image_x, image_y, color='red', ms=8)
    time += dt

    # reset the time and drawing
    if time > 1:
        print(imgFile)
        name,*_ = imgFile.split('.')
        plt.savefig(name + "ft.svg")
        image_x, image_y = [], []
        time = 0


def show(img, edges):
    '''
    REQUIRES: 2D Raster of the edged-image
    ENSURES: plots before and after image
    '''

    plt.subplot(121)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    plt.xticks([])
    plt.yticks([])

    plt.subplot(122)
    plt.imshow(edges, cmap='gray')
    plt.title('Edge Image')
    plt.xticks([])
    plt.yticks([])

    plt.show()


def reOrganize(pos: Tuple[int, int]) -> Tuple[List[int], List[int]]:
    '''
    REQUIRES: tuple list of coordinates
    ENSURES: returns a "sorted" list of coordiates, 
    ordered by distance between coordinates
    '''

    posSorted = [next(pos)]
    def dist(x1, y1, x2, y2): return (x1-x2)**2+(y1-y2)**2
    for x1, y1 in pos:
        minDist = float('inf')
        index = 0
        for i, (x2, y2) in enumerate(posSorted):
            d = dist(x1, y1, x2, y2)
            if d < minDist:
                minDist = d
                index = i
        posSorted.insert(index+1, (x1, y1))

    return list(zip(*posSorted))


def log(func_name):
    '''
    REQUIRES: function that returns string
    ENSURES: writes args, kwargs, and return
    value to debug.txt. Also prints the statment
    in the terminal
    '''

    import logging
    logging.basicConfig(filename='debug.txt', level=logging.INFO)

    @wraps(func_name)
    def debug(*args, **kwargs):

        logging.info(f'--> FUNCTION NAME = {logging.__name__}:')
        try:
            logging.info(f'--> ARGS = {args}')
        except:
            print("No arguments passed")

        try:
            logging.info(f'--> KARGS = {kargs}')
        except:
            print("No key arguments passed")

        s = str(func_name(*args, **kwargs))
        logging.info(f'--> RET VAL = {s} \n')

        return s

    return debug


def draw():

    # @log
    # def debuginfo(s):
    #     return s

    # debuginfo("hello mom")

    dt = 1 / len(x)
    attributes = transform(x=x, y=y)

    ani = FuncAnimation(plt.gcf(), animate,
                        fargs=(dt, attributes, boundaries), interval=10)

    plt.show()



def video():
    '''
    REQUIRES: True
    ENSURES: Records a video, using ML to detect face, take picture
    and save it the the imgs directory
    '''


    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # To capture video from webcam. 
    cap = cv2.VideoCapture(0)
    # To use a video file as input 
    # cap = cv2.VideoCapture('filename.mp4')

    while True:
        _, frame = cap.read()

        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray_img,
            scaleFactor=1.1,
            minNeighbors=5,
        )

        width = 0
        height = 0
        for (x, y, w, h) in faces:
            width = w
            height = h
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow('img', frame)

        k = cv2.waitKey(1) & 0xff
        
        if k == ord('c'):
            # Crop from x, y, w, h -> 100, 200, 300, 400
            crop_img = frame[y: y + h, x: x + w] 
            cv2.imwrite("../img/face.jpg", crop_img)
        elif k == ord('q'):
            cap.release()
            break

    # Release the VideoCapture object
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    ans = input('Would you like to use camera to capture face?[y/n] ').lower().strip()

    if ans in {'y', 'yes'}:
        video()
        imgFile = "face.jpg"
        txtFile = "face.txt"
    else:
        print('All good')

    x = []
    y = []

    if os.path.exists(os.path.join(pathXY, txtFile)):
        boundaries = readFile(x=x, y=y)
        edges = cv2.Canny(cv2.imread(pathIMG + imgFile, 0), 50, 110)
    else:
        edges = writeFile()
        boundaries = readFile(x, y)

    show(img=cv2.imread(pathIMG + imgFile, 0), edges=edges)

    ans = input('Continue to draw?[y/n]')
    if ans != 'n':
        draw()
    else:
        print('Have a nice day')
    

'''
TODO: Add facial recognition and provide
and option to access webcam to take a 
pic of face
MORETODO: Try to convert svg to list of points
'''
