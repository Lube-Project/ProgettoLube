from pytesseract import Output
from skimage.metrics import structural_similarity as ssim
import argparse
import imutils
import cv2
from PIL import Image
import pytesseract
import numpy as np


# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--first", required=True,
#	help="first input image")
# ap.add_argument("-s", "--second", required=True,
#	help="second")
# args = vars(ap.parse_args())

class OpenCV:

    def processImage(self, pathimg1, pathimg2):
        # load the two input images
        imageA = cv2.imread(pathimg1)
        imageB = cv2.imread(pathimg2)
        print('Original Dimensions Image A : ', imageA.shape)
        print('Original Dimensions Image B : ', imageB.shape)
        w, h, _ = imageA.shape
        print("Larghezza Image A : ", w)
        print("Altezza Image A : ", h)
        imageB = cv2.resize(imageB, (h, w))
        # imageB = image_resize(imageB, height=h, width=w)
        # imageB = imutils.resize(imageB, width=h,height=w)
        print('Modified Dimensions Image B : ', imageB.shape)
        # img = Image.open(pathimg1)
        # img2 = Image.open(pathimg2)
        # w, h, _ = imageA.shape
        # imageB = img2.resize((w, h))  # image resizing

        # converto l'immagine 2 con la stessa misura della 1
        # w, h, _ = imageA.shape
        # imageB = cv2.resize(imageB, (w, h))
        # convert the images to grayscale
        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

        # compute the Structural Similarity Index (SSIM) between the two
        # images, ensuring that the difference image is returned
        (score, diff) = ssim(grayA, grayB, full=True)
        diff = (diff * 255).astype("uint8")
        print("SSIM: {}".format(score))

        # threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(diff, 0, 255,
                               cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        for c in cnts:
            # compute the bounding box of the contour and then draw the
            # bounding box on both input images to represent where the two
            # images differ
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # show the output images
        cv2.imshow("Original", imageA)
        cv2.imshow("Modified", imageB)
        cv2.imshow("Diff", diff)
        cv2.imshow("Thresh", thresh)
        cv2.waitKey(0)

    def read_text(self, path):
        pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\pytesseract\tesseract.exe'
        image = cv2.imread(path)
        # scale_percent = 250  # percent of original size
        # width = int(image.shape[1] * scale_percent / 100)
        # height = int(image.shape[0] * scale_percent / 100)
        # dim = (width, height)
        # resize image
        # image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        # converting image into gray scale image
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow('grey image', gray_image)
        cv2.waitKey(0)
        # converting it to binary image by Thresholding
        # this step is require if you have colored image because if you skip this part
        # then tesseract won't able to detect text correctly and this will give incorrect result
        threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # threshold_img = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
        #                cv2.THRESH_BINARY, 11, 2)
        # threshold_img = cv2.adaptiveThreshold(gray_image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
        #   cv2.THRESH_BINARY,11,2)
        # display image
        cv2.imshow('threshold image', threshold_img)
        # Maintain output window until user presses a key
        cv2.waitKey(0)
        # Destroying present windows on screen
        cv2.destroyAllWindows()
        # configuring parameters for tesseract
        custom_config = r'--oem 3 --psm 11'
        # custom_config = '--psm 11'
        # now feeding image to tesseract
        text = pytesseract.image_to_string(threshold_img)
        print(text)
        details = pytesseract.image_to_data(threshold_img, output_type=Output.DICT,
                                            config=custom_config,
                                            lang='eng'
                                            )
        print(details.keys())
        print(details['text'])

        # total_boxes = len(details['text'])

        # for sequence_number in range(total_boxes):
        # if int(details['conf'][sequence_number]) > 30:
        # (x, y, w, h) = (
        # details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],
        # details['height'][sequence_number])
        # threshold_img = cv2.rectangle(threshold_img, (x, y), (x + w, y + h), (255, 255, 255), 2)
        # display image
        # cv2.imshow('capturedtext', threshold_img)
        # Maintain output window until user presses a key
        # cv2.waitKey(0)
        # Destroying present windows on screen
        # cv2.destroyAllWindows()
        # print(details['text'])

        print('ALTRA PROVA')

        # pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\pytesseract\tesseract.exe'
        path_to_image = "logo.png"
        # path_to_image = "logo1.png"

        # Threshold to obtain binary image
        # thresh = cv2.threshold(image, 220, 255, cv2.THRESH_BINARY)[1]

        # Create custom kernel
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # Perform closing (dilation followed by erosion)
        # close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # Invert image to use for Tesseract
        # result = 255 - close
        # cv2.imshow('thresh', thresh)
        # cv2.imshow('close', close)
        # cv2.imshow('result', result)

        # Throw image into tesseract
        # print(pytesseract.image_to_string(result))
        # cv2.waitKey()

        # Read image from which text needs to be extracted
        # img = cv2.imread(path)

        # Preprocessing the image starts

        # Convert the image to gray scale
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Performing OTSU threshold
        # ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

        # Specify structure shape and kernel size.
        # Kernel size increases or decreases the area
        # of the rectangle to be detected.
        # A smaller value like (10, 10) will detect
        # each word instead of a sentence.
        # rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

        # Appplying dilation on the threshold image
        # dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

        # Finding contours
        # contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
        # cv2.CHAIN_APPROX_NONE)

        # Creating a copy of image
        # im2 = img.copy()

        # A text file is created and flushed
        # file = open("text.txt", "w+")
        # file.write("")
        # file.close()

        # Looping through the identified contours
        # Then rectangular part is cropped and passed on
        # to pytesseract for extracting text from it
        # Extracted text is then written into the text file
        # for cnt in contours:
        # x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image
        # rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        # cropped = im2[y:y + h, x:x + w]

        # Open the file in append mode
        # with open("C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\text.txt", "a") as file:
        # Apply OCR on the cropped image
        # cv2.imshow('cropped', cropped)
        # cv2.waitKey()
        # text = pytesseract.image_to_string(cropped)

        # Appending the text into file
        # file.write(text)
        # file.write("\n")

        # Close the file
        # file.close

        # img = cv2.imread(path, 0)
        # img = imutils.resize(img, width=400)
        # blur = cv2.GaussianBlur(img, (7, 7), 0)
        # thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # result = 255 - thresh

        # data = pytesseract.image_to_string(result, lang='eng', config='--psm 6')
        # print(data)

        # cv2.imshow('thresh', thresh)
        # cv2.imshow('result', result)
        # cv2.waitKey()

        # gry = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # thr = cv2.adaptiveThreshold(gry, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        #                           cv2.THRESH_BINARY_INV, 21, 9)
        # txt = pytesseract.image_to_string(thr)
        # print(txt)

    def read_text_two(self, path):
        pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\pytesseract\tesseract.exe'
        # pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\pytesseract\tesseract.exe'
        path_to_image = "logo.png"
        # path_to_image = "logo1.png"
        image = cv2.imread(path)
        h, w, _ = image.shape
        w *= 3
        h *= 3
        w = (int)(w)
        h = (int)(h)
        # image = cv2.resize(image, (w, h), interpolation=cv2.INTER_AREA)  # Resize 3 times
        image = cv2.resize(image, (w, h), fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
        # converting image into gray scale image
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow('grey image', gray_image)
        cv2.waitKey(0)
        # converting it to binary image by Thresholding
        # this step is require if you have colored image because if you skip this part
        # then tesseract won't able to detect text correctly and this will give incorrect result
        # threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # display image
        threshold_img = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              cv2.THRESH_BINARY, 13,
                                              3)  # cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,2)[1]
        # threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # threshold_img = cv2.threshold(cv2.bilateralFilter(gray_image, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # threshold_img = cv2.threshold(cv2.medianBlur(gray_image, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # threshold_img = cv2.adaptiveThreshold(cv2.bilateralFilter(gray_image, 9, 75, 75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        # cv2.THRESH_BINARY, 31, 2)
        # threshold_img = cv2.adaptiveThreshold(cv2.medianBlur(gray_image, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        cv2.imshow('threshold image', threshold_img)
        cv2.waitKey(0)
        # threshold_img = cv2.GaussianBlur(threshold_img,(3,3),0)
        # threshold_img = cv2.GaussianBlur(threshold_img,(3,3),0)
        threshold_img = cv2.medianBlur(threshold_img, 5)
        cv2.imshow('medianBlur', threshold_img)
        cv2.waitKey(0)
        # threshold_img = cv2.bitwise_not(threshold_img)
        # cv2.imshow('Invert', threshold_img)
        # cv2.waitKey(0)
        kernel = np.ones((5, 5), np.uint8)
        # threshold_img = cv2.dilate(threshold_img, kernel, iterations=1)
        # threshold_img = cv2.erode(threshold_img, kernel, iterations=1)
        # threshold_img = cv2.morphologyEx(threshold_img, cv2.MORPH_CROSS, kernel)
        # threshold_img = cv2.erode(threshold_img, kernel, iterations=1)
        # cv2.imshow('svuota', threshold_img)
        # v2.waitKey(0)
        # cv2.imshow('threshold image', threshold_img)
        # Maintain output window until user presses a key
        # cv2.waitKey(0)
        # Destroying present windows on screen
        cv2.destroyAllWindows()
        # now feeding image to tesseract
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(threshold_img,
                                           config=custom_config
                                           )
        print(text)
        details = pytesseract.image_to_data(threshold_img, output_type=Output.DICT,
                                            config=custom_config,
                                            lang='eng'
                                            )
        print(details.keys())
        print(details['text'])

    def read_text_three(self, path):
        pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\pytesseract\tesseract.exe'
        image = cv2.imread(path)
        h, w, _ = image.shape
        w *= 3
        h *= 3
        w = int(w)
        h = int(h)
        image = cv2.resize(image, (w, h), interpolation=cv2.INTER_AREA)  # Resize 3 times
        # image = cv2.resize(image, (w, h), fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 13,
                                       3)
        # Morph open to remove noise and invert image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        invert = 255 - opening
        # threshold_img = cv2.bitwise_not(opening)
        cv2.imshow('thresh', thresh)
        cv2.waitKey(0)
        cv2.imshow('opening', opening)
        cv2.waitKey(0)
        # cv2.imshow('invert', threshold_img)
        # cv2.waitKey(0)
        # Draw bounding boxes
        cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            opening = cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)

        cv2.imshow('opening', opening)
        cv2.waitKey(0)
        # OCR
        # data = pytesseract.image_to_string(255 - thresh, lang='eng', config='--psm 6')
        # print(data)
        custom_config = r'--oem 3 --psm 11'
        # Perform text extraction
        # boxes = pytesseract.image_to_boxes(opening)
        # for b in boxes.splitlines():
        # b = b.split(' ')
        # opening = cv2.rectangle(opening, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

        # show annotated image and wait for keypress
        # cv2.imshow('opening', opening)
        # cv2.waitKey(0)
        data = pytesseract.image_to_string(opening,
                                           # lang='eng',
                                           config=custom_config)
        details = pytesseract.image_to_data(opening, output_type=Output.DICT,
                                            config=custom_config,
                                            # lang='eng'
                                            )
        print(data)
        # total_boxes = len(details['text'])

        # for sequence_number in range(total_boxes):
        # if int(details['conf'][sequence_number]) > 30:
        # (x, y, w, h) = (
        # details['left'][sequence_number],
        # details['top'][sequence_number],
        # details['width'][sequence_number],
        # details['height'][sequence_number])
        # opening = cv2.rectangle(opening, (x, y), (x + w, y + h), (36, 255, 12), 2)
        # display image
        # cv2.imshow('capturedtext', opening)
        # Maintain output window until user presses a key
        # cv2.waitKey(0)
        print(details['text'])

    def roba(self, path):
        image = cv2.imread(path)
        image = cv2.resize(image, (600, 200), interpolation=cv2.INTER_AREA)
        cv2.imshow('image', image)
        cv2.waitKey(0)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        cnts = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            opening = cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)

        cv2.imshow('opening', opening)
        cv2.waitKey(0)

    def roba2(self, path):
        image = cv2.imread(path)
        image = cv2.resize(image, (600, 200), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 5)
        sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

        thresh = cv2.threshold(sharpen, 160, 255, cv2.THRESH_BINARY_INV)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

        cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        min_area = 0
        max_area = 50000000
        image_number = 0
        for c in cnts:
            area = cv2.contourArea(c)
            if min_area < area < max_area:
                x, y, w, h = cv2.boundingRect(c)
                ROI = image[y:y + h, x:x + h]
                cv2.imwrite('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\ROI_{}.png'.format(image_number),
                            ROI)
                cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
                image_number += 1

        cv2.imshow('sharpen', sharpen)
        cv2.imshow('close', close)
        cv2.imshow('thresh', thresh)
        cv2.imshow('image', image)
        cv2.waitKey()
