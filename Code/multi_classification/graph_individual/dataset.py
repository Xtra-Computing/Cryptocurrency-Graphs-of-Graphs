import argparse
import networkx as nx
import pandas as pd
from tqdm import tqdm
import torch
from torch_geometric.data import InMemoryDataset
import os
from torch_geometric.data import Data


import warnings
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='Cora')
parser.add_argument('--hidden_channels', type=int, default=16)
parser.add_argument('--lr', type=float, default=0.001)
parser.add_argument('--epochs', type=int, default=200)
parser.add_argument('--use_gdc', action='store_true', help='Use GDC')
parser.add_argument('--wandb', action='store_true', help='Track experiment')
args, unknown = parser.parse_known_args()

class TransactionDataset(InMemoryDataset):
    def __init__(self, root, transaction_dfs, labels, contract_addresses, chain, transform=None, pre_transform=None):
        self.transaction_dfs = transaction_dfs
        self.labels = labels
        self.contract_addresses = contract_addresses
        self.chain = chain 
        super(TransactionDataset, self).__init__(root, transform, pre_transform)

    @property
    def processed_file_names(self):
        return 'data.pt'

    def process(self):
        data_list = [self.graph_to_data_object(self.create_graph(df), label, contract) 
                     for df, label, contract in zip(self.transaction_dfs, self.labels, self.contract_addresses)]
        data, slices = self.collate(data_list)
        torch.save((data, slices), self.processed_paths[0])

    def create_graph(self, transaction_df):
        # Normalize transaction values
        transaction_df['value'] = pd.to_numeric(transaction_df['value'].replace(',', ''), errors='coerce')
        min_value = transaction_df['value'].min()
        max_value = transaction_df['value'].max()
        transaction_df['scaled_value'] = ((transaction_df['value'] - min_value) / (max_value - min_value)) * 100

        graph = nx.DiGraph()
        unique_addresses = list(set(transaction_df['from']) | set(transaction_df['to']))
        address_to_node = {address: i for i, address in enumerate(unique_addresses)}
        for _, row in transaction_df.iterrows():
            from_node, to_node = address_to_node[row['from']], address_to_node[row['to']]
            scaled_value = row['scaled_value']
            timestamp = row['timestamp']
            graph.add_edge(from_node, to_node, weight=scaled_value, timestamp=timestamp)
        
        return graph

    def graph_to_data_object(self, graph, label, contract_address):
        if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
            print("Empty graph detected, skipping.")
            return None  # Return None if graph is empty.

        adj = nx.to_scipy_sparse_array(graph, nodelist=sorted(graph.nodes()), format='coo')
        edge_index = torch.tensor([adj.row, adj.col], dtype=torch.long)
        edge_attr = torch.tensor([[graph.edges[u, v]['weight'], graph.edges[u, v]['timestamp']] 
                                  for u, v in zip(adj.row, adj.col)], dtype=torch.float)

        num_nodes = graph.number_of_nodes()
        total_degree = [graph.degree(i) for i in range(num_nodes)]
        in_degree = [graph.in_degree(i) for i in range(num_nodes)]
        out_degree = [graph.out_degree(i) for i in range(num_nodes)]

        in_value = [sum(data['weight'] for _, _, data in graph.in_edges(i, data=True)) for i in range(num_nodes)]
        out_value = [sum(data['weight'] for _, _, data in graph.out_edges(i, data=True)) for i in range(num_nodes)]

        x = torch.tensor([[td, ind, outd, inv, outv] for td, ind, outd, inv, outv in zip(total_degree, in_degree, out_degree, in_value, out_value)], dtype=torch.float)

        timestamps = [data['timestamp'] for _, _, data in graph.edges(data=True)]
        if timestamps:
            min_timestamp, max_timestamp = min(timestamps), max(timestamps)
            average_timestamp = sum(timestamps) / len(timestamps)
        else:
            min_timestamp = max_timestamp = average_timestamp = 0  

        chain_index = chain_indexes.get(self.chain, None)
        contract_index = all_address_index.get(contract_address, None)

        graph_attr = torch.tensor([min_timestamp, max_timestamp, average_timestamp, 
                                   chain_index, contract_index], dtype=torch.float)

        y = torch.tensor([label], dtype=torch.long)

        data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr, y=y, 
                    num_nodes=num_nodes, graph_attr=graph_attr)
        return data

if __name__ == "__main__":
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    chain = 'Polygon'
    labels = pd.read_csv('../data/labels.csv').query('Chain == @chain')

    transaction_dfs = []

    for i in tqdm(labels.Address.values):
        tx = pd.read_csv(f'../data/transactions/{chain}/{i}.csv')
        tx['date'] = pd.to_datetime(tx['timestamp'], unit='s')
        transaction_dfs.append(tx)

    chain_indexes = {'Ethereum': 1, 'Polygon': 2, 'BNB': 3}
    all_address_index = dict(zip(labels.Contract, labels.index))

    dataset = TransactionDataset(root=f'../GCN/{chain}', 
                                transaction_dfs=transaction_dfs, 
                                labels=list(labels.Category.values),
                                contract_addresses=list(labels.Contract.values),
                                chain=chain)