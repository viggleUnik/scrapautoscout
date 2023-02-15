import logging
import argparse
import os

def get_sum(a, b):
    print(a+b)


def get_dif(a, b):
    print(a-b)

log = logging.getLogger(os.path.basename(__file__))

parser = argparse.ArgumentParser()

parser.add_argument("a", type=int, help="First arg")
parser.add_argument("b", type=int, help="Second arg")

parser.add_argument("-a", "--action", help="sum or dif", required=True)
args = parser.parse_args()



if args.action == 'sum':
    get_sum(args.a, args.b)
elif args.action == 'dif':
    get_dif(args.a, args.b)




