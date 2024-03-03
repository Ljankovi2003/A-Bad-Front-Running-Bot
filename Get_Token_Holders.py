import datetime
import time
from urllib.request import Request, urlopen
import bs4
from web3 import Web3
from web3.middleware import geth_poa_middleware

# Import ABI
from uniswap_router_abi import abi

# Initialize Web3 with Binance Smart Chain node
bsc_provider = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc_provider))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Contract address
PancakeRouterAddress = "0x10ed43c718714eb63d5aa57b78b54704e256024e"

# Function to fetch holders of a token
def fetch_token_holders(token_address):
    try:
        link = f"https://bscscan.com/token/{token_address}"
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = bs4.BeautifulSoup(webpage, "html.parser")
        element = soup.findAll('div', {'class': "mr-3"})[0].text
        holders_txt = element.split(" ")[0]
        holders = int(holders_txt.replace(",", ""))
        return holders
    except Exception as e:
        print(f"Error fetching token holders for {token_address}: {e}")
        return None

# Main loop
def main_loop():
    while True:
        try:
            blockdata = web3.eth.getBlock(block_identifier="latest", full_transactions=True)
            transactions = blockdata['transactions']

            for tx in transactions:
                input_data = tx["input"]
                if input_data.startswith("0xf305d719"):  # Check if it's a PancakeSwap transaction
                    try:
                        byte = tx["hash"]
                        txhash = web3.toHex(byte)

                        # Decode function input
                        contract = web3.eth.contract(address=PancakeRouterAddress, abi=abi)
                        data = contract.decode_function_input(input_data)
                        token_address = data[1]["token"]
                        
                        # Fetch holders count
                        holders_count = fetch_token_holders(token_address)
                        if holders_count is not None and holders_count < 5:
                            print(f"Low holders for token {token_address}: {holders_count}")
                            # Do something with low holders
                    except Exception as e:
                        print(f"Error processing transaction: {e}")
        except Exception as e:
            print(f"Error fetching latest block: {e}")
        time.sleep(1)

# Example usage
if __name__ == "__main__":
    main_loop()
