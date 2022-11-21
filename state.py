#!/usr/bin/python
import os
import subprocess
import time
import json

ARPA_HOLDER_ADDRESS = "0xf977814e90da44bfa03b6295a0616a897441acec"
ARPA_ADDRESS = "0xBA50933C268F567BDC86E1aC131BE072C6B0b71a"
ACCOUNT_PATH = "accounts.json"
ACCOUNT_NUMBER = 20
accountSet = []
def killAnvil():
    os.system("killall -9 anvil")

def execCmd(cmd):
    p = subprocess.Popen(cmd)
    p.wait()

def startChain(accountNumber, balance):
    killAnvil()
    mainnetUrl = 'https://mainnet.infura.io/v3/e263f48ae1f545198575c7c7d4088f57'
    cmd = ['anvil', '--fork-url', mainnetUrl, '--accounts', str(accountNumber), '--balance', str(balance)]
    p = subprocess.Popen(cmd)
    time.sleep(20)

def mineBlock(number):
    cmd = ['cast', 'rpc', 'anvil_mine', str(number)]
    execCmd(cmd)

def setAccountBalance(account, balance):
    cmd = ['cast', 'rpc', 'anvil_setBalance', account, str(balance)]
    execCmd(cmd)

def getAccountBalance(account):
    cmd = ['cast', 'balance', account]
    outPut = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    stdout, stderr = outPut.communicate()
    for line in stdout.decode().split('\n'):
        if line.find("0x"):
            return int(line)
    return -1

def impersonateAccount(account):
    cmd = ['cast', 'rpc', 'anvil_impersonateAccount', account]
    execCmd(cmd)

def stopImpersonateAccount(account):
    cmd = ['cast', 'rpc', 'anvil_stopImpersonatingAccount', account]
    execCmd(cmd)

def transferArpa(addressTo, addressFrom, value):
    cmd = ['cast', 'send', ARPA_ADDRESS, 'transfer(address, uint256)',
            str(addressTo), str(value), '--from', addressFrom]
    execCmd(cmd)   

def getArpaBalance(address):
    cmd = ['cast', 'call', ARPA_ADDRESS, 'balanceOf(address)', str(address)]
    execCmd(cmd)

def loadAccounts(accountPath):
    accounFile = open(accountPath)
    accountSet = json.load(accounFile)
    impersonateAccount(ARPA_HOLDER_ADDRESS)
    for account in accountSet:
        transferArpa(account["account"], ARPA_HOLDER_ADDRESS, account["balance"])
        getArpaBalance(account["account"])
    stopImpersonateAccount(ARPA_HOLDER_ADDRESS)

def getAccountSet():
    return accountSet

def main():
    startChain(ACCOUNT_NUMBER, 1000)
    loadAccounts(ACCOUNT_PATH)
    mineBlock(3)
    

if __name__== "__main__" :
    main()