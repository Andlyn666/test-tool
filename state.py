#!/usr/bin/python
import os
import subprocess
import time

def kill_anvil():
    os.system("killall -9 anvil")

def deploy_token():
    cmd = ['forge', 'create', 'src/arpa.sol:HydronG', '--private-key', '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80']
    outPut = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    stdout, stderr = outPut.communicate()
    for line in stdout.decode().split('\n'):
        addressLine = line.split("Deployed to: ")
        if len(addressLine) > 1 :
            return addressLine[1]
    return

def setCoinbase(contractAddress):
    cmd = ['cast', 'rpc', 'anvil_setCoinbase', contractAddress]
    subprocess.Popen(cmd)

def start_chain(accountNum, balance):
    kill_anvil()
    cmd = ['anvil', '--accounts', accountNum, '--balance', balance]
    subprocess.Popen(cmd)
    time.sleep(2)
    contractAddress = deploy_token()
    setCoinbase(contractAddress)

def mine_block(number):
    cmd = ['cast', 'rpc', 'anvil_mine', str(number)]
    subprocess.Popen(cmd)

def set_account_balance(account, balance):
    cmd = ['cast', 'rpc', 'anvil_setBalance', account, str(balance)]
    subprocess.Popen(cmd)

def get_account_balance(account) :
    cmd = ['cast', 'balance', account]
    subprocess.Popen(cmd)

def main():
    start_chain('20', '80000')
    get_account_balance('0x70997970c51812dc3a010c7d01b50e0d17dc79c8')
    time.sleep(1)
    set_account_balance('0x70997970c51812dc3a010c7d01b50e0d17dc79c8', 888)
    time.sleep(1)
    get_account_balance('0x70997970c51812dc3a010c7d01b50e0d17dc79c8')
    mine_block(3)

if __name__== "__main__" :
    main()