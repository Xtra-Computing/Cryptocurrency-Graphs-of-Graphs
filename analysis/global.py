import networkx as nx
import community as community_louvain
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict
import json
import seaborn as sns
import numpy as np
import random
from scipy.stats import pearsonr

import warnings
warnings.filterwarnings("ignore")


chain = 'polygon'

# read in labels file
chain_labels = pd.read_csv(f'../data/labels.csv').query('Chain == @chain')
chain_class = dict(zip(chain_labels.Contract, chain_labels.Category))

# read in file include the calculated common node statistics
global_link = pd.read_csv(f'../graphs/{chain}/{chain}_common_nodes_except_null_labels.csv') 
# read in file include the calculated metadata: number of unique address and number of transactions of each token
chain_metadata = pd.read_csv(f'../graphs/{chain}/{chain}_metadata.csv') 

global_link['Class1'] = global_link['Contract1'].map(chain_class)
global_link['Class2'] = global_link['Contract2'].map(chain_class)

global_link['Same_Class'] = global_link['Class1'] == global_link['Class2']
global_link['Jaccard_Coefficient'] = global_link['Common_Nodes']/global_link['Unique_Addresses']
filtered_link = global_link[global_link['Jaccard_Coefficient'] > 0]
global_link = global_link.query('Contract1 in @chain_class and Contract2 in @chain_class')


global_link['Contract1_short'] = global_link['Contract1'].apply(lambda x: x[0:6]+'...'+x[-6:])
global_link['Contract2_short'] = global_link['Contract2'].apply(lambda x: x[0:6]+'...'+x[-6:])
global_link[['Contract1_short', 'Contract2_short', 'Class1', 'Class2',
             'Jaccard_Coefficient']].sort_values(by = 'Jaccard_Coefficient', ascending = False).head(5)


global_graph = nx.Graph()
edges = zip(filtered_link['Contract1'], 
            filtered_link['Contract2'], 
            filtered_link['Jaccard_Coefficient'])

global_graph.add_weighted_edges_from(edges, weight='weight')
print("Graph construction complete")


nodes = []
for i in global_graph:
    nodes.append(i)
node_set = set(nodes)


def approximate_average_shortest_path_length(G, num_landmarks=10):
    nodes = list(G.nodes())
    landmarks = random.sample(nodes, k=num_landmarks)
    total_path_length = 0
    total_paths = 0

    for landmark in landmarks:
        path_lengths = nx.single_source_shortest_path_length(G, landmark)
        total_path_length += sum(path_lengths.values())
        total_paths += len(path_lengths) - 1  # Exclude the path to itself

    return total_path_length / total_paths if total_paths > 0 else None

def calculate_effective_diameter(G, percentile=90):
    path_lengths = []
    nodes = list(G.nodes())

    for node in nodes:
        lengths = nx.single_source_shortest_path_length(G, node)
        path_lengths.extend(lengths.values())

    if path_lengths:
        return np.percentile(path_lengths, percentile)
    else:
        return None


num_nodes = global_graph.number_of_nodes()
print("Number of Nodes:", num_nodes)

num_edges = global_graph.number_of_edges()
print("Number of Edges:", num_edges)

density = nx.density(global_graph)
print("Density:", density)

average_degree = sum(dict(global_graph.degree()).values()) / num_nodes if num_nodes > 0 else 0
print("Average Degree:", average_degree)

if num_nodes > 1:
    assortativity = nx.degree_assortativity_coefficient(global_graph)
    print("Assortativity:", assortativity)
else:
    print("Assortativity: Not applicable")

reciprocity = nx.overall_reciprocity(global_graph) if num_nodes > 0 else 0
print("Reciprocity:", reciprocity)

average_shortest_path_length = approximate_average_shortest_path_length(global_graph)
print("Average Shortest Path Length:", average_shortest_path_length)

effective_diameter = calculate_effective_diameter(global_graph)
print("Effective Diameter:", effective_diameter)

if num_nodes > 0:
    clustering_coefficient = nx.average_clustering(global_graph.to_undirected())
    print("Clustering Coefficient:", clustering_coefficient)
else:
    print("Clustering Coefficient: Not applicable")



unweighted_degree_centrality = {node: len(global_graph.edges(node)) for node in global_graph.nodes()}
top_5_unweighted_degree = sorted(unweighted_degree_centrality.items(), key=lambda item: item[1], reverse=True)[:5]

weighted_degree_centrality = {node: sum(data['weight'] for _, _, data in global_graph.edges(node, data=True)) for node in global_graph.nodes()}
top_5_weighted_degree = sorted(weighted_degree_centrality.items(), key=lambda item: item[1], reverse=True)[:5]

top_5_unweighted_degree_address = [i[0] for i in top_5_unweighted_degree]
top_5_weighted_degree_address = [i[0] for i in top_5_weighted_degree]


chain_metadata_select = chain_metadata.query('contract_address in @chain_class')
chain_metadata_select['class'] = chain_metadata_select['contract_address'].apply(lambda x: chain_class[x] if x in chain_class else 'Others')

chain_graphs_edges = dict(zip(chain_metadata_select.contract_address, chain_metadata_select.number_of_transactions))

y_values = [chain_graphs_edges[node] for node in global_graph.nodes()]
x_values = [unweighted_degree_centrality[node] for node in global_graph.nodes()]

# Calculate Pearson correlation coefficient and p-value
correlation, p_value = pearsonr(x_values, y_values)

# Plotting the scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(x_values, y_values, color='blue')
plt.yscale('log')
plt.xlabel('Node Degree Centrality (Global)')
plt.ylabel('Number of Transactions (Local)')
plt.annotate(f'Pearson r: {correlation:.2f}, p-value: {p_value:.3f}', xy=(0.05, 0.95), xycoords='axes fraction', verticalalignment='top')
plt.show()

print("Pearson correlation coefficient:", correlation)
print("P-value:", p_value)

# Plot edge weight distribution
edge_weights = [data['weight'] for _, _, data in global_graph.edges(data=True)]
print(max(edge_weights))

edge_weights_sorted = np.sort(edge_weights)
cdf = np.arange(1, len(edge_weights_sorted) + 1) / len(edge_weights_sorted)

edge_weight_75 = np.percentile(edge_weights_sorted, 75)
edge_weight_90 = np.percentile(edge_weights_sorted, 90)

plt.figure(figsize=(5, 3))
plt.plot(edge_weights_sorted, cdf, label='CDF of Edge Weights')
plt.xlabel('Edge Weight')
plt.ylabel('CDF (Percentage)')

plt.axhline(y=0.75, color='red', linestyle='--', label='75% Threshold')
plt.axhline(y=0.90, color='green', linestyle='--', label='90% Threshold')

plt.scatter(edge_weight_75, 0.75, color='red', marker='o')
plt.scatter(edge_weight_90, 0.90, color='green', marker='o')

# Annotating the edge weights
plt.annotate(f'weight = {edge_weight_75:.3f}', xy=(0.4, 0.7), xytext=(10, -10),
             textcoords='offset points', ha='right', va='bottom', color='red')
plt.annotate(f'weight = {edge_weight_90:.3f}', xy=(0.4, 0.85), xytext=(10, 10),
             textcoords='offset points', ha='right', va='bottom', color='green')

plt.legend()
plt.show()