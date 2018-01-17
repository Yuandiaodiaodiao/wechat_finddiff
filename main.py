import os
import subprocess
import numpy
import cv2
import random
from PIL import Image
import matplotlib
from io import StringIO
from matplotlib import pyplot as plt
from matplotlib.widgets import Button,RadioButtons
SCREENSHOT_WAY = 1

"""
图一 左上角  199 ,97 
右下角 1023,921
图二  左上角
199,997
右下角1023 ,1821
"""
def duibi(imagex,a=1.2,b=100):
    rows,cols,channels=imagex.shape
    dst=imagex.copy()


    for i in range(rows):
        for j in range(cols):
            for c in range(3):
                color=imagex[i,j][c]+imagex[i,j][c]*a+b
                if color>25:
                    dst[i,j][0]=random.randrange(0,255)
                    dst[i,j][1]=random.randrange(0,255)
                    dst[i,j][2]=255
                elif color<25:

                    dst[i,j]=image2[i,j]
    return dst

def pull_screenshot():
    """
    获取屏幕截图，目前有 0 1 2 3 四种方法，未来添加新的平台监测方法时，
    可根据效率及适用性由高到低排序
    """

    global SCREENSHOT_WAY
    if 1 <= SCREENSHOT_WAY <= 3:
        process = subprocess.Popen(
            'adb shell screencap -p',
            shell=True, stdout=subprocess.PIPE)
        binary_screenshot = process.stdout.read()
        if SCREENSHOT_WAY == 2:
            binary_screenshot = binary_screenshot.replace(b'\r\n', b'\n')
        elif SCREENSHOT_WAY == 1:

            binary_screenshot = binary_screenshot.replace(b'\r\r\n', b'\n')
            print("截图完成")
        f = open('autojump1.png', 'wb')
        f.write(binary_screenshot)
        f.close()
        return binary_screenshot
    elif SCREENSHOT_WAY == 0:
        os.system('adb shell screencap -p /sdcard/autojump.png')
        os.system('adb pull /sdcard/autojump.png .')
def inverse_color(image):

    height,width,temp = image.shape
    img2 = image.copy()

    for i in range(height):
        for j in range(width):
            img2[i,j] = (255-image[i,j][0],255-image[i,j][1],255-image[i,j][2])
    return img2
def on_press(event):
    if event.inaxes == None:
        print(0)
        return
    fig = event.inaxes.figure
    ax = fig.add_subplot(122)

    ax.imshow(image1, cmap="gray")
    print(event.xdata)
    ax1.scatter(event.xdata, event.ydata)
    plt.axis("off")
    fig.canvas.draw()
def thumbnail_string(buf, size=(50, 50)):
    f = StringIO.StringIO(buf)
    image = Image.open(f)
    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')
        image = image.resize(size, Image.ANTIALIAS)
        o = StringIO.StringIO()
        image.save(o, "JPEG")
        return o.getvalue()

if __name__=="__main__":

    while 1:
        pull_screenshot()


        img = cv2.imread("autojump1.png")
        # img = Image.frombuffer(mode="RGBA",size=(1080,1920),data=pull_screenshot())
        # img=Image.open("autojump1.png")
        # img=Image.open(StringIO(pull_screenshot()))
        # print(img.size)
        # print(img.mode)
        # img = cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)
        global image1
        global image2
        image1=img[97:921:4,199:1023:4]
        image2=img[997:1821:4,199:1023:4]
        # plt.subplot(231),plt.imshow(image1)
        # plt.subplot(232),plt.imshow(image2)
        # plt.show()
        diff=cv2.absdiff(image2,image1)
    # plt.close()


        # fanse=inverse_color(diff)
        # plt.imshow(fanse)
        # plt.show()
        fanse=duibi(diff,5,20)
        # rows, cols, channels = image2.shape
        # for i in range(rows):
        #     for j in range(cols):
        #         if fanse[i][j][1]==255:
        #             fanse[i][j]=image2[i][j]
        #overlapping = cv2.addWeighted(fanse, 0.8, image1, 0.2, 0)
        cv2.namedWindow("找不同",cv2.WINDOW_NORMAL )
        cv2.imshow("找不同",fanse)
        cv2.waitKey(0)
        # print("233")
        # fig=plt.figure()
        # fig.canvas.mpl_connect("button_press_event", on_press)
        # ax1 = fig.add_subplot(121)
        # ax1.imshow(fanse)
        # plt.axis("off")
        # plt.show()
