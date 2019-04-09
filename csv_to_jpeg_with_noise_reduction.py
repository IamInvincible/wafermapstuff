#!/usr/bin/env python
# coding: utf-8

# In[1]:


from PIL import Image
import numpy as np
from IPython.display import display
import os


# In[2]:


import pandas as pd
data = pd.read_csv('Device1_MP1_TI_Confidential.csv')
print(data.head())
print(data.shape)


# In[3]:


print(data['X'].max())
print(data['X'].min())
print(data['Y'].max())
print(data['Y'].min())


# In[4]:


#dimensions of wafermap
#need to add 1 because of zero-indexing
columns = data['X'].max() + 1
rows = data['Y'].max() + 1


# In[5]:


bins = data.loc[:,'BIN']
bins_color = []
for i in range(0,len(bins)):
    if bins[i]==1:
        bins_color.append('green')
    else:
        bins_color.append('red')
color = []
for i in range(0,len(bins)):
    if bins[i]==1:
        color.append([0,255,0])
    else:
        color.append([255,0,0])
data['bin_color'] = bins_color
data['color'] = color


# In[6]:


data.head()


# In[7]:


data['WAFER']
wafermaps = {}
for i in range(0,len(data['WAFER'])):
    wafermap_id = data.loc[i,'WAFER']
    if(wafermap_id not in wafermaps):
        wafermaps[wafermap_id] = Image.new(mode='RGB', size=[columns,rows], color=0)


# In[8]:


for i in range(0,len(data['WAFER'])):
        wafermaps[data.loc[i,'WAFER']].putpixel(xy=(data.loc[i,'X'],rows-data.loc[i,'Y']),value=(data.loc[i,'color'][0],data.loc[i,'color'][1],data.loc[i,'color'][2]))


# In[9]:


#for wafermap in wafermaps:
    #display(wafermaps[wafermap].resize((columns*10,rows*10)))


# In[10]:


red = (255,0,0)
green = (0,255,0)
blue = (0,255,0) #currently equal to green. change value to (0,0,255) for debugging
black = (0,0,0)

for i in wafermaps:
    wafermap = wafermaps[i]
    wafermap_pixelaccess = wafermaps[i].load()
    for x in range(0,columns):
        for y in range(0,rows):
            if wafermap_pixelaccess[x,y]==red:
                #check neighbors: north,east,west,south
            
                if(x==0): #left edge
                    if(y==0): #top left corner pixel
                        if (
                            (wafermap_pixelaccess[x+1,y] != red) and #E
                            (wafermap_pixelaccess[x,y+1] != red) and #S
                            (wafermap_pixelaccess[x+1,y+1] != red)
                           ):#SE
                            wafermap.putpixel(xy=(x,y),value=blue)
                    elif(y==columns-1): #bottom left corner pixel
                        if(
                            (wafermap_pixelaccess[x,y-1] != red) and #N
                            (wafermap_pixelaccess[x+1,y-1] != red) and #NE
                            (wafermap_pixelaccess[x+1,y] != red)#E
                        ):
                            wafermap.putpixel(xy=(x,y),value=blue)
                    else: #non corner pixel
                        if (
                            (wafermap_pixelaccess[x,y-1] != red) and #N
                            (wafermap_pixelaccess[x+1,y-1] != red) and #NE
                            (wafermap_pixelaccess[x+1,y] != red) and #E
                            (wafermap_pixelaccess[x,y+1] != red) and #S
                            (wafermap_pixelaccess[x+1,y+1] != red) #SE
                        ):
                            wafermap.putpixel(xy=(x,y),value=blue)
    
                elif(x==columns-1): #right edge
                    if(y==0): #top right corner pixel
                        if(
                            (wafermap_pixelaccess[x-1,y] != red) and #W
                            (wafermap_pixelaccess[x-1,y+1] != red) and #SW
                            (wafermap_pixelaccess[x,y+1] != red)#S
                        ):
                            wafermap.putpixel(xy=(x,y),value=blue)
                    elif(y==columns-1): #bottom right corner pixel
                        if(
                            (wafermap_pixelaccess[x-1,y-1] != red) and #NW
                            (wafermap_pixelaccess[x,y-1] != red) and #N    
                            (wafermap_pixelaccess[x-1,y] != red) #W
                        ):
                            wafermap.putpixel(xy=(x,y),value=blue)
                    else: #non corner pixel
                        if(
                            (wafermap_pixelaccess[x-1,y-1] != red) and #NW
                            (wafermap_pixelaccess[x,y-1] != red) and #N
                            (wafermap_pixelaccess[x-1,y] != red) and #W
                            (wafermap_pixelaccess[x-1,y+1] != red) and #SW
                            (wafermap_pixelaccess[x,y+1] != red) #S
                        ):
                            wafermap.putpixel(xy=(x,y),value=blue)
                elif(y==0): #top edge
                    if(
                        (wafermap_pixelaccess[x-1,y] != red) and #W
                        (wafermap_pixelaccess[x+1,y] != red) and #E
                        (wafermap_pixelaccess[x-1,y+1] != red) and #SW
                        (wafermap_pixelaccess[x,y+1] != red) and #S
                        (wafermap_pixelaccess[x+1,y+1] != red) #SE
                    ):
                        wafermap.putpixel(xy=(x,y),value=blue)
                elif(y==rows-1): #bottom edge
                    if(
                        (wafermap_pixelaccess[x-1,y-1] != red) and #NW
                        (wafermap_pixelaccess[x,y-1] != red) and #N
                        (wafermap_pixelaccess[x+1,y-1] != red) and #NE
                        (wafermap_pixelaccess[x-1,y] != red) and #W
                        (wafermap_pixelaccess[x+1,y] != red)#E
                    ):
                        wafermap.putpixel(xy=(x,y),value=blue)
                else: #non-edge pixel
                    if (
                        (wafermap_pixelaccess[x-1,y-1] != red) and #NW
                        (wafermap_pixelaccess[x,y-1] != red) and #N
                        (wafermap_pixelaccess[x+1,y-1] != red) and #NE
                        (wafermap_pixelaccess[x-1,y] != red) and #W
                        (wafermap_pixelaccess[x+1,y] != red) and #E
                        (wafermap_pixelaccess[x-1,y+1] != red) and #SW
                        (wafermap_pixelaccess[x,y+1] != red) and #S
                        (wafermap_pixelaccess[x+1,y+1] != red) #SE
                    ):
                        wafermap.putpixel(xy=(x,y),value=blue)
    #display(wafermap.resize((200,200)))


# In[13]:


#make output directory
try:
    output_directory = os.path.join(os.curdir,'output')
    print(output_directory)
    os.makedirs(output_directory)
except FileExistsError:
    # directory already exists
    pass


# In[14]:


#make output_resize directory
try:
    output_directory = os.path.join(os.curdir,'output_resize299')
    print(output_directory)
    os.makedirs(output_directory)
except FileExistsError:
    # directory already exists
    pass


# In[15]:


for wafermap in wafermaps:
    #display(wafermaps[wafermap])
    name = 'device1_'+str(wafermap)+'.png'
    
    #save original img
    path = os.path.join('output',name)
    print(path)
    
    wafermaps[wafermap].save(path,'png',compress_level=0)
    #save resized img
    resize_path = os.path.join('output_resize299',name)
    print(resize_path)
    wafermaps[wafermap].resize((299,299)).save(resize_path,'png',compress_level=0)


#    wafermaps[wafermap].save()
    #resize_path = os.path.join('output_resize',)

#    wafermaps[wafermap].resize((299,299)).save(output + "device1_" + str(wafermap) + ".png", "png")

