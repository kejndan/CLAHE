from core import CLAHE

if __name__ == '__main__':
    alg = CLAHE('imgs/xinwei1.png')
    alg.run()
    alg.save('result/res1.png')
