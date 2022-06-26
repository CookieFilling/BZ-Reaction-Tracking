import cv2

def rgbValues(start, end, interval):
    # input in milisec
    # returns list of ["time, r, g, b\n",...] for some time interval
    table = [];

    cap = cv2.VideoCapture("IMG_6048.MOV") # code from https://stackoverflow.com/questions/55827496/how-to-read-pixels-from-a-specific-video-frame
    cap.set(0, start) # specify where the video should be at in milliseconds
    res, frame = cap.read() # gets a specific frame from video
    height, width, channels = frame.shape

    # mac crosshair measurements
    # height: 25-810
    # length: 0:443
    # chosen location: (255, 375)
    # white square (w,h) = (180,355)

    h = int(height * (355-25)/(810-25))
    w = int(width * 180/443)

    table.append(Entry(start, frame[h,w]))

    timeStamp = start + interval
    while timeStamp <= end:
        cap.set(0, timeStamp)
        res, frame = cap.read()
        table.append(Entry(timeStamp, frame[h,w]))
        timeStamp += interval

    return table

def Entry(milisec, rgb):
    # outputs a string entry for rgbValues() in form "time, r, g, b\n"
    b, g, r = rgb # frame rbg info
    return str(milisec) + ", " + str(r) + ", " + str(g) + ", " + str(b) + "\n"

# creates a csv that holds the time and current r g b values
csv = open("periodData.csv", "w")
csv.writelines(["timestamp (ms), red value, green value, blue value\n"] + rgbValues(20000,805000, 1000))
csv = open("periodData.csv")

content = csv.read()
csv.close()

print(content)


def plotting():
    # plotting a temp black spot on the frame at the location
    cap = cv2.VideoCapture("IMG_6048.MOV") # code from https://stackoverflow.com/questions/55827496/how-to-read-pixels-from-a-specific-video-frame
    cap.set(0, 331*1000) # specify where the video should be at in milliseconds
    res, frame = cap.read() # gets a specific frame from video
    height, width, channels = frame.shape

    h = int(height * (355-25)/(810-25))
    w = int(width * 180/443)

    for x in range(10):
        for y in range(10):
            frame[h+y,w+x,2] = 0
            frame[h+y,w+x,1] = 0
            frame[h+y,w+x,0] = 0

    cv2.imshow('Frame', frame)
    # got the waitKey() from https://learnopencv.com/read-write-and-display-a-video-using-opencv-cpp-python/
    cv2.waitKey(0)