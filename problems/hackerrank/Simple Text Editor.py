# Enter your code here. Read input from STDIN. Print output to STDOUT
class text:
    def __init__(self):
        self.curr = ''
        self.prev = []
    
    def append(self, string):
        self.prev.append(str(self.curr))
        self.curr += string
    
    def delete(self, k):
        self.prev.append(str(self.curr))
        self.curr = self.curr[:len(self.curr) - k]
    
    def print(self, k):
        print(self.curr[k-1])
        
    def undo(self):
        self.curr = self.prev.pop()
        

if __name__ == '__main__':
    res = text()
    q = int(input())
    
    for i in range(q):
        c = input()
        c = c.split(' ')
        
        if c[0] == '1':
            res.append(c[1])
            
        if c[0] == '2':
            res.delete(int(c[1]))
        
        if c[0] == '3':
            res.print(int(c[1]))
            
        if c[0] == '4':
            res.undo()