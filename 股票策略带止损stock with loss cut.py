# coding:utf-8
#!/usr/bin/env python
from PoboAPI import *
import datetime
#用poboquant python实现，在poboquant上运行，如果有问题 可加群 726895887 咨询
#开始时间，用于初始化一些参数
def OnStart(context) :
    print "I\'m starting..."
    #设定一个全局变量品种
    g.code = "002714.SZSE"
    #订阅实时数据，用于驱动OnQuote事件
    SubscribeQuote(g.code)
    #订阅K线数据，用于驱动OnBar事件
    SubscribeBar(g.code, BarType.Day)
    #登录交易账号，需在主页用户管理中设置账号，并把证券测试替换成您的账户名称
    context.myacc = None
    if context.accounts.has_key("回测证券") :
        print "登录交易账号[回测证券]"
        if context.accounts["回测证券"].Login() :
            context.myacc = context.accounts["回测证券"]
  
#实时行情事件，当有新行情出现时调用该事件
def OnQuote(context, code) :
    #过滤掉不需要的行情通知
    if code != g.code :
        return

    #获取最新行情
    dyndata = GetQuote(code)
    if dyndata :
        #.now指最新价，详细属性见API文档
        now1 = dyndata.now
        #打印最新价
        log.info("最新价: " + str(dyndata.now))

    #获取K线数据
    klinedata = GetHisData(code, BarType.Day)
    #打印K线数据，如最新一根K线的最高价
    if len(klinedata) > 0 :
        lasthigh = klinedata[-1].high
        log.info("最新K线的最高价: "  + str(lasthigh))
    #如果配置好交易账号了，可以根据条件下单，需把下面中的证券测试账号换成您设置的账号名称
    if len(klinedata) > 1 and klinedata[-1].close > klinedata[-2].close * 1.01 and context.myacc :
        # 当日收盘价大于昨收的1.01倍则买入
        context.myacc.InsertOrder(code, BSType.Buy, dyndata.now, 1000)
    elif len(klinedata) > 1 and klinedata[-1].close > klinedata[-2].close * 1.02 and context.myacc :
        # 当日收盘价大于昨收的1.02倍则卖出
        context.myacc.InsertOrder(code, BSType.Sell, dyndata.now, 1000)
        
    elif len(klinedata) > 1 and klinedata[-1].close < klinedata[-2].close * 0.99 and context.myacc :
        # 当日收盘价小于昨收的0.99则卖出 止损
        context.myacc.InsertOrder(code, BSType.Sell, dyndata.now, 1000)    

#委托回报事件，当有委托回报时调用
def OnOrderChange(context, AccountName, order) :
    #打印委托信息，id是编号，volume是数量，详细见API文档
    print "委托编号： " + order.id + "   账号名称： " + AccountName
    print "Vol: " + str(order.volume) + " Price: " + str(order.price)
