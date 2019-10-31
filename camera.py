# microsoft live hd-3000 camera
import cv2

class Camera():
    def __init__(self, id):
        """
        microsoft live hd-3000 camera
        """
        self.cam = cv2.VideoCapture(id)

    def get_image(self):
        ret, img = self.cam.read()
        if ret:
            return img
        return None

    def __del__(self):
        self.cam.release()


###################### for testing
if __name__ == '__main__':
    cam_obj = Camera(0)
    while True:
        cv2.imshow('frame',cam_obj.get_image())
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
