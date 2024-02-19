import requests
import json
import time
from datetime import datetime

# Important Note: This script is run every day at 00:35 UTC+0
# The holder snapshot can be verified at https://ibit.infinitybit.io/contest/holder-snapshots

network_id = '1'  # Ethereum Mainnet
token_addr = '0xA3cB87080e68AD54D00573983D935Fa85d168FDE' # IBIT
api_key = ''  # Replace with Chainbase API key
limit = 100  # Maximum number of token holders to fetch per request

if not api_key:
    print("Error: API key is required")
    quit(1)

def fetch_token_holders(network_id, token_addr, api_key, page, limit):
    """
    Fetches token holders from the API, paginated by the 'page' number.
    """
    url = f"https://api.chainbase.online/v1/token/holders?chain_id={network_id}&contract_address={token_addr}&page={page}&limit={limit}"
    headers = {
        "x-api-key": api_key,
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()
    else:
        print(f"HTTP Error: {response.status_code}")
        return None

all_holders = []
page = 1
is_last_page = False
errors = 0

while not is_last_page:
    response = fetch_token_holders(network_id, token_addr, api_key, page, limit)
    if response and 'data' in response:
        all_holders.extend(response['data'])
        page += 1
        print(f"Fetched from page {page - 1}")
        if len(response['data']) < limit:
            is_last_page = True
    else:
        errors += 1
        if errors >= 10:
            is_last_page = True
        print("Error occurred or reached last page of data.")
        time.sleep(1)
    time.sleep(0.25)

invalid_addresses = [
    '0x000000000000000000000000000000000000dead',  # Dead address
    '0xA3cB87080e68AD54D00573983D935Fa85d168FDE',  # Token contract address
    '0xC707E0854DA2d72c90A7453F8dc224Dd937d7E82',  # NULS NerveNetwork Parnership - Bank Node Multisig
    '0x5899bef146be8228788c476b6384044d1a51f96e',  # Uniswap V2
    '0xd1CB9007D51FB812805d80618A97418Fd388B0C5',  # V2 Marketing & Dev Wallet
    '0xA6e18D5F6b20dFA84d7d245bb656561f1f9aff69',  # V1 Legacy Marketing Wallet
    '0x9d0D8E5e651Ab7d54Af5B0F655b3978504E67E0C',  # V1 Legacy Dev Wallet
    '0x02DAb704810C40C87374eBD85927c3D8a9815Eb0',  # V2 Legacy Dev Wallet
    '0x6d9e1352e1f8f66f96669cc28fdcfe8e7fcf5524',  # Legacy Operations Wallet
    '0x3d61e4968cc10cf3bd008835f1d78ecbac334609'   # Operations Wallet
]

def filter_invalid_addresses(holders, invalid_addresses):
    """
    Filters out holders with addresses listed as invalid, ignoring case sensitivity.
    """
    # Convert all invalid addresses to lowercase for case-insensitive comparison
    invalid_addresses_lower = [addr.lower() for addr in invalid_addresses]
    # Filter holders by converting each address to lowercase before the comparison
    return [holder for holder in holders if holder.lower() not in invalid_addresses_lower]

filtered_holders = filter_invalid_addresses(all_holders, invalid_addresses)

print(f"Total Holders Fetched After Filtering: {len(filtered_holders)}")

# Save the filtered holders to a JSON file
file_name = f"./holders_{datetime.now().strftime('%Y%m%d')}.json"
with open(file_name, "w") as file:
    json.dump(filtered_holders, file)

print(f"Filtered holders saved to {file_name}")
