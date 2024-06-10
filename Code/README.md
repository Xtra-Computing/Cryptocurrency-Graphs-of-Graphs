# Code for Graph Analysis and Graph Neural Network Models

This directory contains all the code used in our research for analyzing blockchain transactions, detecting anomalies, and performing multi-class classification using both individual graphs and graphs-of-graphs frameworks.

## Directory Structure

### Analysis
This folder contains scripts for analyzing both local and global graphs within the blockchain datasets:
- `analyze_local_graphs.py`: Script for performing detailed analysis on local graphs.
- `analyze_global_graphs.py`: Script for analyzing global graph structures and metrics.
- `combine_analysis.py`: Combines results from local and global graph analyses.
- `local_metric/`: Contains scripts and utilities specifically for calculating various graph metrics on local graphs.

### Fraud Detection
Includes subdirectories for anomaly detection methodologies applied to individual graphs and graphs-of-graphs:
- `graph_individual/`: Contains code for detecting anomalies in individual graph structures. These scripts use various graph-based anomaly detection techniques tailored for single graphs.
- `graph_of_graphs/`: Includes code for anomaly detection across a system of interconnected graphs, employing techniques that consider the relationships and interactions between multiple graphs.

### Multi-Class Classification
Contains scripts and models for performing multi-class classification on both individual graphs and graphs-of-graphs:
- `graph_individual/`: This folder includes models and scripts for classifying individual graphs into multiple categories based on their structural and transactional features.
- `graph_of_graphs/`: Contains models and scripts for classifying systems of graphs, leveraging the interdependencies and collective properties of multiple graphs to enhance classification performance.

## Requirements
To run the scripts, you need Python 3.10.14 and the following packages:
- NumPy version 1.26.2
- pandas version 1.3.5
- PyTorch version 2.3.0+cu118
- networkx version 3.3

You can install any missing packages using pip:
```bash
pip install numpy==1.26.2 pandas==1.3.5 torch==2.3.0+cu118 networkx==3.3
