from PIL import Image
from autocrop import Cropper
import shutil
import os

for root, dirs, files in os.walk('HistoryFaceDetect'):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))