from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import argparse
import numpy as np
import tensorflow as tf
import tkinter as tk 
from tkinter import filedialog
from tkinter import *
from tkinter import *  
from PIL import ImageTk,Image  

#initialization stuff idk
r = tk.Tk() 
r.title('Counting Seconds') #window title

#define global variables here
#global_file_name = "" #we hardcoded the file name
global_img = ""

#define widget independent functions here
def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph


def read_tensor_from_image_file(file_name,
                                input_height=96,
                                input_width=96,
                                input_mean=0,
                                input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(
        file_reader, channels=3, name="png_reader")
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(
        tf.image.decode_gif(file_reader, name="gif_reader"))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
  else:
    image_reader = tf.image.decode_jpeg(
        file_reader, channels=3, name="jpeg_reader")
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0)
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)
  return result


def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label


#define widget dependent functions here
def askopen():
	#root.filename =  filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
	filename =  filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*"))) #doesnt work without all files for some reason
	text = Text(r)
	#text.insert(INSERT, "Hello.....") 
	#text.insert(END, "Bye Bye.....") #END is last index
	text.insert(INSERT,filename)
	text.pack()

def classifyimage():
	file_name =  filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("jpeg files","*.jpeg"),("png files","*.png"),("all files","*.*"))) #doesnt work without all files for some reason
	img = ImageTk.PhotoImage(Image.open(file_name)) 

	#canvas.create_image(200, 200, image=img) 
	canvas.image=img
	if __name__ == "__main__":
	  file_name = file_name #"device1_8-8618387-05.png" #need to display this
	  model_file = "mobilenet_output/retrain.pb"
	  label_file = "mobilenet_output/output_labels.txt"
	  input_height = 96
	  input_width = 96
	  input_mean = 0
	  input_std = 255
	  input_layer = "Placeholder"
	  output_layer = "final_result"  

	  graph = load_graph(model_file)
	  t = read_tensor_from_image_file(
	      file_name,
	      input_height=input_height,
	      input_width=input_width,
	      input_mean=input_mean,
	      input_std=input_std)

	  input_name = "import/" + input_layer
	  output_name = "import/" + output_layer
	  input_operation = graph.get_operation_by_name(input_name)
	  output_operation = graph.get_operation_by_name(output_name)

	  with tf.Session(graph=graph) as sess:
	    results = sess.run(output_operation.outputs[0], {
	        input_operation.outputs[0]: t
	    })
	  results = np.squeeze(results)

	  text = Text(r) #this shouldnt be here either. can't classify multiple images!!
	  text.pack()

	  top_k = results.argsort()[-5:][::-1]
	  labels = load_labels(label_file)
	  for i in top_k:
	    #print(labels[i], results[i])
	    print(labels[i], results[i], flush=True)
	    text.insert(INSERT,labels[i]+":"+str(results[i])+"\n")


#define widgets here
button = tk.Button(r, text='exit', width=25, command=r.destroy) #press 'Stop' closes window
button.pack() #puts the button on the window

button_askopen = tk.Button(r,text='upload',width=25,command=askopen)
button_askopen.pack()

button_classify = tk.Button(r,text='classify',width=25,command=classifyimage)
button_classify.pack()

canvas = Canvas(r, width = 300, height = 300)  
canvas.pack()  

"""
canvas = Canvas(r, width = 300, height = 300)  
canvas.pack()  
img = ImageTk.PhotoImage(Image.open(hardcoded image name here)) 
canvas.create_image(200, 200, anchor=NW, image=img)  
"""

#infinite loop
r.mainloop() 