# Data Documentation

This directory hosts datasets integral to our research on analyzing blockchain transactions across multiple chains. It encompasses comprehensive transaction data, graph representations, and categorization labels for contracts involved in the transactions.

## Dataset Overview

### Global Graphs
The `global graph` folder contains graph data for three major blockchain chains: Ethereum, Polygon, and BNB. Each blockchain's corresponding folder includes two specific files:
- `{chain}_graph_more_than_1_ratio.csv`: Contains edges where the weight—indicative of transactional or interaction metrics—exceeds 1\%. This is the same as the setting of our experiments in the paper. In this file, contracts are denoted by numerical indices rather than traditional addresses.
- `{chain}_contract_to_number_mapping.json`: Maps each contract's address to a numerical index utilized in the global graph files, facilitating cross-reference and analysis.

### Transactions
The `transactions` folder houses zipped archives with detailed transaction records for all labeled contracts within the aforementioned chains:
- `ethereum.zip`
- `polygon.zip`
- `bnb.zip`
Each zip file includes comprehensive transaction data such as block number, sender (from), receiver (to), transaction hash, value, and timestamp.

### Labels
The `labels.csv` file categorizes each contract across different chains. It includes the following columns:
- `Chain`: Specifies the blockchain platform (e.g., Ethereum, Polygon, BNB).
- `Contract`: Lists the contract address or identifier.
- `Category`: Represents the category of the contract, indexed by the prevalence of contracts within that category (Category 0 contains the most contracts).

## Accessing the Data
The dataset is available for download via the following link: [Token Data](https://drive.google.com/drive/folders/1VV5ht9Eh8WGtKfkS0ipIk0FNI7g-WJfJ?usp=share_link).

## Utilizing the Dataset
To effectively use this dataset, follow these steps:
1. Download the necessary files using the link provided above.
2. Decompress each chain's transaction archive to access individual transaction details.
3. Employ the JSON mapping files to decode contract indices within the global graphs.
4. Refer to `labels.csv` to understand the categorization of each contract, which is crucial for targeted analysis and comparative studies across different categories.

