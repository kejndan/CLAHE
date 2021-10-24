from core import CLAHE

if __name__ == '__main__':
    alg = CLAHE('imgs/indi.png')
    alg.run()
    alg.save('result/res1.png')
