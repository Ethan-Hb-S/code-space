# Enter your code here. Read input from STDIN. Print output to STDOUT

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.first = None
    
    def enqueue(self, value):
        new = Node(value)
        
        if self.head is None:
            self.head = new
            self.first = new.value
        
        if self.tail is not None:
            self.tail.next = new
        self.tail = new
    
    def dequeue(self):
        if self.head == self.tail:
            self.head = None
            self.tail = None
            self.first = None
        else:
            self.head = self.head.next
            self.first = self.head.value
            
    def print(self):
        print(self.first)
        

if __name__ == '__main__':
    q = int(input())
    
    queue = Queue()
    for i in range(q):
        qry = input()
        args = qry.split(' ')
        if len(args) == 2:
            queue.enqueue(int(args[1]))
        else:
            if args[0] == '2':
                queue.dequeue()
            else:
                queue.print()

                