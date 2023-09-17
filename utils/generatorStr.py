# coding:utf-8
# Author:mylady
# 2023/9/17 7:53
import random


def pass_generator(n=11) -> str:
    lst1 = list(range(65, 91))
    lst2 = list(range(97, 123))
    lst3 = list(range(10))
    lst4 = ['+', '-', '=', '@', '#', '$', '%', '^']
    s1 = ''.join(chr(c) for c in lst1)  # ABCDEFGHIJKLMNOPQRSTUVWXYZ
    s2 = ''.join(chr(c) for c in lst2)  # abcdefghijklmnopqrstuvwxyz
    s3 = ''.join(str(i) for i in lst3)  # 0123456789
    # s4 = ''.join(c for c in lst4)       # +-=@#$%^
    s4 = ""
    s = s1 + s2 + s3 + s3 + s4 + s4

    p = ''
    for _ in range(n):
        p += random.choice(s)
    return p


def main():
    pass


if __name__ == "__main__":
    main()
