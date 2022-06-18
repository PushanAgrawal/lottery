from brownie import accounts, network, MockV3Aggregator, config, Contract, VRFCoordinatorMock, LinkToken, interface
from web3 import Web3


FORKED_LOCAL_ENVO = ['mainnet-fork','mainnet-for-dev']
lOCAL_BLOCKCHAIN_ENVO=['development','ganache-locals']
Decimall=8
starting_price=200000000000


def get_account(index=None, id=None):
    if index:
        return accounts[index]

    if id:
        return  accounts.load(id)     
        

    if network.show_active() in lOCAL_BLOCKCHAIN_ENVO or network.show_active in FORKED_LOCAL_ENVO:
        return accounts[0]

        
    # return  accounts.load("pushanag") 

contract_to_mock = {'eth_usd_price_feed':MockV3Aggregator, 'vrf_cordinator':VRFCoordinatorMock, 'link_token':LinkToken}    

def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in lOCAL_BLOCKCHAIN_ENVO:
        if len(contract_type) <= 0 :
            deploy_mocks()
        contract = contract_type[-1]

    else:
        contract_address = config['networks'][network.show_active()][contract_name]     
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)

    return contract    


def deploy_mocks():
    print('deploying mock......................')
    
    MockV3Aggregator.deploy(Decimall,Web3.toWei(starting_price, 'ether'),{'from':get_account()})
    link_token = LinkToken.deploy({'from':get_account()})
    VRFCoordinatorMock.deploy(link_token.address,{'from':get_account()})
    

    print("mock deployed.....................")  

def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000,):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract('link_token')
    tx = link_token.transfer(contract_address, amount, {'from':account})
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx= link_token_contract.transfer(contract_address, amount, {'from':account})
    tx.wait(1)
    print('funded')
    return tx
    
