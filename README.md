# Elevate & Earn: $20,000 USDT InfinityBit Contest

Welcome to the official GitHub repository for the Elevate & Earn: $20,000 USDT InfinityBit Contest. This open-source codebase contains the scripts utilised to run our provably fair contest, designed to directly reward our community as our social media presence expands.

## About the Contest

The InfinityBit contest runs from February 20th to March 20th and is structured to reward our supporters in tandem with the growth of our digital footprint on Twitter. For every 1,000 new followers on our official Twitter account [@infinitybit_io](https://twitter.com/infinitybit_io), the daily prize pool increases by $10. This structure ensures that as our community grows, so do the rewards for our supporters.

- **Start Date:** February 20th
- **End Date:** March 20th
- **Daily Prize Increase:** $10 for every 1,000 new followers
- **Maximum Prize Pool:** $20,000 USDT
- **Eligibility:** Must hold a minimum of 5,000 InfinityBit Tokens (IBIT) and follow [@infinitybit_io](https://twitter.com/infinitybit_io) on Twitter. Must follow @infinitybit_io and make at least one tweet with $IBIT and tag @infinitybit_io. Additional requirements apply.  See https://ibit.infinitybit.io/contest/ for full eligibility requirements. Void where prohibited.

## Repository Contents

This repository contains two Python scripts essential for the contest's operation:

- `get-holders.py`: This script is responsible for fetching the current holders of InfinityBit Tokens (IBIT) and determining their eligibility based on the contest rules.
- `select-winner.py`: Utilises a provably fair mechanism to select a daily winner from the pool of eligible participants. The winner selection is based on the hash of a specific Ethereum block, ensuring fairness and transparency.

## How It Works

### Fetching Holders

The `get-holders.py` script fetches the list of current IBIT token holders and filters them based on the eligibility criteria for the contest. It ensures that only participants meeting the minimum token holding requirement are considered for the daily draw.

### Selecting Winners

The `select-winner.py` script selects the daily winner using a provably fair algorithm. It employs the hash of a predetermined Ethereum block to ensure randomness that cannot be manipulated. The selection process is transparent, allowing anyone to verify the fairness of the draw.

## Installation and Usage

To use the scripts, you will need Python3 installed on your system. Clone this repository and navigate to its directory. Install the required dependencies by running:

```bash
pip install -r requirements.txt
