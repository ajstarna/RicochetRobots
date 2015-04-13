from ctypes import *
import MCPlayer
COLORS = {
    0: 'R',
    1: 'G',
    2: 'B',
    3: 'Y',
}

DIRECTIONS = {
    1: 'N',
    2: 'E',
    4: 'S',
    8: 'W',
}

dll = CDLL('/home/yifeng/Projects/Ricochet/_ricochet')

class Game(Structure):
    _fields_ = [
        ('grid', c_uint * 256),
        ('moves', c_uint * 256),
        ('robots', c_uint * 4),
        ('token', c_uint),
        ('last', c_uint),
    ]

CALLBACK_FUNC = CFUNCTYPE(None, c_uint, c_uint, c_uint, c_uint)

def search(game, callback=None):
    callback = CALLBACK_FUNC(callback) if callback else None
    data = game.export()
    #game object is here
    
    
    
    
    game = Game()
    game.token = data['token']
    game.last = 0
    for index, value in enumerate(data['grid']):
        game.grid[index] = value
    for index, value in enumerate(data['robots']):
        game.robots[index] = value
    robot = data['robot']
    colors = list('RGBY')
    colors[0], colors[robot] = colors[robot], colors[0]
    game.robots[0], game.robots[robot] = game.robots[robot], game.robots[0]
    path = create_string_buffer(256)
    depth = dll.search(byref(game), path, callback)
    result = []
    for value in path.raw[:depth]:
        value = ord(value)
        color = colors[(value >> 4) & 0x0f]
        direction = DIRECTIONS[value & 0x0f]
        result.append((color, direction))
    
    return result
    
    
    
    #======================================================================================================================
    #                           this is our code now
def search2(game, callback=None):
    transform =[0,1,2,3,4,5,6,7,8,9,'a','b','c','d','e']
    callback = CALLBACK_FUNC(callback) if callback else None
    data = game.export2()
    #game object is here
    a =0
    b =[3,2,0,1]
    c = [2,3,1,0]
    
    a =data['robot']
    colors = list('RGBY')
    colors [a], colors[0] = colors[0],colors[a]
    a=b[a]
    data['robots'][0], data['robots'][1],data['robots'][2], data['robots'][3] = data['robots'][2],data['robots'][3],data['robots'][1], data['robots'][0]
    
    data['robots'][0],data['robots'][a] = data['robots'][a],data['robots'][0]
     
    ourc = list  ('BYGR')   
    check = ourc[a]
    ourc[0],ourc[a] = ourc[a],ourc[0]
     
    
    
    f = open ('temp.txt','w')
    
    string =''
    for i in xrange(16):
    	string=''
    	for j in xrange(16):
    		if (data['grid'][i*16+j]<16):
    			string += str(transform[(data['grid'][i*16+j])])
    		else:
    			string +='E'
    	f.write(string +'\n')
    	string =''
    
    x,y=convert(data['robots'][0])
    f.write("BLUE="+str(x)+","+str(y)+'\n')
    x,y=convert(data['robots'][1])
    f.write("YELLOW="+str(x)+","+str(y)+'\n')
    x,y=convert(data['robots'][2])
    f.write("GREEN="+str(x)+","+str(y)+'\n')
    x,y=convert(data['robots'][3])
    f.write("RED="+str(x)+","+str(y)+'\n')
    x,y=convert(data['token'])
    f.write("T="+str(x)+","+str(y)+'\n')
    f.close()
    #insert mc player
    #path  =  ourMCPlayer.findsolution('temp.txt')
    paths = MCPlayer.playGivenFile('temp.txt')
    
    
   
    for i in xrange( len(paths)):
    	if (paths[i][0]=='B'):
    		paths[i]= (check,paths[i][1])
    	elif (paths[i][0]==check):
    		paths[i]= ('B',paths[i][1])
    
    
    
    
    
    
    
    return paths

def convert(a):
    return a //16, a%16

if __name__ == '__main__':
    import model
    import time
    import random
    import collections
    count = 0
    best = (0, 0)
    hist = collections.defaultdict(int)
    def callback(depth, nodes, inner, hits):
        print 'Depth: %d, Nodes: %d (%d inner, %d hits)' % (depth, nodes, inner, hits)
    seed = 0
    while True:
        count += 1
        #seed = random.randint(0, 0x7fffffff)
        seed += 1
        start = time.clock()
        path = search(model.Game(seed))#, callback)
        moves = len(path)
        hist[moves] += 1
        key = (moves, seed)
        if key > best:
            best = key
        path = [''.join(move) for move in path]
        path = ','.join(path)
        duration = time.clock() - start
        #print '%d. %2d (%.3f) %s [%s]'% (count, moves, duration, best, path)
        #print dict(hist)
        print '%d %d [%s]' % (seed, moves, path)
