import numpy as np
import cv2
IMROOT="/home/tamaru/scene_categorize/main/data/"
bgr = cv2.imread(IMROOT + "dog.jpg")
h, w = bgr.shape[:2]
mask = np.zeros((h,w), dtype = np.uint8)
bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)
rect=(1,1,w,h)
cv2.grabCut(bgr, mask, rect, bgdModel, fgdModel, 10, cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
bgr2 = bgr*mask2[:,:,np.newaxis]
cv2.imshow("bgr", bgr)
cv2.imshow("bgr2", bgr2)
cv2.waitKey(0)
cv2.destroyAllWindows()