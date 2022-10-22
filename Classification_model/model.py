import tensorflow as tf
import numpy as np


def build_and_load_model(checkpoint_file_path):
    
    #specifiying the image resolution
    img_height = 128
    img_width = 128
    
    # create the model
    model = tf.keras.Sequential([
    
    tf.keras.Input(shape=(img_height, img_width, 3)),
    tf.keras.layers.experimental.preprocessing.Rescaling(1./255),

    # Block 1
    #best tmp
    #tf.keras.layers.Conv2D(64, (2, 2), activation='relu', kernel_regularizer=tf.keras.regularizers.l1_l2(l1=1e-5, l2=1e-4)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_regularizer=tf.keras.regularizers.l1_l2(l1=1e-5, l2=1e-4)),
    tf.keras.layers.MaxPooling2D((2,2)),

    # Block 2
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_regularizer=tf.keras.regularizers.l1_l2(l1=1e-5, l2=1e-4)),
    tf.keras.layers.MaxPooling2D((2,2)),

    # Block 3
    tf.keras.layers.Conv2D(256, (5, 5), activation='relu', kernel_regularizer=tf.keras.regularizers.l1_l2(l1=1e-5, l2=1e-4)),
    tf.keras.layers.Conv2D(256, (3, 3), activation='relu', kernel_regularizer=tf.keras.regularizers.l1_l2(l1=1e-5, l2=1e-4)),
    tf.keras.layers.Conv2D(256, (3, 3), activation='relu', kernel_regularizer=tf.keras.regularizers.l1_l2(l1=1e-5, l2=1e-4)),
    tf.keras.layers.MaxPooling2D((2,2)),

    # Flatten
    tf.keras.layers.Flatten(),

    # Fully connected layers
    tf.keras.layers.Dense(512, activation='relu',kernel_regularizer=tf.keras.regularizers.l1_l2(l1=1e-5, l2=1e-4)),
    tf.keras.layers.Dropout(.2),
    tf.keras.layers.Dense(256, activation='relu',kernel_regularizer=tf.keras.regularizers.l1_l2(l1=1e-5, l2=1e-4)),
    tf.keras.layers.Dropout(.2),
    tf.keras.layers.Dense(128, activation='relu',kernel_regularizer=tf.keras.regularizers.l1_l2(l1=1e-5, l2=1e-4)),
    tf.keras.layers.Dropout(.2),
    tf.keras.layers.Dense(64, activation='relu',kernel_regularizer=tf.keras.regularizers.l1_l2(l1=1e-5, l2=1e-4)),
    tf.keras.layers.Dropout(.2),
    tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    model.load_weights(checkpoint_file_path)
    
    return model

def load_image(image):
    #image = Image.open(filename)
    image = image.convert("RGB")
    image = tf.image.resize(image,(150,150))
    np_image = np.expand_dims(image/255.0, axis=0)
    
    return np_image
    