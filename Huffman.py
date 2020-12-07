"""
Huffman.py by Ryan Latham
Latest modification made on 4/30/2011
"""
class Node:
    "Class used to represent Nodes or Leaves in a Huffman tree. Must explicitly initialize with a frequency"

    """
    The frequency is how often the symbol appears in text/chart/data. The value should be left at None unless
    the node is a leaf.
    """
    def __init__(self, frequency, value = None, left = None, right = None):
        self.frequency = frequency
        self.value = value
        self.left = left
        self.right = right

    """
    These are overloaded rich comparisons, which are required for my heap algorithm.
    
    I intially thought I would just overload the __cmp__ function and that it would be
    a lot cleaner and more efficent. After digging through python 3.0 documentation
    though, I discovered that cmp is no longer supported and the paradigm has shifted
    to rich comparisons only. With that being said, these could be a lot cleaner by
    making calls to each other instead of always checking for isinstance. In the next
    release, that will be one of the first things that gets fixed.
    
    """
    def __add__(self, other):
        if(isinstance(other, Node)):
            return Node(self.frequency + other.frequency, None, self, other)
        else:
            return NotImplemented
        
    def __eq__(self, other):
        if(isinstance(other, Node)):
            return self.frequency == other.frequency
        else:
            return NotImplemented

    def __ne__(self, other):
        equal = self.__eq__(other)
        if(equal is not NotImplemented):
            return not equal
        else:
            return NotImplemented

    def __lt__(self, other):
        instance = isinstance(self, Node)
        if(instance):
           return self.frequency < other.frequency
        else:
            return NotImplemented
    def __le__(self, other):
        instance = isinstance(self, Node)
        if(instance):
           return self.frequency <= other.frequency
        else:
            return NotImplemented
    def __gt__(self, other):
        instance = isinstance(self, Node)
        if(instance):
           return self.frequency > other.frequency
        else:
            return NotImplemented
    def __ge__(self, other):
        instance = isinstance(self, Node)
        if(instance):
           return self.frequency >= other.frequency
        else:
            return NotImplemented
        
#Unsure of how to implement the tree. Possibly as a module instead of class
class Tree:
    """
    Class that creates a Huffman tree and also a lookup dictionary. The dictionary
    is used to relate symbols without having to traverse the tree each time. It
    is very efficent for small Huffman trees but is impratical for large tree
    deployements as it will consume a lot of memory.
    """
    import heapq

    """
    The frequency chart for the huffman tree, may be explicitly given when the tree is created,
    but will default to frequency.txt. The frequency.txt allows upper case and lower case alphabet
    characters and spaces. If a custom frequency chart is provided, it must be in the form..

    symbol:frequency;symbol:frequency;......

    Alternate forms of frequency data could be very easily supported, and indeed will be included
    in the next release.
    """
    def __init__(self, freqFile = 'frequency.txt', freqData = None):

        
        with open(freqFile, 'r') as f:
            self.text = f.read().split(';')

            
        """Not sure why but this is causing a blank list entry at the end of the list.
        Depending on the data read in, it may also add a '\n' entry. Must investigate
        the cause and find a more elegant solution then merely popping off the end"""
        self.symbolCode = ""
        self.text.pop()
        self.nodeList = []
        self.codeLookUp =  {}

        #Parses the frequency data and creates a list of leaves in the form of Nodes.
        for value in self.text:
            nodeData = value.split(':')
            self.nodeList.append(Node(float(nodeData[1]), nodeData[0]))

        #Turn the list into a heap for easier, faster removal and insertion
        self.heapq.heapify(self.nodeList)

        """
        Creation of the tree. Works by removing the lowest frequency Nodes from the heap, adding them
        together to create a new Node that points at them. This new node is inserted back into the
        heap and is sorted into the proper order. When the loop finishes, there should only be one Node
        left in the heap, which is the Root Node of the tree.
        """
        while len(self.nodeList) > 1:
            leftNode = self.heapq.heappop(self.nodeList)
            rightNode = self.heapq.heappop(self.nodeList)
            self.heapq.heappush(self.nodeList,  leftNode + rightNode)

    #Currently I am calling this externally, which in my belief is pretty poor coding style but still seems to fit the python syntax. I would 
    #like to change this in my next release to either move it out of the tree class or have it be called internally as a helper function
    """
    A function that creates a code lookup dictionary. The key of the dictionary is a symbol and the
    value is a huffman code for that symbol. It works by recursively traversing the tree and creating
    keys when it reaches a leaf node. At that point it returns None and moves back up the tree, looking
    for more leaf Nodes. When it has trasversed the entire tree, it exits.
    """
    def generateCodes(self, root, theCode):
        if(root.value != None):
            self.codeLookUp[root.value] = theCode
        if(root.right != None):
            theCode += "1"
            self.generateCodes(root.right, theCode)
            theCode = theCode[0: len(theCode) - 1]
        if(root.left != None):
            theCode += "0"
            self.generateCodes(root.left, theCode)
            theCode = theCode[0: len(theCode) - 1]
        return None
            
            
        
        
