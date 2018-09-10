#!/usr/bin/env python
#! -*- coding:utf-8 -*-

import random
import time

from xmax import account, trx, rpc, transfer

from urllib import request, parse

RPC_SERVER_POINT = 'http://127.0.0.1:18801'

GET_INFO_RPC = RPC_SERVER_POINT + '/v0/xmaxchain/get_info'

CREATOR_PRI_KEY = '5KDVLHu4YDA6bBnu9GQbr25saJoNZrHRb4mq1WQwDouhGizqQvU'
CREATOR_NAME = 'testerb'

OWNER_KEY = 'XMX5Wgr3AkX9k1hLjymep9snY2AwvXDAVJBTEQw38t49A8RCR2H3j'
ACTIVE_KEY = 'XMX7zXBwWFHgk9ovzZtUf5y3FK6Sk85biSbZgFTWTcnZewHaXUSCT'
ACTIVE_KEY_PRIVATE = '5KDVLHu4YDA6bBnu9GQbr25saJoNZrHRb4mq1WQwDouhGizqQvU'

RANCHARS =['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4']

NEWACC_PREFIX = 'tn'

def checkConnect():
    try:
        rpc.rpcCall(GET_INFO_RPC, "", False)
    except Exception:
        print('no connection, sleep...')
        return False
    else:
        return True

def newAccount(accname, amount, show = False):
    newaccjson = account.newAccountJson(CREATOR_NAME, accname, amount, OWNER_KEY, ACTIVE_KEY)

    scopes = [CREATOR_NAME]

    trxjson = trx.formatTrxJson([newaccjson], scopes)

    postjson = trx.formatPostJson([CREATOR_PRI_KEY], [trxjson])

    rpc.pushTrxRpc(RPC_SERVER_POINT, postjson, False)

    if show:
        print('new account: ' + accname)

    return

def transferTest(Acc1, Acc2, amount):
    newjson1 = transfer.transferJson(Acc1, Acc2, amount, "")
    scopes = [Acc1, Acc2]
    scopes.sort()
    msgs = [newjson1]

    trxjson = trx.formatTrxJson(msgs, scopes)

    postjson = trx.formatPostJson([ACTIVE_KEY_PRIVATE], [trxjson])

    rpc.pushTrxRpc(RPC_SERVER_POINT, postjson, False)
    return  

TEST_TRANSFER_COUNT = 10
TEST_MEGS_IN_TRX = 300
TEST_ACC_COUNT = 50
TEST_TRANSFER_AMOUNT = 1
SLEEP_TIME = 0.7


ranchars = random.sample(RANCHARS, 4)
rstr = ''
rstr = rstr.join(ranchars)

prefix = NEWACC_PREFIX + rstr + '.'

accpool = []

accs = []

while(True):
    if checkConnect():
        break
    else:
        time.sleep(5)


print('new accounts ...')

for idx in range(0, TEST_ACC_COUNT):

    s = str(idx).zfill(5)
    tempacc = prefix + s
    accs.append(tempacc)
    accpool.append(tempacc)
    if len(accs) >= 50:
        for acc in accs:
            newAccount(acc, 100)
        accs.clear()
        time.sleep(SLEEP_TIME)

if len(accs) > 0:
    for acc in accs:
        newAccount(accs[acc], 100)
    accs.clear()


time.sleep(1)

print('tps test begin ...')

sleeptime = 1.5 + random.random() * 4

time.sleep(sleeptime)

def newBatch():
    transsuite = int(20 + random.random() * 100)
    msgjs = []
    scopes = set()
    acccount = len(accpool)
    print('tps batch msgs: ' + str(transsuite * 2))

    for idx in range(0, transsuite):
        idx1 = int(random.random() * acccount)
        step = 1 + int(random.random() * acccount / 2)
        idx2 = int(idx1 + step) % acccount

        acc1 = accpool[idx1]
        acc2 = accpool[idx2]

        newjson1 = transfer.transferJson(acc1, acc2, TEST_TRANSFER_AMOUNT, "")
        newjson2 = transfer.transferJson(acc2, acc1, TEST_TRANSFER_AMOUNT, "")
        msgjs.append(newjson1)
        msgjs.append(newjson2)

        scopes.add(acc1)
        scopes.add(acc2)
    

    ss = [i for i in scopes]
    ss.sort()

    trxjson = trx.formatTrxJson(msgjs, ss)

    postjson = trx.formatPostJson([ACTIVE_KEY_PRIVATE], [trxjson])

    rpc.pushTrxRpc(RPC_SERVER_POINT, postjson, False)


while True:
    rentran = random.random()

    if rentran < 0.3:
        print('tps batch none ...')
        continue

    while(True):
        if checkConnect():
            break
        else:
            time.sleep(5)

    try:
        newBatch()
    except Exception as e:
        print("Exception: " + str(e))
        time.sleep(5)

    time.sleep(0.5)



print('tps test end ...')
            
