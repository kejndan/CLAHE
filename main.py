from core import CLAHE
import time

if __name__ == '__main__':
    alg = CLAHE('indi.png')
    alg.show()
    alg.divide_into_rect()
    alg.walking_by_central_point()
    alg.fill_each_point()
    alg.show()
