import cv2
import numpy as np
from PIL import Image
import copy
import timeit
import random
import sklearn
from tempfile import TemporaryFile
global PIL_background
global trick
global treat
global bug_o
global x_v
global y_v
global road
global road2


PIL_background=Image.open('grass.jpg')
PIL_background=PIL_background.resize((800,1200), Image.ANTIALIAS)

road=Image.open('road.jpg')
road=road.resize((600,1200), Image.ANTIALIAS)


road2=Image.open('road2.jpg')
road2=road2.resize((600,1200), Image.ANTIALIAS)


trick=Image.open('trick.png')
trick=trick.resize((300,300), Image.ANTIALIAS)

bug_o=Image.open('car.png')
bug_o=bug_o.resize((300,720), Image.ANTIALIAS)


x_v=600/300
y_v=1200/40

def play(model) :
	terminate=0
	point_c=0
	flag_trc=1

	ux=100 + 300*int(random.random() * 2)
	uy=600

	trcx=100 + 300*int(random.random() * 2)
	trcy=0

	i=0
	while True :
		i+=1
		Display=True
		point=1

		x=np.zeros((x_v,y_v,2))
		x[(ux-100)/300,uy/40,0]=1
		x[(trcx-100)/300,trcy/40,1]=1
		x=np.reshape(x,(1,2*x_v*y_v))


		qval=model.predict_on_batch(x)
		move=np.argmax(qval)
		

		if move==1 :
			ux=400
		if move==0 :
			ux=100
			
			
	
		trcy=trcy+40


		if abs(ux-trcx)<100 and abs(uy-trcy)<299 and flag_trc==1:
			terminate=1
			point=-1000
			probabilty=int(2*random.random())
			if probabilty==1 :
				flag_trc=1
				trcx=100 + 300*int(random.random() * 2)
				trcy=0
			else :
				flag_trc=0
		
		if trcy>900 or flag_trc==0 :
			probabilty=int(2*random.random())
			if probabilty==1 :
				flag_trc=1
				trcx=100 + 300*int(random.random() * 2)
				trcy=0
			if probabilty==0 :
				flag_trc=0
		print qval,
		print move
		
		
		point_c+=point



		if Display==True :
			frame=PIL_background.copy()
			if i%2 == 1 :
				frame.paste(road, (100,0))
			else :
				frame.paste(road2, (100,0))

			bug=bug_o.copy()
			if flag_trc==1 :
				frame.paste(trick, (trcx,trcy),trick)
		
			frame.paste(bug, (ux,uy),bug)
			frame= cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)

		


			val=int(point)
			font = cv2.FONT_HERSHEY_SIMPLEX
			cv2.putText(frame,'Score:' +str(point_c),(10,30), font, 1,(255,255,0),2)
			cv2.imshow('Car Chase',frame)
		
		
		
		k=cv2.waitKey(200)
		if k==27:
			break
		


		if terminate==1 :
			break
	cv2.destroyAllWindows()
	return 0



def state(Display,model,iterations,species) :

	terminate=0
	move_s=[]
	point_c=0
	Y=[]
	flag_trc=1

	ux=100 + 300*int(random.random() * 2)
	uy=600

	trcx=100 + 300*int(random.random() * 2)
	trcy=0

	temp=np.zeros((x_v,y_v,2))
	X=np.reshape(temp,(1,2*x_v*y_v))
	move_s.append(0)
	Y.append(1)
	
	for i in range(0,iterations):
		point=1
		x=np.zeros((x_v,y_v,2))
		x[(ux-100)/300,uy/40,0]=1
		x[(trcx-100)/300,trcy/40,1]=1
		x=np.reshape(x,(1,2*x_v*y_v))


		qval=model.predict_on_batch(x)
		move=np.argmax(qval)
		

		X=np.vstack((X,x))
		move_s.append(move)

		if move==1 :
			ux=400
		if move==0 :
			ux=100
			
			
	
		trcy=trcy+40


		if abs(ux-trcx)<100 and abs(uy-trcy)<299 and flag_trc==1:
			terminate=1
			point=-1000
			probabilty=int(2*random.random())
			if probabilty==1 :
				flag_trc=1
				trcx=100 + 300*int(random.random() * 2)
				trcy=0
			else :
				flag_trc=0
		
		if trcy>900 or flag_trc==0 :
			probabilty=int(2*random.random())
			if probabilty==1 :
				flag_trc=1
				trcx=100 + 300*int(random.random() * 2)
				trcy=0
			if probabilty==0 :
				flag_trc=0
		print qval,
		print move
		
		

		Y.append(point)
		point_c+=point



		if Display==True :
			frame=PIL_background.copy()
			if i%2 == 1 :
				frame.paste(road, (100,0))
			else :
				frame.paste(road2, (100,0))

			bug=bug_o.copy()
			if flag_trc==1 :
				frame.paste(trick, (trcx,trcy),trick)
		
			frame.paste(bug, (ux,uy),bug)
			frame= cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)

		


			val=int(point)
			font = cv2.FONT_HERSHEY_SIMPLEX
			cv2.putText(frame,'Time:' +str(point_c) + ' Species:' + str(species),(10,30), font, 1,(255,255,0),2)
			cv2.imshow('Wasp Chase',frame)
		
		
		
		k=cv2.waitKey(200)
		if k==27:
			break
		


		if terminate==1 :
			break
	cv2.destroyAllWindows()

	return X,Y,move_s


