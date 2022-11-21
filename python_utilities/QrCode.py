import cv2 as cv


def read_qr_code(img):
    try:
        img = cv.imread(img)
        detect = cv.QRCodeDetector()
        value, points, straight_qrcode = detect.detectAndDecode(img)
        return value
    except:
        return None
