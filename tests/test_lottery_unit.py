from urllib.request import Request
from brownie import Lottery, accounts, config, network , exceptions
import pytest
from web3 import Web3
from scripts.deploy_lottery import deploy_lottery, end_lottery
from scripts.helpful_scripts import fund_with_link, get_account,get_contract ,lOCAL_BLOCKCHAIN_ENVO


def test_get_entrance_fee():
    # arrange
    lottery= deploy_lottery()
    # act
    entracne_fee = lottery.getEntranceFee()
    
    # assert 
    assert entracne_fee >= Web3.toWei(0.016, 'ether')
    assert entracne_fee <= Web3.toWei(0.018, 'ether')

def test_cant_enter_unless_started():
    # arrange
    if network.show_active not in lOCAL_BLOCKCHAIN_ENVO:
        pytest.skip()
    lottery= deploy_lottery()
    # act / assert 
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({'from':get_account(), 'value': lottery.getEntranceFee()})

def test_can_start_enter_lottery():
    # arrange     
    if network.show_active not in lOCAL_BLOCKCHAIN_ENVO:
        pytest.skip()
    lottery= deploy_lottery()
    account = get_account()
    # act 
    lottery.startLottery({'from':account,})    
    lottery.enter({'from':get_account(), 'value': lottery.getEntranceFee()})
    # assert 
    assert lottery.players(0)==account

def test_can_end_lottery():
    # arrange     
    if network.show_active not in lOCAL_BLOCKCHAIN_ENVO:
        pytest.skip()
    lottery= deploy_lottery()
    account = get_account()
    lottery.startLottery({'from':account,})    
    lottery.enter({'from':get_account(), 'value': lottery.getEntranceFee()})
    fund_with_link(lottery)
    # act 
    lottery.endLottery({'from':lottery})
    # assert 
    assert lottery.lottery_state() == 2

def test_can_pick_winner_corectly():
    # arrange  
    # print(network.sh)   
    if network.show_active() not in lOCAL_BLOCKCHAIN_ENVO:
        pytest.skip()
    lottery= deploy_lottery()
    account = get_account()
    lottery.startLottery({'from':account,})    
    lottery.enter({'from':get_account(), 'value': lottery.getEntranceFee()})
    lottery.enter({'from':get_account(index=1), 'value': lottery.getEntranceFee()}) 
    lottery.enter({'from':get_account(index=2), 'value': lottery.getEntranceFee()})
    fund_with_link(lottery)  
    transaction = lottery.endLottery({'from':account})  
    requestId = transaction.events['RequestedRandomness']['requestId']
    get_contract('vrf_cordinator').callBackWithRandomness(requestId, 777,lottery.address,{'from':account})
    
    starting_balance_of_account = account.balance()
    starting_balance_of_lottery = lottery.balance()
    
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account+starting_balance_of_lottery










