from skimage.metrics import structural_similarity as ssim
import argparse
import imutils
import cv2
from PIL import Image


# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--first", required=True,
#	help="first input image")
# ap.add_argument("-s", "--second", required=True,
#	help="second")
# args = vars(ap.parse_args())
class ImageWorker:

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
        #imageB = image_resize(imageB, height=h, width=w)
        #imageB = imutils.resize(imageB, width=h,height=w)
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


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized
