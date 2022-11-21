import cv2 as cv
import matplotlib.pyplot as plt


class Picture:
    def __init__(self, fileName=None):
        self.__img = None
        if fileName is not None:
            self.__loadImage(fileName)
        pass

    @staticmethod
    def show(img, cmap: str = 'gray'):
        images = img if isinstance(img, (dict, list)) else [img]

        for image in images:
            plt.figure()
            plt.imshow(image, cmap=cmap)

        plt.show()
        pass

    @staticmethod
    def startVideoCapture(outputFilename, width: int = 640, height: int = 480):
        cap = cv.VideoCapture(0)
        fourcc = cv.VideoWriter_fourcc(*'XVID')
        out = cv.VideoWriter(outputFilename, fourcc, 20.0, (width, height))
        return out, cap

    @staticmethod
    def releaseVideoCapture(cap, out):
        cap.release()
        out.release()
        cv.destroyAllWindows()
        pass

    @staticmethod
    def readCapture(cap, out=None):
        _, frame = cap.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        if out is not None:
            out.write(frame)

        return frame, gray

    def __loadImage(self, fileName: str):
        self.__img = cv.imread(fileName, cv.IMREAD_UNCHANGED)
        pass

    def setImage(self, img):
        self.__img = img
        pass

    def getImage(self):
        return self.__img

    def getSize(self):
        return self.__img.size

    def getImageSize(self):
        s = self.__img.size()
        return s.width, s.height

    def getChannels(self):
        return self.__img.channels()

    def resizeImage(self, width: int, height: int):
        img_resized = cv.resize(self.__img, (width, height), interpolation=cv.INTER_NEAREST)
        return img_resized

    def rotate(self, rotate: int):
        if rotate == 180:
            code = cv.ROTATE_180
        elif rotate == 90:
            code = cv.ROTATE_90_CLOCKWISE
        elif rotate == -90:
            code = cv.ROTATE_90_COUNTERCLOCKWISE

        img_rotated = cv.rotate(self.__img, code)
        return img_rotated

    def crop(self, x1: int, y1: int, x2: int, y2: int):
        img_cropped = self.__img[x1:y1, x2:y2];
        return img_cropped

    def findCountours(self):
        img_gray = cv.cvtColor(self.__img, cv.COLOR_BGR2GRAY)
        ret, threshold = cv.threshold(img_gray, 150, 255, cv.THRESH_BINARY)
        contours, hierarchy = cv.findContours(image=threshold, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)

        img_copy = self.__img.copy()
        cv.drawContours(image=img_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv.LINE_AA)
        return contours, img_copy

