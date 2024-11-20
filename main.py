import os
import time
from multiprocessing import Pool
from typing import List, Tuple, Dict


def parse_input(file_path: str) -> Tuple[int, List[Tuple[str, set]]]:
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


def create_frameglasses(paintings: List[Tuple[str, set]]) -> List[Tuple[List[int], set]]:
    """
    Creates frameglasses and precomputes their tags.
    Skips pairing logic if there are no portraits.
    """
    landscapes = []
    portraits = []

    for i, (ptype, tags) in enumerate(paintings):
        if ptype == "L":
            landscapes.append(([i], tags))
        elif ptype == "P":
            portraits.append((i, tags))

    # If there are no portraits, return only landscapes
    if not portraits:
        return landscapes

    # Pair portraits to form frameglasses
    paired_portraits = []
    used = set()
    for i in range(len(portraits)):
        if i in used:
            continue
        best_pair = None
        best_tags = set()
        for j in range(i + 1, len(portraits)):
            if j in used:
                continue
            combined_tags = portraits[i][1] | portraits[j][1]
            if len(combined_tags) > len(best_tags):
                best_tags = combined_tags
                best_pair = j
        if best_pair is not None:
            paired_portraits.append(([portraits[i][0], portraits[best_pair][0]], best_tags))
            used.add(i)
            used.add(best_pair)
        else:
            paired_portraits.append(([portraits[i][0]], portraits[i][1]))

    return landscapes + paired_portraits


def calculate_local_satisfaction(tags1: set, tags2: set) -> int:
    """
    Calculates the local satisfaction score for two frameglasses.
    """
    common = len(tags1 & tags2)
    only_in_tags1 = len(tags1 - tags2)
    only_in_tags2 = len(tags2 - tags1)
    return min(common, only_in_tags1, only_in_tags2)


def optimize_chunk(chunk: List[Tuple[List[int], set]]) -> List[Tuple[List[int], set]]:
    """
    Optimizes the order of frameglasses in a chunk using a greedy algorithm.
    """
    remaining = chunk[:]
    sequence = [remaining.pop(0)]  # Start with the first frameglass

    while remaining:
        best_next = None
        best_score = -1
        current_tags = sequence[-1][1]

        for i, (_, tags) in enumerate(remaining):
            score = calculate_local_satisfaction(current_tags, tags)
            if score > best_score:
                best_score = score
                best_next = i

        sequence.append(remaining.pop(best_next))

    return sequence


def merge_chunks(chunks: List[List[Tuple[List[int], set]]]) -> List[Tuple[List[int], set]]:
    """
    Merges optimized chunks into a single sequence.
    """
    sequence = []
    for chunk in chunks:
        sequence.extend(chunk)
    return sequence


def calculate_global_score(sequence: List[Tuple[List[int], set]]) -> int:
    """
    Calculates the global robotic satisfaction score for a sequence of frameglasses.
    """
    total_score = 0
    for i in range(len(sequence) - 1):
        tags1 = sequence[i][1]
        tags2 = sequence[i + 1][1]
        total_score += calculate_local_satisfaction(tags1, tags2)
    return total_score


def process_data(input_file: str, output_file: str, num_processes: int = 4, chunk_size: int = 2000) -> None:
    """
    Processes the dataset with multiprocessing and efficient strategies.
    Skips unnecessary computations if only one type of photo is present.
    """
    start_time = time.time()

    # Step 1: Parse input
    num_paintings, paintings = parse_input(input_file)

    # Step 2: Create frameglasses
    frameglasses = create_frameglasses(paintings)

    # Step 3: Check for empty frameglasses
    if not frameglasses:
        print("No valid frameglasses found. Exiting.")
        return

    # Step 4: Divide frameglasses into chunks
    chunks = [frameglasses[i:i + chunk_size] for i in range(0, len(frameglasses), chunk_size)]

    # Step 5: Optimize each chunk in parallel
    with Pool(num_processes) as pool:
        optimized_chunks = pool.map(optimize_chunk, chunks)

    # Step 6: Merge chunks
    optimized_sequence = merge_chunks(optimized_chunks)

    # Step 7: Calculate score
    score = calculate_global_score(optimized_sequence)
    print(f"Global Satisfaction Score: {score}")

    # Step 8: Write output
    with open(output_file, "w") as file:
        file.write(f"{len(optimized_sequence)}\n")
        for frame, _ in optimized_sequence:
            file.write(" ".join(map(str, frame)) + "\n")

    end_time = time.time()
    print(f"Execution Time: {end_time - start_time:.6f} seconds")


if __name__ == "__main__":
    input_path = r"D:\KWC_2\input\10_computable_moments.txt"  # Replace with the actual input file
    output_path = r"D:\KWC_2\output\optimized_output.txt"  # Replace with the desired output file
    process_data(input_path, output_path, num_processes=4, chunk_size=5000)
