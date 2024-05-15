import itertools
import random
import matplotlib.pyplot as plt
import math

## User configurable parameters

# N
nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

## Construct Layout

def construct_layout(seq):
    # P
    layout = []
    # L
    rankings = {}
    # Rankings of nodes in N
    node_rankings = {}

    for n in nodes:
        node_rankings[n] = 0

    for i in range(len(seq) - 1):
        pair = [seq[i], seq[i + 1]]
        pair.sort()
        node_rankings[pair[0]] += 1
        node_rankings[pair[1]] += 1

        edge = (pair[0], pair[1])
        if not edge in rankings:
            rankings[edge] = 0

        rankings[edge] += 1

    sorted_rankings = []
    for k in rankings.keys():
        sorted_rankings += [(k, rankings[k])]

    sorted_rankings.sort(reverse=True, key=lambda k: k[1])

    layout += [sorted_rankings[0][0][0]]
    layout += [sorted_rankings[0][0][1]]

    for k, r in sorted_rankings[1:]:
        highest_ranked = (k[0], k[0], len(sorted_rankings))

        for node in k:
            if node in layout:
                continue

            for v in layout:
                idx = 0
                key = sorted([node, v])
                key = (key[0], key[1])

                for edge in sorted_rankings:
                    if edge[0] == key:
                        break
                    else:
                        idx += 1

                if idx <= highest_ranked[2]:
                    highest_ranked = (node, v, idx)

        # If neither node on this edge is in the layout already nor connected to any
        # nodes that are, just append them both to the end
        if highest_ranked[2] == len(sorted_rankings) and not k[0] in layout and k[1] not in layout:
            head_rank = node_rankings[layout[0]]
            tail_rank = node_rankings[layout[1]]
            if node_rankings[k[0]] > node_rankings[k[1]]:
                if head_rank < tail_rank:
                    layout = [k[0], k[1]] + layout
                else:
                    layout += [k[1], k[0]]

            else:
                if head_rank < tail_rank:
                    layout = [k[1], k[0]] + layout
                else:
                    layout += [k[0], k[1]]

        elif not highest_ranked[0] in layout:
            not_highest = k[0]
            if highest_ranked[0] == k[0]:
                not_highest = k[1]

            connected_idx = layout.index(highest_ranked[1])
            if connected_idx < len(layout) // 2:
                if not not_highest in layout:
                    layout = [not_highest, highest_ranked[0]] + layout
                else:
                    layout = [highest_ranked[0]] + layout

            else:
                if not not_highest in layout:
                    layout += [highest_ranked[0], not_highest]
                else:
                    layout += [highest_ranked[0]]

    return layout


## Compute distance

def distance(seq, arr):
    cur_idx = arr.index(seq[0])
    dist_sum = 0

    for node in seq[1:]:
        idx = arr.index(node)
        dist_sum += abs(idx - cur_idx)
        cur_idx = idx

    return dist_sum

p = list(itertools.permutations(nodes))

ratios = []
for k in range(10000):
    sequence_length = random.randint(50, 150)
    sequence = [random.choice(nodes)]
    while len(sequence) < sequence_length:
        c = random.choice(nodes)
        while c == sequence[-1]:
            c = random.choice(nodes)

        sequence += [c]

    min_brute_force = (0, distance(sequence, p[0]))
    for i in range(len(p) - 1):
        l = p[i+1]
        d = distance(sequence, l)
        if d < min_brute_force[1]:
            min_brute_force = (i+1, d)

    algo_dist = distance(sequence, construct_layout(sequence))
    ratios += [algo_dist / min_brute_force[1]]

m, bins, patches = plt.hist(x=ratios, bins='auto', color='#0530aa', rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Ratio of Traversal Length on Algorithm P to True Optimal P')
plt.ylabel('Frequency')
plt.title('Algorithm Performance Assessment')
maxfreq = m.max()
plt.ylim(ymax=math.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
plt.savefig("performance.png")
