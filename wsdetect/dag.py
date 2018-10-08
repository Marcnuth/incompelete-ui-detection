from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from wsdetect.settings import RESOURCE_DIR
from wsdetect import cnn
from keras.callbacks import TensorBoard, EarlyStopping
from pathlib import Path
import shutil
import numpy as np
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from keras.models import load_model



def train():

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    set_session(sess)

    tb_dir = Path('e:/tmp/wsdetect')
    if tb_dir.exists():
        shutil.rmtree(tb_dir.absolute().as_posix(), ignore_errors=True)
    tb_dir.mkdir(parents=True, exist_ok=True)

    train_data_dir = RESOURCE_DIR / 'data' / 'train'
    train_datagen = ImageDataGenerator(rescale=1./255, horizontal_flip=True, vertical_flip=True)
    test_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        train_data_dir.absolute().as_posix(),
        target_size=(96, 54),
        batch_size=32,
        class_mode='categorical')

    validation_generator = test_datagen.flow_from_directory(
        train_data_dir.absolute().as_posix(),
        target_size=(96, 54),
        batch_size=32,
        class_mode='categorical')

    callbacks = [
        TensorBoard(log_dir=tb_dir.absolute().as_posix(), histogram_freq=0, write_graph=True, write_images=True),
        EarlyStopping(monitor='val_acc', min_delta=0.0001, patience=5, verbose=2, mode='auto')
    ]

    model = cnn.build(input_shape=(96, 54, 3))
    model.fit_generator(
        train_generator,
        steps_per_epoch=2000,
        epochs=50,
        verbose=2,
        validation_data=validation_generator,
        validation_steps=800,
        callbacks=callbacks
    )

    print('finish training, save the model')
    model.save((RESOURCE_DIR / 'models' / 'cnn.h5').absolute().as_posix())


def predict(model_file, image_file):

    model = load_model(Path(model_file).absolute().as_posix())
    img = load_img(Path(image_file).absolute().as_posix(), target_size=(96, 54))
    img_tensor = np.expand_dims(img_to_array(img), axis=0) / 255.0

    probs = model.predict(img_tensor, verbose=2)
    return probs.argmax(axis=-1)[0], probs.max()

