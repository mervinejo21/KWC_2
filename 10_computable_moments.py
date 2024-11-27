import time
from typing import List, Tuple, Set
 
def parse_input(file_path: str) -> Tuple[int, List[Tuple[str, Set[str]]]]:
    """
    Parses the input file and converts tags to sets for efficient operations.
    """
    with open(file_path, "r") as file:
        lines = file.readlines()
 
    num_paintings = int(lines[0].strip())
    paintings = []
    for i, line in enumerate(lines[1:]):
        parts = line.strip().split(maxsplit=2)
        painting_type = parts[0]
        tags = set(parts[2].split()) if len(parts) > 2 else set()
        paintings.append((painting_type, tags))
    return num_paintings, paintings
 
def create_frameglasses(paintings: List[Tuple[str, Set[str]]]) -> List[Tuple[List[int], Set[str]]]:
    """
    Creates frameglasses and precomputes their tags with efficient pairing.
    """
    landscapes = []
    portraits = []
 
    for i, (ptype, tags) in enumerate(paintings):
        if ptype == "L":
            landscapes.append(([i], tags))
        elif ptype == "P":
            portraits.append((i, tags))
 
    if not portraits:
        return landscapes
 
    # Efficient pairing of portraits
    portraits.sort(key=lambda x: len(x[1]), reverse=True)  # Sort by number of tags
    paired_portraits = []
    while len(portraits) > 1:
        p1 = portraits.pop(0)
        best_match_idx = max(range(len(portraits)), key=lambda j: len(p1[1] | portraits[j][1]))
        p2 = portraits.pop(best_match_idx)
        paired_portraits.append(([p1[0], p2[0]], p1[1] | p2[1]))
 
    # Add any remaining portrait
    if portraits:
        paired_portraits.append(([portraits[0][0]], portraits[0][1]))
 
    return landscapes + paired_portraits
 
def calculate_local_satisfaction(tags1: Set[str], tags2: Set[str]) -> int:
    """
    Calculates the local satisfaction score for two frameglasses.
    """
    common = len(tags1 & tags2)
    only_in_tags1 = len(tags1 - tags2)
    only_in_tags2 = len(tags2 - tags1)
    return min(common, only_in_tags1, only_in_tags2)
 
def optimize_sequence(frameglasses: List[Tuple[List[int], Set[str]]]) -> List[Tuple[List[int], Set[str]]]:
    """
    Optimizes the order of frameglasses using a greedy algorithm.
    """
    sequence = [frameglasses.pop(0)]
    while frameglasses:
        current_tags = sequence[-1][1]
        best_next = max(frameglasses, key=lambda fg: calculate_local_satisfaction(current_tags, fg[1]))
        sequence.append(best_next)
        frameglasses.remove(best_next)
    return sequence
 
def calculate_global_score(sequence: List[Tuple[List[int], Set[str]]]) -> int:
    """
    Calculates the global robotic satisfaction score for a sequence of frameglasses.
    """
    return sum(
        calculate_local_satisfaction(sequence[i][1], sequence[i + 1][1])
        for i in range(len(sequence) - 1)
    )
 
def process_data(input_file: str, output_file: str) -> None:
    """
    Processes the dataset and outputs the results.
    """
    start_time = time.time()
 
    # Step 1: Parse input
    num_paintings, paintings = parse_input(input_file)
 
    # Step 2: Create frameglasses
    frameglasses = create_frameglasses(paintings)
 
    # Step 3: Optimize the sequence of frameglasses
    optimized_sequence = optimize_sequence(frameglasses)
 
    # Step 4: Calculate score
    score = calculate_global_score(optimized_sequence)
    print(f"Global Satisfaction Score: {score}")
 
    # Step 5: Write output
    with open(output_file, "w") as file:
        file.write(f"{len(optimized_sequence)}\n")
        for frame, _ in optimized_sequence:
            file.write(" ".join(map(str, frame)) + "\n")
 
    end_time = time.time()
    print(f"Execution Time: {end_time - start_time:.6f} seconds")
 
if __name__ == "__main__":
    input_path = r"D:\KWC_2\input\10_computable_moments.txt"  # Replace with actual input file
    output_path = r"D:\KWC_2\output\optimized_computable_moments.txt"  # Replace with desired output file
    process_data(input_path, output_path)
                                                                   