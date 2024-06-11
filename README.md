# Graph-of-graphs Dataset

Welcome to the repository for "Multi-Chain Graphs of Graphs: A New Paradigm in Blockchain Dataset." This comprehensive study introduces a pioneering, large-scale, cross-chain dataset using a graphs-of-graphs approach to analyze complex blockchain networks.

## Table of Contents
- [Repository Overview](#repository-overview)
- [Dataset Schema](#dataset-schema)
- [Dataset Overview](#dataset-overview)
- [Code Structure](#code-structure)
- [Getting Started](#getting-started)
- [Using the Dataset](#using-the-dataset)
- [Using the Code](#using-the-code)
- [License](#license)
- [Contributing](#contributing)

## Repository Overview
- **`data/`**: Contains datasets used in our research with links to download and guidelines for access.
- **`code/`**: Houses all scripts used for data analyses and machine learning models.

## Dataset Schema
Here is a summary of key statistics for each blockchain included in our dataset:

| Chain     | # Token | Start Months | End Months | # Transactions | # Addresses | # Categories |
|-----------|---------|--------------|------------|----------------|-------------|--------------|
| Ethereum  | 14,464  | 2016-02      | 2024-02    | 81,788,211     | 10,247,767  | 290          |
| Polygon   | 2,353   | 2020-08      | 2024-02    | 64,882,233     | 1,801,976   | 112          |
| BNB       | 7,499   | 2020-09      | 2024-02    | 121,612,480    | 6,550,399   | 149          |

## Dataset Overview
### Global Graphs
- **Ethereum, Polygon, BNB**: Each contains two files:
  - `{chain}_graph_more_than_1_ratio.csv`: Edges with weights over 1\%, using numerical indices for contracts.
  - `{chain}_contract_to_number_mapping.json`: Mapping from contract addresses to numerical indices.

### Transactions
- Detailed transaction data in zipped files: `ethereum.zip`, `polygon.zip`, `bnb.zip`.

### Labels
- `labels.csv` provides categorization for each contract by chain, address, and category.

## Code Structure
### Analysis
- Scripts for both local and global graph analysis.
- `local_metric/`: Specific utilities for graph metrics calculation.

### Fraud Detection
- Anomaly detection in `graph_individual/` and `graph_of_graphs/`.

### Multi-Class Classification
- Classification models in `graph_individual/` and `graph_of_graphs/`.

## Getting Started
### Installation
Clone the repository and install required Python packages.
```bash
git clone https://github.com/YourUsername/Graph-of-graphs-dataset.git
cd Graph-of-graphs-dataset
pip install -r requirements.txt
