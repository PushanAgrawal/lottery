import imp
from brownie import Lottery, accounts, config, network
import pytest
from scripts.helpful_scripts import fund_with_link, get_account, lOCAL_BLOCKCHAIN_ENVO 
from scripts.deploy_lottery import deploy_lottery
import time


def test_can_pick_winner():
    if network.show_active() in lOCAL_BLOCKCHAIN_ENVO:
        pytest.skip
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({'from':account})
    lottery.enter({'from':account, 'value':lottery.getEntranceFee()})
    lottery.enter({'from':account, 'value':lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({'from':account})
    time.sleep(60)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    


