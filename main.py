# main.py
# Entry point for the 8-puzzle solver application.

import random
from utils import generate_fixed_puzzle
import pygame
from collections import deque
from gui import WINDOW, draw_title_and_footer,  draw_board, draw_buttons, draw_step_count, draw_input_board, draw_progress_bar, get_clicked_button, get_clicked_input_cell, algorithm_results, draw_result_table
from algorithms import ac3, and_or_search, bfs_solve, constraint_checking_solve, create_consistent_state, create_constraints, dfs_solve, find_solution_path, perform_ac3_with_solution, ucs_solve, greedy_solve, iddfs_solve, astar_solve, idastar_solve, hill_climbing_solve, steepest_ascent_hill_climbing_solve, stochastic_hill_climbing_solve, simulated_annealing_solve, beam_search_solve,partial_observable_search, no_observation_search
from algorithms import backtracking_csp, ac3_solve, genetic_algorithm_solve, q_learning_solve
import time
import gui  # 👈 Thêm dòng này để truy cập gui.editing_state

# Initialize Pygame
pygame.init()

clock = pygame.time.Clock()
white = (255, 255, 255)

# Helper: Trích hành động từ cây kế hoạch AND-OR
def extract_moves_from_plan(plan):
    path = []
    while isinstance(plan, dict):
        action = next(iter(plan))
        path.append(action)
        plan = plan[action][0]  # lấy nhánh đầu tiên của AND-node
    return path if plan == 'GOAL' else None

# Helper: Chuyển tên hành động (UP, DOWN,...) thành các bước di chuyển chỉ số
def convert_moves_to_indices(start_state, move_names):
    state = start_state[:]
    solution = []
    move_map = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

    for move in move_names:
        zero_idx = state.index(0)
        new_idx = zero_idx + move_map[move]
        if 0 <= new_idx < 9 and (
            (move in ['LEFT', 'RIGHT'] and zero_idx // 3 == new_idx // 3) or
            (move in ['UP', 'DOWN'])
        ):
            state[zero_idx], state[new_idx] = state[new_idx], state[zero_idx]
            solution.append((zero_idx, new_idx))
        else:
            break  # Nếu move không hợp lệ thì dừng
    return solution
def update_input_cell(state, index):
    current = state[index]
    used = set(val for i, val in enumerate(state) if i != index and val is not None)

    # Nếu ô đang trống hoặc là 0 thì bắt đầu từ 1
    start = 1 if current is None or current == 0 else current + 1

    for val in range(start, 9):
        if val not in used:
            state[index] = val
            return

    # Nếu không còn số nào sau đó, thử từ đầu (1 → hiện tại)
    for val in range(1, start):
        if val not in used:
            state[index] = val
            return

    # Nếu đủ 1-8 rồi thì gán 0
    state[index] = 0


# Main Function
def main():
    original_state = generate_fixed_puzzle()    
    input_state = [None] * 9
    editing_state = True
    start_state = original_state[:]

    running = True
    solving = False
    solution = []
    step = 0
    selected_algorithm = None
    selected_algorithm_name = None
    step_count = 0
    ac3_data = None

    while running:
        WINDOW.fill(white)
        draw_board(start_state, editing_state)
        draw_buttons()
        draw_step_count(step_count)
        draw_title_and_footer()  
        draw_result_table(algorithm_results)
        if editing_state:
            draw_input_board(input_state)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if editing_state:
                    clicked_cell = get_clicked_input_cell(event.pos)
                    if clicked_cell is not None:
                        if event.button == 3:  # Chuột phải → giảm
                            if input_state[clicked_cell] is None or input_state[clicked_cell] == 0:
                                input_state[clicked_cell] = 8
                            else:
                                input_state[clicked_cell] = (input_state[clicked_cell] - 1) % 9
                        elif event.button == 1:  # Chuột trái → tăng không trùng
                            update_input_cell(input_state, clicked_cell)

                selected_algorithm, selected_algorithm_name = get_clicked_button(event.pos)
                if selected_algorithm:
                    if selected_algorithm == "reset":
                        start_state = original_state[:]
                        solving = False
                        step = 0
                        step_count = 0
                        selected_algorithm_name = None
                        editing_state = True
                        input_state = [None] * 9
                    
                    elif selected_algorithm == "random":
                        nums = list(range(9))
                        random.shuffle(nums)
                        input_state = nums
                        print(f"Random in›put: {input_state}")
                    elif selected_algorithm == "Input":
                        editing_state = True
                        gui.editing_state = True  # ✅ đảm bảo GUI cập nhật
                        selected_algorithm_name = None
                        step = 0
                        step_count = 0
                        solving = False
                        print("📝 Đã quay lại chế độ nhập.")
                    elif selected_algorithm == "apply":
                        if selected_algorithm_name == "Backtracking":
                            result = backtracking_csp()

                            if result and result["solution"]:
                                # Start with an empty board
                                start_state = [0] * 9
                                solution_path = result["path"]
                                solving = True
                                step = 0
                                step_count = 0
                                expansions = result["nodes_expanded"]
                                elapsed = 0.001
                                algorithm_results.append(("Backtracking", elapsed, expansions))

                                print(f"Đã sinh trạng thái hợp lệ bằng CSP. Đã mở rộng {expansions} node.")

                                # Animate the solution path step by step
                                for state in solution_path:
                                    if isinstance(state, list) and len(state) == 3:
                                        start_state = [num for row in state for num in row]
                                        if 0 not in start_state:
                                            start_state.append(0)  # Safeguard to ensure 0 is present
                                        draw_board(start_state, editing_state)
                                        pygame.display.flip()
                                        pygame.time.delay(500)  # Delay for animation

                                # Display the final solution
                                if result["solution"]:
                                    start_state = [num for row in result["solution"] for num in row]
                                    if 0 not in start_state:
                                        start_state.append(0)  # Safeguard to ensure 0 is present
                                    draw_board(start_state, editing_state)
                                    pygame.display.flip()
                            else:
                                print("Không thể sinh trạng thái hợp lệ bằng Backtracking CSP.")
                            # Removed the return statement to prevent premature exit
                            solving = False  # Ensure solving is set to False if no solution is found

                        # Xử lý các thuật toán còn lại
                        # Tự động điền nếu còn thiếu đúng 1 số
                        filled = [x for x in input_state if x is not None]
                        if len(filled) == 8:
                            missing = list(set(range(9)) - set(filled))[0]
                            for i in range(9):
                                if input_state[i] is None:
                                    input_state[i] = missing
                                    print(f"⚠️ Ô trống thứ {i} được tự động gán là: {missing}")
                                    break

                        # Kiểm tra trạng thái hợp lệ
                        if all(x is None for x in input_state):
                            # Nếu chưa nhập gì thì bỏ qua nhập, dùng trạng thái gốc
                            start_state = original_state[:]
                            editing_state = False
                            gui.editing_state = False
                            print("📌 Không nhập gì. Dùng trạng thái gốc và chuyển sang chế độ giải.")
                        elif None not in input_state and sorted(input_state) == list(range(9)):
                            # Nhập hợp lệ
                            start_state = input_state[:]
                            original_state = input_state[:]
                            editing_state = False
                            gui.editing_state = False
                            print(f"✅ Trạng thái hợp lệ: {start_state}")
                        else:
                            print("❌ Trạng thái không hợp lệ. Vui lòng nhập đủ số từ 0 đến 8.")

                    elif callable(selected_algorithm):
                        if selected_algorithm_name == "Backtracking":
                            # Run Backtracking directly without requiring input state validation
                            result = backtracking_csp()

                            if result and result["solution"]:
                                # Start with an empty board
                                start_state = [0] * 9
                                solution_path = result["path"]
                                solving = True
                                step = 0
                                step_count = 0
                                expansions = result["nodes_expanded"]
                                elapsed = 0.001
                                algorithm_results.append(("Backtracking", elapsed, expansions))

                                print(f"Đã sinh trạng thái hợp lệ bằng CSP. Đã mở rộng {expansions} node.")

                                # Animate the solution path step by step
                                for state in solution_path:
                                    if isinstance(state, list) and len(state) == 3:
                                        start_state = [num for row in state for num in row]
                                        if 0 not in start_state:
                                            start_state.append(0)  # Safeguard to ensure 0 is present
                                        draw_board(start_state, editing_state)
                                        pygame.display.flip()
                                        pygame.time.delay(500)  # Delay for animation

                                # Display the final solution
                                if result["solution"]:
                                    start_state = [num for row in result["solution"] for num in row]
                                    if 0 not in start_state:
                                        start_state.append(0)  # Safeguard to ensure 0 is present
                                    draw_board(start_state, editing_state)
                                    pygame.display.flip()
                            else:
                                print("Không thể sinh trạng thái hợp lệ bằng Backtracking CSP.")
                            # Removed the return statement to prevent premature exit
                            solving = False  # Ensure solving is set to False if no solution is found
                        elif selected_algorithm_name == "Genetic Algo":
                            solving = True
                            solution = genetic_algorithm_solve(start_state)
                            step = 0
                            if solution:
                                algorithm_results.append(("Genetic", 0.001, len(solution)))
                            if solution is None:
                                solving = False
                                selected_algorithm_name += " (No Solution)"
                                print(f"Không tìm thấy giải pháp cho trạng thái: {start_state}")
                        elif selected_algorithm_name == "Q-Learning":
                            solving = True
                            print("Đang chạy thuật toán Q-Learning...")
                            # Giới hạn số tập huấn luyện để không mất quá nhiều thời gian
                            solution = q_learning_solve(start_state, episodes=5000, alpha=0.1, gamma=0.9, epsilon=0.2)
                            step = 0
                            if solution:
                                algorithm_results.append(("Q-Learning", 0.001, len(solution)))
                            if solution is None:
                                solving = False
                                selected_algorithm_name += " (No Solution)"
                                print(f"Không tìm thấy giải pháp cho trạng thái: {start_state}")
    
                        elif selected_algorithm_name == "Const Checking":
                            solving = True
                            result = constraint_checking_solve()
                            if result and result['solution']:
                                solution_path = result['path']
                                algorithm_results.append(("Const Checking", 0.001, result["nodes_expanded"]))
                                step = 0
                                step_count = 0

                                # Animate the solution path step by step
                                for state in solution_path:
                                    start_state[:] = [val for row in state for val in row]
                                    draw_board(start_state, editing_state)
                                    pygame.display.flip()
                                    pygame.time.delay(500)  # Delay to visualize each step

                                print(f"Solution found after expanding {result['nodes_expanded']} nodes!")
                            else:
                                print("No solution found using Constraint Checking.")
                            solving = False
                        elif selected_algorithm_name == "And-Or Search":
                            solving = True
                            print("Đang chạy thuật toán And-Or Tree Search...")
                            belief_states = [tuple(start_state)]
                            plan = and_or_search(belief_states, max_depth=30)

                            if plan:
                                print("Đã tìm được cây kế hoạch:")
                                print(plan)

                                move_names = extract_moves_from_plan(plan)
                                if move_names:
                                    print("Chuỗi hành động:", move_names)
                                    solution = convert_moves_to_indices(start_state, move_names)
                                    step = 0
                                else:
                                    solving = False
                                    print("Không thể trích xuất được hành động từ cây kế hoạch.")
                            else:
                                solving = False
                                selected_algorithm_name += " (No Solution)"
                                print("Không tìm được lời giải với thuật toán And-Or.")
                        elif selected_algorithm_name == "No Observation Search":
                            solving = True
                            print("🔍 Đang chạy thuật toán No Observation Search...")
                            solution = no_observation_search(start_state)
                            step = 0
                            if solution is None:
                                solving = False
                                selected_algorithm_name += " (No Solution)"
                                print("❌ Không tìm được lời giải với No Observation Search.")
                            else:
                                print(f"✅ Đã tìm thấy chuỗi hành động ({len(solution)} bước):")
                                print(solution)
                        
                        elif selected_algorithm_name == "Partial Obser":
                            solving = True
                            print("🔍 Đang chạy thuật toán Partial Observable Search...")

                            start_set = {tuple(start_state)}
                            goal_set = {tuple([1, 2, 3, 4, 5, 6, 7, 8, 0])}
                            solution, expansions = partial_observable_search(start_set, goal_set)
                            elapsed = 0.001  # nếu bạn không đo thời gian cụ thể
                            algorithm_results.append(("Partial Obser", elapsed, expansions))
                            step = 0

                            if solution is None:
                                solving = False
                                selected_algorithm_name += " (No Solution)"
                                print("❌ Không tìm được lời giải với Partial Observable Search.")
                            else:
                                print(f"✅ Đã tìm thấy chuỗi hành động ({len(solution)} bước):")
                                print("👉", solution)
                                print(f"🧠 Số lượng belief mở rộng: {expansions}")

                                # 🛠️ Chuyển danh sách hành động thành step tuple: (zero_idx, new_idx)
                                temp_state = start_state[:]
                                action_to_move = {
                                    'up': -3,
                                    'down': 3,
                                    'left': -1,
                                    'right': 1
                                }
                                real_steps = []
                                for action in solution:
                                    zero_idx = temp_state.index(0)
                                    move = action_to_move[action]
                                    new_idx = zero_idx + move
                                    temp_state[zero_idx], temp_state[new_idx] = temp_state[new_idx], temp_state[zero_idx]
                                    real_steps.append((zero_idx, new_idx))
                                solution = real_steps  # Gán lại cho đúng định dạng GUI đang cần


                        elif selected_algorithm_name == "AC3":
                            solving = True
                            print("Running AC3 algorithm to create and solve a valid 8-puzzle state...")
                            
                            # Khởi tạo bảng trống khi sử dụng AC3
                            empty_state = [None] * 9  # Board trống không có số
                            start_state = empty_state[:]  # Cập nhật bảng chính thành trạng thái trống
                            draw_board(start_state, editing_state)  # Hiển thị bảng trống
                            pygame.display.flip()
                            pygame.time.delay(500)  # Delay để hiển thị bảng trống trước khi bắt đầu thuật toán
                            
                            # Run AC3 directly without requiring input state validation
                            result = ac3_solve()
                           
                            if result and result["solution"]:
                                # Bắt đầu với bảng trống
                                solution_path = result["path"]
                                solving = True
                                step = 0
                                step_count = 0
                                expansions = result["nodes_expanded"]
                                elapsed = 0.001
                                algorithm_results.append(("AC-3", elapsed, expansions))
                                print(f"Generated valid state using AC3. Expanded {expansions} nodes.")

                                # Animate the solution path step by step
                                for state in solution_path:
                                    if isinstance(state, list) and len(state) == 3:
                                        start_state = [num for row in state for num in row]
                                        if 0 not in start_state:
                                            start_state.append(0)  # Safeguard to ensure 0 is present
                                        draw_board(start_state, editing_state)
                                        pygame.display.flip()
                                        pygame.time.delay(500)  # Delay for animation

                                # Display the final solution
                                if result["solution"]:
                                    start_state = [num for row in result["solution"] for num in row]
                                    if 0 not in start_state:
                                        start_state.append(0)  # Safeguard to ensure 0 is present
                                    draw_board(start_state, editing_state)
                                    pygame.display.flip()
                            else:
                                print("Could not generate valid state using AC3 algorithm.")
                            solving = False  # Ensure solving is set to False after processing
                        else:
                            solving = True
                            step = 0
                            step_count = 0
                            start = time.time()
                            solution = selected_algorithm(start_state)
                            elapsed = time.time() - start
                            expansions = len(solution) if solution else 0
                            algorithm_results.append((selected_algorithm_name, elapsed, expansions))

                            if solution is None:
                                solving = False
                                selected_algorithm_name += " (No Solution)"
                                print(f"Không tìm thấy giải pháp cho trạng thái: {start_state}")



        if solving and solution:
            draw_progress_bar(step, len(solution))
            if step < len(solution):
                # Ensure solution[step] is a tuple of two values
                if isinstance(solution[step], tuple) and len(solution[step]) == 2:
                    zero_idx, move_idx = solution[step]
                    start_state[zero_idx], start_state[move_idx] = start_state[move_idx], start_state[zero_idx]
                    step += 1
                    step_count += 1
                    pygame.display.flip()
                    pygame.time.delay(200)
                else:
                    print("Invalid step format in solution. Expected a tuple of two values.")
                    solving = False
            else:
                solving = False

        if ac3_data and ac3_data['auto_running']:
            current_time = pygame.time.get_ticks()
            # Giảm tần suất cập nhật để giảm hiện tượng giật
            if current_time - ac3_data['last_update_time'] > 500:  # Update mỗi 500ms
                ac3_data['last_update_time'] = current_time

                # Kiểm tra trạng thái hội tụ - nếu không có thay đổi trong domains trong vài bước
                if 'previous_domains' in ac3_data:
                    # So sánh domains hiện tại với domains trước đó
                    current_domains_str = str(ac3_data['csp']['domains'])
                    if current_domains_str == ac3_data['previous_domains']:
                        ac3_data['unchanged_count'] += 1
                    else:
                        ac3_data['unchanged_count'] = 0
                        ac3_data['previous_domains'] = current_domains_str

                    # Nếu domains không thay đổi sau 5 lần kiểm tra liên tiếp, kết thúc thuật toán
                    if ac3_data['unchanged_count'] >= 5:
                        print("Thuật toán AC3 đã hội tụ - không có sự thay đổi sau nhiều bước.")
                        # Kết thúc thuật toán và hiển thị kết quả
                        ac3_data['queue'].clear()  # Xóa queue để kết thúc thuật toán
                        
                        # Hiển thị kết quả cuối cùng và dừng vòng lặp
                        print(f"AC3 đã hoàn thành. Số cung đã xử lý: {ac3_data['counter'][0]}")
                        # Tạo trạng thái kết quả từ domains đã được thu hẹp
                        final_state = [ac3_data['csp']['domains'][f"X{i+1}"][0] for i in range(9)]
                        print(f"Final state: {final_state}")
                        
                        # Áp dụng trạng thái cuối cùng
                        start_state[:] = final_state
                        # Vẽ trạng thái cuối cùng
                        draw_board(start_state, editing_state)
                        pygame.display.flip()
                        pygame.time.delay(1000)  # Dừng lâu hơn để người dùng xem trạng thái cuối
                        print("AC3 đã tìm được giải pháp hợp lệ!")
                        
                        # Kết thúc AC3
                        ac3_data['auto_running'] = False
                        solving = False
                        continue  # Bỏ qua phần còn lại của vòng lặp
                else:
                    # Khởi tạo biến theo dõi sự hội tụ lần đầu
                    ac3_data['previous_domains'] = str(ac3_data['csp']['domains'])
                    ac3_data['unchanged_count'] = 0
                
                # Tạo hàm callback để vẽ trạng thái hiện tại
                def draw_board_callback(state):
                    # Kiểm tra xem state có hợp lệ không
                    if state and len(state) == 9 and None not in state:
                        # Kiểm tra xem mỗi giá trị từ 0-8 xuất hiện đúng một lần
                        if sorted(state) == list(range(9)):
                            print(f"Displaying state: {state}")
                            # Đảm bảo state được sao chép sang start_state
                            for i in range(9):
                            # Vẽ trạng thái mới
                                draw_board(start_state, editing_state)
                            pygame.display.flip()
                            # Dừng một chút để người dùng có thể nhìn thấy thay đổi
                            pygame.time.delay(50)
                
                # Chỉ thực hiện một bước AC3 nếu vẫn chưa hội tụ và queue không rỗng
                if ac3_data['auto_running'] and ac3_data['queue']:
                    result = ac3(ac3_data['csp'], ac3_data['counter'], draw_board_callback, ac3_data['queue'])
                    ac3_data['step'] += 1
                    
                    # Nếu queue rỗng hoặc thuật toán thất bại
                    if not ac3_data['queue'] or not result:
                        if result:
                            print(f"AC3 đã hoàn thành. Số cung đã xử lý: {ac3_data['counter'][0]}")
                            # Tạo trạng thái kết quả từ domains đã được thu hẹp
                            final_state = [ac3_data['csp']['domains'][f"X{i+1}"][0] for i in range(9)]
                            print(f"Final state: {final_state}")
                            
                            # Kiểm tra xem kết quả có hợp lệ không
                            if 0 in final_state and len(set(final_state)) == 9:
                                # Áp dụng trạng thái cuối cùng
                                start_state[:] = final_state
                                # Vẽ trạng thái cuối cùng
                                draw_board(start_state, editing_state)
                                pygame.display.flip()
                                pygame.time.delay(1000)  # Dừng lâu hơn để người dùng xem trạng thái cuối
                                print("AC3 đã tìm được giải pháp hợp lệ!")
                            else:
                                print("Lỗi: Trạng thái kết quả không hợp lệ")
                                # Hiển thị lại trạng thái ban đầu
                                start_state[:] = ac3_data['initial_state']
                        else:
                            print("AC3 không tìm được giải pháp hợp lệ.")
                            # Khôi phục trạng thái ban đầu
                            start_state[:] = ac3_data['initial_state']
                        
                        # Vẽ lại board sau khi đã cập nhật start_state
                        draw_board(start_state, editing_state)
                        pygame.display.flip()
                        
                        # Kết thúc AC3
                        ac3_data['auto_running'] = False
                        solving = False

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()

