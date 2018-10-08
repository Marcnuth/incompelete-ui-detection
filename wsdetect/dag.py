from keras.preprocessing.image import ImageDataGenerator
from wsdetect.settings import RESOURCE_DIR
from wsdetect import cnn
from keras.callbacks import TensorBoard
from pathlib import Path
import shutil



def train():

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

    cb = TensorBoard(log_dir=tb_dir.absolute().as_posix(), histogram_freq=1, write_graph=True, write_images=True)
    model = cnn.build(input_shape=(96, 54, 3))
    model.fit_generator(
        train_generator,
        steps_per_epoch=2000,
        epochs=50,
        verbose=2,
        validation_data=validation_generator,
        validation_steps=800,
        callbacks=[cb]
    )

    print('finish training, save the model')
    model.save((RESOURCE_DIR / 'models' / 'cnn.h5').absolute().as_posix())