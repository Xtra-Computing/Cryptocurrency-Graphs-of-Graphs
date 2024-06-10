# Data Documentation

This directory contains datasets related to our research on analyzing blockchain transactions across multiple chains. It includes detailed transaction data, graph representations, and labels for the contracts.

## Dataset Overview

### Global Graphs
The `global graph` folder contains the graph data for three blockchain chains: Ethereum, Polygon, and BNB. Each chain's folder includes the following files:
- `{chain}_graph_more_than_1_ratio.csv`: This file contains all edges in the global graph where the weight (representing some form of transactional or interaction metric) exceeds 1%. Here, contracts are represented by indices, not addresses.
- `{chain}_contract_to_number_mapping.json`: Provides a mapping from each contract's address to its numerical index used in the global graph files.

### Transactions
The `transactions` folder includes zipped files containing detailed transaction records for all labeled contracts within the three chains mentioned. Each chain's transactions are compiled into a single compressed file to facilitate easier handling and analysis:
- `ethereum_transactions.zip`
- `polygon_transactions.zip`
- `bnb_transactions.zip`

### Labels
The `labels.csv` file includes the categorization of each contract on the different chains. Columns in this file are:
- `Chain`: The blockchain platform (E.g., Ethereum, Polygon, BNB).
- `Contract`: The contract address or identifier.
- `Category`: An index representing the category of the contract, sorted by the number of contracts per category (Category 0 has the most contracts).

## Accessing the Data
The dataset can be accessed via the links provided below. Each link corresponds to a specific part of the dataset as organized in this repository: https://drive.google.com/drive/folders/1VV5ht9Eh8WGtKfkS0ipIk0FNI7g-WJfJ?usp=share_link.

## Using the Dataset
To use this dataset effectively:
1. Download the relevant files from the links provided above.
2. Decompress the transaction files for each chain to access the transaction data.
3. Use the provided JSON mapping files to interpret contract indices in the global graphs.
4. Consult `labels.csv` for the categorization of each contract to facilitate analysis across different categories.
