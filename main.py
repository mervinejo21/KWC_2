import os
import random
from typing import List, Tuple

# Function to read and parse the input file
def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Extract the number of frameglasses
    num_frameglasses = int(lines[0].strip())
    
    # Extract the details of the paintings
    paintings = [line.strip() for line in lines[1:]]
    
    return num_frameglasses, paintings

# Function to generate frameglasses
def generate_frameglasses(paintings):
    frameglasses = []
    used_indexes = set()
    portraits = []
    landscapes = []

    for i, painting in enumerate(paintings):
        if i in used_indexes:
            continue  # Skip already used indexes
        
        parts = painting.split()
        painting_type = parts[0]
        tags = parts[2:]
        
        if painting_type == "L":  # Landscape painting
            landscapes.append((i, tags))  # Store index and tags
            used_indexes.add(i)
        elif painting_type == "P":  # Portrait painting
            portraits.append((i, tags))  # Store index and tags
            used_indexes.add(i)
    
    # Add landscapes first
    for landscape in landscapes:
        frameglasses.append(landscape)
    
    # Pair up portraits
    for j in range(0, len(portraits) - 1, 2):
        pair = (portraits[j][0], portraits[j][1] + portraits[j + 1][1])  # Merge tags
        frameglasses.append(pair)
    
    return frameglasses

# Function to calculate local satisfaction
def calculate_local_satisfaction(tags_current: set, tags_next: set) -> int:
    common_tags = len(tags_current & tags_next)
    tags_in_current_not_in_next = len(tags_current - tags_next)
    tags_in_next_not_in_current = len(tags_next - tags_current)
    return min(common_tags, tags_in_current_not_in_next, tags_in_next_not_in_current)

# Function to calculate the global satisfaction
def calculate_global_satisfaction(frameglasses: List[Tuple[int, List[str]]]) -> int:
    total_score = 0
    
    for i in range(len(frameglasses) - 1):
        # Tags for the current and next frameglass
        tags_current = set(frameglasses[i][1])
        tags_next = set(frameglasses[i + 1][1])
        
        # Local satisfaction
        local_satisfaction = calculate_local_satisfaction(tags_current, tags_next)
        total_score += local_satisfaction
    
    return total_score

# Function to optimize the sequence of frameglasses
def optimize_frameglass_sequence(frameglasses: List[Tuple[int, List[str]]]) -> List[Tuple[int, List[str]]]:
    optimized_sequence = []
    remaining_frameglasses = frameglasses[:]
    
    # Start with any frameglass
    current_frameglass = remaining_frameglasses.pop(0)
    optimized_sequence.append(current_frameglass)
    
    while remaining_frameglasses:
        best_next_frameglass = None
        best_score = -1
        
        # Find the next frameglass that maximizes local satisfaction
        for next_frameglass in remaining_frameglasses:
            tags_current = set(current_frameglass[1])
            tags_next = set(next_frameglass[1])
            local_satisfaction = calculate_local_satisfaction(tags_current, tags_next)
            
            if local_satisfaction > best_score:
                best_score = local_satisfaction
                best_next_frameglass = next_frameglass
        
        # Add the best frameglass to the sequence
        optimized_sequence.append(best_next_frameglass)
        remaining_frameglasses.remove(best_next_frameglass)
        current_frameglass = best_next_frameglass
    
    return optimized_sequence

# Function to write the output file
def write_output_file(folder_path, file_name, frameglasses):
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)
    
    with open(file_path, 'w') as file:
        # Write the number of frameglasses
        file.write(f"{len(frameglasses)}\n")
        
        # Write the details of each frameglass
        for frameglass in frameglasses:
            file.write(f"{frameglass[0]}\n")
    
    print(f"Output written to: {file_path}")

# Main function to process the data
def process_data(input_file, output_folder):
    # Read and parse the file
    num_frameglasses, paintings = read_file(input_file)
    
    # Generate frameglasses
    frameglasses = generate_frameglasses(paintings)
    
    # Calculate initial score
    initial_score = calculate_global_satisfaction(frameglasses)
    print(f"Initial Global Satisfaction Score: {initial_score}")
    
    # Optimize the sequence
    optimized_frameglasses = optimize_frameglass_sequence(frameglasses)
    
    # Calculate optimized score
    optimized_score = calculate_global_satisfaction(optimized_frameglasses)
    print(f"Optimized Global Satisfaction Score: {optimized_score}")
    
    # Write the optimized output
    write_output_file(output_folder, "optimized_output.txt", optimized_frameglasses)

# Execute the script
if __name__ == "__main__":
    input_file_path = r'D:\KWC_2\input\1_binary_landscapes.txt'
    output_folder = 'output'
    process_data(input_file_path, output_folder)
