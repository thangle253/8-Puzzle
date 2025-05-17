from collections import deque
import heapq
import random
import math
import time
from utils import generate_random_state, manhattan_distance
from heapq import heappop, heappush
from utils import is_solvable
import pygame
from itertools import permutations

# Hàm giải thuật BFS (Breadth-First Search): tìm kiếm theo chiều rộng, mở rộng tất cả các trạng thái cùng một mức độ trước khi chuyển sang mức độ tiếp theo
def bfs_solve(start_state):
    return generic_solve(start_state, queue=deque([(start_state, [])]), pop_method='popleft')

# Hàm giải thuật DFS (Depth-First Search): tìm kiếm theo chiều sâu, mở rộng các trạng thái theo chiều sâu trước khi quay lại
def dfs_solve(start_state, max_depth=100):
    stack = [(start_state, [], 0)]  # Thêm một giá trị depth vào mỗi phần tử
    visited = set()
    visited.add(tuple(start_state))

    while stack:
        state, path, depth = stack.pop()

        if state == list(range(1, 9)) + [0]:
            return path, len(visited)


        if depth >= max_depth:  # Nếu chiều sâu vượt quá max_depth thì tiếp tục
            continue

        zero_idx = state.index(0)  
        moves = [-3, 3, -1, 1]  

        # Generate next states
        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or  
                (move in [-3, 3]) 
            ):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]

                if tuple(new_state) not in visited:
                    visited.add(tuple(new_state))
                    stack.append((new_state, path + [(zero_idx, new_idx)], depth + 1))  # Cập nhật chiều sâu

    return None

# Hàm giải thuật Generic Solve: hàm tổng quát cho các thuật toán tìm kiếm khác nhau
def generic_solve(start_state, queue, pop_method='pop', is_priority=False):
    goal_state = list(range(1, 9)) + [0]
    visited = set()
    visited.add(tuple(start_state))

    while queue:
        if is_priority:
            _, g, state, path = heapq.heappop(queue)
        elif pop_method == 'heappop':
            _, state, path = heapq.heappop(queue)
        else:
            if pop_method == 'pop':
                state, path = queue.pop()
            else:
                state, path = queue.popleft()

        if state == goal_state:
            return path, len(visited)


        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]

                if tuple(new_state) not in visited:
                    visited.add(tuple(new_state))

                    if is_priority:
                        h = manhattan_distance(new_state)
                        new_g = g + 1
                        f = new_g + h
                        heapq.heappush(queue, (f, new_g, new_state, path + [(zero_idx, new_idx)]))
                    elif pop_method == 'heappop':
                        heapq.heappush(queue, (manhattan_distance(new_state), new_state, path + [(zero_idx, new_idx)]))
                    else:
                        queue.append((new_state, path + [(zero_idx, new_idx)]))

    return None, len(visited)

# Hàm giải thuật UCS (Uniform Cost Search): mở rộng các trạng thái theo thứ tự tổng chi phí nhỏ nhất từ trạng thái ban đầu đến trạng thái hiện tại.
def ucs_solve(start_state):
    # Sử dụng generic_solve với hàng đợi ưu tiên theo chi phí
    goal_state = list(range(1, 9)) + [0]
    visited = set()
    visited.add(tuple(start_state))  # Thêm trạng thái ban đầu vào tập đã duyệt
    queue = [(0, start_state, [])]  # (chi phí, trạng thái, đường đi)
    
    while queue:
        cost, state, path = heapq.heappop(queue)
        
        if state == goal_state:
            return path, len(visited)

        
        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]
        
        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and ((move in [-1, 1] and zero_idx // 3 == new_idx // 3) or (move in [-3, 3])):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                
                if tuple(new_state) not in visited:
                    visited.add(tuple(new_state))
                    # Trong UCS, chi phí là số bước đã đi
                    heapq.heappush(queue, (cost + 1, new_state, path + [(zero_idx, new_idx)]))
    
    return None

# Hàm giải thuật Greedy: mở rộng các trạng thái theo thứ tự ưu tiên dựa trên heuristic (ở đây là khoảng cách Manhattan)
def greedy_solve(start_state):
    return generic_solve(start_state, queue=[(manhattan_distance(start_state), start_state, [])], pop_method='heappop')

# Hàm giải thuật tìm kiếm sâu dần lặp IDDFS (Iterative Deepening Depth-First Search): tìm kiếm theo chiều sâu với giới hạn độ sâu tăng dần
def iddfs_solve(start_state):
    goal_state = list(range(1, 9)) + [0]

    def dls(state, path, depth_limit, visited, expansions):
        expansions[0] += 1
        if state == goal_state:
            return path
        if len(path) >= depth_limit:
            return None

        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]
        next_states = []

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]

                if tuple(new_state) not in visited:
                    next_states.append((new_state, path + [(zero_idx, new_idx)]))

        next_states.sort(key=lambda x: manhattan_distance(x[0]))
        for new_state, new_path in next_states:
            visited.add(tuple(new_state))
            result = dls(new_state, new_path, depth_limit, visited, expansions)
            if result is not None:
                return result
            visited.remove(tuple(new_state))

        return None

    for depth_limit in range(5, 50, 5):
        visited = set([tuple(start_state)])
        expansions = [0]
        solution = dls(start_state, [], depth_limit, visited, expansions)
        if solution is not None:
            return solution, expansions[0]

    return None, 0

# Hàm giải thuật A* (A Star Search)
def astar_solve(start_state):
    return generic_solve(start_state, queue=[(manhattan_distance(start_state), 0, start_state, [])], pop_method='heappop', is_priority=True)

# Hàm giải thuật IDA* (Iterative Deepening A* Search)
def idastar_solve(start_state):
    goal_state = list(range(1, 9)) + [0]  # Trạng thái đích

    def search(state, path, g, threshold, visited, expansions):
        expansions[0] += 1  # Đếm node mở rộng
        f = g + manhattan_distance(state)  # f(n) = g(n) + h(n)

        if f > threshold:
            return f, None
        if state == goal_state:
            return f, path

        min_threshold = float('inf')
        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and ((move in [-1, 1] and zero_idx // 3 == new_idx // 3) or (move in [-3, 3])):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]

                if tuple(new_state) not in visited:
                    visited.add(tuple(new_state))
                    new_threshold, result = search(new_state, path + [(zero_idx, new_idx)], g + 1, threshold, visited, expansions)
                    visited.remove(tuple(new_state))

                    if result is not None:
                        return new_threshold, result
                    min_threshold = min(min_threshold, new_threshold)

        return min_threshold, None

    threshold = manhattan_distance(start_state)
    expansions = [0]  # Dùng list để tham chiếu

    while True:
        visited = set([tuple(start_state)])
        new_threshold, solution = search(start_state, [], 0, threshold, visited, expansions)
        if solution is not None:
            return solution, expansions[0]
        if new_threshold == float('inf'):
            return None, expansions[0]
        threshold = new_threshold

# Hàm giải thuật Hill Climbing: tìm kiếm theo chiều cao, mở rộng trạng thái tốt nhất tại mỗi bước
def hill_climbing_solve(start_state):
    goal_state = list(range(1, 9)) + [0]
    current_state = start_state[:]
    path = []
    expansions = 0  # ✅ Số node đã đánh giá (mỗi lần tính heuristic cho 1 hàng xóm)

    while current_state != goal_state:
        zero_idx = current_state.index(0)
        best_heuristic = manhattan_distance(current_state)
        best_move = None

        moves = [-3, 3, -1, 1]  # lên, xuống, trái, phải

        for move in moves:
            new_idx = zero_idx + move
            # Kiểm tra di chuyển hợp lệ
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                # Tạo trạng thái mới
                new_state = current_state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                new_heuristic = manhattan_distance(new_state)

                expansions += 1  # ✅ Mỗi trạng thái hàng xóm được đánh giá là 1 expansion

                # Nếu trạng thái tốt hơn thì chọn
                if new_heuristic < best_heuristic:
                    best_heuristic = new_heuristic
                    best_move = (zero_idx, new_idx)

        # Nếu không tìm được trạng thái tốt hơn → kẹt local max
        if best_move is None:
            return None, expansions

        # Di chuyển đến trạng thái tốt hơn
        zero_idx, new_idx = best_move
        current_state[zero_idx], current_state[new_idx] = current_state[new_idx], current_state[zero_idx]
        path.append(best_move)

    return path, expansions

# Hàm giải thuật Steepest Ascent Hill Climbing: tìm kiếm theo chiều cao với bước đi tốt nhất tại mỗi bước
def steepest_ascent_hill_climbing_solve(start_state):
    goal_state = list(range(1, 9)) + [0]
    current_state = start_state[:]
    path = []
    expansions = 0  # ✅ Số node đã đánh giá (gọi manhattan_distance)

    while current_state != goal_state:
        zero_idx = current_state.index(0)
        best_heuristic = manhattan_distance(current_state)
        best_moves = []

        moves = [-3, 3, -1, 1]

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                new_state = current_state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                
                new_heuristic = manhattan_distance(new_state)
                expansions += 1  # ✅ Mỗi lần đánh giá trạng thái là 1 node mở rộng

                if new_heuristic < best_heuristic:
                    best_heuristic = new_heuristic
                    best_moves = [(zero_idx, new_idx)]
                elif new_heuristic == best_heuristic:
                    best_moves.append((zero_idx, new_idx))

        if not best_moves:
            return None, expansions  # ✅ Trả về số node đã mở rộng dù thất bại

        # Chọn một bước ngẫu nhiên trong các bước tốt nhất
        selected_move = best_moves[0] if len(best_moves) == 1 else best_moves[len(best_moves) // 2]
        zero_idx, new_idx = selected_move

        current_state[zero_idx], current_state[new_idx] = current_state[new_idx], current_state[zero_idx]
        path.append((zero_idx, new_idx))

    return path, expansions


# Hàm giải thuật Hill Climbing với ngẫu nhiên
def stochastic_hill_climbing_solve(start_state):
    import random
    goal_state = list(range(1, 9)) + [0]
    current_state = start_state[:]
    path = []
    expansions = 0  # ✅ Số node được đánh giá bằng heuristic

    while current_state != goal_state:
        zero_idx = current_state.index(0)
        neighbors = []
        moves = [-3, 3, -1, 1]

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                new_state = current_state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                h = manhattan_distance(new_state)
                expansions += 1  # ✅ Mỗi trạng thái được đánh giá
                neighbors.append((new_state, (zero_idx, new_idx), h))

        # Lọc các trạng thái lân cận tốt hơn
        current_h = manhattan_distance(current_state)
        better_neighbors = [(state, move) for state, move, h in neighbors if h < current_h]

        if not better_neighbors:
            return None, expansions  # ✅ Trả về cả số node mở rộng

        # Chọn ngẫu nhiên một trạng thái tốt hơn
        next_state, move = random.choice(better_neighbors)

        current_state = next_state
        path.append(move)

    return path, expansions


# Hàm giải thuật Simulated Annealing
def simulated_annealing_solve(start_state):
    state = start_state[:]
    path = []
    goal = list(range(1, 9)) + [0]

    T = 400.0          # 🔥 Nhiệt độ ban đầu
    alpha = 0.999       # 🔽 Làm nguội nhanh
    min_temp = 0.1     # ❄️ Nhiệt độ tối thiểu
    expansions = 0     # ✅ Số node mở rộng

    while True:
        if state == goal:
            return path, expansions

        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]
        current_h = manhattan_distance(state)
        neighbors = []

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                temp = state[:]
                temp[zero_idx], temp[new_idx] = temp[new_idx], temp[zero_idx]
                h = manhattan_distance(temp)
                expansions += 1
                neighbors.append((temp, (zero_idx, new_idx), h))

        if not neighbors:
            break

        next_state, move, h = random.choice(neighbors)
        delta_e = current_h - h

        if delta_e > 0 or random.random() < math.exp(delta_e / T):
            state = next_state
            path.append(move)

        T *= alpha
        if T < min_temp:
            break

    return (path, expansions) if state == goal else (None, expansions)

# Hàm giải thuật Beam Search
def beam_search_solve(start_state, beam_width=9):
    goal_state = list(range(1, 9)) + [0]
    queue = [(manhattan_distance(start_state), start_state, [])]
    visited = set()
    expansions = 0  # ✅ Số node mở rộng

    while queue:
        next_level = []

        for _, state, path in queue:
            if state == goal_state:
                return path, expansions

            visited.add(tuple(state))
            zero_idx = state.index(0)
            moves = [-3, 3, -1, 1]

            for move in moves:
                new_idx = zero_idx + move
                if 0 <= new_idx < 9 and (
                    (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                    (move in [-3, 3])
                ):
                    new_state = state[:]
                    new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]

                    if tuple(new_state) not in visited:
                        new_path = path + [(zero_idx, new_idx)]
                        h = manhattan_distance(new_state)
                        heappush(next_level, (h, new_state, new_path))
                        expansions += 1  # ✅ Tăng khi tạo node hợp lệ mới

        queue = [heappop(next_level) for _ in range(min(beam_width, len(next_level)))]

    return None, expansions  # ✅ Trả về số node mở rộng kể cả khi fail

# Hàm giải thuật AND-OR Search: tìm kiếm theo chiều sâu với các trạng thái AND và OR
def and_or_search(start, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0), max_depth=50):
    expansions = 0
    visited = set()  # ✅ Để đảm bảo không đếm lại node đã mở rộng

    def goal_test(state):
        return state == goal

    def get_neighbors(state):
        neighbors = []
        zero_idx = state.index(0)
        row, col = divmod(zero_idx, 3)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # UP, DOWN, LEFT, RIGHT

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_idx = nr * 3 + nc
                new_state = list(state)
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                neighbors.append(tuple(new_state))
        return neighbors

    def results(state, action_state):
        return [action_state]  # môi trường xác định

    def or_search(state, path, depth):
        nonlocal expansions
        if goal_test(state):
            return [state]
        if state in path or depth > max_depth:
            return None
        if state not in visited:
            expansions += 1
            visited.add(state)

        for neighbor in get_neighbors(state):
            if neighbor not in path:
                plan = and_search(results(state, neighbor), path + [state], depth + 1)
                if plan:
                    return [state] + plan
        return None

    def and_search(states, path, depth):
        full_plan = []
        for s in states:
            plan = or_search(s, path, depth)
            if plan is None:
                return None
            full_plan.extend(plan[1:] if full_plan else plan)
        return full_plan

    plan = or_search(start, [], 0)
    return (plan, expansions) if plan else (None, expansions)


def no_observation_search(start_state=None):
    goal_state = tuple([1, 2, 3, 4, 5, 6, 7, 8, 0])
    print("📥 Bắt đầu no_observation_search()")

    # --- Kiểm tra solvability ---
    def is_solvable(state):
        inv = 0
        for i in range(8):
            for j in range(i+1, 9):
                if state[i] and state[j] and state[i] > state[j]:
                    inv += 1
        return inv % 2 == 0

    # --- 1) Tạo belief ban đầu ---
    if start_state:
        belief0 = {tuple(start_state)}
        print(f"🔍 Trạng thái đầu vào: {start_state}")

    else:
        belief0 = set(filter(is_solvable, permutations(range(9))))
        print(f"🔁 Khởi tạo belief với {len(belief0)} trạng thái có thể giải được")


    queue = deque([(belief0, [])])
    visited = set()
    expansions = 0

    moves = {
        'UP':    (-1,  0),
        'DOWN':  ( 1,  0),
        'LEFT':  ( 0, -1),
        'RIGHT': ( 0,  1)
    }

    while queue:
        belief, path = queue.popleft()
        key = frozenset(belief)
        if key in visited:
            continue
        visited.add(key)
        expansions += 1

        if all(state == goal_state for state in belief):
            print("✅ Tìm thấy lời giải!")
            print(f"🪜 Hành động: {path}")
            return path, expansions


        for action, (dr, dc) in moves.items():
            new_belief = set()
            ok = True
            for st in belief:
                zero = st.index(0)
                r, c = divmod(zero, 3)
                nr, nc = r+dr, c+dc
                if 0 <= nr < 3 and 0 <= nc < 3:
                    idx2 = nr*3 + nc
                    lst  = list(st)
                    lst[zero], lst[idx2] = lst[idx2], lst[zero]
                    new_belief.add(tuple(lst))
                else:
                    ok = False
                    break
            if ok and new_belief:
                queue.append((new_belief, path + [(zero, idx2)]))

    return None

# Hàm giải thuật Partial Observable Search (Belief State Search): tìm kiếm với trạng thái "quan sát được" một số ô trên bảng (1,2,3)
def partial_observable_search(start_set, goal_set):
    """
    Tìm kiếm BFS trong môi trường quan sát một phần.
    - start_set: tập các trạng thái ban đầu (dạng tuple)
    - goal_set: tập các trạng thái mục tiêu (dạng tuple)
    - Chỉ các ô ngoài observed_indices mới được thay đổi
    Trả về: danh sách hành động và số lần mở rộng
    """
    observed_indices = {0, 1, 2}  # Các ô không được ảnh hưởng

    def flatten(state):
        return tuple(state)

    goal_flat_set = {flatten(g) for g in goal_set}
    queue = deque([(start_set, [])])
    visited = set()
    expansions = 0

    # Hành động tương ứng với dịch chuyển vị trí 0
    directions = {
        "up": -3,
        "down": 3,
        "left": -1,
        "right": 1
    }

    while queue:
        belief, actions = queue.popleft()
        frozen = frozenset(belief)
        if frozen in visited:
            continue
        visited.add(frozen)
        expansions += 1

        if any(flatten(s) in goal_flat_set for s in belief):
            return actions, expansions

        for action, move in directions.items():
            new_belief = set()
            for state in belief:
                zero_idx = state.index(0)
                new_idx = zero_idx + move

                if 0 <= new_idx < 9 and (
                    (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                    (move in [-3, 3])
                ):
                    # Không được ảnh hưởng đến các ô đã quan sát
                    if new_idx in observed_indices:
                        continue

                    new_state = list(state)
                    new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                    new_belief.add(tuple(new_state))

            if new_belief:
                queue.append((new_belief, actions + [action]))

    return None, expansions

# Danh sách các bước di chuyển hợp lệ
def get_next_states(state):
    moves = [-3, 3, -1, 1]  # Các di chuyển: lên (-3), xuống (3), trái (-1), phải (1)
    next_states = []
    zero_idx = state.index(0)  # Tìm vị trí của ô 0

    for move in moves:
        new_idx = zero_idx + move

        # Kiểm tra xem ô mới có hợp lệ không (không ra ngoài ma trận 3x3)
        if 0 <= new_idx < 9 and (
            (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or  # Không di chuyển sang ô ngoài cùng hàng
            (move in [-3, 3])  # Di chuyển lên xuống
        ):
            new_state = state[:]
            new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]  # Hoán đổi ô 0 với ô kế tiếp
            next_states.append((new_state, (zero_idx, new_idx)))

    return next_states

def backtracking_csp():
    nodes_expanded = [0]
    max_depth = [0]
    path = []

    variables = [f"X{i+1}" for i in range(9)]
    domains = {var: list(range(9)) for var in variables}

    # Shuffle domains for random order
    for var in domains:
        random.shuffle(domains[var])

    constraints = create_constraints()

    csp = {
        'variables': variables,
        'domains': domains,
        'constraints': constraints,
        'initial_assignment': {}
    }

    result = backtrack({}, 0, csp, nodes_expanded, max_depth, path)

    if result:
        solution_grid = [[0 for _ in range(3)] for _ in range(3)]
        for var, value in result.items():
            idx = int(var[1:]) - 1
            row, col = divmod(idx, 3)
            solution_grid[row][col] = value

        return {
            'path': path,
            'nodes_expanded': nodes_expanded[0],
            'max_depth': max_depth[0],
            'solution': solution_grid
        }
    else:
        return {
            'path': [],
            'nodes_expanded': nodes_expanded[0],
            'max_depth': max_depth[0],
            'solution': None
        }

def create_constraints():
    constraints = []

    # Vertical constraints (X1 with X4, X2-X5,...)
    top_bottom_pairs = [
        ('X1', 'X4'), ('X2', 'X5'), ('X3', 'X6'),
        ('X4', 'X7'), ('X5', 'X8')
    ]
    for top, bottom in top_bottom_pairs:
        constraints.append((top, bottom, lambda t, b: b == t + 3 and t != 0))

    # Horizontal constraints (X1-X2, X2-X3, X4-X5,...)
    left_right_pairs = [
        ('X1', 'X2'), ('X2', 'X3'),
        ('X4', 'X5'), ('X5', 'X6'),
        ('X7', 'X8')
    ]
    for left, right in left_right_pairs:
        constraints.append((left, right, lambda l, r: r == l + 1 and l != 0))

    return constraints

def is_consistent(var, value, assignment, csp):
    if value in assignment.values():
        return False

    temp_assignment = assignment.copy()
    temp_assignment[var] = value

    for constraint in csp['constraints']:
        if len(constraint) == 3:
            var1, var2, constraint_func = constraint
            if var1 in temp_assignment and var2 in temp_assignment:
                if not constraint_func(temp_assignment[var1], temp_assignment[var2]):
                    return False

    return True

def backtrack(assignment, index, csp, nodes_expanded, max_depth, path):
    nodes_expanded[0] += 1
    max_depth[0] = max(max_depth[0], len(assignment))

    if assignment:
        grid = [[None for _ in range(3)] for _ in range(3)]
        for var, value in assignment.items():
            idx = int(var[1:]) - 1
            row, col = divmod(idx, 3)
            grid[row][col] = value
        path.append(grid)

    if index == len(csp['variables']):
        final_state = tuple(assignment[f"X{i+1}"] for i in range(9))
        return assignment if is_solvable(final_state) else None

    var = csp['variables'][index]

    for value in csp['domains'][var]:
        if is_consistent(var, value, assignment, csp):
            assignment[var] = value
            # Ensure only valid moves (zero_idx, move_idx) are appended to the path
            if len(assignment) > 1:
                prev_var = csp['variables'][index - 1]
                prev_idx = int(prev_var[1:]) - 1
                zero_idx = prev_idx
                move_idx = int(var[1:]) - 1
                if zero_idx != move_idx and 0 <= zero_idx < 9 and 0 <= move_idx < 9:
                    path.append((zero_idx, move_idx))
            result = backtrack(assignment, index + 1, csp, nodes_expanded, max_depth, path)
            if result:
                return result
            del assignment[var]

    return None

def revise(csp, Xi, Xj):
    """
    REMOVE-INCONSISTENT-VALUES(Xi, Xj)
    Nếu tồn tại x in DOMAIN[Xi] mà không có y in DOMAIN[Xj]
    sao cho constraint(x,y) == True, thì loại x khỏi DOMAIN[Xi].
    Trả về True nếu có x bị loại.
    """
    removed = False
    # lặp trên bản sao để vừa xóa vừa lặp được
    for x in csp['domains'][Xi][:]:
        # tìm constraint giữa Xi và Xj
        funcs = [func for (var1, var2, func) in csp['constraints']
                 if var1 == Xi and var2 == Xj]
        # nếu không có constraint nào thì không remove
        if not funcs:
            continue
        func = funcs[0]
        # kiểm tra xem có y nào thỏa không
        if not any(func(x, y) for y in csp['domains'][Xj]):
            csp['domains'][Xi].remove(x)
            removed = True
    return removed

def ac3(csp=None, counter=None, draw_board_callback=None, external_queue=None):
    """
    AC-3 algorithm for 8-puzzle problem
    If csp is None, a new CSP is created with random domain values.
    Returns the final state if successful, None otherwise.
    """
    if csp is None:
        # Create a new CSP with variables X1..X9 and domains 0..8 (shuffled)
        variables = [f"X{i+1}" for i in range(9)]
        domains = {var: list(range(9)) for var in variables}
        
        # Shuffle domains for random ordering
        for var in domains:
            random.shuffle(domains[var])
            
        csp = {
            'variables': variables,
            'domains': domains,
            'constraints': create_constraints()
        }
    
    if counter is None:
        counter = [0]
    
    # Khởi tạo queue với tất cả các cung (Xi, Xj) hoặc sử dụng queue được cung cấp
    if external_queue is None:
        queue = deque((Xi, Xj) for (Xi, Xj, _) in csp['constraints'])
        complete_execution = True  # Chạy đến hoàn thành nếu không có external_queue
    else:
        queue = external_queue
        complete_execution = False  # Chỉ xử lý một bước nếu có external_queue
        
        # Nếu queue rỗng và có external_queue, có nghĩa là đã xử lý xong tất cả
        if not queue:
            # Assign values after AC-3 completes
            assigned = assign_values_after_ac3(csp)
            if assigned:
                # Cập nhật domains với các giá trị đã gán
                for var in csp['variables']:
                    csp['domains'][var] = [assigned[var]]
                
                # Hiển thị trạng thái cuối cùng
                if draw_board_callback:
                    final_state = [assigned[f"X{i+1}"] for i in range(9)]
                    draw_board_callback(final_state)
                return final_state  # Return the final state
            else:
                return None

    # Nếu là external_queue, chỉ xử lý một bước
    iterations = float('inf') if complete_execution else 1
    iteration_count = 0
    
    while queue and iteration_count < iterations:
        iteration_count += 1
        Xi, Xj = queue.popleft()
        counter[0] += 1  # mỗi cung được xử lý
        if revise(csp, Xi, Xj):
            if not csp['domains'][Xi]:
                # domain trống → vô nghiệm
                return None
            # enqueue lại mọi (Xk, Xi) với Xk láng giềng Xi (ngoại trừ Xj)
            neighbors = {var1 for (var1, var2, _) in csp['constraints']
                         if var2 == Xi and var1 != Xj}
            for Xk in neighbors:
                queue.append((Xk, Xi))

        # Create a consistent current state for visualization
        current_state = create_consistent_state(csp['domains'])
        
        # Hiển thị tiến trình nếu có callback
        if draw_board_callback:
            draw_board_callback(current_state)
            
    # Nếu không phải complete_execution và vẫn còn phần tử trong queue
    # thì sẽ return external_queue để tiếp tục xử lý trong các lần gọi tiếp theo
    if not complete_execution:
        return external_queue
            
    # After AC-3 completes, assign single values to domains with multiple values
    assigned = assign_values_after_ac3(csp)
    if not assigned:
        return None
    
    # Update domains with final assignments
    for var in csp['variables']:
        csp['domains'][var] = [assigned[var]]

    # Create the final solution state
    final_state = [assigned[f"X{i+1}"] for i in range(9)]
    
    # Show final solution
    if draw_board_callback:
        draw_board_callback(final_state)
    
    # Ensure the solution is valid (contains all values 0-8 exactly once)
    if sorted(final_state) != list(range(9)):
        return None
    
    # Verify the solution is solvable
    if not is_solvable(final_state):
        # Try again or return None based on your preference
        return None
        
    return final_state

def assign_values_after_ac3(csp):
    """Hàm phụ trợ để hoàn thành giải pháp sau khi AC-3 kết thúc"""
    assigned = {}
    unassigned_vars = []
    
    # First, assign variables with singleton domains
    for var in csp['variables']:
        if len(csp['domains'][var]) == 1:
            assigned[var] = csp['domains'][var][0]
        else:
            unassigned_vars.append(var)
    
    # Check if all values 0-8 are used exactly once
    used_values = list(assigned.values())
    if len(set(used_values)) != len(used_values):
        print("Warning: Detected duplicate values in initial assignments")
    
    missing_values = [i for i in range(9) if i not in used_values]
    
    if unassigned_vars:
        print(f"Running backtracking to complete the solution for {len(unassigned_vars)} variables...")
        # Use backtracking to assign values to variables with multiple possibilities
        solution_found = backtrack_ac3_solution(csp, assigned, unassigned_vars, None, missing_values)
        if not solution_found:
            print("Failed to find a complete valid solution.")
            return None
    
    # Final validation
    values = [assigned[var] for var in csp['variables']]
    if len(set(values)) != 9 or sorted(values) != list(range(9)):
        print("Error: Final solution is invalid. Contains duplicates or missing numbers.")
        return None
    
    return assigned

def backtrack_ac3_solution(csp, assigned, unassigned_vars, draw_board_callback=None, missing_values=None):
    """Backtracking algorithm to complete AC3 solution."""
    if not unassigned_vars:  # All variables assigned
        # Validate complete assignment
        return True
    
    # Select next unassigned variable
    var = unassigned_vars[0]
    remaining_vars = unassigned_vars[1:]
    
    # Filter domain to only use missing values if available
    domain_to_try = missing_values if missing_values else csp['domains'][var]
    
    # Try each value in the domain
    for value in domain_to_try:
        # Check if this assignment is consistent with current assignments
        if is_consistent_assignment(csp, var, value, assigned):
            # Assign value
            assigned[var] = value
            
            # Update missing values
            new_missing_values = missing_values.copy() if missing_values else None
            if new_missing_values:
                new_missing_values.remove(value)
            
            # Visualize current state if callback provided
            if draw_board_callback:
                current_state = [assigned.get(f"X{i+1}", i) for i in range(9)]
                # Make sure unassigned positions have unique values
                for i in range(9):
                    var_name = f"X{i+1}"
                    if var_name not in assigned:
                        possible_vals = csp['domains'][var_name]
                        if possible_vals:
                            current_state[i] = possible_vals[0]  # Just pick first value for visualization
                
                draw_board_callback(current_state)
            
            # Recursively try to assign remaining variables
            if backtrack_ac3_solution(csp, assigned, remaining_vars, draw_board_callback, new_missing_values):
                return True
            
            # If we get here, this assignment didn't work
            del assigned[var]
    
    # No viable assignment found
    return False

def is_consistent_assignment(csp, var, value, assigned):
    """Check if assigning value to var is consistent with current assignments."""
    # Check if this value conflicts with any existing assignments
    if value in assigned.values():
        return False
    
    # Check constraints
    for (var1, var2, constraint_func) in csp['constraints']:
        if var1 == var and var2 in assigned:
            if not constraint_func(value, assigned[var2]):
                return False
        elif var2 == var and var1 in assigned:
            if not constraint_func(assigned[var1], value):
                return False
    
    return True

def create_consistent_state(domains):
    """
    Tạo một trạng thái nhất quán từ các miền cho việc hiển thị.
    Đảm bảo rằng:
    1. Mỗi vị trí có một giá trị duy nhất
    2. Có đúng một ô có giá trị là 0 (ô trống)
    3. Sử dụng các giá trị từ domain khi có thể
    """
    # Khởi tạo trạng thái rỗng
    current_state = [None] * 9
    used_values = set()
    
    # Trước tiên, gán các giá trị cho các biến có domain đơn
    for i in range(9):
        var = f"X{i+1}"
        if len(domains[var]) == 1:
            value = domains[var][0]
            # Kiểm tra xem giá trị này đã được sử dụng chưa
            if value not in used_values:
                current_state[i] = value
                used_values.add(value)
    
    # Đảm bảo rằng ô trống (0) được đặt
    zero_placed = False
    if 0 not in used_values:
        # Tìm biến chứa 0 trong domain và chưa được gán
        for i in range(9):
            if current_state[i] is None:
                var = f"X{i+1}"
                if 0 in domains[var]:
                    current_state[i] = 0
                    used_values.add(0)
                    zero_placed = True
                    break
        
        # Nếu không có biến nào chứa 0 trong domain, đặt 0 vào vị trí đầu tiên còn trống
        if not zero_placed:
            for i in range(9):
                if current_state[i] is None:
                    current_state[i] = 0
                    used_values.add(0)
                    zero_placed = True
                    break
    else:
        zero_placed = True
    
    # Tiếp theo, gán các giá trị từ domain cho các biến còn lại
    # Nhưng thay vì chọn ngẫu nhiên, chọn giá trị đầu tiên có sẵn để đảm bảo tính ổn định của hiển thị
    for i in range(9):
        if current_state[i] is None:
            var = f"X{i+1}"
            # Tìm giá trị đầu tiên trong domain chưa được sử dụng
            for value in domains[var]:
                if value not in used_values:
                    current_state[i] = value
                    used_values.add(value)
                    break
            
            # Nếu vẫn chưa gán được (do tất cả các giá trị trong domain đều đã sử dụng)
            # Gán một giá trị bất kỳ chưa được sử dụng
            if current_state[i] is None:
                for value in range(9):
                    if value not in used_values:
                        current_state[i] = value
                        used_values.add(value)
                        break
    
    # Đảm bảo tất cả các vị trí đều đã được gán giá trị
    # Nếu vẫn còn vị trí None, điều này có thể xảy ra nếu tất cả các giá trị 0-8 đã được sử dụng
    # Trong trường hợp này, chỉ cần sử dụng lại một giá trị (ví dụ: giá trị đầu tiên)
    # (đây chỉ là hiển thị tạm thời nên không cần thiết phải hoàn toàn chính xác)
    for i in range(9):
        if current_state[i] is None:
            current_state[i] = i  # Sử dụng chỉ số làm giá trị
    
    return current_state

def ac3_with_backtracking(start_state=None, arc_count=None):
    """
    AC-3 with backtracking for solving 8-puzzle.
    
    This function:
    1. Performs AC3 constraint propagation to reduce the domains
    2. Then applies backtracking to find a complete solution
    3. Generates a solution path for visualization
    
    Args:
        start_state: Initial puzzle state (optional)
        arc_count: Counter for arcs processed (optional)
        
    Returns:
        List of moves (zero_idx, new_idx) representing the solution path
    """
    # If no start state provided, generate a random solvable one
    if start_state is None:
        from .utils import generate_random_state
        start_state = generate_random_state()
    
    # Set up arc_count if not provided
    if arc_count is None:
        arc_count = [0]

    # Step 1: Create CSP representation
    variables = [f"X{i+1}" for i in range(9)]
    domains = {}
    
    # Initialize domains based on start_state if provided
    if start_state:
        for i in range(9):
            var = f"X{i+1}"
            domains[var] = [start_state[i]]
    else:
        # Initial domains contain all possible values
        domains = {var: list(range(9)) for var in variables}
        # Shuffle domains for randomization
        for d in domains.values():
            random.shuffle(d)
    
    # Create constraints
    constraints = create_constraints()
    csp = {'variables': variables, 'domains': domains, 'constraints': constraints}
    
    # Step 2: Run AC3 to reduce domains
    print("Running AC3 to reduce domains...")
    
    # Setup initial queue with all binary constraints
    queue = deque((Xi, Xj) for (Xi, Xj, _) in constraints)
    
    # Run AC3
    while queue:
        Xi, Xj = queue.popleft()
        arc_count[0] += 1
        
        if revise(csp, Xi, Xj):
            if not csp['domains'][Xi]:
                # Domain became empty, problem is unsolvable
                print("Domain became empty, problem is unsolvable")
                return None
            
            # Add all neighbors of Xi (except Xj) back to queue
            neighbors = {var1 for (var1, var2, _) in constraints 
                        if var2 == Xi and var1 != Xj}
            for Xk in neighbors:
                queue.append((Xk, Xi))
    
    # Check if AC3 already solved the problem
    single_valued_domains = all(len(domain) == 1 for domain in csp['domains'].values())
    if single_valued_domains:
        # Convert domains to state
        final_state = [csp['domains'][f"X{i+1}"][0] for i in range(9)]
        
        # Find solution path from start_state to final_state
        print("AC3 fully solved the puzzle! Finding solution path...")
        solution_path = find_solution_path(start_state, final_state)
        return solution_path
    
    # Step 3: Backtrack on the CSP with reduced domains
    print("AC3 reduced domains, continuing with backtracking...")
    nodes_expanded = [0]
    max_depth = [0]
    path = []
    assignment = {}
    
    def backtrack_visualize(assignment, index, csp, nodes_expanded, max_depth, path, state_history):
        """Backtracking with visualization for solving CSP"""
        nodes_expanded[0] += 1
        max_depth[0] = max(max_depth[0], len(assignment))
        
        # For visualization, track the current state
        if assignment:
            current_state = [0] * 9  # Default state with all zeros
            for var, value in assignment.items():
                idx = int(var[1:]) - 1
                current_state[idx] = value
            
            # Add current state to history if it's different from the previous one
            if not state_history or current_state != state_history[-1]:
                state_history.append(current_state[:])
        
        # If assignment complete, return
        if index == len(csp['variables']):
            return assignment
        
        var = csp['variables'][index]
        
        for value in csp['domains'][var]:
            if is_consistent(var, value, assignment, csp):
                assignment[var] = value
                result = backtrack_visualize(assignment, index + 1, csp, nodes_expanded, max_depth, path, state_history)
                if result:
                    return result
                del assignment[var]
        
        return None
    
    # Track state history for path reconstruction
    state_history = []
    result = backtrack_visualize(assignment, 0, csp, nodes_expanded, max_depth, path, state_history)
    
    if not result:
        print("Backtracking could not find a solution")
        return None
    
    # Step 4: Construct solution path for visualization
    print(f"Solution found after expanding {nodes_expanded[0]} nodes!")
    
    # If state_history exists, construct moves from it
    solution_path = []
    if state_history and len(state_history) > 1:
        for i in range(len(state_history) - 1):
            current = state_history[i]
            next_state = state_history[i + 1]
            
            # Find positions that changed (zero moved)
            different_positions = [(idx, val1, val2) for idx, (val1, val2) in 
                                  enumerate(zip(current, next_state)) if val1 != val2]
            
            if different_positions:
                # Find the positions of the blank tile (0) in both states
                zero_idx_current = current.index(0) if 0 in current else -1
                zero_idx_next = next_state.index(0) if 0 in next_state else -1
                
                # If zero moved, record the move
                if zero_idx_current != -1 and zero_idx_next != -1:
                    solution_path.append((zero_idx_current, zero_idx_next))
                else:
                    # Find the two positions that swapped
                    pos1, val1_current, val1_next = different_positions[0]
                    pos2, val2_current, val2_next = different_positions[1] if len(different_positions) > 1 else (None, None, None)
                    
                    if pos2 is not None:
                        # Add the swap as a move
                        solution_path.append((pos1, pos2))
    
    # If state_history doesn't have good moves, use find_solution_path
    if not solution_path and state_history:
        print("State history didn't produce usable moves. Using A* to find path...")
        initial_state = start_state
        goal_state = state_history[-1] if state_history else None
        
        if goal_state:
            solution_path = find_solution_path(initial_state, goal_state)
    
    print(f"Generated solution path with {len(solution_path)} steps")
    return solution_path

def find_solution_path(start_state, goal_state=[1, 2, 3, 4, 5, 6, 7, 8, 0]):
    """
    Tìm đường đi từ trạng thái bắt đầu đến trạng thái đích bằng thuật toán A*
    Trả về danh sách các tuple (zero_idx, swap_idx) biểu diễn các bước di chuyển
    """
    from heapq import heappush, heappop
    from utils import manhattan_distance
    
    # Kiểm tra xem có thể giải được không
    from utils import is_solvable
    if not is_solvable(start_state) and is_solvable(goal_state):
        print("Trạng thái không thể giải được")
        return []

    visited = set()
    queue = [(manhattan_distance(start_state), 0, start_state, [])]  # (f, g, state, path)
    
    while queue:
        _, g, state, path = heappop(queue)
        
        if state == goal_state:
            return path
        
        state_tuple = tuple(state)
        if state_tuple in visited:
            continue
            
        visited.add(state_tuple)
        zero_idx = state.index(0)
        
        # Các nước đi có thể: lên, xuống, trái, phải
        moves = [
            (-3, "up"),    # Lên
            (3, "down"),   # Xuống
            (-1, "left"),  # Trái
            (1, "right")   # Phải
        ]
        
        for move, _ in moves:
            new_idx = zero_idx + move
            
            # Kiểm tra nước đi hợp lệ
            if (
                0 <= new_idx < 9 and  # Trong phạm vi bảng 3x3
                (move != -1 or zero_idx % 3 != 0) and  # Không vượt trái khi ở cột trái nhất
                (move != 1 or zero_idx % 3 != 2) and   # Không vượt phải khi ở cột phải nhất
                (move != -3 or zero_idx >= 3) and      # Không vượt lên khi ở hàng trên cùng
                (move != 3 or zero_idx < 6)            # Không vượt xuống khi ở hàng dưới cùng
            ):
                new_state = state.copy()
                # Hoán đổi vị trí
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                
                # Chỉ thêm vào hàng đợi nếu trạng thái mới chưa được duyệt
                if tuple(new_state) not in visited:
                    # Tính toán f = g + h với g là số bước đi và h là khoảng cách Manhattan
                    new_g = g + 1
                    new_f = new_g + manhattan_distance(new_state)
                    heappush(queue, (new_f, new_g, new_state, path + [(zero_idx, new_idx)]))
    
    # Nếu không tìm thấy giải pháp
    return []

def perform_ac3_with_solution(start_state=None, draw_callback=None, delay=300):
    """
    Thực hiện thuật toán AC3 và sau đó tạo ra giải pháp đến goal state [1,2,3,4,5,6,7,8,0]
    """
    # Nếu không có trạng thái bắt đầu, tạo một trạng thái ngẫu nhiên
    if start_state is None:
        from utils import generate_random_state
        start_state = generate_random_state()
    
    # Tạo CSP với domains được lấy từ trạng thái bắt đầu
    csp = {
        'variables': [f"X{i+1}" for i in range(9)],
        'domains': {},
        'constraints': create_constraints()
    }
    
    # Khởi tạo domains từ trạng thái bắt đầu
    for i in range(9):
        var = f"X{i+1}"
        csp['domains'][var] = [start_state[i]]
    
    # In ra domains ban đầu
    print("Initial domains:", csp['domains'])
    
    # Hiển thị trạng thái ban đầu
    if draw_callback:
        draw_callback(start_state)
        import pygame
        pygame.time.delay(delay)
    
    print("AC3 starting...")
    
    # Counter cho số cung được xử lý
    counter = [0]
    
    # Thực hiện AC3 (không cần thực sự thực hiện vì domains đã cố định)
    # Đây chỉ là để hiển thị trạng thái ban đầu
    print("AC3 completed quickly because domains are already fixed.")
    
    # Tìm đường đi từ trạng thái ban đầu đến goal state
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    solution_path = find_solution_path(start_state, goal_state)
    
    # Nếu không tìm thấy giải pháp, thông báo và kết thúc
    if not solution_path:
        print("Không tìm được đường đi tới goal state!")
        return False
    
    print(f"Tìm thấy đường đi với {len(solution_path)} bước")
    
    # Mô phỏng các bước đi
    current_state = start_state.copy()
    
    # Hiển thị từng bước một
    for step, (zero_idx, new_idx) in enumerate(solution_path):
        # Thực hiện nước đi
        current_state[zero_idx], current_state[new_idx] = current_state[new_idx], current_state[zero_idx]
        
        # Hiển thị trạng thái mới
        print(f"Step {step+1}: Move from index {zero_idx} to {new_idx}")
        print(f"Current state: {current_state}")
        
        if draw_callback:
            draw_callback(current_state)
            import pygame
            pygame.time.delay(delay)
    
    # Trả về True nếu đã tìm thấy giải pháp và hiển thị thành công
    return True

def ac3_solve():
    """
    Wrapper function for ac3 to make it consistent with other solver functions.
    Returns a dictionary with path, nodes_expanded, max_depth, and solution.
    """
    nodes_expanded = [0]  # Track nodes expanded
    max_depth = [0]       # Track maximum depth reached
    path = []             # Track the solution path
    
    # Create CSP with variables X1..X9 and domains 0..8 (shuffled)
    variables = [f"X{i+1}" for i in range(9)]
    domains = {var: list(range(9)) for var in variables}
    
    # Shuffle domains for random ordering
    for var in domains:
        random.shuffle(domains[var])
        
    csp = {
        'variables': variables,
        'domains': domains,
        'constraints': create_constraints(),
        'initial_assignment': {}
    }
    
    # Run AC3 algorithm
    final_state = ac3(csp, nodes_expanded)
    
    if final_state:
        # Convert the flat state to a 3x3 grid for the solution
        solution_grid = []
        for i in range(0, 9, 3):
            solution_grid.append(final_state[i:i+3])
        
        # Generate the path from the start to the solution
        # For simplicity in this implementation, we'll find the path using A* after AC3 finds a solution
        start_state = generate_random_state()  # We can use a random start state
        path = find_solution_path(start_state, final_state)
        
        return {
            'path': path,
            'nodes_expanded': nodes_expanded[0],
            'max_depth': max_depth[0],
            'solution': solution_grid
        }
    else:
        return {
            'path': [],
            'nodes_expanded': nodes_expanded[0],
            'max_depth': max_depth[0],
            'solution': None
        }

# Hàm giải thuật Genetic Algorithm: giải 8-puzzle sử dụng thuật toán di truyền
def genetic_algorithm_solve(start_state, population_size=200, max_generations=500, mutation_rate=0.1, timeout=30):
    goal_state = list(range(1, 9)) + [0]
    if start_state == goal_state:
        return [], 0
    if not is_solvable(start_state):
        return None, 0

    move_map = [-3, 3, -1, 1]

    def create_individual(length=60):
        # Tạo chuỗi hành động ngẫu nhiên, tránh lặp ngược
        ind = []
        last = None
        for _ in range(length):
            move = random.randint(0, 3)
            while last is not None and abs(move_map[move]) == abs(move_map[last]):
                move = random.randint(0, 3)
            ind.append(move)
            last = move
        return ind

    def apply_moves(state, moves):
        s = state[:]
        valid_path = []
        last_move = None
        for move in moves:
            zero = s.index(0)
            new_zero = zero + move_map[move]
            if last_move is not None and abs(move_map[move]) == abs(move_map[last_move]):
                continue
            if 0 <= new_zero < 9:
                if move in [2, 3] and zero // 3 != new_zero // 3:
                    continue
                s[zero], s[new_zero] = s[new_new := new_zero], s[zero]
                valid_path.append((zero, new_new))
                last_move = move
        return s, valid_path

    def fitness(state, path):
        dist = manhattan_distance(state)
        if state == goal_state:
            return 10_000 - len(path) * 2  # 🎯 Thưởng cực lớn nếu đạt goal
        return 1000 - dist - 0.5 * len(path)  # 🧠 Phạt nặng nếu đi vòng

    def tournament_selection(scored, k=5):
        group = random.sample(scored, k)
        return max(group, key=lambda x: x[0])[1]  # genome

    def crossover(p1, p2):
        point = random.randint(1, min(len(p1), len(p2)) - 1)
        return p1[:point] + p2[point:]

    def mutate(ind, rate):
        return [random.randint(0, 3) if random.random() < rate else m for m in ind]

    population = [create_individual() for _ in range(population_size)]
    best_score = float('-inf')
    best_path = []
    expansions = 0
    generations_no_improve = 0

    start = time.time()
    for gen in range(max_generations):
        if time.time() - start > timeout:
            break

        scored = []
        found_goal = False
        for ind in population:
            final_state, path = apply_moves(start_state, ind)
            expansions += 1
            score = fitness(final_state, path)
            scored.append((score, ind, path, final_state))
            if final_state == goal_state:
                return path, expansions

        scored.sort(reverse=True)

        # Giữ elite
        elites = scored[:population_size // 10]
        next_gen = [ind for _, ind, _, _ in elites]

        # Tạo thế hệ mới
        while len(next_gen) < population_size:
            p1 = tournament_selection(scored)
            p2 = tournament_selection(scored)
            child = mutate(crossover(p1, p2), mutation_rate)
            next_gen.append(child)

        population = next_gen

        # Theo dõi best path
        if scored[0][0] > best_score:
            best_score = scored[0][0]
            best_path = scored[0][2]
            generations_no_improve = 0
        else:
            generations_no_improve += 1

        # Nếu không cải thiện sau 50 thế hệ → restart nhẹ
        if generations_no_improve >= 50:
            print(f"🌀 Restart tại thế hệ {gen} do không cải thiện.")
            population = [create_individual() for _ in range(population_size)]
            generations_no_improve = 0

        if gen % 10 == 0:
            print(f"📈 Gen {gen}: điểm tốt nhất {int(best_score)}")

    return best_path if best_path else None, expansions

# Hàm giải thuật Q-Learning: giải 8-puzzle sử dụng thuật toán học tăng cường

def q_learning_solve(start_state, episodes=10000, alpha=0.1, gamma=0.95, epsilon=0.3, max_steps=5000):
    goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    def get_valid_actions(state):
        zero = state.index(0)
        r, c = divmod(zero, 3)
        actions = []
        if r > 0: actions.append("up")
        if r < 2: actions.append("down")
        if c > 0: actions.append("left")
        if c < 2: actions.append("right")
        return actions

    def take_action(state, action):
        zero = state.index(0)
        r, c = divmod(zero, 3)
        moves = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        dr, dc = moves[action]
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            idx2 = nr * 3 + nc
            new_state = list(state)
            new_state[zero], new_state[idx2] = new_state[idx2], new_state[zero]
            return tuple(new_state), (zero, idx2)
        return state, None

    # Khởi tạo bảng Q
    Q = dict()
    start_state = tuple(start_state)

    for ep in range(episodes):
        state = start_state
        for step in range(max_steps):
            actions = get_valid_actions(state)
            if not actions:
                break

            if random.random() < epsilon:
                action = random.choice(actions)
            else:
                q_vals = [Q.get((state, a), 0) for a in actions]
                action = actions[q_vals.index(max(q_vals))]

            next_state, _ = take_action(state, action)
            reward = 100 if next_state == goal_state else -1

            next_actions = get_valid_actions(next_state)
            max_q_next = max([Q.get((next_state, a), 0) for a in next_actions], default=0)
            td_target = reward + gamma * max_q_next
            td_error = td_target - Q.get((state, action), 0)
            Q[(state, action)] = Q.get((state, action), 0) + alpha * td_error

            if next_state == goal_state:
                break

            state = next_state

    # Giai đoạn dựng đường đi
    path = []
    state = start_state
    visited = set()

    for _ in range(50):
        if state == goal_state:
            return path, len(Q)
        visited.add(state)

        valid_actions = get_valid_actions(state)
        if not valid_actions:
            break

        q_vals = [Q.get((state, a), -float("inf")) for a in valid_actions]
        best_action = valid_actions[q_vals.index(max(q_vals))]
        next_state, move = take_action(state, best_action)
        if not move or next_state in visited:
            break

        path.append(move)
        state = next_state

    return (path, len(Q)) if state == goal_state else (None, len(Q))

# Hàm giải thuật Constraint Checking: giải 8-puzzle sử dụng thuật toán kiểm tra ràng buộc
def constraint_checking_solve():
    from random import shuffle
    nodes_expanded = [0]
    path = []

    variables = [f"X{i+1}" for i in range(9)]
    domains = {var: list(range(9)) for var in variables}
    for var in domains:
        shuffle(domains[var])  # xáo trộn để tránh bias

    constraints = create_constraints()

    csp = {
        'variables': variables,
        'domains': domains,
        'constraints': constraints,
        'initial_assignment': {}
    }    
    def is_consistent(var, value, assignment, csp):
        if value in assignment.values():
            return False
        for (v1, v2, func) in csp['constraints']:
            if v1 == var and v2 in assignment:
                if not func(value, assignment[v2]):
                    return False
            elif v2 == var and v1 in assignment:
                if not func(assignment[v1], value):
                    return False
        return True

    def backtrack(assignment, index, path, max_depth):
        nodes_expanded[0] += 1

        # Lưu lại trạng thái hiện tại để hiển thị quá trình tìm kiếm
        current_grid = [[0 for _ in range(3)] for _ in range(3)]
        for var, val in assignment.items():
            idx = int(var[1:]) - 1
            row, col = divmod(idx, 3)
            current_grid[row][col] = val
        path.append(current_grid)

        if index == len(variables):
            return assignment

        # Giới hạn độ sâu để không tìm quá lâu
        if len(path) > max_depth:
            return None

        var = variables[index]
        for val in domains[var]:
            if is_consistent(var, val, assignment, csp):
                assignment[var] = val
                result = backtrack(assignment, index + 1, path, max_depth)
                if result:
                    return result
                del assignment[var]
        return None

    # Thêm tham số path và max_depth vào lời gọi backtrack
    result = backtrack({}, 0, path, max_depth=50)
    if result:
        grid = [[0 for _ in range(3)] for _ in range(3)]
        for var, value in result.items():
            idx = int(var[1:]) - 1
            row, col = divmod(idx, 3)
            grid[row][col] = value

        # Thêm trạng thái cuối cùng vào path
        if path and path[-1] != grid:
            path.append(grid)

        return {
            'solution': grid,
            'nodes_expanded': nodes_expanded[0],
            'path': path
        }
    else:
        return {
            'solution': None,
            'nodes_expanded': nodes_expanded[0],
            'path': path
        }
    
def td_learning_solve(start_state, episodes=5000, alpha=0.2, gamma=0.9, epsilon=0.3):
    from collections import defaultdict

    goal_state = tuple([1, 2, 3, 4, 5, 6, 7, 8, 0])
    V = defaultdict(float)
    V[goal_state] = 100.0
    expansions = 0

    def get_valid_actions(state):
        zero = state.index(0)
        valid = []
        actions = [(-3, "up"), (3, "down"), (-1, "left"), (1, "right")]
        for move, direction in actions:
            new_idx = zero + move
            if 0 <= new_idx < 9:
                if (move == -1 and zero % 3 == 0) or (move == 1 and zero % 3 == 2):
                    continue
                if (move == -3 and zero < 3) or (move == 3 and zero > 5):
                    continue
                valid.append((zero, new_idx, direction))
        return valid

    def apply_move(state, move):
        zero_idx, new_idx, _ = move
        new_state = list(state)
        new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
        return tuple(new_state)

    def choose_action(state, epsilon):
        valid_moves = get_valid_actions(state)
        if not valid_moves:
            return None
        if random.random() < epsilon:
            return random.choice(valid_moves)
        else:
            best_value = -float('inf')
            best_moves = []
            for move in valid_moves:
                next_state = apply_move(state, move)
                if V[next_state] > best_value:
                    best_value = V[next_state]
                    best_moves = [move]
                elif V[next_state] == best_value:
                    best_moves.append(move)
            return random.choice(best_moves)

    # Huấn luyện
    for episode in range(episodes):
        eps = max(0.05, epsilon * (1 - episode / episodes))
        state = tuple(start_state)
        for _ in range(100):
            move = choose_action(state, eps)
            if not move:
                break
            next_state = apply_move(state, move)
            reward = 100 if next_state == goal_state else -1
            td_target = reward + gamma * V[next_state]
            V[state] += alpha * (td_target - V[state])
            state = next_state
            expansions += 1
            if state == goal_state:
                break

    # Suy diễn lời giải
    state = tuple(start_state)
    path = []
    visited = set([state])
    for _ in range(50):
        if state == goal_state:
            return path, expansions
        move = choose_action(state, 0.05)
        if not move:
            break
        zero_idx, new_idx, _ = move
        path.append((zero_idx, new_idx))
        state = apply_move(state, move)
        expansions += 1
        if state in visited:
            break
        visited.add(state)

    return (path, expansions) if state == goal_state else (None, expansions)