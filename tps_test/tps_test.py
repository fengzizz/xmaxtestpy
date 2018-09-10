#!/usr/bin/env python
#! -*- coding:utf-8 -*-

#import xmax.trx

import random
import time

from xmax import account, trx, rpc

from urllib import request, parse


print("test begin")

CREATOR_PRI_KEY = '5KDVLHu4YDA6bBnu9GQbr25saJoNZrHRb4mq1WQwDouhGizqQvU'
CREATOR_NAME = 'testerb'

OWNER_KEY = 'XMX5Wgr3AkX9k1hLjymep9snY2AwvXDAVJBTEQw38t49A8RCR2H3j'
ACTIVE_KEY = 'XMX7zXBwWFHgk9ovzZtUf5y3FK6Sk85biSbZgFTWTcnZewHaXUSCT'

RPC_SERVER_POINT = 'http://127.0.0.1:18801'

GET_ACC_RPC = RPC_SERVER_POINT + '/v0/xmaxchain/get_account'

RANCHARS =['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4']

NEWACC_PREFIX = 'tn'

def accName(prefix, idx):
    accname = prefix + str(idx)
    return accname


TEST_NEWACC_COUNT = 2000
SLEEP_POINT = 100
SLEEP_TIME = 0.001

ranchars = random.sample(RANCHARS, 4)
rstr = ''
rstr = rstr.join(ranchars)

prefix = NEWACC_PREFIX + rstr + '.'

for idx in range(0, TEST_NEWACC_COUNT):

    if(idx % SLEEP_POINT == 0):
        print('sleepping...')
        time.sleep(SLEEP_TIME)

    accname = accName(prefix, idx)
    newaccjson = account.newAccountJson(CREATOR_NAME, accname, 1, OWNER_KEY, ACTIVE_KEY)

    scopes = [CREATOR_NAME]

    trxjson = trx.formatTrxJson([newaccjson], scopes)

    postjson = trx.formatPostJson([CREATOR_PRI_KEY], [trxjson])

    print('new account: ' + accname)

    rpc.pushTrxRpc(RPC_SERVER_POINT, postjson, False)

    #print(postjson)

time.sleep(0.5)

for idx in range(0, TEST_NEWACC_COUNT):

    accname = accName(prefix, idx)
    getjson = account.getAccountJson(accname)
    rpc.rpcCall(GET_ACC_RPC, getjson, True)
    time.sleep(SLEEP_TIME)

