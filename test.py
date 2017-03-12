from gamev2 import *
from keras.models import Sequential
from keras.layers import Dense
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import Adam
import numpy as np
from keras.models import model_from_yaml

yaml_file = open('model.yaml', 'r')
loaded_model_yaml = yaml_file.read()
yaml_file.close()
model = model_from_yaml(loaded_model_yaml)
# load weights into new model
model.load_weights("model.h5")
print("Loaded model from disk")

adam = Adam(lr=1e-1)
model.compile(loss='mse',optimizer=adam)
model.summary()

play(model)