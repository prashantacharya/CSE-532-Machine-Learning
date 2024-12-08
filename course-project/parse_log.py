import json
import os


def parse_logs_to_json(logs):
    algorithms = {}
    lines = logs.strip().split("\n")

    current_algorithm = None
    window_size = None
    accuracy = precision = recall = f1_score = None

    for line in lines:
        if line.startswith("Training"):
            parts = line.split()
            current_algorithm = parts[1]
            if current_algorithm not in algorithms:
                algorithms[current_algorithm] = []
            # Extract window size
            window_size = int(parts[-1])
        elif line.startswith("Accuracy"):
            accuracy = float(line.split(": ")[1])
        elif line.startswith("Precision"):
            precision = float(line.split(": ")[1])
        elif line.startswith("Recall"):
            recall = float(line.split(": ")[1])
        elif line.startswith("F1 Score"):
            f1_score = float(line.split(": ")[1])
        elif line.startswith("=================================================="):
            # Add results for the current algorithm and window size
            if all(
                v is not None
                for v in [window_size, accuracy, precision, recall, f1_score]
            ):
                algorithms[current_algorithm].append(
                    {
                        "window_size": window_size,
                        "accuracy": accuracy,
                        "precision": precision,
                        "f1_score": f1_score,
                        "recall_score": recall,
                    }
                )
            # Reset metrics for safety
            window_size = accuracy = precision = recall = f1_score = None

    # Convert to the desired JSON format
    json_output = [
        {"algorithm": algo, "results": results} for algo, results in algorithms.items()
    ]

    # write json output to output.json
    with open("output.json", "w") as f:
        json.dump(json_output, f, indent=4)


with open("log", "r") as f:
    log_data = f.read()

# Parse logs again
parse_logs_to_json(log_data)
