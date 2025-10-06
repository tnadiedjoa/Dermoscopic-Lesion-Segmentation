import numpy as np
import cv2

'''Je charge ici une image, en l'occurence ISIC_0000140.jpg'''

im1 = cv2.imread("melanoma/ISIC_0000140.jpg", cv2.IMREAD_COLOR)
im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2RGB)

if im1 is None:
    print("image pas chargée")
else:
    print(im1.shape[:2])

'''la fonction cadre noire permet d'enlever le cadre noir qui apparait autour d'une melanome 
lorsqu'on le capture, permet de réduire le nombre de pixel noir et donc son impact sur l'algo utilisé'''

def cadre_noire(img):
    #Calcul de lightness
    
    pixel_noir = np.zeros((img.shape[0], img.shape[1]), dtype=np.float32)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            max_rgb = float(np.max(img[i, j]))
            min_rgb = float(np.min(img[i,j]))
            lightness = (max_rgb +min_rgb)/2.0

            if lightness < 20:
                pixel_noir[i,j] = lightness
            else:
                pixel_noir[i,j] = 255
            

    print(pixel_noir)


    cv2.imwrite("masquenoir.jpg", pixel_noir.astype(np.uint8))
    #Image/masque binaire, compare chaque pixel à 20

    def cherche_retrait_indes(mask_noir = pixel_noir, axis=0):
        if axis == 0:
            start, end = 0, img.shape[0]
            taille = img.shape[0]
        else:
            start, end = 0, img.shape[1]
            taille = img.shape[1]


        for i in range(taille): 
            if axis == 0:
                ligne = mask_noir[i, :]
            else:
                ligne = mask_noir[:, i] #en realité colonne mais on dit ligne pour que ça soit plus simple
            
            k = 0
            for j in range(len(ligne)):
                if ligne[j] != 255:
                    k = k+1
                

            if k/(len(ligne)) < 0.6:
                start = i
                break
        
        print(start)

        for i in reversed(range(taille)): #on commence du bas ou de la droite selon la valeur de axis
            if axis == 0:
                ligne = mask_noir[i, :]
            else:
                ligne = mask_noir[:, i]

            k = 0
            for j in range(len(ligne)):
                if ligne[j] != 255:
                    k = k+1

            if k/(len(ligne)) < 0.6:
                end = i+1
                break

        print(end)

        return start,end
    
    top, bottom = cherche_retrait_indes(pixel_noir, axis=0)
    left, right = cherche_retrait_indes(pixel_noir, axis=1)

    cropped_img = img[top:bottom, left:right]
    return cropped_img

im1_coupé = cadre_noire(im1)
cv2.imwrite("image_coupé.png", im1_coupé)

