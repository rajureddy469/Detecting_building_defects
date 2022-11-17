# -*- coding: utf-8 -*-

# import the necessary packages
from flask import Flask,render_template,request
# Flask-It is our framework which we are going to use to run/serve our application.
#request-for accessing file which was uploaded by the user on our application.
import cv2 # opencv library
from tensorflow.keras.models import load_model#to load our trained model
import numpy as np
#import os
from tensorflow.keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
'''
def playaudio(text):
    speech=gTTS(text)
    print(type(speech))
    speech.save("output1.mp3")
    playsound("output1.mp3")
    return
'''
app = Flask(__name__,template_folder="templates") # initializing a flask app
# Loading the model
model=load_model(r'C:\Users\varun\OneDrive\Desktop\project\Model Building\Model Building\model_building_defects_vgg16.h5')
print("Loaded model from disk")


#app=Flask(__name__,template_folder="templates") 
@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')
@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')
@app.route('/intro', methods=['GET'])
def about():
    return render_template('intro.html')
@app.route('/upload', methods=['GET','POST'])
def predict():
            
        # Get a reference to webcam #0 (the default one)
        
        print("[INFO] starting video stream...")
        vs = cv2.VideoCapture(0)
        #writer = None
        (W, H) = (None, None)
 
# loop over frames from the video file stream
        while True:
        	# read the next frame from the file
            (grabbed, frame) = vs.read()
         
        	# if the frame was not grabbed, then we have reached the end
        	# of the stream
            if not grabbed:
                break
         
        	# if the frame dimensions are empty, grab them
            if W is None or H is None:
                (H, W) = frame.shape[:2]
        
        	# clone the output frame, then convert it from BGR to RGB
        	# ordering and resize the frame to a fixed 64x64
            output = frame.copy()
            #print("apple")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (224, 224))
            #frame=image.img_to_array(frame)
            #frame = frame.astype("float32")
            x=image.img_to_array(frame)
            x=np.expand_dims(frame, axis=0)
            img_data=preprocess_input(x)
            result = np.argmax(model.predict(img_data), axis=-1)
            index=['crack','flakes','roof']
            result=str(index[result[0]])
            #print(result)
            #result=result.tolist()
            
            cv2.putText(output, "Defect: {}".format(result), (10, 120), cv2.FONT_HERSHEY_PLAIN,
                        2, (0,255,255), 1)
            #playaudio("Emergency it is a disaster")
            cv2.imshow("Output", output)
            key = cv2.waitKey(1) & 0xFF
        	 
        		# if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
         
        # release the file pointers
        print("[INFO] cleaning up...")
        vs.release()
        cv2.destroyAllWindows()
        return render_template("upload.html")

    
if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8000, debug=False)