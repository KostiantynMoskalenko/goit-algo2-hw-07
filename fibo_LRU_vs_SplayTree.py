import time
import matplotlib.pyplot as plt
from functools import lru_cache


class Node:
    def __init__(self, data, value, parent=None):
        self.data = data
        self.value = value
        self.parent = parent
        self.left_node = None
        self.right_node = None

class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, data, value):
        if self.root is None:
            self.root = Node(data,value)
        else:
            self._insert_node(data, value, self.root)

    def _insert_node(self, data, value, current_node):
        if data < current_node.data:
            if current_node.left_node:
                self._insert_node(data, value, current_node.left_node)
            else:
                current_node.left_node = Node(data, value, current_node)
        else:
            if current_node.right_node:
                self._insert_node(data, value, current_node.right_node)
            else:
                current_node.right_node = Node(data, value, current_node)

    def find(self, data):
        node = self.root
        while node is not None:
            if data < node.data:
                node = node.left_node
            elif data > node.data:
                node = node.right_node
            else:
                self._splay(node)
                return node.data, node.value
        return None

    def _splay(self, node):
        while node.parent is not None:
            if node.parent.parent is None:
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif node == node.parent.left_node and node.parent == node.parent.parent.left_node:
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif node == node.parent.right_node and node.parent == node.parent.parent.right_node:
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        left_child = node.left_node
        if left_child is None:
            return

        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node

        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child

        left_child.right_node = node
        node.parent = left_child

    def _rotate_left(self, node):
        right_child = node.right_node
        if right_child is None:
            return

        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node

        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child

        right_child.left_node = node
        node.parent = right_child

@lru_cache()
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n-1) + fibonacci_lru(n-2)

def fibonacci_splay(n, tree):

    if n <= 1:
        return n
    if tree.find(n):
        return tree.find(n)[1]
    else:
        suma = fibonacci_splay(n-1, tree) + fibonacci_splay(n-2, tree)
        tree.insert(n, suma)
        return suma


if __name__ == "__main__":
    tree = SplayTree()
    array = []
    result_LRU = []
    result_ST =[]
    fib_LRU = []
    fib_ST = []
    j = 0

    for i in range(19):
        array.append(j)
        j += 50

    for i in range(19):
        time_start_LRU = time.time()
        fib_LRU.append(fibonacci_lru(array[i]))
        time_end_LRU = time.time()
        result_LRU.append(time_end_LRU - time_start_LRU)
        time_start_ST = time.time()
        fib_ST.append(fibonacci_splay(array[i], tree))
        time_end_ST = time.time()
        result_ST.append(time_end_ST - time_start_ST)
    #print(result_LRU)
    #print(result_ST)
    #print(fib_LRU)
    #print(fib_ST)
    print('n         LRU Cache Time (s)          Splay Tree Time (s)')
    print('{:-^50}'.format(''))
    for i in range(19):
        print('{:>3}{:^30}{:^30}'.format(array[i], result_LRU[i], result_ST[i]))

    plt.title('Порівняння часу виконання для LRU Cache та Splay Tree')
    plt.plot(array, result_LRU, color='blue', label='LRU Cache')
    plt.plot(array, result_ST, color='orange', label='Splay Tree')
    plt.xlabel('Число Фібоначчі (n)')
    plt.ylabel('Середній час виконання (секунди)')
    plt.legend()
    plt.show()

'''
CONCLUSIONS
Accordingly with received results usage of LRU Cache is a bit faster than Splay Tree.
And this difference increases with increasing of resources limit. For fast CPU and discs
all time delays for both algorithms are zero. But if we use a bit slower hardware we can
see that both algorithms spend time and LRU Cache works faster. 
'''