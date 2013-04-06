# -*- coding: utf-8 -*-
import PIL, sys, os
from PIL import Image

"""
Reglas:
Articulo pequeño:
    
"""

#http://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio

#@param img: Image -  an Image-object
#@param box: tuple(x, y) - the bounding box of the result image
#@param fix: boolean - crop the image to fill the box
#@param out: file-like-object - save the image into the output stream
def resizeMal(img, box, fit, out):
    #preresize image with factor 2, 4, 8 and fast algorithm
    factor = 1
    print('IN')
    print(img.size[0])
    print(box[0])
    print(fit)
    
    while img.size[0] / factor > 2 * box[0] and img.size[1]*2 / factor > 2 * box[1]:
        factor *= 2
    if factor > 1:
        img.thumbnail((img.size[0] / factor, img.size[1] / factor), Image.NEAREST)

    #calculate the cropping box and get the cropped part
    if fit:
        x1 = y1 = 0
        x2, y2 = img.size
        wRatio = 1.0 * x2 / box[0]
        hRatio = 1.0 * y2 / box[1]
        if hRatio > wRatio:
            y1 = y2 / 2 - box[1]*wRatio / 2
            y2 = y2 / 2 + box[1]*wRatio / 2
        else:
            x1 = x2 / 2 - box[0]*hRatio / 2
            x2 = x2 / 2 + box[0]*hRatio / 2
            
        img = img.crop((x1, y1, x2, y2))

    #Resize the image with best quality algorithm ANTI-ALIAS
    img.thumbnail(box, Image.ANTIALIAS)
    
    #save it into a file-like object
    img.save(out, "JPEG", quality=80)

#resize

def resize1(im,percent):
    """ retaille suivant un pourcentage 'percent' """
    w,h = im.size
    return im.resize(((percent*w)/100,(percent*h)/100))

def resize2(im,pixels):
    """ retaille le coté le plus long en 'pixels' 
        (pour tenir dans une frame de pixels x pixels)
    """
    (wx,wy) = im.size
    rx=1.0*wx/pixels
    ry=1.0*wy/pixels
    if rx>ry:
        rr=rx
    else:
        rr=ry

    return im.resize((int(wx/rr), int(wy/rr)))


def myresize(img, importance):
    """ retaille le coté le plus long en 'pixels' 
        (pour tenir dans une frame de pixels x pixels)
    """
    _sP = 'portrait'
    _sL = 'landscape'
    _PHI = 1.61803399
    
    pixels = {
        'H-A': 600, 'H-M': 375, 'H-B': 250,
        'V-A': 600, 'V-M': 400, 'V-B': 200
        }
    
    # tel['H-A']
    
    
    ancho=img.size[0]
    alto=img.size[1]
    if ancho > alto:
        shape = 'H' #landscape
        rat = ancho / alto
        res = shape + '-' + importance
        nuevoAncho = pixels[res]
        # Calculo proporcionalmente el alto
        # si 
        nuevoAlto = alto * nuevoAncho / ancho
    else:
        rat = alto / ancho
        shape = 'V' #_sP
        res = shape + '-' + importance
        nuevoAlto = pixels[res]
        # Calculo proporcionalmente el ancho
        nuevoAncho = ancho * nuevoAlto / alto
       

    clase='imagen'
    #Si el ratio es mayor que phi, la imagen va centrada, no tiene clase izqu ni dcha
    if rat > _PHI:
        noclase=True
        print ('proporcion mayor aurea, tiende a lo largo')
    else:
        print ('proporcion menor aurea, tiende a cuadradota')

    print(ancho, alto, shape, rat)
    print(nuevoAncho, nuevoAlto)
    # TODO: comprobar que no hago un resize para arriba 
    return img.resize((int(nuevoAncho), int(nuevoAlto)))

def trataImg (dir, file, imp):
    dirout = dir + '/web' 
    imagefileIn = dir + '/' + file
    imagefileOut = dirout + '/' + file
    if not os.path.exists(dirout):
        os.makedirs(dirout)

    im = Image.open(imagefileIn)
    fout = os.path.splitext(imagefileOut)[0]+"_"+imp+".jpg"
    out = open(fout, "w")
    print ("\nTratsando: "+imagefileIn + " de importancia " + imp )
    print ("Creando: " + fout)    
    #save it into a file-like object
    im=myresize(im, imp)
    im.save(out, "JPEG", quality=80)
    return im


directory = '../data/IMAGENES153'


print ('\n\n\n')

images = (
         ('s153a2i1.jpg', 'M'),
         ('s153a2i2.jpg', 'M'),
         ('s153a2i3.jpg', 'M'),
         ('s153a3i1.jpg', 'M'),
         ('s153a4i1.jpg', 'M'),
         ('s153a5i1.jpg', 'M'),
         ('s153a5i2.jpg', 'M'),
         ('s153a5i3.TIFF', 'M'),
         ('s153a5i4.TIFF', 'M'),
         ('s153a5i5.tif', 'M'),
         ('s153a6i1.jpg', 'M'),
         ('s153a6i2.JPG', 'M'),
         ('s153a6i3.jpg', 'M'),
         ('s153a6i4.jpg', 'M'),
         ('s153a6i5.JPG', 'M'),
         ('s153a6i6.JPG', 'M'),
         ('s153a6i7.JPG', 'M'),
         ('s153a7i1.jpg', 'M'),
         ('s153a7i2.jpg', 'M'),
         ('s153a8i1.jpg', 'M'),
         ('s153a8i2.jpg', 'M'),
         ('s153a8i3.jpg', 'A'),
         ('s153a9i1.jpg', 'M')
      )

i=0
for img in images:
    i += 1
    trataImg(directory, img[0], img[1])



