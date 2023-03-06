from PIL import Image
import numpy as np
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'


def getLicensePlate():
    img = Image.open('FromDB.jpg')  # 50001 50002

    width, height = img.size

    left = 15
    top = 0
    right = width
    bottom = height

    img2 = img.crop((left, top, right, bottom))
    img2.save('./result_bw.png')

    img = cv2.imread('./result_bw.png', 1)
    median_blur = cv2.GaussianBlur(img, (5, 5), 0)

    gray_image = cv2.cvtColor(median_blur, cv2.COLOR_BGR2GRAY)

    cv2.imwrite('./result_bw.png', gray_image)

    im = Image.open('./result_bw.png')

    filename = './result_bw.png'

    img = cv2.imread("./result_bw.png")

    img = cv2.inRange(img, (0, 0, 0), (110, 110, 110))

    img = cv2.bitwise_not(img)

    img = Image.fromarray(img)

    plate = pytesseract.image_to_string(img, config='--psm 7')
    plate = plate.replace(" ", "")

    print("Number plate is:", plate)
    return plate
