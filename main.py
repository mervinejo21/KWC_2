import os
import random
import time


def calculate_local_satisfaction(frame1, frame2, painting_tags):
    """
    Calculate Local Robotic Satisfaction between two frameglasses.
    Args:
        frame1 (list): Tags of the first frameglass.
        frame2 (list): Tags of the second frameglass.
        painting_tags (dict): A mapping of painting IDs to their tags.
    Returns:
        int: Local Robotic Satisfaction score.
    """
    tags1 = set()
    tags2 = set()

    # Collect tags from all paintings in each frameglass
    for painting in frame1:
        tags1.update(painting_tags[painting])

    for painting in frame2:
        tags2.update(painting_tags[painting])

    common_tags = len(tags1 & tags2)
    unique_to_frame1 = len(tags1 - tags2)
    unique_to_frame2 = len(tags2 - tags1)

    return min(common_tags, unique_to_frame1, unique_to_frame2)


def calculate_global_satisfaction(frameglasses, painting_tags):
    """
    Calculate Global Robotic Satisfaction for an order of frameglasses.
    Args:
        frameglasses (list): List of frameglasses.
        painting_tags (dict): A mapping of painting IDs to their tags.
    Returns:
        int: Global Robotic Satisfaction score.
    """
    total_satisfaction = 0
    for i in range(len(frameglasses) - 1):
        total_satisfaction += calculate_local_satisfaction(
            frameglasses[i], frameglasses[i + 1], painting_tags
        )
    return total_satisfaction


def save_output_file(frameglasses, output_file):
    """
    Save the frameglass data in the required format to the output file.
    Args:
        frameglasses (list): List of frameglasses.
        output_file (str): Path to the output file.
    """
    with open(output_file, "w") as file:
        # Write the number of frameglasses
        file.write(f"{len(frameglasses)}\n")
        # Write each frameglass
        for frameglass in frameglasses:
            file.write(" ".join(map(str, frameglass)) + "\n")


def main(input_file, output_folder):
    """
    Main function to parse input, process frameglasses, and generate output files.
    Args:
        input_file (str): Path to the input file.
        output_folder (str): Path to the output folder.
    """
    start_time = time.time()

    # Parse input file
    painting_tags = {}
    frameglasses = []
    with open(input_file, "r") as file:
        lines = file.readlines()
        num_paintings = int(lines[0].strip())  # First line gives the number of paintings
        painting_id = 0

        for line in lines[1:]:
            parts = line.strip().split()
            painting_type = parts[0]
            tags = parts[2:]

            painting_tags[painting_id] = tags
            if painting_type == "P":  # Portrait has two paintings
                painting_tags[painting_id + 1] = tags

            if painting_type == "L":
                frameglasses.append([painting_id])
                painting_id += 1
            elif painting_type == "P":
                frameglasses.append([painting_id, painting_id + 1])
                painting_id += 2

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Output file paths
    output_files = {
        "same_order": os.path.join(output_folder, "output_same_order.txt"),
        "reverse_order": os.path.join(output_folder, "output_reverse_order.txt"),
        "random_order": os.path.join(output_folder, "output_random_order.txt"),
        "tag_order": os.path.join(output_folder, "output_tag_order.txt"),
    }

    # Save outputs for the four conditions
    save_output_file(frameglasses, output_files["same_order"])
    save_output_file(frameglasses[::-1], output_files["reverse_order"])
    save_output_file(random.sample(frameglasses, len(frameglasses)), output_files["random_order"])
    save_output_file(
        sorted(frameglasses, key=lambda x: sum(len(painting_tags[p]) for p in x), reverse=True),
        output_files["tag_order"],
    )

    # Calculate scores
    scores = {
        "same_order": calculate_global_satisfaction(frameglasses, painting_tags),
        "reverse_order": calculate_global_satisfaction(frameglasses[::-1], painting_tags),
        "random_order": calculate_global_satisfaction(
            random.sample(frameglasses, len(frameglasses)), painting_tags
        ),
        "tag_order": calculate_global_satisfaction(
            sorted(frameglasses, key=lambda x: sum(len(painting_tags[p]) for p in x), reverse=True),
            painting_tags,
        ),
    }

    # Print execution time and scores
    print(f"Output files saved in '{output_folder}' successfully!")
    print(f"Total Execution Time: {time.time() - start_time:.4f} seconds")

    print("\nScores:")
    for order, score in scores.items():
        print(f"  {order.replace('_', ' ').title()}: {score}")


# File paths
input_file = r"D:\KWC_2\input\11_randomizing_paintings.txt"  # Replace with the input file path
output_folder = "output"  # Replace with the desired output folder path

# Run the program
main(input_file, output_folder)
