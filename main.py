import os
import time
from typing import List, Tuple
 
 
def read_file(file_path: str) -> Tuple[int, List[List[str]]]:
    with open(file_path, 'r') as file:
        lines = file.readlines()
 
    num_paintings = int(lines[0].strip())
    paintings = [line.strip().split(maxsplit=2) for line in lines[1:]]
    for p in paintings:
        if len(p) < 3:
            p.append("")
    return num_paintings, paintings
 
 
def precompute_tags(paintings: List[List[str]]) -> List[set]:
    return [set(p[2].split()) for p in paintings]
 
 
def calculate_tags(indices: List[int], precomputed_tags: List[set]) -> set:
    tags = set()
    for idx in indices:
        tags.update(precomputed_tags[idx - 1])
    return tags
 
 
def pair_portraits_optimized(portraits: List[int], precomputed_tags: List[set]) -> List[List[int]]:
    if len(portraits) < 2:
        return [[p] for p in portraits]
 
    pairs = []
    used = set()
 
    while len(used) < len(portraits):
        best_pair = None
        best_score = -1
 
        for i in range(len(portraits)):
            if portraits[i] in used:
                continue
            for j in range(i + 1, len(portraits)):
                if portraits[j] in used:
                    continue
 
                score = len(precomputed_tags[portraits[i] - 1] | precomputed_tags[portraits[j] - 1]) - len(
                    precomputed_tags[portraits[i] - 1] & precomputed_tags[portraits[j] - 1]
                )
                if score > best_score:
                    best_score = score
                    best_pair = (portraits[i], portraits[j])
 
        if best_pair:
            p1, p2 = best_pair
            pairs.append([p1, p2])
            used.add(p1)
            used.add(p2)
        else:
            break
 
    # Add unpaired portraits
    for p in portraits:
        if p not in used:
            pairs.append([p])
 
    return pairs
 
 
def build_sequence(frameglasses: List[List[int]], precomputed_tags: List[set]) -> List[List[int]]:
    sequence = []
    sequence.append(frameglasses.pop(0))  # Start with the first group
 
    while frameglasses:
        best_next = None
        best_score = -1
        current_tags = calculate_tags(sequence[-1], precomputed_tags)
 
        for i, group in enumerate(frameglasses):
            next_tags = calculate_tags(group, precomputed_tags)
            common = len(current_tags & next_tags)
            only_in_current = len(current_tags - next_tags)
            only_in_next = len(next_tags - current_tags)
            score = min(common, only_in_current, only_in_next)
 
            if score > best_score:
                best_score = score
                best_next = i
 
        sequence.append(frameglasses.pop(best_next))
 
    return sequence
 
 
def calculate_score(frameglasses: List[List[int]], precomputed_tags: List[set]) -> int:
    score = 0
    for i in range(len(frameglasses) - 1):
        tags1 = calculate_tags(frameglasses[i], precomputed_tags)
        tags2 = calculate_tags(frameglasses[i + 1], precomputed_tags)
        common = len(tags1 & tags2)
        only_in_tags1 = len(tags1 - tags2)
        only_in_tags2 = len(tags2 - tags1)
        score += min(common, only_in_tags1, only_in_tags2)
    return score
 
 
def generate_optimized_order(paintings: List[List[str]]) -> Tuple[List[List[int]], int]:
    precomputed_tags = precompute_tags(paintings)
 
    landscapes = [i + 1 for i, p in enumerate(paintings) if p[0] == "L"]
    portraits = [i + 1 for i, p in enumerate(paintings) if p[0] == "P"]
 
    frameglasses = [[l] for l in landscapes] + pair_portraits_optimized(portraits, precomputed_tags)
    optimized_sequence = build_sequence(frameglasses, precomputed_tags)
    global_score = calculate_score(optimized_sequence, precomputed_tags)
 
    return optimized_sequence, global_score
 
 
def write_output_file(folder_path: str, file_name: str, frameglasses: List[List[int]]) -> None:
    """
    Writes the frameglasses to an output file in the specified format.
    Adjusts indices to start from 0.
    """
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)
 
    with open(file_path, 'w') as file:
        file.write(f"{len(frameglasses)}\n")  # Write number of frameglasses
        for frameglass in frameglasses:
            file.write(" ".join(map(lambda x: str(x - 1), frameglass)) + "\n")  # Adjust index to start from 0
 
    print(f"Output written to: {file_path}")
 
 
 
def process_data(input_file: str, output_folder: str) -> None:
    num_paintings, paintings = read_file(input_file)
 
    start_time = time.time()
    frameglasses, global_score = generate_optimized_order(paintings)
    end_time = time.time()
 
    write_output_file(output_folder, "optimized_output.txt", frameglasses)
 
    print(f"\nExecution time: {end_time - start_time:.6f} seconds")
    print(f"Global Satisfaction Score: {global_score}")
 
 
# Execute the script
if __name__ == "__main__":
    input_file_path = r"D:\KWC_2\input\10_computable_moments.txt"
    output_folder = "output"
    process_data(input_file_path, output_folder)