import pandas as pd
import time
from typing import List, Dict, Set, Tuple


def read_input(file_path: str) -> Tuple[int, pd.DataFrame, Dict[str, List[int]]]:
    """
    Reads and parses the input file into a pandas DataFrame and creates a tag-to-painting map.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    num_paintings = int(lines[0].strip())
    data = [line.strip().split(maxsplit=2) for line in lines[1:]]
    df = pd.DataFrame(data, columns=["Type", "Tag_Count", "Tags"])
    df["Tag_Count"] = df["Tag_Count"].astype(int)
    df["Tags"] = df["Tags"].apply(lambda x: set(x.split()))

    # Create a tag-to-painting map
    tag_to_paintings = {}
    for idx, row in df.iterrows():
        for tag in row["Tags"]:
            if tag not in tag_to_paintings:
                tag_to_paintings[tag] = []
            tag_to_paintings[tag].append(idx)

    return num_paintings, df, tag_to_paintings


def construct_graph(tag_to_paintings: Dict[str, List[int]]) -> Dict[int, Set[int]]:
    """
    Constructs a graph where each painting is a node, and edges connect paintings sharing a common tag.
    """
    graph = {}
    for tag, paintings in tag_to_paintings.items():
        if len(paintings) == 2:
            p1, p2 = paintings
            if p1 not in graph:
                graph[p1] = set()
            if p2 not in graph:
                graph[p2] = set()
            graph[p1].add(p2)
            graph[p2].add(p1)
    return graph


def traverse_graph(graph: Dict[int, Set[int]], start: int, visited: Set[int]) -> List[int]:
    """
    Traverses the graph starting from a given node to form a sequence of paintings.
    """
    sequence = []
    stack = [start]

    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        sequence.append([current])
        for neighbor in graph[current]:
            if neighbor not in visited:
                stack.append(neighbor)

    return sequence


def process_landscapes_with_graph(file_path: str, output_path: str) -> None:
    """
    Processes the input file containing only landscapes using the optimized graph-based algorithm.
    """
    start_time = time.time()

    # Step 1: Read input and create tag-to-painting map
    num_paintings, df, tag_to_paintings = read_input(file_path)

    # Step 2: Construct the graph
    graph = construct_graph(tag_to_paintings)

    # Step 3: Traverse the graph to form sequences
    visited = set()
    sequences = []

    for painting in range(num_paintings):
        if painting not in visited:
            sequences.extend(traverse_graph(graph, painting, visited))

    # Step 4: Calculate score
    tags_cache = {idx: row["Tags"] for idx, row in df.iterrows()}
    score = calculate_score(sequences, tags_cache)

    # Step 5: Write output
    with open(output_path, 'w') as file:
        file.write(f"{len(sequences)}\n")
        for frame in sequences:
            file.write(" ".join(map(str, frame)) + "\n")

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Processed {file_path}:")
    print(f"Score = {score}")
    print(f"Execution Time = {execution_time:.2f} seconds")


# Utility Function to Calculate Score
def calculate_score(frames: List[List[int]], tags_cache: Dict[int, Set[str]]) -> int:
    """
    Calculates the global satisfaction score for a sequence of frames.
    """
    score = 0
    for i in range(len(frames) - 1):
        tags1 = set.union(*[tags_cache[idx] for idx in frames[i]])
        tags2 = set.union(*[tags_cache[idx] for idx in frames[i + 1]])
        common = len(tags1 & tags2)
        unique_tags1 = len(tags1 - tags2)
        unique_tags2 = len(tags2 - tags1)
        score += min(common, unique_tags1, unique_tags2)
    return score


# File paths
input_file = r"D:\KWC_2\input\1_binary_landscapes.txt"
output_file = r"D:\KWC_2\output\optimized_landscape_paintings_graph.txt"

# Process the file
process_landscapes_with_graph(input_file, output_file)
