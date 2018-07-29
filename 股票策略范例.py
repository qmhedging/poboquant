#!/usr/bin/env python
# coding:utf-8
from PoboAPI import *
def OnStart(context) :
    print "I\'m starting..."
    g.code = "600519.SHSE"
    SubscribeQuote( "600519.SHSE")
    SubscribeBar( "600519.SHSE",BarType.Day)    
    if context.accounts.has_key("回测证券") :
        print "登录交易账号 证券测试"
        context.accounts["回测证券"].Login()
        
def OnQuote(context,code) :
    print '调用到OnQuote事件'
    dyndata = GetQuote("600519.SHSE")
    now1 = dyndata.now
    option = PBObj()
    klinedata = GetHisData(g.code, BarType.Day, option)
    if klinedata[len(klinedata)-1].close < klinedata[len(klinedata)-2].close :
        # 当日收盘价小于昨收则买入     
        context.accounts["回测证券"].InsertOrder("600519.SHSE", BSType.Buy, dyndata.now, 100) #买入100股
    elif klinedata[len(klinedata)-1].close > klinedata[len(klinedata)-2].close:
        # 当日收盘价大于昨收则卖出
        context.accounts["回测证券"].InsertOrder(code, BSType.Sell, dyndata.now, 100) #卖出100股
