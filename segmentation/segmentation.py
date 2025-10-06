import numpy as np
import platform
import tempfile
import os
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
# necessite scikit-image 
from skimage import io as skio
import IPython
from skimage.transform import rescale

def _to_float255(img: np.ndarray) -> np.ndarray:
    """
    Convertit une image RGB en float32 échelle 0..255, sans changer la gamme relative.
    - uint8  -> float32, 0..255 (copie vue)
    - uint16 -> float32, 0..255 (normalisation 65535 -> 255)
    - float  -> si max<=1 => 0..1 -> *255 ; sinon supposé déjà 0..255
    """
    if img.dtype == np.uint8:
        return img.astype(np.float32, copy=False)
    if img.dtype == np.uint16:
        return (img.astype(np.float32) / 65535.0) * 255.0
    if np.issubdtype(img.dtype, np.floating):
        imgf = img.astype(np.float32, copy=False)
        maxv = float(np.nanmax(imgf)) if imgf.size else 1.0
        if maxv <= 1.0001:  # image float normalisée
            imgf = imgf * 255.0
        return imgf
    # fallback générique
    return img.astype(np.float32)

def luminance_bt601(img_rgb: np.ndarray, *, normalize: bool = False) -> np.ndarray:
    """
    Calcule la luminance Y selon ITU-R BT.601 (R,G,B pondérés 0.299/0.587/0.114).
    Entrée  : img_rgb (H,W,3) en uint8/uint16/float.
    Sortie  : Y en float32.
      - si normalize=False : Y est en échelle 0..255 (recommandé pour la suite LC).
      - si normalize=True  : Y est en échelle 0..1.
    """
    if img_rgb.ndim != 3 or img_rgb.shape[-1] != 3:
        raise ValueError("img_rgb doit avoir la forme (H, W, 3)")

    img = _to_float255(img_rgb)  # float32, 0..255
    R, G, B = img[..., 0], img[..., 1], img[..., 2]
    Y = 0.299 * R + 0.587 * G + 0.114 * B  # BT.601

    if normalize:
        Y = Y / 255.0
    return Y.astype(np.float32, copy=False)

im=skio.imread('dataset/ISIC_0000030.jpg')
print(luminance_bt601(im))
