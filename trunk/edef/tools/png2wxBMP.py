#!/usr/bin/python
import cStringIO
import binascii
import sys

def read_file(fname):
    string = ""
    data = open(fname, "rb").read()
    return binascii.b2a_hex(data)

def pycode( string ):
    return """import wx
import cStringIO
import binascii

image_data = "%s"

def getImage():
    stream = cStringIO.StringIO( binascii.a2b_hex(image_data) )
    return wx.ImageFromStream( stream )

def getBitmap():
    return wx.BitmapFromImage( getImage() )
"""%string
    

if __name__ == "__main__":
    try:
        iname = sys.argv[1]
        oname = sys.argv[2]
    except:
        raise Exception("Usage: png2wxBMP.py infile.png outfile.py")

    pydata = pycode(read_file(iname))

    fp = open(oname, "w")
    fp.write(pydata)
    fp.close()
