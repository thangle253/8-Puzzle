import pygame
import sys
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

def show_log_window(log_lines):
    pygame.init()

    # Cấu hình cửa sổ
    window_width = 500
    window_height = 700
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("📝 Solution Log Viewer")

    # Fonts
    regular_font = pygame.font.SysFont("Courier New", 24)
    bold_font = pygame.font.SysFont("Courier New", 24, bold=True)

    line_height = regular_font.get_height()
    scroll_offset = 0
    dragging = False
    drag_start_y = 0
    start_offset = 0

    # Tính chiều cao toàn bộ nội dung
    content_height = len(log_lines) * (line_height + 5)
    max_scroll = max(0, content_height - window_height + 40)

    running = True
    while running:
        screen.fill((255, 255, 255))  # Nền trắng

        y = 20 - scroll_offset

        # Tô nền khối thông tin đầu tiên (4 dòng)
        if len(log_lines) >= 4:
            block_height = 4 * (line_height + 5)
            pygame.draw.rect(screen, (240, 245, 255), (30, y - 5, window_width - 60, block_height + 10))
            pygame.draw.rect(screen, (180, 210, 255), (30, y - 5, window_width - 60, block_height + 10), 1)

        for idx, line in enumerate(log_lines):
            # Định dạng màu và font
            if idx < 4:
                font = regular_font
                color = (0, 102, 204)
            elif line.startswith("Bước"):
                font = bold_font
                color = (102, 0, 153)
            else:
                font = regular_font
                color = (0, 0, 0)

            text = font.render(line, True, color)
            screen.blit(text, (40, y))
            y += line_height + 5

        # Vẽ thanh cuộn nếu cần
        if content_height > window_height:
            scroll_bar_height = max(40, window_height * window_height // content_height)
            scroll_bar_y = scroll_offset * (window_height - scroll_bar_height) // max_scroll
            pygame.draw.rect(screen, (230, 230, 230), (window_width - 20, 0, 12, window_height))
            pygame.draw.rect(screen, (100, 100, 100), (window_width - 20, scroll_bar_y, 12, scroll_bar_height))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_DOWN:
                    scroll_offset = min(scroll_offset + 40, max_scroll)
                elif event.key == pygame.K_UP:
                    scroll_offset = max(scroll_offset - 40, 0)
            elif event.type == pygame.MOUSEWHEEL:
                scroll_offset = max(0, min(scroll_offset - event.y * 30, max_scroll))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if content_height > window_height:
                    scroll_bar_y = scroll_offset * (window_height - scroll_bar_height) // max_scroll
                    scrollbar_rect = pygame.Rect(window_width - 20, scroll_bar_y, 12, scroll_bar_height)
                    if scrollbar_rect.collidepoint(event.pos):
                        dragging = True
                        drag_start_y = event.pos[1]
                        start_offset = scroll_offset
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                dy = event.pos[1] - drag_start_y
                delta_scroll = dy * max_scroll // (window_height - scroll_bar_height)
                scroll_offset = max(0, min(start_offset + delta_scroll, max_scroll))

    pygame.quit()
