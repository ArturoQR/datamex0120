from matplotlib import pyplot as plt
from descartes import PolygonPatch
#import json
import simplejson
import os
import random

#https://github.com/mledoze/countries/data
BASE_PATH = './data'
ext='.geo.json'
#Colores aleatorios para cada país
r = lambda: random.randint(0,255)

# get all files from path of given extension
def getFiles(path, ext):
    dir = os.listdir(path)
    k = len(dir)
    i = 0
    while i != k:
        f = dir[i]
        if f[len(f)-4:] != ext:
            dir.pop(i)
            i-=1
        i+=1
        k = len(dir)
    return dir

# Abrimos el archivo JSON
def getJSON(path):
    f = open(path)
    return simplejson.loads(f.read())

#Cargamos la geometría...
def plotFeature(fig, geom):
    if geom['type'] == 'Polygon':
        poly = geom
        color = '#%02X%02X%02X' % (r(),r(),r())
        fig.add_patch(PolygonPatch(poly, fc=color, ec=color, 
                                   alpha=1, zorder=2))
    elif geom['type'] == 'MultiPolygon':
        for c in geom['coordinates']:
            poly = {"type": "Polygon", "coordinates": c}
            #print "add path"
            color = '#%02X%02X%02X' % (r(),r(),r())
            fig.add_patch(PolygonPatch(poly, fc=color, ec=color, 
                                       alpha=1, zorder=2))


def start():
    files = getFiles(BASE_PATH, 'json')
    print (files)

    #create figure
    fig = plt.subplot()

    # list directory files
    for f in files:
        path = BASE_PATH+'/'+f
        # get json data
        pydata = getJSON(path)

        print ("draw : ",f)
        # check if has geometry
        if'geometry' in pydata['features'][0].keys():
            geom = pydata['features'][0]['geometry']
            print (geom['type'])
            plotFeature(fig, geom)
    # scale and remove axis
    fig.axis('scaled')
    fig.axis('off')
    #save the plot as an image
    plt.savefig('world.png')


if __name__ == "__main__":
    start()

