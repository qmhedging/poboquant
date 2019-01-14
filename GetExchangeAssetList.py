# coding:utf-8
#!/usr/bin/env python
from PoboAPI import *
import datetime
#用poboquant python实现，在poboquant上运行，如果有问题 可加群 726895887 咨询

def OnStart(context) :

 print "to print exchange asset information"
 ch = GetVarieties("SHSE") #输出支持的交易所品种
 print str(ch)
