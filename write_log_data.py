
from django_init import django_init
django_init()

if True:
    from logging import getLogger, DEBUG, ERROR, WARN, CRITICAL, INFO
    from random import choice


logger = getLogger('web')


def main():
    levels = [CRITICAL, DEBUG, ERROR, INFO, WARN]
    for i in range(2000):
        logger.log(choice(levels), str(i))


if __name__ == '__main__':
    main()
