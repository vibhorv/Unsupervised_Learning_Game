from gamev2 import *
from keras.models import Sequential
from keras.layers import Dense
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import Adam
import numpy as np


x_v=2
y_v=1200/40

model = Sequential()
model.add(Dense(512,input_dim=2*x_v*y_v))
model.add(Activation('tanh'))
model.add(Dense(2))
model.add(Activation('linear'))

adam = Adam(lr=1e-1)
model.compile(loss='mse',optimizer=adam)
model.summary()



species=1
maxs=0
Xi=np.zeros((1,2*x_v*y_v))
Y=np.zeros((1,2))
while True :
	iteration=1000
	X,point,move_s =state(True,model,iteration,species)
	gamma=0.9

	X=np.array(X)
	[ux,uy] = X.shape

	move_s=np.array(move_s)
	move_s=np.reshape(move_s,(1,ux))
	
	point=np.array(point)
	point=np.reshape(point,(1,ux))
	loss=0

	for j in range(0,ux) :
		i=ux-j-1
		xold=X[i,:]
		xold=np.reshape(xold,(1,2*x_v*y_v))
		y=model.predict(xold)

		if i==ux-1 :
			y[0,move_s[0,i]]= point[0,i] 
		else :
			x=X[i+ 1,:]
			x=np.reshape(x,(1,2*x_v*y_v))
			Q=model.predict(x)

			y[0,move_s[0,i]]= point[0,i] + gamma*np.max(Q)
		#loss+=model.train_on_batch(xold,y)
		Xi=np.vstack((Xi,xold))
		Y=np.vstack((Y,y))
		print Xi.shape
		print Y.shape
	loss=model.train_on_batch(Xi,Y)

	
	species+=1
	model_yaml = model.to_yaml()
	with open("model.yaml", "w") as yaml_file:
		yaml_file.write(model_yaml)
	model.save_weights("model.h5")
	print loss

