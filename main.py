import json
import networkx as nx
import matplotlib.pyplot as plt

with open('data.json', 'r') as f:
    data = json.load(f)

G = nx.Graph()


for user in data:
    user_id = user['id']

    friends = user['friends']
    
    for friend_id in friends:
        G.add_edge(user_id, friend_id)

people = {
    184007908: 'Руденок Максим',
    420058114: 'Казьмин Даниил',
    198658352: 'Смелкин Никита'
}

betweenness = nx.betweenness_centrality(G)
betweenness_results = {user_id: betweenness.get(user_id, 0) for user_id in people}

print('\nЦентральность по посредничеству:')
for id, result in betweenness_results.items():
    print(f'\t{people[id]}: {result}')

closeness = nx.closeness_centrality(G)
closeness_results = {user_id: closeness.get(user_id, 0) for user_id in people}

print('\nЦентральность по близости:')
for id, result in closeness_results.items():
    print(f'\t{people[id]}: {result}')

eigenvector = nx.eigenvector_centrality(G)
eigenvector_results = {user_id: eigenvector.get(user_id, 0) for user_id in people}

print('\nЦентральность собственного вектора:')
for id, result in eigenvector_results.items():
    print(f'\t{people[id]}: {result}')

plt.figure(figsize=(8, 8))

pos = nx.spring_layout(G)

nx.draw(G, pos, node_color='skyblue', node_size=10, edge_color='gray')
nx.draw_networkx_nodes(G, pos, nodelist=people, node_color='red', node_size=50)
nx.draw_networkx_labels(G, pos, labels=people, font_size=8, font_color='black', font_weight='bold')

plt.show()
