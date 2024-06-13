import random
from gensim.models import Word2Vec

class DeepWalk:
    def __init__(self, graph, walk_length, num_walks, embedding_dim):
        self.graph = graph
        self.walk_length = walk_length
        self.num_walks = num_walks
        self.embedding_dim = embedding_dim

    def random_walk(self, start_node):
        walk = [start_node]
        while len(walk) < self.walk_length:
            cur = walk[-1]
            neighbors = list(self.graph.neighbors(cur))
            if neighbors:
                walk.append(random.choice(neighbors))
            else:
                break
        return walk

    def generate_walks(self):
        walks = []
        nodes = list(self.graph.nodes())
        for _ in range(self.num_walks):
            random.shuffle(nodes)
            for node in nodes:
                walks.append(self.random_walk(node))
        return walks

    def train(self, walks):
        walks = [list(map(str, walk)) for walk in walks]  
        model = Word2Vec(sentences=walks, vector_size=self.embedding_dim, window=5, min_count=0, sg=1, workers=4)
        return model

    def get_embeddings(self, model):
        embeddings = {}
        for node in self.graph.nodes():
            embeddings[node] = model.wv[str(node)]
        return embeddings
