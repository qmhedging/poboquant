#!/usr/bin/env python
# coding:utf-8
from PoboAPI import *
import datetime


def OnStart(context) :

 print "to print exchange asset information"
 ch = GetVarieties("SHSE") #输出支持的交易所品种
 print str(ch)
