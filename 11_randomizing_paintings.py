import pandas as pd
import time
from typing import List, Dict, Set, Tuple
from collections import Counter, defaultdict
import heapq


def read_input(file_path: str) -> Tuple[int, pd.DataFrame]:
    """
    Reads and parses the input file into a pandas DataFrame.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    num_paintings = int(lines[0].strip())
    data = [line.strip().split(maxsplit=2) for line in lines[1:]]
    df = pd.DataFrame(data, columns=["Type", "Tag_Count", "Tags"])
    df["Tag_Count"] = df["Tag_Count"].astype(int)
    df["Tags"] = df["Tags"].apply(lambda x: set(x.split()))
    return num_paintings, df


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


def pair_portraits(paintings: Dict[int, Set[str]]) -> List[List[int]]:
    """
    Pairs portraits for maximum diversity.
    """
    paired = []
    used = set()
    items = list(paintings.items())

    for i, (idx1, tags1) in enumerate(items):
        if idx1 in used:
            continue
        best_pair = None
        best_score = -1
        for j, (idx2, tags2) in enumerate(items):
            if idx2 in used or idx1 == idx2:
                continue
            common = len(tags1 & tags2)
            diversity = len(tags1 | tags2)
            score = diversity - common
            if score > best_score:
                best_score = score
                best_pair = idx2
        if best_pair is not None:
            paired.append([idx1, best_pair])
            used.add(idx1)
            used.add(best_pair)
        else:
            paired.append([idx1])
    return paired


def arrange_landscapes_by_rare_tags(paintings: Dict[int, Set[str]]) -> List[List[int]]:
    """
    Arranges landscapes by prioritizing rare tags.
    """
    tag_frequencies = Counter(tag for tags in paintings.values() for tag in tags)
    rare_tags = sorted(tag_frequencies.keys(), key=lambda tag: tag_frequencies[tag])

    tag_to_paintings = defaultdict(list)
    for idx, tags in paintings.items():
        for tag in tags:
            tag_to_paintings[tag].append(idx)

    arranged_paintings = []
    used_paintings = set()

    for tag in rare_tags:
        if tag not in tag_to_paintings:
            continue
        for painting_idx in tag_to_paintings[tag]:
            if painting_idx not in used_paintings:
                arranged_paintings.append([painting_idx])
                used_paintings.add(painting_idx)

    return arranged_paintings


def batch_processing(frames: List[List[int]], tags_cache: Dict[int, Set[str]], batch_size: int = 100) -> List[List[int]]:
    """
    Processes frames in batches to reduce computation time.
    """
    batches = [frames[i:i + batch_size] for i in range(0, len(frames), batch_size)]
    ordered_batches = []

    for batch in batches:
        ordered_batches.append(fast_greedy(batch, tags_cache))

    final_sequence = []
    while ordered_batches:
        current_batch = ordered_batches.pop(0)
        if not final_sequence:
            final_sequence.extend(current_batch)
        else:
            final_sequence.extend(fast_greedy(current_batch, tags_cache))
    return final_sequence


def fast_greedy(frames: List[List[int]], tags_cache: Dict[int, Set[str]]) -> List[List[int]]:
    """
    Faster greedy ordering of frames using a priority queue.
    """
    ordered = [frames.pop(0)]
    heap = []

    current_tags = set.union(*[tags_cache[idx] for idx in ordered[-1]])
    for frame in frames:
        candidate_tags = set.union(*[tags_cache[idx] for idx in frame])
        common = len(current_tags & candidate_tags)
        unique_current = len(current_tags - candidate_tags)
        unique_candidate = len(candidate_tags - current_tags)
        score = -min(common, unique_current, unique_candidate)
        heapq.heappush(heap, (score, frame))

    while heap:
        _, best_frame = heapq.heappop(heap)
        ordered.append(best_frame)
        frames.remove(best_frame)

        current_tags = set.union(*[tags_cache[idx] for idx in ordered[-1]])
        heap = []
        for frame in frames:
            candidate_tags = set.union(*[tags_cache[idx] for idx in frame])
            common = len(current_tags & candidate_tags)
            unique_current = len(current_tags - candidate_tags)
            unique_candidate = len(candidate_tags - current_tags)
            score = -min(common, unique_current, unique_candidate)
            heapq.heappush(heap, (score, frame))

    return ordered


def process_file_with_optimizations(file_path: str, output_path: str) -> None:
    """
    Processes the input file and generates an optimized sequence of frames.
    """
    start_time = time.time()

    # Step 1: Read input
    num_paintings, df = read_input(file_path)

    # Step 2: Precompute tags cache
    tags_cache = {idx: row["Tags"] for idx, row in df.iterrows()}

    # Step 3: Separate portraits and landscapes
    portraits = df[df["Type"] == "P"].index.tolist()
    landscapes = df[df["Type"] == "L"].index.tolist()

    # Step 4: Process portraits and landscapes
    portrait_frames = pair_portraits({idx: tags_cache[idx] for idx in portraits})
    landscape_frames = arrange_landscapes_by_rare_tags({idx: tags_cache[idx] for idx in landscapes})

    # Step 5: Combine frames and apply batch processing
    all_frames = portrait_frames + landscape_frames
    ordered_frames = batch_processing(all_frames, tags_cache, batch_size=100)

    # Step 6: Calculate final score
    score = calculate_score(ordered_frames, tags_cache)

    # Step 7: Write output
    with open(output_path, 'w') as file:
        file.write(f"{len(ordered_frames)}\n")
        for frame in ordered_frames:
            file.write(" ".join(map(str, frame)) + "\n")

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Processed {file_path}:")
    print(f"Score = {score}")
    print(f"Execution Time = {execution_time:.2f} seconds")


# File paths
input_file = r"D:\KWC_2\input\11_randomizing_paintings.txt"
output_file = r"D:\KWC_2\output\optimized_randomizing_paintings.txt"

# Process the file
process_file_with_optimizations(input_file, output_file)
