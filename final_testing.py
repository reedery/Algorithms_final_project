#!/usr/bin/python

# top file test environment
# from scipy import spatial
from image import Image
import numpy as np
import sys, os
from kd_tree import KDTree
import pdb
import time

# 1) denoise
# 2) pixel counts
# 3) bounding box
# 5) find main axis, rotate -> np.roll() ?
# 6) num of corners, determine if polygon or digit
# 7) ???
# 8) profit


# def featuresTest(img):
#     main = Image(np.loadtxt(img))
#     print('W: ' + str(main.width) + '\t' + 'H: ' + str(main.height))
#     main.denoise()
#     print('INVERTED: ' + str(main.inverted))
#     main.setCounts()
#     print('ForegroundPX: ' + str(main.foregroundPixels) + '\t' + ' BackgroundPX: ' + str(main.backgroundPixels))
#     # main.search() // bounding box init
#     return ['empty feature array']

def getFeatures(imgpath):
    # print ('\n' + imgpath)
    main = Image(np.loadtxt(imgpath), imgpath)
    main.denoise()
    #main.findMajorAxis()
    main.search()  # bounding box
    main.createLines()
    main.setCounts()
    main.getSymmetry()
    main.getCorners()
    f = main.makeFeatureVector()
    #paths.append(paths)
    #vectors.append(np.ravel(f))
    
    # print('\n' + imgpath)
    # print(f)
    return f  

# EXAMPLE RUN FORMAT:
# Reede$ python testing123.py /Users/Reede/Desktop/test/database /Users/Reede/Desktop/test/queries /Users/Reede/Desktop/test/output 3
# python /Users/daniellenash/Desktop/algorithms-final-project/testing123/py /Users/daniellenash/Desktop/test/database /Users/daniellenash/Desktop/test/queries /Users/daniellenash/Desktop/test/output 4
# python testing123.py /Users/hoodr/Desktop/algorithms-final-project/database /Users/hoodr/Desktop/algorithms-final-project/query /Users/hoodr/Desktop/algorithms-final-project/output 1
# 
# 
if __name__ == '__main__':
    """"
    cmd line args:
        0: unused (name of .py file)
        1: path to database of images
        2: path to query images
        3: path to output file
        4: k
    """
    t0 = time.clock()
    cmdline_args = sys.argv
    db = cmdline_args[1]
    query = cmdline_args[2]
    output_path = cmdline_args[3]
    k = cmdline_args[4]
    
    imgPaths = []
    imgPath_db = []
    query_vectors = []
    db_vectors = []

    database_map = {}
    f = []
    # database calculations...
    for img in os.listdir(db):
        imgpath = db + '/' + img
        f = getFeatures(imgpath)
        database_map[imgpath] = f
        imgPath_db.append(imgpath)
        db_vectors.append(f)
        # print len(f)


    query_map = {}
    q = []
    for img in os.listdir(query):
        imgpath = query + '/' + img
        q = getFeatures(imgpath)
        database_map[imgpath] = q
        imgPaths.append(imgpath)
        query_vectors.append(q)
        #for i in range(len(q)):
            #vectors.append(q[i])
        # print len(q)
        #vectors.append(q)

    # cluster DB images once, find nearest neighbor foreach in query..
    
    #data = zip(new)
    #print len(data)
    #print len(vectors)
    # tree = spatial.KDTree(vectors)
    tree = KDTree(db_vectors)
    for v in range(len(query_vectors)):
        print 'Query Image: {}'.format(imgPaths[v])
        print 'Query vector: {} \n'.format(query_vectors[v])
        distance, ind = tree.query(query_vectors[v], int(k))    
        for i in ind:
            print 'Neighbor: {}'.format(imgPath_db[i])
            print 'Neighbor vector: {}'.format(db_vectors[i])
        print distance, ind
        print '\n'
    print time.clock() - t0
