import cv2
import numpy as np
from PIL import Image
import copy
import timeit
import random
import sklearn


PIL_background=Image.open('grass.jpg')
PIL_background=PIL_background.resize((1024,800), Image.ANTIALIAS)
trick=Image.open('trick.png')
trick=trick.resize((100,100), Image.ANTIALIAS)
treat=Image.open('treat.png')
treat=treat.resize((100,100), Image.ANTIALIAS)
bug_o=Image.open('bug.png')
bug_o=bug_o.resize((100,100), Image.ANTIALIAS)



from sklearn import tree
clf = tree.DecisionTreeClassifier()

a=1
moveint=1
move='o'
point=10
val=0
ux=int(200+random.random() * 700)
uy=int(100+random.random() * 600)

trtx=int(200+random.random() * 700)
trty=int(100+random.random() * 600)

trcx=int(200+random.random() * 700)
trcy=int(100+random.random() * 600)
reset=0
x=np.load('x.npy')
y=np.load('y.npy')
print y.shape
while(True):
	
	frame=PIL_background.copy()
	bug=bug_o.copy()
	x1=[ux,uy,trtx,trty,trcx,trcy]
	y1=moveint
	x=np.append(x,x1);
	y=np.append(y,y1);
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



clf.fit(x, y) 
np.save('x', x)
np.save('y', x)
import cPickle
print y.shape

with open('my_dumped_classifier.pkl', 'rb') as fid:
    clf = cPickle.load(fid)

a=1
moveint=1
move='o'
point=10
val=0
ux=int(200+random.random() * 700)
uy=int(100+random.random() * 600)

trtx=int(200+random.random() * 700)
trty=int(100+random.random() * 600)

trcx=int(200+random.random() * 700)
trcy=int(100+random.random() * 600)
reset=0




while(True):
	
	frame=PIL_background.copy()
	bug=bug_o.copy()
	x1=[ux,uy,trtx,trty,trcx,trcy]

	

	move=clf.predict(x1)
	if move==2:
		uy+=30
		bug = bug.rotate(180)
	elif move==1:
		uy-=30		
	elif move==4:
		ux+=30
		bug = bug.rotate(270)
	elif move==3:
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




	if ux<0 :
		ux=1024
	if ux>1024 :
		ux=0
	if uy<0 :
		uy=1024
	if uy>800 :
		uy=0
		
	




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
	
	


cv2.destroyAllWindows()
