# 🧩 8-Puzzle Visualizer – Trình mô phỏng giải thuật AI với Pygame

## 1. 🎯 Mục đích dự án

Dự án **8-Puzzle Visualizer** được phát triển nhằm:

- 🔍 **Ứng dụng các thuật toán AI đã học**  
  Thực hiện và kiểm thử nhiều thuật toán tìm kiếm khác nhau trong bài toán xếp ô 8-puzzle, bao gồm từ các thuật toán cơ bản như BFS, DFS cho đến nâng cao như A*, IDA*, Hill Climbing, Beam Search, Genetic Algorithm và Q-Learning.

- 🎮 **Xây dựng giao diện mô phỏng bằng Pygame**  
  Giao diện đồ họa sử dụng thư viện Pygame, trực quan sinh động. Người dùng có thể nhập trạng thái khởi đầu, chọn thuật toán từ các nút tương tác, xem quá trình giải từng bước với hiệu ứng, và theo dõi các chỉ số như số bước, số nút mở rộng và thời gian xử lý.

- 📊 **So sánh hiệu năng thuật toán**  
  Hệ thống thống kê thời gian chạy, số bước di chuyển và số lượng node được mở rộng giúp người dùng đánh giá hiệu quả từng thuật toán trong việc tìm lời giải.

- 🎓 **Tăng cường khả năng học tập**  
  Hỗ trợ sinh viên hiểu rõ cách hoạt động bên trong của từng thuật toán thông qua trực quan hóa, từ đó củng cố kiến thức lý thuyết và cải thiện kỹ năng lập trình giải thuật.

---

## 2. 📌 Nội dung tổng quan

Dự án giải quyết bài toán **8 ô số (8-Puzzle)** – một bài toán cổ điển trong AI, yêu cầu đưa các ô số về đúng vị trí bằng cách di chuyển ô trống. Hệ thống tích hợp **6 nhóm giải thuật chính**:

- 🔹 **Tìm kiếm không sử dụng thông tin (Uninformed Search)**  
  Ví dụ: BFS, DFS, UCS, IDDFS – không dùng heuristic, duyệt toàn bộ không gian trạng thái.

- 🔹 **Tìm kiếm có thông tin (Informed Search)**  
  Ví dụ: A*, IDA*, Greedy – sử dụng hàm heuristic như Manhattan để định hướng tìm kiếm.

- 🔹 **Tìm kiếm cục bộ (Local Search)**  
  Bao gồm: Simple Hill Climbing, Steepest Ascent, Stochastic Hill Climbing, Simulated Annealing, Beam Search – cải thiện lời giải dần theo hướng giảm heuristic.

- 🔹 **Tìm kiếm ràng buộc (Constraint Satisfaction)**  
  Triển khai các phương pháp như Backtracking CSP, AC-3 để gán giá trị cho biến mà vẫn tuân thủ ràng buộc.

- 🔹 **Tìm kiếm trong môi trường không hoàn hảo**  
  Gồm các kỹ thuật như No Observation, Partial Observable Search, AND-OR Search – xử lý khi trạng thái không xác định rõ ràng.

- 🔹 **Học tăng cường (Reinforcement Learning)**  
  Q-Learning được triển khai để Pacman học từ trải nghiệm và dần hình thành chính sách tối ưu.

---

### Mỗi thuật toán được hiển thị với:

- ✏️ **Cấu trúc bài toán**: Trạng thái dạng tuple 3x3, định nghĩa hành động (lên, xuống, trái, phải), điều kiện đích và chi phí di chuyển.
- 🔁 **Lộ trình giải**: Dãy bước đi từ trạng thái đầu đến trạng thái đích.
- 🎞️ **Hiệu ứng hoạt hình**: Mỗi bước di chuyển được mô phỏng mượt mà trên giao diện Pygame.
- 📈 **Thống kê kết quả**: Thời gian chạy, số bước thực hiện, số lượng node mở rộng.
- 💬 **Đánh giá thuật toán**: So sánh các phương pháp dựa trên tốc độ, độ chính xác và mức sử dụng bộ nhớ.

---

## 3. 🚀 Cách chạy chương trình

```bash
# Cài đặt các thư viện cần thiết
pip install pygame

# Chạy ứng dụng
python main.py
