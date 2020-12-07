"""
HuffmanApp.py by Ryan Latham
Latest modification made on 4/30/2011
Many thanks to www.newthinktank.com for Tkinterface tutorials that
aided in the creation of this application
"""
#Imports
from Tkinter import *
from Huffman import *
import binascii
import Binary
import ttk
from tkFileDialog import askopenfilename

#Must change names of useful GUI attributes

"""
Creation of a Huffman Tree and a code lookup dictionary. I really am unhappy with
this use and would like to eventually change it.
"""
tree = Tree()
tree.generateCodes(tree.nodeList[0], "")

#Main window creation and configuration
root = Tk()
root.title("Huffman Coding")
root.geometry("450x300+200+200")


#Attribute callback functions
def clearText():
    pass

def clearFiles(*args):
    sourceFileName.set("No file selected")
    destFileName.set("No file selected")

def save():
    pass
def changeEnd():
    pass
def launchPreferences():
    pass
def colorChange():
    pass
def aboutProgram():
    pass
def aboutDev():
    pass
def launchHelp():
    pass
"""
Callback function that depending on the selected mode of operation will either encode a file and save the
encoding to a new file, or will decode one file and save the decode to a new file. The mode of operation
is determined by a radio button selection.

DISCLAIMER: The operation of this function overlaps on the encodeTex() and decodeBin() functions and
therefor contains a lot of redundancies. Due to how the tkinter GUI works, this is intentional if not
good coding style. In a later release, this will be corrected.
Good error checking paradigms and warnings to the user have not yet been implemented and as such the
function MUST be used with CAUTION, as desctruction of data may occur without warning.
END DISCLAIMER

"""
def startCoding():
    try:
        inputFile = open(sourceFileName.get(), "rb")
        outputFile = open(destFileName.get(), "wb")
        inputString = inputFile.read()
        print inputString
        code = ""

        #Encode the text
        if(selectionVar.get()==0):
            
            for letter in inputString:
                code += tree.codeLookUp[letter]
            hexValue = Binary.BinToHex(code)
            if((len(hexValue)%2)!=0):
                hexValue+="0"
            #I am using binascii because Binary.func() only deals with strings. I needed binascii to make actual hex types
            outputFile.write(binascii.a2b_hex(hexValue))
            fileResult.set("The file was successfully encoded and should contain the hex value: " + hexValue)
        else:
            binVal = Binary.HexToBin(binascii.b2a_hex(inputString))
            node = tree.nodeList[0]
            text = ""
            for base in binVal:
                #The if statements are far less then ideal, but for the sake of readability, I left them.
                if(base == "0"):
                    node = node.left
                if(base == "1"):
                    node = node.right
                if(node.value != None):
                    text += node.value
                    node = tree.nodeList[0]
            outputFile.write(text)
            fileResult.set("The file was successfully decoded and should contain the text: " + text)

        print "Success"
        inputFile.close()
        outputFile.close()
    except IOError:
        inputFile.close()
        outputFile.close()
        fileResult.set("File IO Error. Please select new/different files")
        print "One or more files could not be opened"

    


"""
Callback function that gets a string of text and returns a huffman code for the text.The code is based
on a predetermined(for now) frequency chart.

If the function is unable to resolve the huffmnan code from the text, it will throw an internal error that
the user will be unaware of, and will do nothing.
"""
def encodeTex():
    text = textentry.get()
    code = ""
    for letter in text:
        code += " " + tree.codeLookUp[letter]
    #Remove this print statement
    print code
    result.set(code)

"""
Callback function that prompts the user to select a file from their drive. The available filetypes for
selection are determined by selections of a radio button interface. The chosen file has the possibility
of being written to with destruction of prior data.

Until more error checking and saftey measures have been implemented, use with caution.
"""
def destSelect():
    destFileName.set(askopenfilename(filetypes=[(fileTypes[selectionVar.get()-1][0],fileTypes[selectionVar.get()-1][1])]))
    
"""
Callback function that prompts the user to select a file from their drive. The available filetypes for
selection are determined by selections of a radio button interface. The chosen file might be read from
but will not be written to, so selection is safe.
"""
def sourceSelect():
    sourceFileName.set(askopenfilename(filetypes=[(fileTypes[selectionVar.get()][0],fileTypes[selectionVar.get()][1])]))

"""
Callback function that takes a huffman code in binary format, traverses a huffman tree and returns the symbol
that relates to the code.

This function makes the assumption that the frequency chart contains more then one value. Since I am
not allowing the user to define the frequency chart(yet), this is safe behavior.
"""
def decodeBin():
    text = ""
    code = binentry.get().lstrip()
    node = tree.nodeList[0]
    for base in code:
        
        #The if statements are far less then ideal, but for the sake of readability, I left them.
        if(base == "0"):
            node = node.left
        if(base == "1"):
            node = node.right
        if(node.value != None):
            text += node.value
            node = tree.nodeList[0]
            
    result.set(text)

#Container attributes
"""
The Var() types are used in tkinter. They update with changes to GUI widgets and also
have the ability to register callback functions when changes occur.
"""
selectionVar = IntVar()
selectionVar.trace("w", clearFiles)
encTex = StringVar()
encTex.set("")
decTex = StringVar()
decTex.set("")
result = StringVar()
result.set(None)
fileResult = StringVar()
fileResult.set("")
sourceFileName = StringVar()
sourceFileName.set("No source file selected")
destFileName = StringVar()
destFileName.set("No destination file selected")

fileTypes = [["textfiles", "*.txt"], ["encodedfiles", "*.enc"]]


#Menu bar declarations and initializations
"""
While certain functions of the menubar have been created, some functionality
remains to be implemented.
"""
topmenu = Menu(root)
filemenu = Menu(topmenu, tearoff=0)
filemenu.add_command(label="New Text",command=clearText)
filemenu.add_command(label="Save",command=save)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

topmenu.add_cascade(label="File", menu=filemenu)

optionsmenu = Menu(topmenu, tearoff=0)
optionsmenu.add_command(label="Change Endianness",command=changeEnd)
optionsmenu.add_command(label="Change Colors",command=colorChange)
optionsmenu.add_separator()
optionsmenu.add_command(label="Preferences",command=launchPreferences)

topmenu.add_cascade(label="Options", menu=optionsmenu)

helpmenu = Menu(topmenu, tearoff=0)
helpmenu.add_command(label="About Program",command=aboutProgram)
helpmenu.add_command(label="About Developer",command=aboutDev)
helpmenu.add_separator()
helpmenu.add_command(label="Online Help",command=launchHelp)

topmenu.add_cascade(label="Help", menu=helpmenu)

root.config(menu=topmenu)

#Notebook style TTK tab interface declarations and intitializations 
notebook = ttk.Notebook(root)

pageone = ttk.Frame(notebook)
pagetwo = ttk.Frame(notebook)

notebook.add(pageone, text="Manual Encoding and Decoding")
notebook.add(pagetwo, text="File Encoding and Decoding")
notebook.pack(fill=BOTH, expand=1)

#START of pageone members, aka the frame that corresponds to the first tab

#Labels
label1 = ttk.Label(pageone, text="Please enter some text or binary and press appropriate button")
label1.grid(row=0, sticky=W+E+N+S, pady=8, columnspan=5)
label2 = ttk.Label(pageone, text="Text to Encode:")
label2.grid(row=1, sticky=W, pady =2)
label3 = ttk.Label(pageone, text="Binary to Decode:")
label3.grid(row=2, sticky=W, pady =2)
label4 = ttk.Label(pageone, text="Result of operation: ")
label4.grid(row=3, pady =55, sticky=W)
resultLabel = ttk.Label(pageone, text="Nothing coded yet", textvariable=result, wraplength=190)
resultLabel.grid(row=3, column=1, pady=55, sticky=W)

#Entry capable widgets, which use Vars() to record the data and pass it to callback functions
textentry = ttk.Entry(pageone, textvariable=encTex)
textentry.grid(row=1, column=1, columnspan=3, pady=5, sticky=(N, S, E, W))
binentry = ttk.Entry(pageone, textvariable=decTex)
binentry.grid(row=2, column=1, columnspan=3, pady=5, sticky=(N, S, E, W))

#Buttons with attached callback functions
button1 = ttk.Button(pageone, text="Encode Text", command=encodeTex)
button1.grid(row=1, column=5, sticky=W+E)
button2 = ttk.Button(pageone, text="Decode Binary", command=decodeBin)
button2.grid(row=2, column=5, sticky=W+E)
#END of pageone members

#START of pagetwo members, aka the frame that corresponds to the second tab

#Labels
label5 = ttk.Label(pagetwo, text="Please select a source file, destination file, and a coding operation")
label5.grid(row=0, pady=8, columnspan=5)
label6 = ttk.Label(pagetwo, text="Source File: ")
label6.grid(row=2, column=1, sticky=W, pady =2)
sourceLabel = ttk.Label(pagetwo, textvariable=sourceFileName)
sourceLabel.grid(row=2, column=2, sticky=W, pady =2)
label7 = ttk.Label(pagetwo, text="Destination File: ")
label7.grid(row=3, column=1, sticky=W, pady =2)
destLabel = ttk.Label(pagetwo, textvariable=destFileName)
destLabel.grid(row=3, column=2, sticky=W, pady =2)
label8 = ttk.Label(pagetwo, text="Result Log: ")
label8.grid(row=6, pady =10, sticky=W)
label9 = ttk.Label(pagetwo, textvariable=fileResult, wraplength=190)
label9.grid(row=6, column=1, pady =10, sticky=W)

#Buttons with attached callback functions
button3 = ttk.Button(pagetwo, text="Select Source", width=18, command=sourceSelect)
button3.grid(row=2, column=0, sticky=W, pady=10)
button4 = ttk.Button(pagetwo, text="Select Destination", width=18, command=destSelect)
button4.grid(row=3, column=0, sticky=W, pady=10)
button5 = ttk.Button(pagetwo, text="Encode/Decode", width=18, command=startCoding)
button5.grid(row=4, column=0, sticky=W, pady=10)

#Raido buttons that allow the user to select different coding operations
#They map to the same variable because using this behavior causes only one to be selected at a time
radio1 = ttk.Radiobutton(pagetwo, text="Encode Source", value=0, variable=selectionVar)
radio1.grid(row=1, column=0, pady=5)
radio2 = ttk.Radiobutton(pagetwo, text="Decode Source", value=1, variable=selectionVar)
radio2.grid(row=1, column=1, pady=5)
#END of pagetwo members

#mainloop start and visible GUI creation. GUI and callback functions will now become active
root.mainloop()
