from core import CLAHE


if __name__ == '__main__':
    alg = CLAHE('xinwei1.jpg')
    alg.divide_into_rect()
    alg.get_dist_rect(0,0)
    # alg.show()
