import re
import matplotlib.pyplot as plt

# Parse scores from the log
def parse_scores(log_path):
    f1_scores = []
    pos_scores = []
    ndcg_scores = []

    current_f1 = current_pos = current_ndcg = None

    with open(log_path, 'r') as file:
        for line in file:
            if "F1" in line:
                match = re.search(r'F1\s*-\s*([\d.]+)', line)
                if match:
                    current_f1 = float(match.group(1))
            elif "Positional" in line:
                match = re.search(r'Positional\s*-\s*([\d.]+)', line)
                if match:
                    current_pos = float(match.group(1))
            elif "NDCG" in line:
                match = re.search(r'NDCG\s*-\s*([\d.]+)', line)
                if match:
                    current_ndcg = float(match.group(1))
                    # Once all three are captured, append and reset
                    if current_f1 is not None and current_pos is not None:
                        f1_scores.append(current_f1)
                        pos_scores.append(current_pos)
                        ndcg_scores.append(current_ndcg)
                        current_f1 = current_pos = current_ndcg = None

    return f1_scores, pos_scores, ndcg_scores


# Plot metric
def plot_metric(metric_values, title, ylabel):
    plt.figure()
    plt.plot(range(1, len(metric_values) + 1), metric_values, marker='o')
    plt.title(title)
    plt.xlabel("Simulated Failure #")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{title.lower().replace(' ', '_')}.png")

if __name__ == "__main__":
    log_file = "../../output/k10_logfile.log"
    f1_scores, pos_scores, ndcg_scores = parse_scores(log_file)
    plot_metric(f1_scores, "F1 Score over Simulations", "F1 Score")
    plot_metric(pos_scores, "Positional Score over Simulations", "Positional Score")
    plot_metric(ndcg_scores, "NDCG Score over Simulations", "NDCG Score")
