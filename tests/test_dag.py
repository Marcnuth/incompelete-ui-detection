from wsdetect import dag
import time
from wsdetect.settings import RESOURCE_DIR


def test_main():
    dag.train()


def test_predict():
    img1 = RESOURCE_DIR / 'data' / 'train' / 'normal' / '1537430103356.jpg'
    img2 = RESOURCE_DIR / 'data' / 'train' / 'white' / '1542039541188.jpg'
    model_file = RESOURCE_DIR / 'models' / 'cnn_1542356626.h5'


    print(dag.predict(model_file, img1))
    print(dag.predict(model_file, img2))

    cnt = 0
    for img in img2.parent.iterdir():
        cnt += dag.predict(model_file, img)[0]

    print('normal: ', cnt * 1.0 / len(list(img2.parent.iterdir())))

