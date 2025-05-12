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
  Gồm các thuật toán duyệt không gian trạng thái mà không sử dụng heuristic:
  - **BFS** (Breadth-First Search)  
  - **DFS** (Depth-First Search)  
  - **UCS** (Uniform Cost Search)  
  - **IDDFS** (Iterative Deepening DFS)

- 🔹 **Tìm kiếm có thông tin (Informed Search)**  
  Áp dụng heuristic (Manhattan Distance) để dẫn hướng tìm kiếm:
  - **Greedy Search**  
  - **A\*** (A-Star Search)  
  - **IDA\*** (Iterative Deepening A*)

- 🔹 **Tìm kiếm cục bộ (Local Search)**  
  Tối ưu cục bộ thông qua cải tiến liên tục trạng thái:
  - **Simple Hill Climbing**  
  - **Steepest Ascent Hill Climbing**  
  - **Stochastic Hill Climbing**  
  - **Simulated Annealing**  
  - **Beam Search**  
  - **Genetic Algorithm**

- 🔹 **Tìm kiếm ràng buộc (Constraint Satisfaction Search)**  
  Giải bài toán bằng cách gán giá trị cho biến thỏa các ràng buộc:
  - **Backtracking CSP**  
  - **Constraint Checking**  
  - **AC-3** (Arc Consistency 3)

- 🔹 **Tìm kiếm trong môi trường không xác định**  
  Dành cho các bài toán mà trạng thái hoặc kết quả hành động không chắc chắn:
  - **No Observation Search**  
  - **Partial Observable Search**  
  - **AND-OR Search**

- 🔹 **Học tăng cường (Reinforcement Learning)**  
  - **Q-Learning**: Giúp tác nhân học chính sách giải bài toán 8-Puzzle thông qua trải nghiệm thử-sai và cập nhật giá trị hành động dựa trên phần thưởng nhận được.

---

### Mỗi thuật toán được hiển thị với:

- ✏️ **Cấu trúc bài toán**: Trạng thái dạng tuple 3x3, định nghĩa hành động (lên, xuống, trái, phải), điều kiện đích và chi phí di chuyển.
- 🔁 **Lộ trình giải**: Dãy bước đi từ trạng thái đầu đến trạng thái đích.
- 🎞️ **Hiệu ứng hoạt ảnh**: Mỗi bước di chuyển được mô phỏng mượt mà trên giao diện Pygame.
- 📈 **Thống kê kết quả**: Thời gian chạy, số bước thực hiện, số lượng node mở rộng.
- 💬 **Đánh giá thuật toán**: So sánh các phương pháp dựa trên tốc độ, độ chính xác và mức sử dụng bộ nhớ.

---
### 2.1. Nhóm 1: Tìm kiếm không sử dụng thông tin (Uninformed Search)

#### Mô tả bài toán
- **Trạng thái**: Đại diện dưới dạng tuple gồm 9 số nguyên từ 0 đến 8, trong đó 0 tượng trưng cho ô trống.
- **Hành động**: Di chuyển ô trống theo bốn hướng cơ bản: lên, xuống, trái, phải.
- **Điều kiện đích**: Trạng thái cần đạt là (1, 2, 3, 4, 5, 6, 7, 8, 0).
- **Chi phí hành động**: Mỗi bước di chuyển có chi phí bằng 1.
- **Đặc trưng**: Không sử dụng hàm heuristic để đánh giá, duyệt trạng thái theo cấu trúc mở rộng nhất định.

#### Các thuật toán:
- **BFS** – mở rộng đồng loạt theo tầng.
- **DFS** – đi sâu từng nhánh trước, sau đó mới quay lại.
- **UCS** – mở rộng theo tổng chi phí từ gốc.
- **IDDFS** – kết hợp DFS với tăng dần giới hạn độ sâu.

#### Minh họa
![BFS](gif/BFS.gif)  
![DFS](gif/DFS.gif)  
![UCS](gif/UCS.gif)  
![IDDFS](gif/IDDFS.gif)

#### So sánh
![Uninformed Search](img/uninformed.png)

- **Ưu điểm**:
  - BFS và UCS đảm bảo tìm được lời giải tối ưu (nếu có).
  - DFS có thể tìm lời giải nhanh nếu ở gần gốc.
  - IDDFS tiết kiệm bộ nhớ, kết hợp ưu điểm BFS và DFS.

- **Nhược điểm**:
  - BFS và UCS tốn nhiều bộ nhớ vì phải lưu toàn bộ trạng thái theo tầng.
  - DFS không đảm bảo tìm lời giải ngắn nhất, dễ rơi vào vòng lặp.
  - IDDFS chậm nếu lời giải nằm sâu, vì phải lặp lại nhiều tầng.

---

### 2.2. Nhóm 2: Tìm kiếm có thông tin (Informed Search)

#### Mô tả bài toán
- **Heuristic sử dụng**: Hàm Manhattan – tổng khoảng cách từ vị trí hiện tại đến vị trí đích của mỗi ô số.
- **Công thức đánh giá**:
  - **Greedy**: f(n) = h(n)
  - **A\***: f(n) = g(n) + h(n)
  - **IDA\***: giống A* nhưng giới hạn theo ngưỡng f(n), tiết kiệm bộ nhớ.

#### Các thuật toán:
- **Greedy Search** – mở rộng nhanh nhất theo ước lượng heuristic.
- **A\*** – cân bằng giữa chi phí thực và chi phí ước lượng.
- **IDA\*** – giống A* nhưng duyệt theo ngưỡng lặp.

#### Minh họa
![Greedy](gif/GREEDY.gif)  
![A\*](gif/A_STAR.gif)  
![IDA\*](gif/IDA_STAR.gif)

#### So sánh
![Informed Search](img/informed.png)

- **Ưu điểm**:
  - Greedy nhanh, phù hợp khi cần lời giải gấp.
  - A* tìm được đường đi tối ưu nếu heuristic chấp nhận được.
  - IDA* tiết kiệm bộ nhớ, tốt cho bài toán lớn.

- **Nhược điểm**:
  - Greedy dễ bỏ qua lời giải ngắn hơn vì chỉ theo hướng tốt hiện tại.
  - A* tốn RAM nếu đồ thị lớn.
  - IDA* có thể lặp lại nhiều trạng thái vì không lưu toàn bộ cây đã duyệt.

---

### 2.3. Nhóm 3: Tìm kiếm có ràng buộc (Constraint Satisfaction)

#### Mô tả bài toán
- **Biến**: 9 biến X1–X9 đại diện cho 9 ô.
- **Miền giá trị**: Các số từ 0 đến 8, không trùng lặp.
- **Ràng buộc**:
  - Ngang: bên phải phải lớn hơn bên trái 1 đơn vị.
  - Dọc: ô dưới lớn hơn ô trên 3 đơn vị.
  - Không trùng lặp giữa các biến.

#### Các thuật toán:
- **Backtracking CSP** – gán giá trị biến bằng quay lui truyền thống.
- **Constraint Checking** – kiểm tra tính hợp lệ từng bước khi gán.
- **AC-3** – lan truyền ràng buộc, thu hẹp miền giá trị trước khi giải.

#### Minh họa
![CSP](gif/CSP.gif)  
![AC3](gif/AC3.gif)  
![Trial and Error](gif/TRIAL.gif)

#### So sánh
![CSP Overview](img/constraint.png)

- **Ưu điểm**:
  - Backtracking đơn giản, dễ hiểu.
  - Constraint Checking cải thiện độ chính xác khi kiểm tra sớm.
  - AC-3 giảm miền hiệu quả trước khi quay lui.

- **Nhược điểm**:
  - CSP cơ bản chậm vì thử nhiều tổ hợp.
  - Constraint Checking có thể bỏ sót nếu không đầy đủ ràng buộc.
  - AC-3 phức tạp hơn, cần quản lý hàng đợi các cung ràng buộc.

---

### 2.4. Nhóm 4: Tìm kiếm cục bộ (Local Search)

#### Mô tả bài toán
- Dựa vào trạng thái hiện tại, chọn chuyển động “tốt hơn” tiếp theo.
- Không mở rộng toàn bộ cây trạng thái, chỉ cải tiến cục bộ.

#### Các thuật toán:
- **Simple Hill Climbing** – chọn trạng thái gần nhất tốt hơn.
- **Steepest-Ascent** – chọn trạng thái tốt nhất trong tất cả lân cận.
- **Stochastic Hill Climbing** – chọn ngẫu nhiên 1 lân cận tốt hơn.
- **Simulated Annealing** – đôi khi chấp nhận giải xấu để thoát cực trị cục bộ.
- **Genetic Algorithm** – tiến hóa theo quần thể, đột biến và lai ghép.
- **Beam Search** – giữ lại k trạng thái tốt nhất ở mỗi bước.

#### Minh họa
![Simple Hill](gif/SIMPLE_CLIMBING.gif)  
![Steepest](gif/STEEPEST_CLIMBING.gif)  
![Stochastic](gif/STOCHASTIC.gif)  
![SA](gif/SIMULATED.gif)  
![Genetic](gif/GENETIC.gif)  
![Beam](gif/BEAM_SEARCH.gif)

#### So sánh
![Local Search](img/local1.png)

- **Ưu điểm**:
  - Tốc độ cao, bộ nhớ thấp.
  - Phù hợp khi lời giải nằm gần trạng thái ban đầu.
  - Genetic có thể khám phá không gian rộng.

- **Nhược điểm**:
  - Dễ kẹt ở điểm tối ưu cục bộ.
  - Kết quả không đảm bảo tối ưu toàn cục.
  - Cần tinh chỉnh tham số nhiều (SA, GA).

---

### 2.5. Nhóm 5: Môi trường không xác định (Complex / Uncertain Environments)

#### Mô tả bài toán
- Trạng thái không rõ ràng, hoặc tác nhân không quan sát đầy đủ.
- Làm việc với **tập trạng thái khả dĩ (belief states)**.

#### Các thuật toán:
- **No Observation Search** – không biết trạng thái ban đầu là gì.
- **Partial Observable Search** – chỉ biết một phần trạng thái.
- **AND-OR Search** – tìm kế hoạch hành động sao cho mọi nhánh đều dẫn đến đích.

#### Minh họa
![No Obs](gif/SENSORLESS.gif)  
![Partial](gif/BELIEF_BFS.gif)  
![And-Or](gif/AND_OR.gif)

#### So sánh
![Complex](img/complex1.png)

- **Ưu điểm**:
  - Mô hình hóa được bài toán thực tế có yếu tố mơ hồ.
  - AND-OR có thể lập kế hoạch với nhiều kết quả hành động.

- **Nhược điểm**:
  - Rất tốn tài nguyên (RAM, thời gian).
  - Cần xử lý nhiều trạng thái cùng lúc, dễ bị nổ trạng thái.

---

### 2.6. Nhóm 6: Học tăng cường (Reinforcement Learning)

#### Mô tả bài toán
- Tác nhân học từ tương tác với môi trường thay vì duyệt toàn bộ không gian.
- Cập nhật chính sách hành động tối ưu theo bảng **Q-Table**.

#### Thuật toán:
- **Q-Learning** – học thông qua phần thưởng: +100 khi đến đích, -1 cho mỗi bước, và dùng công thức Q-learning để cập nhật giá trị hành động.

#### Minh họa
![Q-Learning](gif/Q_LEARNING.gif)

#### So sánh
![Q-Table](img/qlearning.png)

- **Ưu điểm**:
  - Không cần mô hình rõ ràng.
  - Có khả năng tự thích nghi nếu môi trường thay đổi.
  - Học được chính sách tối ưu qua trải nghiệm.

- **Nhược điểm**:
  - Cần nhiều lần lặp (episode) để hội tụ.
  - Phụ thuộc vào các tham số (alpha, gamma, epsilon).
  - Dễ bị lặp vô ích nếu không xử lý visited tốt.


---
## 3. 🚀 Cách chạy chương trình

```bash
# Cài đặt các thư viện cần thiết
pip install pygame

# Chạy ứng dụng
python main.py
