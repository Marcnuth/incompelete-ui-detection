from wsdetect import dag
from wsdetect.settings import RESOURCE_DIR


def test_main():
    dag.train()


def test_predict():
    img1 = RESOURCE_DIR / 'data' / 'train' / 'normal' / '1537430103356.jpg'
    img2 = RESOURCE_DIR / 'data' / 'train' / 'white' / '1537430102405.jpg'
    model_file = RESOURCE_DIR / 'models' / 'cnn.h5'


    print(dag.predict(model_file, img1))
    print(dag.predict(model_file, img2))