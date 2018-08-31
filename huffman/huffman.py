from itertools import groupby
from heapq import heapify, heappop, heappush
import math


class Node(object):
    left = None
    right = None
    item = None
    weight = 0

    def __init__(self, i, w):
        self.item = i
        self.weight = w

    def link_neighbours(self, ln, rn):
        self.left = ln
        self.right = rn

    def __repr__(self):
        return "%s - %s — %s _ %s" % (self.item, self.weight, self.left, self.right)

    def __le__(self, other):
        return self.weight < self.weight

    def __gt__(self, other):
        return self.weight > self.weight


def compress(text):
    nodes = [Node(key, sum(1 for _ in group)) for key, group in groupby(sorted(text))]
    heapify(nodes)
    while len(nodes) > 1:
        left = heappop(nodes)
        right = heappop(nodes)
        node = Node(None, right.weight + left.weight)
        node.link_neighbours(left, right)
        heappush(nodes, node)

    codes = {}

    def _helper(s, node):
        if node.item:
            if not s:
                codes[node.item] = '0'
            else:
                codes[node.item] = s
        else:
            _helper(s + '0', node.left)
            _helper(s + '1', node.right)

    _helper("", nodes[0])
    return codes, "".join([codes[a] for a in text])


def decompress(codes, compressed_bytes: str):
    result = ''
    while compressed_bytes != '':
        for char, code in codes.items():
            if compressed_bytes.startswith(code):
                compressed_bytes = compressed_bytes[len(code):]
                result += char
                continue
    return result


def get_results(text):
    codes, compressed_text = compress(text)
    decompressed_text = decompress(codes, compressed_text)
    return (
               "{}\n{}".format(str(codes), compressed_text),
               decompressed_text
           ),\
           (
               len(decompressed_text.encode('utf-8')),
               math.ceil(len(compressed_text) / 8),
           )

