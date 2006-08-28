#!/usr/bin/python
#
# The MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of 
# this software and associated documentation files (the "Software"), to deal in the 
# Software without restriction, including without limitation the rights to use, copy, 
# modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, subject to the 
# following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# BillReminder - Copyright (c) 2006 Og Maciel
#
# -*- coding: utf-8 -*-

import os

try:
    from xml.dom.ext.reader.Sax2 import FromXmlFile
    from xml.dom.ext import PrettyPrint
except:
    sys.exit(1)
    
class Xml:
    def __init__(self, xmlfile):
        self.xmlfile = xmlfile
        self.xmldoc = FromXmlFile(xmlfile)

    def addBillNode(self):
        node = self.xmldoc.createElement('Bill')
        
        return node

    def addBill(self, payee):
        node = self.addBillNode()
        child = self.xmldoc.createElement('payee')
        child.appendChild(self.xmldoc.createTextNode(payee))
        
        node.appendChild(child)

        self.xmldoc.childNodes[1].appendChild(node)

    def save(self):
        f = open(self.xmlfile, 'w')
        PrettyPrint(self.xmldoc, f)
        f.close()