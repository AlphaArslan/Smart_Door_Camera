# microsoft live hd-3000 camera
import cv2
import config

class Camera():
    def __init__(self, id):
        """
        microsoft live hd-3000 camera
        """
        self.cam = cv2.VideoCapture(id)

    def get_image(self):
        ret, img = self.cam.read()
        if ret:
            if config.DEBUG_MODE:
                print("[CAM] returned an image")
            im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return im_rgb
        if config.DEBUG_MODE:
            print("[CAM] no image")
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
