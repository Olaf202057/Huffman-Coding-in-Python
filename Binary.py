"""
binary.py by Ryan Latham
Last modification on 4/30/2011

Module that converts between binary or hex strings in the form of "0001" or "AFF" respectively. It
only deals with strings and adds no special formatting. For example it will not take a binary string
in the form of "0001" and convert it to a hex string "\x01" but will convert it to a hex string "01".
"""

#Lookup dictionaries for conversion
HexBin = {'0':'0000', '1':'0001', '2':'0010', '3':'0011', '4':'0100', '5':'0101',
          '6':'0110', '7':'0111', '8':'1000', '9':'1001', 'A':'1010', 'B':'1011',
          'C':'1100', 'D':'1101', 'E':'1110', 'F':'1111'}

BinHex = {'0000':'0', '0001':'1', '0010':'2', '0011':'3', '0100':'4', '0101':'5',
          '0110':'6', '0111':'7', '1000':'8', '1001':'9', '1010':'A', '1011':'B',
          '1100':'C', '1101':'D', '1110':'E', '1111':'F'}

# If I have a chance, play around with hexVal.upper(). Possibly do it right in the arg list
"""
A function that converts a hex string in the form "AF" to a binary string in the form "10101111".
If the hex string is given in lower case, it will be converted to uppercase.
"""
def HexToBin(hexVal):
    output = ""
    hexVal = hexVal.upper()
    for c in hexVal:
        output += HexBin[c]
    return output
"""
Converts from binary string to hexadecimal string. While my huffman program requires that the conversion
give me whole bytes and not just hexadecimal values, for the sake of reuse, I will not enforce that
requirment here.
"""
def BinToHex(binVal):
    output = ""
    bits = []
    length = len(binVal)
    if(length%4 != 0):
        for x in range(4-(length%4)):
            binVal += "0"
            length +=1
    for i in range((length/4)):
        bits.append(binVal[i*4:(4 + (i*4))])
    for halfByte in bits:
        output+= BinHex[halfByte]
    return output
    
