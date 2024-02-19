import requests
import json
import datetime
from pathlib import Path

# Constants
FEB18_START_BLOCK = 19251600
CHAINBASE_API_KEY = ''  # Replace with Chainbase API key

def fetch_block_hash_from_chainbase(block_height):
    """
    Fetches the Ethereum block hash for a given block height using the Chainbase API.

    Args:
    - block_height: The height of the block for which to fetch the hash.

    Returns:
    - The block hash as a string if found, otherwise an error message.
    """
    api_url = f"https://api.chainbase.online/v1/eth/blocks/{block_height}"
    headers = {
        'x-api-key': CHAINBASE_API_KEY,
        'Accept': 'application/json'
    }
    response = requests.get(api_url, headers=headers)

    if response.ok:
        data = response.json()
        return data.get('hash', "Block hash not found or error in API response.")
    else:
        return f"Error fetching block hash: HTTP {response.status_code}"


def calculate_winner_index(block_hash, total_holders):
    """
    Calculates the index of the winning holder using the block hash and the total number of holders.

    Args:
    - block_hash: The hash of the block, used as the seed for the calculation.
    - total_holders: The total number of holders participating.

    Returns:
    - The index of the winning holder.
    """
    block_hash_decimal = int(block_hash, 16)  # Convert hex to decimal
    winner_index = block_hash_decimal % total_holders  # Calculate modulo
    return winner_index


def generate_reward_block_heights():
    """
    Generates a dictionary mapping dates to reward block heights.

    Returns:
    - A dictionary with date keys and block height values.
    """
    reward_block_heights = {}
    block_height = FEB18_START_BLOCK

    # February 18th to 28th
    for day in range(18, 29):
        block_height += (24 * 3600) // 12
        reward_block_heights[f'202402{day:02d}'] = int(block_height)

    # March 1st to 20th
    for day in range(1, 21):
        block_height += (24 * 3600) // 12
        reward_block_heights[f'202403{day:02d}'] = int(block_height)

    return reward_block_heights


# Main execution
if __name__ == "__main__":
    today = datetime.datetime.utcnow().strftime('%Y%m%d')
    holders_file_path = f"holders_{today}.json"
    reward_block_heights = generate_reward_block_heights()

    if Path(holders_file_path).exists():
        with open(holders_file_path, 'r') as file:
            holders = json.load(file)

        if today in reward_block_heights:
            block_height = reward_block_heights[today]
            block_hash = fetch_block_hash_from_chainbase(block_height)
            print(f"Fetched Block Hash: {block_hash}")

            winner_index = calculate_winner_index(block_hash, len(holders))
            winner = holders[winner_index]
            print("Today's Winner:", winner)
        else:
            print("No reward block height for today's date.")
    else:
        print("Error: Holders file does not exist for today.")