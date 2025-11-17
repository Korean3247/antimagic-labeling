import math
import matplotlib.pyplot as plt

k8_result = solve_kn_antimagic(8, time_limit_seconds=60, verbose=False)
k12_result = solve_kn_antimagic(12, time_limit_seconds=600, verbose=False)

if k8_result is None:
    raise RuntimeError("K8 Not Found.")
if k12_result is None:
    raise RuntimeError("K12 Not Found.")


def draw_kn_labeling_from_result(result, title=None, save_path=None):
    n = result["n"]
    a = result["a"]
    labels = result["labels"]

    pos = {}
    for i in range(n):
        angle = 2 * math.pi * i / n
        pos[i] = (math.cos(angle), math.sin(angle))

    if title is None:
        title = f"K_{n} (a={a},1)-antimagic labeling"

    plt.figure(figsize=(6, 6))

    for (u, v), lab in labels.items():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        plt.plot([x1, x2], [y1, y2])
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        plt.text(mx, my, str(lab), fontsize=6, ha='center', va='center')

    xs = [pos[i][0] for i in range(n)]
    ys = [pos[i][1] for i in range(n)]
    plt.scatter(xs, ys)

    for i in range(n):
        x, y = pos[i]
        plt.text(x, y, str(i), fontsize=10, ha='center', va='center', fontweight='bold')

    plt.axis('equal')
    plt.axis('off')
    plt.title(title)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Image Saved: {save_path}")

    plt.show()



draw_kn_labeling_from_result(k8_result,
                             title="K8 (98,1)-antimagic labeling",
                             save_path="K8_antimagic.png")

draw_kn_labeling_from_result(k12_result,
                             title="K12 (363,1)-antimagic labeling",
                             save_path="K12_antimagic.png")
