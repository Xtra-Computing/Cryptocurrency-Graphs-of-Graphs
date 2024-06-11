# Multi-Chain Graphs of Graphs Dataset

This is the repository for "Multi-Chain Graphs of Graphs: A New Paradigm in Blockchain Dataset". This comprehensive study introduces a pioneering, large-scale, cross-chain dataset using a graphs-of-graphs approach to analyze complex blockchain networks. 

## Table of Contents
- [Repository Overview](#repository-overview)
- [Dataset Schema](#dataset-schema)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Requirements](#requirements)
  - [Dataset Overview](#dataset-overview)
  - [Dataset Access and Usage](#dataset-access-and-usage)
- [Analyses and Experiments](#using-the-dataset)
  - [Data Preparation](#data-prepare)
  - [Data Analysis](#data-analysis)
  - [Fraud Detection](#fraud-detection)
  - [Multi-Class Classification](#multi-class-classification)
- [License](#license)

## Repository Overview
This repository contains both the datasets used in our research and the code for analysis and model training. Here you can find everything needed to replicate our studies or use our data and models for your own research.

## Dataset Schema
Below are key statistics for each blockchain included in our dataset:

| Chain     | # Tokens | Start Months | End Months | # Transactions | # Addresses | # Categories |
|-----------|----------|--------------|------------|----------------|-------------|--------------|
| Ethereum  | 14,464   | 2016-02      | 2024-02    | 81,788,211     | 10,247,767  | 290          |
| Polygon   | 2,353    | 2020-08      | 2024-02    | 64,882,233     | 1,801,976   | 112          |
| BNB       | 7,499    | 2020-09      | 2024-02    | 121,612,480    | 6,550,399   | 149          |

## Getting Started
### Installation
Clone this repository to your local machine using:
```bash
git clone https://github.com/YourUsername/Graph-of-graphs-dataset.git
cd Graph-of-graphs-dataset
```

### Requirements
Ensure your environment meets the following specifications to run the scripts and models:
- Python 3.10.14
- Libraries: NumPy 1.26.2, pandas 1.3.5, PyTorch 2.3.0+cu118, networkx 3.3

Install required packages using:
```bash
pip install numpy==1.26.2 pandas==1.3.5 torch==2.3.0+cu118 networkx==3.3
```

### Dataset Overview
#### Global Graphs
- Contains data for Ethereum, Polygon, and BNB within the `global graph` folder:
  - `{chain}_graph_more_than_1_ratio.csv`: Contains edges where the weight—indicative of transactional or interaction metrics—exceeds 1\%. This is the same as the setting of our experiments in the paper. In this file, contracts are denoted by numerical indices rather than traditional addresses.
  - `{chain}_contract_to_number_mapping.json`:  Maps each contract's address to a numerical index utilized in the global graph files, facilitating cross-reference and analysis.

- Example code to build the global graphs for exploration:
```bash 
import networkx as nx
import pandas as pd

df = pd.read_csv(f'{chain}_graph_more_than_1_ratio.csv')
G = nx.Graph()  
for idx, row in df.iterrows():
    G.add_edge(row['Contract1'], row['Contract2'], weight=row['weight'])
```

#### Transactions
The `transactions` folder houses zipped archives with detailed transaction records for all labeled contracts within the aforementioned chains:
- `ethereum.zip`
- `polygon.zip`
- `bnb.zip`
Each zip file includes comprehensive transaction data such as block number, sender (from), receiver (to), transaction hash, value, and timestamp.

- Example code to build the local graphs for exploration:
```bash 
import networkx as nx
import pandas as pd

df = pd.read_csv(f'{contract_address}.csv')
G = nx.Graph()  
for idx, row in df.iterrows():
    G.add_edge(row['from'], row['to'], weight=row['value'])
```

#### Labels
The `labels.csv` file categorizes each contract across different chains. It includes the following columns:
- `Chain`: Specifies the blockchain platform (e.g., Ethereum, Polygon, BNB).
- `Contract`: Lists the contract address or identifier.
- `Category`: Represents the category of the contract, indexed by the prevalence of contracts within that category (Category 0 contains the most contracts).

### Dataset Access and Usage
The dataset is available via [Token Data](https://drive.google.com/drive/folders/1VV5ht9Eh8WGtKfkS0ipIk0FNI7g-WJfJ?usp=share_link). 

To effectively use this dataset, follow these steps:
1. Download the necessary files using the link provided above.
2. Decompress each chain's transaction archive to access individual transaction details.
3. Employ the JSON mapping files to decode contract indices within the global graphs.
4. Refer to `labels.csv` to understand the categorization of each contract, which is crucial for targeted analysis and comparative studies across different categories.

## Analyses and Experiments

### Data Preparation
Scripts for preparing data are under `dataset/`. 
- `individual`: Script for preparing data for individual graph learning models.
- `gog`: Script for preparing data for GoG-based learning models.

### Data Analysis
Scripts for analyzing both local and global graphs are located under `analysis/`. 
- `analyze_local_graphs.py`: Script for performing detailed analysis on local graphs.
- `analyze_global_graphs.py`: Script for analyzing global graph structures and metrics.
- `combine_analysis.py`: Combines results from local and global graph analyses.
- `local_metric/`: Contains scripts and utilities specifically for calculating various graph metrics on local graphs.

Run the following commands for respective analyses:
```bash
python analyze_local_graphs.py
python analyze_global_graphs.py
```

### Fraud Detection
Navigate to `fraud_detection/` to access scripts for anomaly detection applied to individual graphs and graphs-of-graphs:
- `graph_individual/`: Contains code for detecting anomalies in individual graph structures. These scripts use various graph-based anomaly detection techniques tailored for individual graphs.
- `graph_of_graphs/`: Includes code for anomaly detection employing techniques that consider graphs-of-graphs model.

```bash
cd graph_individual/
python main.py

cd ../graph_of_graphs/
python main.py
```

### Multi-Class Classification
Navigate to `multi-class_classification/` to access scripts for performing multi-class classification on both individual graphs and graphs-of-graphs:
- `graph_individual/`: This folder includes models and scripts for classifying individual graphs into multiple categories based on their structural and transactional features.
- `graph_of_graphs/`: Contains models and scripts for classifying graphs with graphs-of-graphs model.

```bash
cd graph_individual/
python main.py --chain polygon --model GCN

cd ../graph_of_graphs/
python main.py --chain polygon --model SEAL
```

## License
The dataset is released under the Creative Commons Attribution-NonCommercial-ShareAlike (CC BY-NC-SA) license. This means that anyone can use, distribute, and modify the data for non-commercial purposes as long as they give proper attribution and share the derivative works under the same license terms.
