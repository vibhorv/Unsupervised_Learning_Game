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


PIL_background=Image.open('grass.jpg')
PIL_background=PIL_background.resize((1000,800), Image.ANTIALIAS)
trick=Image.open('trick.png')
trick=trick.resize((100,100), Image.ANTIALIAS)
treat=Image.open('treat.png')
treat=treat.resize((100,100), Image.ANTIALIAS)
bug_o=Image.open('bug.png')
bug_o=bug_o.resize((100,100), Image.ANTIALIAS)





def play_user() :
	move=1
	point=0
	ux=int(200+random.random() * 700) #rgggs
	uy=int(100+random.random() * 600)
	trtx=int(200+random.random() * 700)
	trty=int(100+random.random() * 600)
	trcx=int(200+random.random() * 700)
	trcy=int(100+random.random() * 600)
	reset=0

	while(True):
		frame=PIL_background.copy()
		bug=bug_o.copy()
		if move=='d':
			uy+=30
			bug = bug.rotate(180)
		elif move=='u':
			uy-=30		
		elif move=='l':
			ux+=30
			bug = bug.rotate(270)
		elif move=='r':
			ux-=30
			bug = bug.rotate(90)

		frame.paste(trick, (trcx,trcy),trick)
		frame.paste(treat, (trtx,trty),treat)
		frame.paste(bug, (ux,uy),bug)
		frame= cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
		if reset>100:
			trtx=int(200+random.random() * 700)
			trty=int(100+random.random() * 600)
			trcx=int(200+random.random() * 700)
			trcy=int(100+random.random() * 600)
			reset=0



		if abs(ux-trtx)<30 and abs(uy-trty)<30 :
			trtx=int(200+random.random() * 700)
			trty=int(100+random.random() * 600)
			trcx=int(200+random.random() * 700)
			trcy=int(100+random.random() * 600)
			reset=0
			point+=100

		if abs(ux-trcx)<30 and abs(uy-trcy)<30 :
			trtx=int(200+random.random() * 700)
			trty=int(100+random.random() * 600)
			trcx=int(200+random.random() * 700)
			trcy=int(100+random.random() * 600)
			reset=0
			point-=100




		if ux<0 or ux>1024:
			print 'Game Ends'
			break
		elif uy<0 or uy>800:
			print  'Game Ends'
			break




		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(frame,'Score :  ' +str(point),(10,50), font, 1,(255,255,255),2)
		cv2.imshow('grass',frame)
	
		val=int(point)
		reset+=1
		k=cv2.waitKey(100)
		if k==27:
			break
		elif k==-1: 
			continue
		elif k==63232 and move!='u':
			move='u'
			moveint=1
		elif k==63233 and move!='d':
			move='d'
			moveint=2
		elif k==63234 and move!='r':
			move='r'
			moveint=3
		elif k==63235 and move!='l':
			move='l'
			moveint=4

	cv2.destroyAllWindows()

def state(Display,model) :
	
	ux=int(200+random.random() * 700)
	uy=int(100+random.random() * 600)
	trtx=int(200+random.random() * 700)
	trty=int(100+random.random() * 600)
	trcx=int(200+random.random() * 700)
	trcy=int(100+random.random() * 600)
	reset=0
	point=0
	#loading model
	#starting model
	#Code goes here
	x=np.zeros((1,6))
	x[0,0]=ux
	x[0,1]=uy
	x[0,2]=trtx
	x[0,3]=trty
	x[0,4]=trcx
	x[0,5]=trcy
	X=x
	while (True):
		frame=PIL_background.copy()
		bug=bug_o.copy()
		if reset==50 :
			reset-=1
			break
		x[0,0]=ux+30
		x[0,1]=uy
		x[0,2]=trtx
		x[0,3]=trty
		x[0,4]=trcx
		x[0,5]=trcy
		qval_px1=model.predict_on_batch(x)
		val=qval_px1
		maxq=1
		x[0,0]=ux-30
		x[0,1]=uy
		x[0,2]=trtx
		x[0,3]=trty
		x[0,4]=trcx
		x[0,5]=trcy
		qval_nx1=model.predict_on_batch(x) 
		if val < qval_nx1 :
			maxq=-1
			val=qval_nx1
		x[0,0]=ux
		x[0,1]=uy+30
		x[0,2]=trtx
		x[0,3]=trty
		x[0,4]=trcx
		x[0,5]=trcy
		qval_py1=model.predict_on_batch(x)
		if val < qval_py1 :
			maxq=2
			val=qval_py1 
		x[0,0]=ux
		x[0,1]=uy-30
		x[0,2]=trtx
		x[0,3]=trty
		x[0,4]=trcx
		x[0,5]=trcy
		qval_ny1=model.predict_on_batch(x)
		if val < qval_ny1 :
			maxq=-2
			val=qval_ny1

		if (maxq%2)==0 :
			uy=uy + maxq*15
		else :
			ux=ux + maxq*30

		x[0,0]=ux
		x[0,1]=uy
		x[0,2]=trtx
		x[0,3]=trty
		x[0,4]=trcx
		x[0,5]=trcy
		X=np.vstack((X,x))
		#input data              												work left here
		if maxq==2:
			bug = bug.rotate(180)
		elif maxq==1:
			bug = bug.rotate(270)
		elif maxq==-1:
			bug = bug.rotate(90)

		if abs(ux-trtx)<30 and abs(uy-trty)<30 :
			point=100
			break

		if abs(ux-trcx)<30 and abs(uy-trcy)<30 :
			point=-100
			break

		if ux<40 :
			ux=960
		if ux>1024:
			ux=40

		if uy<40 :
			uy=760
		if uy>760:
			uy=40
		
		reset+=1
		if Display==True :
			
			frame.paste(trick, (trcx,trcy),trick)
			frame.paste(treat, (trtx,trty),treat)
			frame.paste(bug, (ux,uy),bug)
			frame= cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
			font = cv2.FONT_HERSHEY_SIMPLEX
			cv2.putText(frame,'Score :  ' +str(point),(10,50), font, 1,(255,255,255),2)
			cv2.imshow('The Wasp Hunt',frame)

		k=cv2.waitKey(100)
		if k==27:
			break
		elif k==-1: 
			continue

		cv2.destroyAllWindows()


	return X,point,reset

		

def get_reward_fx(point,reset_state,gamma) :
	temp_reward=float(point)
	init_reward=point*pow(gamma,reset_state+1)
	Y=[]
	reward=init_reward
	for i in range(0,reset_state+2) :
		Y.append(reward)
		reward=reward/gamma
	return np.array(Y)


def play(model) :

	point=0
	ux=int(200+random.random() * 700)
	uy=int(100+random.random() * 600)

	trtx=int(200+random.random() * 700)
	trty=int(100+random.random() * 600)

	trcx=int(200+random.random() * 700)
	trcy=int(100+random.random() * 600)
	reset=0

	x=np.zeros((1,6))
	x[0,0]=ux
	x[0,1]=uy
	x[0,2]=trtx
	x[0,3]=trty
	x[0,4]=trcx
	x[0,5]=trcy
	while(True):
		if reset==100 :
			break
		x[0,0]=ux+30
		x[0,1]=uy
		x[0,2]=trtx
		x[0,3]=trty
		x[0,4]=trcx
		x[0,5]=trcy
		qval_px1=model.predict_on_batch(x)
		val=qval_px1
		maxq=1
		x[0,0]=ux-30
		x[0,1]=uy
		x[0,2]=trtx
		x[0,3]=trty
		x[0,4]=trcx
		x[0,5]=trcy
		qval_nx1=model.predict_on_batch(x) 
		if val < qval_nx1 :
			maxq=-1
			val=qval_nx1
		x[0,0]=ux
		x[0,1]=uy+30
		x[0,2]=trtx
		x[0,3]=trty
		x[0,4]=trcx
		x[0,5]=trcy
		qval_py1=model.predict_on_batch(x)
		if val < qval_py1 :
			maxq=2
			val=qval_py1 
		x[0,0]=ux
		x[0,1]=uy-30
		x[0,2]=trtx
		x[0,3]=trty
		x[0,4]=trcx
		x[0,5]=trcy
		qval_ny1=model.predict_on_batch(x)
		if val < qval_ny1 :
			maxq=-2
			val=qval_ny1

		if (maxq%2)==0 :
			uy=uy + maxq*15
		else :
			ux=ux + maxq*30

		if maxq==2:
			bug = bug.rotate(180)		
		elif maxq==1:
			bug = bug.rotate(270)
		elif maxq==-1:
			bug = bug.rotate(90)

		frame.paste(trick, (trcx,trcy),trick)
		frame.paste(treat, (trtx,trty),treat)
		frame.paste(bug, (ux,uy),bug)
		frame= cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)

		if reset>100:
			trtx=int(200+random.random() * 700)
			trty=int(100+random.random() * 600)
			trcx=int(200+random.random() * 700)
			trcy=int(100+random.random() * 600)
			reset=0



		if abs(ux-trtx)<60 and abs(uy-trty)<60 :
			trtx=int(200+random.random() * 700)
			trty=int(100+random.random() * 600)
			trcx=int(200+random.random() * 700)
			trcy=int(100+random.random() * 600)
			reset=0
			point+=100

		if abs(ux-trcx)<60 and abs(uy-trcy)<60 :
			trtx=int(200+random.random() * 700)
			trty=int(100+random.random() * 600)
			trcx=int(200+random.random() * 700)
			trcy=int(100+random.random() * 600)
			reset=0
			point-=100

		if ux<40 :
			ux=960
		if ux>1024:
			ux=40

		if uy<40 :
			uy=760
		if uy>760:
			uy=40
		
		reset+=1
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(frame,'Score :  ' +str(point),(10,50), font, 1,(255,255,255),2)
		cv2.imshow('The Wasp Hunt',frame)

		k=cv2.waitKey(100)
		if k==27:
			break
		elif k==-1: 
			continue

		cv2.destroyAllWindows()

	return 0
