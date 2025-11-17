from ortools.sat.python import cp_model


def build_complete_graph_edges(n):
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            edges.append((i, j))
    return edges


def solve_kn_antimagic(n, time_limit_seconds=None, verbose=True):
    
    # 1. Calculating basic parameters
    m = n * (n - 1) // 2 

    numerator = m * (m + 1) - (n * (n - 1) // 2)

    if numerator % n != 0:
        if verbose:
            print(f"K_{n}: a is not an integer → (a,1)-antimagic impossible")
        return None

    a = numerator // n
    target_sums = [a + i for i in range(n)]

    if verbose:
        print(f"===== Checking K_{n} =====")
        print(f"n = {n}, m = {m}")
        print(f"a = {a}")
        print(f"Target vertex sums = {target_sums}")
        print()

    # 2. Generating graph and model
    edges = build_complete_graph_edges(n) 
    assert len(edges) == m

    edge_index = {}
    for idx, (u, v) in enumerate(edges):
        edge_index[(u, v)] = idx
        edge_index[(v, u)] = idx 

    model = cp_model.CpModel()

    x = [
        model.NewIntVar(1, m, f"x_{u}_{v}")
        for (u, v) in edges
    ]

    model.AddAllDifferent(x)

    for i in range(n):
        incident_indices = []
        for j in range(n):
            if i == j:
                continue
            idx = edge_index[(min(i, j), max(i, j))]
            incident_indices.append(idx)
        model.Add(sum(x[idx] for idx in incident_indices) == a + i)

    # 3. Brief symmetry breaking
    if n >= 2:
        idx_01 = edge_index[(0, 1)]
        model.Add(x[idx_01] == 1)

    # 4. Solver Setting & Implementation
    solver = cp_model.CpSolver()
    if time_limit_seconds is not None:
        solver.parameters.max_time_in_seconds = float(time_limit_seconds)

    solver.parameters.log_search_progress = False

    status = solver.Solve(model)

    # 5. Result Analysis
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        if verbose:
            print(f"K_{n}: Found an (a,1)-antimagic labeling!")
            print(f"Status = {solver.StatusName(status)}")
            print()

            print("Edge labels (u, v) : label")
            for (u, v), idx in edge_index.items():
                if u < v:
                    label = solver.Value(x[idx])
                    print(f"({u}, {v}) : {label}")
            print()

            print("Vertex sums (verification):")
            for i in range(n):
                incident_indices = []
                for j in range(n):
                    if i == j:
                        continue
                    idx = edge_index[(min(i, j), max(i, j))]
                    incident_indices.append(idx)
                vertex_sum = sum(solver.Value(x[idx]) for idx in incident_indices)
                print(f"  v{i}: sum = {vertex_sum} (target {a + i})")

        labeling = {
            "n": n,
            "m": m,
            "a": a,
            "edges": edges,
            "labels": {edges[i]: solver.Value(x[i]) for i in range(m)},
        }
        return labeling
    else:
        if verbose:
            print(f"K_{n}: No (a,1)-antimagic labeling exists.")
            print(f"Status = {solver.StatusName(status)}")
        return None


if __name__ == "__main__":
    solve_kn_antimagic(8, time_limit_seconds=60)
    print("\n" + "=" * 60 + "\n")
    solve_kn_antimagic(12, time_limit_seconds=600)
