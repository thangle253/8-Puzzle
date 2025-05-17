# gui.py
# This module contains all GUI-related functions for the 8-puzzle problem.

import pygame
from utils import manhattan_distance
from utils import is_movable
from algorithms import  td_learning_solve, and_or_search, backtracking_csp, bfs_solve, constraint_checking_solve, dfs_solve, no_observation_search, ucs_solve, greedy_solve, iddfs_solve, astar_solve, idastar_solve, hill_climbing_solve, steepest_ascent_hill_climbing_solve, stochastic_hill_climbing_solve, simulated_annealing_solve, beam_search_solve, partial_observable_search,  ac3, genetic_algorithm_solve, q_learning_solve
from show_log_window import show_log_window
# Initialize Pygame
pygame.init()

# Constants
info = pygame.display.Info()
WIDTH = int(info.current_w * 0.99)
HEIGHT = int(info.current_h * 0.84)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Puzzle Solver")

TILE_SIZE = 110  # Giảm kích thước ô
PADDING = 30
MARGIN_TOP_INPUT = 450

# Colors
background_color = (240, 248, 255)  # Màu nền sáng hơn
board_color = (0, 102, 102)
tile_gradient_top = (102, 204, 255)
tile_gradient_bottom = (0, 153, 204)
white = (255, 255, 255)
black = (50, 50, 50)
button_color = (0, 153, 76)
button_hover_color = (0, 204, 102)
reset_color = (204, 0, 0)
reset_hover_color = (255, 51, 51)

# Fonts
tile_font = pygame.font.SysFont("arial", 60, bold=True)  # Font nhỏ hơn
button_font = pygame.font.SysFont("arial", 22, bold=True)

selected_algorithm_name = None
algorithm_results = []  # List chứa các tuple: (name, time, expansions)
editing_state = True  # default True

def draw_board(state, is_editing=True):
    # Màu nền và ô số pastel dịu mắt
    grey = (255, 250, 250)            # Nền trắng hồng kem
    tile_color = (255, 182, 193)      # Hồng pastel dễ thương
    text_color = (70, 30, 50)         # Màu chữ tím nâu nhẹ

    # Kích thước ô và font chữ phụ thuộc vào chế độ hiển thị
    size = TILE_SIZE if is_editing else int(TILE_SIZE * 2.5)
    font_size = 40 if is_editing else int(40 * 2)
    tile_font = pygame.font.SysFont('Arial', font_size, bold=True)

    board_x = PADDING
    board_y = PADDING

    # Vẽ nền toàn bộ bảng 3x3
    pygame.draw.rect(WINDOW, grey, (board_x, board_y, size * 3, size * 3))

    # Vẽ từng ô số
    for i, num in enumerate(state):
        x = (i % 3) * size + board_x
        y = (i // 3) * size + board_y

        # ✅ Chỉ vẽ ô nếu có giá trị hợp lệ
        if num not in [None, 0]:
            pygame.draw.rect(WINDOW, tile_color, (x, y, size - 2, size - 2), border_radius=10)  # Bo góc
            text = tile_font.render(str(num), True, text_color)
            text_rect = text.get_rect(center=(x + size // 2, y + size // 2))
            WINDOW.blit(text, text_rect)


# Vẽ các nút chọn thuật toán + Reset + Apply
def draw_buttons():
    grouped_buttons = [
        ("Uninformed", ["BFS", "DFS", "UCS", "IDDFS"], (100, 180, 255), (140, 210, 255)),
        ("Informed", ["Greedy", "A*", "IDA*"], (255, 178, 102), (255, 204, 153)),
        ("Local", ["Hill Climbing", "SA HC", "Stochastic HC", "Simu Annealing", "Genetic", "Beam Search"], (0, 153, 76), (0, 204, 102)),
        ("Complex", ["And-Or Search", "Partial Obser", "No Observation"], (153, 102, 255), (204, 153, 255)),
        ("Constraint", ["Backtracking", "Const Checking", "AC3"], (120, 120, 120), (160, 160, 160)),
        ("RL", ["Q-Learning","TD Learning"], (255, 220, 50), (255, 240, 100)),
        ("Action", ["Reset", "Apply", "Input", "Random","Show Log"], (204, 0, 0), (255, 51, 51))
    ]

    button_width, button_height = 200, 45
    spacing = 10
    start_x1 = WIDTH - button_width * 2 - 50
    start_x2 = start_x1 + button_width + spacing
    start_y = PADDING
    mouse_x, mouse_y = pygame.mouse.get_pos()
    current_y = start_y

    for group in grouped_buttons:
        _, buttons, base_color, hover_color = group
        for i, btn_text in enumerate(buttons):
            col = i % 2
            row = i // 2
            x = start_x1 if col == 0 else start_x2
            y = current_y + row * (button_height + spacing)

            rect = pygame.Rect(x, y, button_width, button_height)
            is_hovered = rect.collidepoint(mouse_x, mouse_y)
            current_color = hover_color if is_hovered else base_color

            if btn_text == selected_algorithm_name:
                current_color = (50, 150, 255)
                pygame.draw.rect(WINDOW, (255, 255, 255), rect, width=3, border_radius=20)

            shadow = pygame.Rect(rect.x + 2, rect.y + 2, rect.width, rect.height)
            pygame.draw.rect(WINDOW, (180, 180, 180), shadow, border_radius=20)
            pygame.draw.rect(WINDOW, current_color, rect, border_radius=20)
            pygame.draw.rect(WINDOW, white, rect, width=2, border_radius=20)

            text = button_font.render(btn_text, True, white)
            text_rect = text.get_rect(center=rect.center)
            WINDOW.blit(text, text_rect)

        # Cập nhật current_y nhưng không thêm khoảng trắng lớn giữa nhóm
        num_rows = (len(buttons) + 1) // 2
        current_y += num_rows * (button_height + spacing)

def get_clicked_button(pos):
    button_width, button_height = 200, 45
    spacing = 10
    start_x1 = WIDTH - button_width * 2 - 50
    start_x2 = start_x1 + button_width + spacing
    start_y = PADDING

    grouped_algorithms = [
        ("Uninformed", [("BFS", bfs_solve), ("DFS", dfs_solve), ("UCS", ucs_solve), ("IDDFS", iddfs_solve)]),
        ("Informed", [("Greedy", greedy_solve), ("A*", astar_solve), ("IDA*", idastar_solve)]),
        ("Local", [("Hill Climbing", hill_climbing_solve), ("SA HC", steepest_ascent_hill_climbing_solve),
                   ("Stochastic HC", stochastic_hill_climbing_solve), ("Simu Annealing", simulated_annealing_solve),
                   ("Genetic", genetic_algorithm_solve), ("Beam Search", beam_search_solve)]),
        ("Complex", [("And-Or Search", and_or_search), ("Partial Obser", partial_observable_search),
                     ("No Observation", no_observation_search)]),
        ("Constraint", [("Backtracking", backtracking_csp), ("Const Checking", constraint_checking_solve), ("AC3", ac3)]),
        ("RL", [("Q-Learning", q_learning_solve), ("TD Learning", td_learning_solve)]),
       ("Action", [("Reset", "reset"), ("Apply", "apply"), ("Input", "input"), ("Random", "random"), ("Show Log", "Show Log")])

    ]

    current_y = start_y

    for group_name, algorithms in grouped_algorithms:
        for i, (btn_text, algorithm) in enumerate(algorithms):
            col = i % 2
            row = i // 2
            x = start_x1 if col == 0 else start_x2
            y = current_y + row * (button_height + spacing)

            rect = pygame.Rect(x, y, button_width, button_height)
            if rect.collidepoint(pos):
                return algorithm, btn_text

        num_rows = (len(algorithms) + 1) // 2
        current_y += num_rows * (button_height + spacing)

    return None, None

# Vẽ ô nhập liệu
def draw_input_board(state):
    grey = (200, 200, 200)
    blue = (0, 102, 204)

    guide_font = pygame.font.SysFont("arial", 23, bold=True)
    guide_text = guide_font.render("Input initial state (click cells to change values):", True, black)
    WINDOW.blit(guide_text, (PADDING, MARGIN_TOP_INPUT - 30))

    mouse_pos = pygame.mouse.get_pos()

    # Vẽ nền bảng input
    pygame.draw.rect(WINDOW, grey, (PADDING, MARGIN_TOP_INPUT, TILE_SIZE * 3, TILE_SIZE * 3))

    for i in range(9):
        row, col = i // 3, i % 3
        x = col * TILE_SIZE + PADDING
        y = row * TILE_SIZE + MARGIN_TOP_INPUT
        tile_rect = pygame.Rect(x, y, TILE_SIZE - 2, TILE_SIZE - 2)

        pygame.draw.rect(WINDOW, blue, tile_rect)

        if tile_rect.collidepoint(mouse_pos):
            pygame.draw.rect(WINDOW, white, tile_rect, width=3)

        num = state[i]
        if num is not None and num != 0:
            text = tile_font.render(str(num), True, black)
            text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
            WINDOW.blit(text, text_rect)

# Hiển thị số bước
def draw_step_count(step_count):
    large_font = pygame.font.SysFont("arial", 50, bold=True)  # 👈 tăng size tại đây
    step_text = large_font.render(f"Steps: {step_count}", True, black)  # ✅ dùng font lớn
    step_rect = step_text.get_rect(bottomright=(WIDTH - 30, HEIGHT - 25))
    WINDOW.blit(step_text, step_rect)


# Kiểm tra click vào ô nhập liệu
def get_clicked_input_cell(pos):
    for i in range(9):
        row, col = i // 3, i % 3
        x = col * TILE_SIZE + PADDING
        y = row * TILE_SIZE + MARGIN_TOP_INPUT  # Sử dụng MARGIN_TOP_INPUT thay vì 400
        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        if rect.collidepoint(pos):
            return i
    return None

# Vẽ thanh tiến trình
def draw_progress_bar(current_step, total_steps):
    bar_width = 400
    bar_height = 50
    progress = current_step / total_steps if total_steps > 0 else 0
    progress_width = int(bar_width * progress)

    # Tính toán vị trí giữa theo chữ "Chiến Thắng"
    left_margin = 3 * TILE_SIZE + 2 * PADDING
    right_margin = WIDTH - (2 * 200 + 60)
    center_x = left_margin + (right_margin - left_margin) // 2 + 220

    x = center_x - bar_width // 2
    y = PADDING + TILE_SIZE * 3 + 430  # dưới bảng 9x9

    # Vẽ nền và khung thanh
    pygame.draw.rect(WINDOW, (180, 180, 180), (x, y, bar_width, bar_height), border_radius=12)
    pygame.draw.rect(WINDOW, (50, 200, 50), (x, y, progress_width, bar_height), border_radius=12)

    # Vẽ chữ phần trăm giữa thanh
    font = pygame.font.SysFont("arial", 26, bold=True)
    percent_text = font.render(f"{int(progress * 100)}%", True, (0, 0, 0))
    percent_rect = percent_text.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
    WINDOW.blit(percent_text, percent_rect)


# Vẽ ô với gradient
def draw_tile_with_gradient(surface, rect):
    height = rect.height
    for y in range(height):
        ratio = y / height
        color = [
            tile_gradient_top[0] + (tile_gradient_bottom[0] - tile_gradient_top[0]) * ratio,
            tile_gradient_top[1] + (tile_gradient_bottom[1] - tile_gradient_top[1]) * ratio,
            tile_gradient_top[2] + (tile_gradient_bottom[2] - tile_gradient_top[2]) * ratio
        ]
        pygame.draw.line(surface, color, (rect.x, rect.y + y), (rect.x + rect.width - 1, rect.y + y), 1)
    pygame.draw.rect(surface, (255, 255, 255), rect, width=2, border_radius=15)

def draw_and_or_state(state):
    """
    Hiển thị trạng thái hiện tại trong quá trình thực thi thuật toán AND-OR Search.
    """
    draw_board(state)
    pygame.display.flip()
    pygame.time.delay(500)  # Delay để người dùng có thể quan sát trạng thái

def draw_result_table(results):
    col_widths = [185, 130, 170, 90]
    table_width = sum(col_widths)  # để tính start_x và bảng

    table_height = 500
    row_height = 50

    # Tính toán vị trí
    left_margin = 3 * TILE_SIZE + 2 * PADDING
    right_margin = WIDTH - (2 * 200 + 60)
    start_x = left_margin + (right_margin - left_margin - table_width) // 2 + 240
    start_y = PADDING + 200

    header_font = pygame.font.SysFont("arial", 26, bold=True)
    cell_font = pygame.font.SysFont("arial", 22)

    # Vẽ bảng
    pygame.draw.rect(WINDOW, (230, 230, 230), (start_x, start_y, table_width, table_height))
    pygame.draw.rect(WINDOW, (0, 0, 0), (start_x, start_y, table_width, table_height), 2)

    headers = ["Algorithm", "Time (s)", "Expansions", "Steps"]
    for i, header in enumerate(headers):
        text = header_font.render(header, True, (0, 0, 0))
        text_rect = text.get_rect()
        if i < 2:
            text_rect.topleft = (start_x + sum(col_widths[:i]) + 10, start_y + 5)
        else:
            text_rect.centerx = start_x + sum(col_widths[:i]) + col_widths[i] // 2
            text_rect.y = start_y + 5
        WINDOW.blit(text, text_rect)

    for idx, (algo_name, time_taken, expansions, steps) in enumerate(results):
        y = start_y + (idx + 1) * row_height + 5
        values = [algo_name, f"{time_taken:.4f}", str(expansions), str(steps)]
        for j, val in enumerate(values):
            text = cell_font.render(val, True, (0, 0, 0))
            text_rect = text.get_rect()
            if j < 2:
                text_rect.topleft = (start_x + sum(col_widths[:j]) + 10, y)
            else:
                text_rect.centerx = start_x + sum(col_widths[:j]) + col_widths[j] // 2
                text_rect.y = y
            WINDOW.blit(text, text_rect)

def draw_title_and_footer():
    title_font = pygame.font.SysFont("arial", 68, bold=True)
    footer_font = pygame.font.SysFont("arial", 64, bold=True)

    title_text = title_font.render("8 - Puzzle Solver", True, (30, 30, 120))
    footer_text = footer_font.render("Chiến Thắng", True, (0, 150, 0))

    table_width = 430
    left_margin = 3 * TILE_SIZE + 2 * PADDING
    right_margin = WIDTH - (2 * 200 + 60)
    center_x = left_margin + (right_margin - left_margin) // 2 + 230

    title_rect = title_text.get_rect(center=(center_x, PADDING + 25))
    footer_rect = footer_text.get_rect(center=(center_x, PADDING + 110))  # 👈 tăng từ 50 → 80

    WINDOW.blit(title_text, title_rect)
    WINDOW.blit(footer_text, footer_rect)

