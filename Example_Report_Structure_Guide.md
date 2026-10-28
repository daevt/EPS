---
document_type: report_structure_and_writing_specification
language: vi
source_file: Example_Report.pdf
source_title: Course Management System - Final Report
source_course: System Design - IT3120E
source_date: 2024-12-18
analysis_date: 2026-10-21
source_pdf_pages: 163
source_sha256: df48a93fb761c2dc6affd9ce6777f4ab3297302248ddc0cf9738e9706097c3cc
structure_mode: strict_with_domain_adaptation
normalized_nonfunctional_section: "3.5"
source_nonfunctional_section: "3.4 (trùng số với Sequence Diagram)"
---

# Hướng dẫn AI viết report bám sát Example_Report.pdf

## A. Mục đích, cách sử dụng và độ tin cậy

Tài liệu này phân tích **kết cấu báo cáo mẫu**, xác định **mục tiêu, đầu ra, giới hạn và điều kiện hoàn thành của từng phần**, để AI dùng làm đặc tả khi soạn report sau này. Đây không phải bản tóm tắt nghiệp vụ Course Management System và không phải đề bài hoặc thang chấm chính thức của giảng viên.

AI cần đọc tài liệu này trước khi lập dàn ý hoặc viết report. Giữ khung chương và các nhóm đầu ra; thay nghiệp vụ, vai trò, use case, lớp, bảng và màn hình theo đề tài thực tế. **Không sao chép tên Course Management System, Student, Instructor hoặc các chức năng giáo dục sang đề tài khác nếu không có căn cứ.**

### A.1. Phân biệt ba loại thông tin

| Loại | Ý nghĩa | Cách AI sử dụng |
|---|---|---|
| **Quan sát từ mẫu** | Nội dung, tiêu đề, hình thức hoặc số lượng được thấy trong PDF | Dùng để nhận diện cấu trúc; không tự biến mọi chi tiết của đề tài mẫu thành yêu cầu của đề tài mới |
| **Quy tắc bám mẫu** | Quy tắc viết được xác lập để thực hiện yêu cầu giữ kết cấu | Áp dụng mặc định cho report mới, trừ khi người dùng hoặc đề bài yêu cầu khác |
| **Kiểm soát chất lượng** | Cách tránh thiếu sót, mâu thuẫn hoặc lỗi của mẫu | Thực hiện trong quá trình soạn và rà soát; không tự tạo thêm chương trong report |

Thứ tự ưu tiên: **yêu cầu trực tiếp của người dùng và đề bài thực tế > quy tắc bám mẫu trong tài liệu này > chi tiết minh họa của Course Management System**. Nếu cần đổi cấu trúc do yêu cầu mới, ghi rõ thay đổi; không âm thầm đổi dàn ý.

### A.2. Cơ sở kiểm chứng và giới hạn đọc nguồn

- Nguồn phân tích duy nhất là `Example_Report.pdf` trong thư mục dự án. Không dùng các PDF khác để suy ra yêu cầu của mẫu.
- Đã trích xuất nội dung, kiểm tra ảnh tổng quan của toàn bộ 163 trang và xem phóng lớn các trang đại diện cho sơ đồ, kiến trúc, dữ liệu, screen flow và tài liệu tham khảo.
- Bản PDF được cung cấp thiếu phần kết thúc và bảng chỉ mục cuối file. Đã dựng lại chỉ mục trong bộ nhớ để đọc cây 163 trang và các đối tượng nội dung còn có; **không sửa file gốc**.
- Một đối tượng font cuối file chưa đầy đủ; font phục vụ phần References không đọc/hiển thị chính xác. Vì vậy xác nhận được vị trí và hình thức danh mục tham khảo, nhưng **không coi nội dung thư mục của từng tài liệu là đã kiểm chứng hoàn toàn**.
- Mọi số trang dưới đây là **số thứ tự trang PDF, bắt đầu từ 1**, không phải số trang do AI tự gán. Một số mục bắt đầu cuối trang; hình tương ứng nằm trang tiếp theo. Mục lục cũng có một số vị trí chưa cập nhật.
- Mục tiêu và tiêu chí hoàn thành là diễn giải chức năng của từng phần để AI thực hiện được; PDF không cung cấp rubric chính thức hay giới hạn từ bắt buộc.

## B. Quy tắc bắt buộc để giữ kết cấu và giới hạn phạm vi

1. Giữ thứ tự: **Cover -> Table of Contents -> Introduction -> Planning -> Analysis -> Design -> Conclusion and Future Work -> References**.
2. Giữ **5 chương nội dung chính**. References đứng riêng, không đánh số thành chương 6.
3. Không tự thêm Abstract, Acknowledgements, Literature Review, Implementation, Testing, Deployment, Business Model, Risk Management hoặc Appendix thành phần độc lập. Chỉ thêm khi đề bài hoặc người dùng yêu cầu; nếu chỉ cần giải thích ngắn, đặt vào tiểu mục phù hợp có sẵn.
4. Giữ các nhóm tiểu mục cố định trong dàn ý ở phần D. Các mục lặp theo actor, lớp, bảng và màn hình được thay theo đề tài; không ép số lượng của mẫu.
5. Analysis phải đi theo chuỗi: **use case tổng quan -> đặc tả use case -> activity -> sequence -> yêu cầu phi chức năng**. Không thay chuỗi này bằng một danh sách tính năng chung.
6. Design phải đi theo chuỗi: **kiến trúc/package -> đặc tả lớp -> lưu trữ dữ liệu -> giao diện/prototype/specification/screen flow**.
7. Mặc định giữ tổ chức **MVC: Model, View, Controller** và ba nhóm đặc tả lớp tương ứng. Nếu đề tài được yêu cầu dùng kiến trúc khác, giải thích cách ánh xạ vào mục 4.1 và 4.2; không tự thay kiến trúc chỉ vì sở thích của AI.
8. Khóa danh sách chức năng thuộc phạm vi hiện tại ở 2.4.1. Các chương 3 và 4 phải triển khai danh sách này. Ý tưởng chưa nằm trong phạm vi chỉ được ghi ở 5.2, hoặc đánh dấu là yêu cầu cần xác nhận trước khi đưa vào phạm vi.
9. Duy trì mã use case, actor, tên lớp, tên phương thức, tên bảng và tên màn hình nhất quán xuyên suốt. Không sao chép lỗi mã và tham chiếu của mẫu.
10. Không bịa chi phí, tiến độ, tải hệ thống, nguồn khảo sát, nguồn luật, kết quả kiểm thử hoặc trạng thái triển khai. Dữ liệu thiếu phải đánh dấu rõ theo phần M.
11. Không tuyên bố đã xây dựng, chạy thử hoặc kiểm thử thành công nếu đầu vào chỉ chứng minh hoạt động phân tích và thiết kế.
12. Không cố kéo report đến đúng 163 trang. **Giữ cấu trúc và mức độ chi tiết tương ứng với phạm vi**, không giữ số trang bằng cách chèn khoảng trắng, tăng cỡ chữ hoặc tạo thêm thực thể không cần thiết.

## C. Bản đồ cấu trúc và trọng tâm của mẫu

| Khối | Vị trí trong PDF | Vai trò | Đặc điểm cần giữ |
|---|---|---|---|
| Cover | 1 | Nhận diện báo cáo và nhóm | Thông tin học phần, đề tài, người hướng dẫn, thành viên, ngày |
| Table of Contents | 2-5 | Cho thấy toàn bộ hệ thống tiêu đề | Mục lục nhiều cấp, có số trang, bao gồm các lớp và màn hình |
| 1. Introduction | 6-7 | Xác định vấn đề và hướng giải quyết | Hai mục: Problem Definition, Proposed Solution |
| 2. Planning | 7-14 | Chứng minh lý do, giá trị, tính khả thi và kế hoạch | Motivation; System Request; 5 loại feasibility; Project Plan |
| 3. Analysis | 14-69 | Làm rõ hệ thống phải thực hiện những gì | Use case, bảng đặc tả, activity, sequence, NFR |
| 4. Design | 69-161 | Chỉ rõ cấu trúc giải pháp và cách hiện thực ở mức thiết kế | MVC, lớp chi tiết, dữ liệu, giao diện |
| 5. Conclusion and Future Work | 161-163 | Đánh giá kết quả và hướng phát triển | Conclusion trước, Future Work sau |
| References | 163 | Ghi nguồn | Tiêu đề riêng sau chương 5 |

Các khoảng trang giao nhau vì các chương hoặc tiểu mục nối tiếp trên cùng một trang. Không cộng trực tiếp các khoảng này để tính tổng độ dài.

### C.1. Số lượng quan sát được, không phải chỉ tiêu bắt buộc

| Thành phần | Số lượng trong mẫu | Diễn giải |
|---|---:|---|
| Actor trong phần giải thích sơ đồ tổng quan | 4 | User, Instructor, Student, Email System; Admin còn xuất hiện ở luồng chi tiết nhưng chưa được giải thích nhất quán |
| Use case được đặc tả | 22 | 6 User + 7 Instructor + 9 Student |
| Activity diagram | 22 | Theo các use case trên, từ trang 32 đến 52 |
| Sequence diagram | 21 | 6 User + 6 Instructor + 9 Student; không có sequence riêng cho I1 Manage Courses |
| Hình kiến trúc/package chi tiết | 4 | 1 hình MVC tổng quát + 3 hình theo package |
| Lớp trong đặc tả 4.2 | 61 | 15 Model + 30 View + 16 Control/Controller |
| Bảng trong danh mục tổng quan dữ liệu | 18 | Danh mục ở trang 130-132 |
| Bảng được đặc tả chi tiết | 20 | Có thêm Study Group và StudentAndGroup; danh mục tổng quan chưa khớp |
| Nhóm giao diện được liệt kê | 14 | Mỗi nhóm có mục prototype và specification tương ứng |
| Ảnh prototype | 16 | Nhiều hơn số nhóm giao diện vì Update Information có nhiều trạng thái/ảnh |
| Screen flow | 2 | Student và Instructor |

**Kết luận về trọng tâm:** đây là report phân tích và thiết kế hệ thống, có phần đặc tả rất lớn. Chương 4.2 và bộ sơ đồ ở chương 3 chiếm phần lớn tài liệu. Bản viết mới không đạt mức tương đương nếu chỉ có mô tả ý tưởng và vài hình tổng quát.

## D. Dàn ý chuẩn để AI sử dụng

Giữ tên tiếng Anh sau đây nếu chưa có yêu cầu đổi ngôn ngữ report. Hướng dẫn giải thích bằng tiếng Việt không có nghĩa report đầu ra bắt buộc viết tiếng Việt.

```text
Cover
Table of Contents

1. Introduction
   1.1. Problem Definition
   1.2. Proposed Solution

2. Planning
   2.1. Motivation
   2.2. Initial System Request
       2.2.1. Business Need
       2.2.2. Business Requirements
       2.2.3. Business Value
       2.2.4. Special Issues or Constraints
   2.3. Feasibility Analysis
       2.3.1. Technical Feasibility
       2.3.2. Operational Feasibility
       2.3.3. Economic Feasibility
       2.3.4. Legal & Regulatory Feasibility
       2.3.5. Market Feasibility
   2.4. Initial Project Plan
       [Đoạn mô tả phương pháp phát triển và lý do lựa chọn]
       2.4.1. Project Scope Estimation
       2.4.2. Staffing Plan
       2.4.3. CASE Tools

3. Analysis
   3.1. General Use cases Diagram
   3.2. Use case Details
       3.2.1. [Actor/group 1]'s Use cases Details
       3.2.2. [Actor/group 2]'s Use cases Details
       3.2.n. [Actor/group n]'s Use cases Details
   3.3. Activity Diagram
       3.3.1. [Actor/group 1]'s Use cases
       3.3.2. [Actor/group 2]'s Use cases
       3.3.n. [Actor/group n]'s Use cases
   3.4. Sequence Diagram
       3.4.1. [Actor/group 1]'s Use cases
       3.4.2. [Actor/group 2]'s Use cases
       3.4.n. [Actor/group n]'s Use cases
   3.5. Non-functional Requirements

4. Design
   4.1. Architecture Design
       4.1.1. Package Diagram
       4.1.2. Detailed Package Diagram
           4.1.2.1. Model Package
           4.1.2.2. View Package
           4.1.2.3. Controller Package
   4.2. Class Specification Design
       4.2.1. Model Package
           4.2.1.i. Class [M_ClassName]
       4.2.2. View Package
           4.2.2.i. Class [V_ClassName]
       4.2.3. Control Package
           4.2.3.i. Class [C_ClassName]
   4.3. Data Storage Design
       4.3.1. Overview
       4.3.2. Detailed Data Storage Design
           [Table 1]
           [Table 2]
           [Table n]
   4.4. User Interface Design
       4.4.1. Interface prototype
           4.4.1.i. [Screen/flow name]
       4.4.2. Interface specification
           4.4.2.i. [Cùng Screen/flow name ở 4.4.1.i]
       4.4.3. Screen Flow
           [Luồng màn hình theo từng vai trò chính]

5. Conclusion and Future Work
   5.1. Conclusion
   5.2. Future Work

References
```

**Hiệu chỉnh số mục:** mẫu đánh số cả Sequence Diagram và Non-functional Requirements là `3.4`. Bản chuẩn dùng `3.5` cho NFR để có định danh duy nhất, đồng thời giữ nguyên vị trí và nội dung của phần này. Đây là sửa lỗi đánh số, không phải thêm mục.

`i` và `n` chỉ là ký hiệu hướng dẫn trong tài liệu này. Khi viết report phải thay bằng số mục thực tế, không để nguyên ký hiệu.

## E. Phần đầu và chương 1: xác định báo cáo và vấn đề

### E.1. Cover - trang 1

**Mục tiêu:** người đọc xác định được đây là báo cáo nào, thuộc học phần nào, ai chịu trách nhiệm và được lập vào thời điểm nào.

**Cấu trúc quan sát từ trên xuống:** tên trường -> đơn vị/khoa -> logo -> `Final Report` -> tên hệ thống -> Course -> Class Code -> Supervisor -> Group Members -> địa điểm và ngày.

**Đầu ra cần có:** bìa có tên đề tài, thông tin học phần/lớp, người hướng dẫn; bảng thành viên gồm họ tên, mã sinh viên và email nếu dữ liệu thực tế có cung cấp.

**Giới hạn:** không đưa tóm tắt nội dung, tính năng hoặc phần quảng bá lên bìa. Không tái sử dụng danh tính, mã sinh viên, email, logo hoặc ngày của nhóm mẫu cho nhóm mới.

**Đạt khi:** toàn bộ thông tin nhận diện nhất quán với report; dữ liệu chưa có được nêu rõ trong bản nháp.

### E.2. Table of Contents - trang 2-5

**Mục tiêu:** thể hiện được toàn bộ hệ thống tiêu đề, kể cả các đặc tả lớp và màn hình ở cấp sâu.

**Đầu ra cần có:** mục lục nhiều cấp, số mục và số trang cập nhật theo bản xuất cuối. Trong mẫu, danh mục lớp đi đến cấp `4.2.x.y`; danh mục giao diện đi đến cấp `4.4.x.y`.

**Giới hạn:** không tự thêm List of Figures hoặc List of Tables thành phần mới nếu chưa có yêu cầu. Không giữ số trang lấy từ mẫu sau khi thay nội dung.

**Đạt khi:** từng mục trong mục lục có tiêu đề tương ứng trong thân bài; không trùng số, thiếu mục hoặc chỉ sai trang do cập nhật chưa hoàn tất.

### E.3. 1.1. Problem Definition - trang 6

**Mục tiêu:** làm rõ vấn đề hiện tại và hậu quả khiến việc xây dựng hệ thống trở nên cần thiết.

**Nội dung cần đạt theo trình tự:**

1. Bối cảnh và đối tượng đang tham gia quy trình hiện tại.
2. Cách làm hiện tại hoặc hệ thống hiện tại.
3. Các điểm nghẽn cụ thể, ví dụ nhập liệu lặp, thao tác thủ công, thông tin phân tán, phản hồi chậm.
4. Hậu quả đối với từng bên liên quan.
5. Nhu cầu cải thiện và thách thức chính mà giải pháp phải xử lý.

**Dạng trình bày:** các đoạn văn liên kết; mẫu dùng khoảng một trang rồi chuyển sang giải pháp.

**Giới hạn:** không biến thành khảo cứu dài, không trình bày UML, lược đồ dữ liệu, danh sách API hoặc chi tiết công nghệ. Không đưa số liệu về hiện trạng nếu chưa có nguồn.

**Đạt khi:** mỗi vấn đề có chủ thể chịu tác động và tạo được căn cứ cho ít nhất một khả năng của giải pháp ở 1.2.

### E.4. 1.2. Proposed Solution - trang 6-7

**Mục tiêu:** trả lời hệ thống đề xuất sẽ giải quyết những nhóm vấn đề nào và đem lại kết quả gì.

**Đầu ra cần có:** một đoạn giới thiệu giải pháp; danh sách các nhóm khả năng chính, mỗi nhóm có một câu về công dụng; đoạn kết nối lại với vấn đề.

**Quan sát từ mẫu:** các nhóm khả năng gồm quản lý khóa học, cộng tác, phân tích, dự đoán, sự kiện và phản hồi. Đây là nội dung của đề tài mẫu, không phải danh sách chức năng bắt buộc của mọi report.

**Giới hạn:** chỉ mô tả ở mức chức năng/giá trị; chưa liệt kê từng bước use case và chưa chọn cấu trúc lớp. Không hứa tính năng sẽ không xuất hiện trong phạm vi và thiết kế phía sau.

**Đạt khi:** giải pháp có liên hệ trực tiếp với 1.1 và không vượt danh mục phạm vi sẽ khóa ở 2.4.1.

## F. Chương 2: Planning

### F.1. 2.1. Motivation - trang 7

**Mục tiêu:** giải thích vì sao nhóm lựa chọn đề tài này và vì sao cần thực hiện vào bối cảnh đang xét.

**Đầu ra cần có:** nhu cầu từ người dùng/tổ chức, khoảng trống của cách tiếp cận hiện tại, giá trị mà nhóm kỳ vọng và lý do hướng giải quyết phù hợp.

**Giới hạn:** không chép lại toàn bộ 1.1. Problem Definition mô tả vấn đề; Motivation tập trung vào động lực chọn và đầu tư cho đề tài. Không biến thành câu chuyện cá nhân dài hoặc bài giới thiệu công nghệ.

**Đạt khi:** người đọc hiểu lý do chọn đề tài và mức ưu tiên của các nhu cầu.

### F.2. 2.2. Initial System Request - trang 8-9

**Mục tiêu chung:** chuyển ý tưởng thành yêu cầu khởi tạo dự án, trước khi đặc tả hành vi chi tiết.

| Tiểu mục | Mục tiêu | Nội dung/đầu ra cần có | Giới hạn và điều kiện đạt |
|---|---|---|---|
| **2.2.1. Business Need** | Xác định nhu cầu tổ chức/nghiệp vụ | Bên có nhu cầu; vấn đề kinh doanh/vận hành; kết quả mong muốn | Không kể từng thao tác màn hình. Đạt khi nhu cầu đủ rõ để đánh giá giải pháp có đáp ứng hay không |
| **2.2.2. Business Requirements** | Liệt kê các khả năng hệ thống phải cung cấp | Danh sách yêu cầu chức năng cấp cao, theo nhóm nghiệp vụ và vai trò | Không thay bằng bảng trường dữ liệu hoặc công nghệ. Đạt khi từng yêu cầu có thể truy vết sang use case hoặc được ghi rõ ngoài phạm vi |
| **2.2.3. Business Value** | Nêu lợi ích nếu đáp ứng các yêu cầu | Hiệu quả vận hành, giảm lỗi/công sức, trải nghiệm, khả năng quản lý hoặc giá trị khác phù hợp đề tài | Phân biệt lợi ích định tính và mục tiêu định lượng; không tự tạo ROI hay tỷ lệ tăng trưởng. Đạt khi mỗi giá trị gắn với nhu cầu/yêu cầu cụ thể |
| **2.2.4. Special Issues or Constraints** | Ghi các điều kiện giới hạn thiết kế | Tài nguyên, thời gian, tích hợp, khả năng mở rộng, an toàn dữ liệu, khả dụng, tiếp cận hoặc các ràng buộc thực tế khác | Đây là danh sách ràng buộc đầu vào; đặc tả đo lường chi tiết đặt ở NFR. Đạt khi ràng buộc ảnh hưởng được đến lựa chọn/ưu tiên trong kế hoạch và thiết kế |

### F.3. 2.3. Feasibility Analysis - trang 9-11

**Mục tiêu chung:** đánh giá khả năng thực hiện trong điều kiện cụ thể, bao gồm điểm thuận lợi, trở ngại và cách xử lý. Không chỉ khẳng định “khả thi”.

| Tiểu mục | Nội dung quan sát từ mẫu | Mục tiêu và đầu ra cho report mới | Giới hạn |
|---|---|---|---|
| **2.3.1. Technical Feasibility** | Công nghệ sẵn có; hiểu biết nghiệp vụ/công nghệ của nhóm; hạ tầng; bảo mật; quy mô; thời gian; tương thích trình duyệt | Xác định công nghệ ứng viên, năng lực thực tế, tích hợp cần có, rủi ro kỹ thuật và biện pháp đáp ứng | Không biến thành tài liệu cài đặt. Không chốt hạ tầng/công nghệ ngoài đầu vào mà không ghi giả định |
| **2.3.2. Operational Feasibility** | Dễ sử dụng; bảo trì; nhân lực vận hành | Chỉ rõ ai sử dụng, ai quản trị, đào tạo/hỗ trợ ra sao và tổ chức có thể tiếp nhận hệ thống thế nào | Không lặp lại bảng chức năng; không giả định có sẵn đội vận hành hoặc người dùng chấp thuận |
| **2.3.3. Economic Feasibility** | Chi phí phát triển; chi phí định kỳ; nguồn thu/tiết kiệm; ROI và hòa vốn | Lập cơ sở chi phí/lợi ích; nêu đơn vị tiền, kỳ tính và giả định; kết luận có điều kiện | Không sao chép ngân sách của mẫu. Nếu chưa có dữ liệu, nêu mô hình ước lượng và dữ liệu cần bổ sung; không bịa số |
| **2.3.4. Legal & Regulatory Feasibility** | Quy định liên quan, quyền riêng tư, sở hữu trí tuệ, hợp đồng/dịch vụ bên thứ ba | Nhận diện nhóm nghĩa vụ phù hợp loại hệ thống và phạm vi áp dụng; nguồn cần kiểm chứng | Các viện dẫn trong report năm 2024 không tự chứng minh tình trạng pháp lý hiện hành. Không sao chép quy định giáo dục hoặc GDPR sang mọi đề tài |
| **2.3.5. Market Feasibility** | Nhu cầu; đối thủ/giải pháp hiện có; lợi thế của giải pháp bản địa hóa | Chỉ rõ nhóm người dùng đích, giải pháp thay thế, mức phù hợp và khác biệt có căn cứ | Không biến thành kế hoạch marketing; không tuyên bố dẫn đầu thị trường khi chưa có bằng chứng |

**Đạt khi:** cả năm góc nhìn đều có đánh giá gắn với hoàn cảnh của dự án; các giả định quan trọng, hạn chế và kết luận khả thi được nêu rõ. Bản mẫu thiên về diễn giải định tính; việc thêm một câu kết luận cho mỗi góc nhìn là kiểm soát chất lượng, không phải một mục mới.

### F.4. 2.4. Initial Project Plan - trang 12-14

**Phần mở đầu ngay dưới 2.4:** nêu phương pháp phát triển và lý do phù hợp. Mẫu lựa chọn Agile, giải thích tính lặp, phản hồi liên tục, phối hợp với bên liên quan và giảm rủi ro.

**Mục tiêu:** cho thấy một cách tổ chức công việc có thể thực hiện được. Không bắt buộc dùng Agile nếu đề bài hoặc điều kiện dự án chỉ ra lựa chọn khác.

| Tiểu mục | Mục tiêu | Đầu ra cần có | Giới hạn/đạt khi |
|---|---|---|---|
| **2.4.1. Project Scope Estimation** - trang 13 | Khóa phạm vi và ước lượng thời gian | Hai nhóm như mẫu: `Scope Size` và `Time Estimate`; chức năng trong phạm vi; giới hạn phạm vi; các giai đoạn/sprint và thời lượng | Không nhồi thêm tính năng vì có trong mẫu. Tổng thời lượng phải khớp các giai đoạn và 2.3.1. Đạt khi phân biệt được phần sẽ thiết kế và phần để tương lai |
| **2.4.2. Staffing Plan** - trang 13-14 | Giao trách nhiệm thực hiện | Phân công theo giai đoạn: planning, design, development, testing/deployment nếu dự án thực sự có; người/vai trò phụ trách và công việc cụ thể | Không tái dùng tên thành viên mẫu. Nếu chỉ làm thiết kế, không diễn đạt như đã phát triển và triển khai. Đạt khi mỗi nhóm công việc có chủ thể chịu trách nhiệm |
| **2.4.3. CASE Tools** - trang 14 | Xác định công cụ hỗ trợ kỹ nghệ phần mềm | Công cụ cho UML, dữ liệu và quản lý công việc; công dụng của từng công cụ | Không liệt kê công cụ chỉ để tăng độ dài; không trình bày hướng dẫn cài đặt. Đạt khi công cụ gắn với đầu ra cần tạo |

**Lưu ý thời gian của nguồn:** 2.3.1 nêu 6-9 tháng, trong khi 2.4.1 nêu 6-8 sprint hai tuần, tổng 12-16 tuần. Lịch chi tiết ở 2.4.1 cũng cần đối soát phép cộng. Không dùng các con số này làm kế hoạch mặc định.

## G. Chương 3: Analysis

### G.1. 3.1. General Use cases Diagram - trang 14-16

**Mục tiêu:** mô tả phạm vi hành vi của hệ thống và ai tương tác với hệ thống, ở mức tổng quan.

**Đầu ra cần có:**

- Một sơ đồ use case tổng quan có tên/ranh giới hệ thống, actor và các use case chính.
- Quan hệ actor-use case; include/extend/generalization chỉ sử dụng khi có ý nghĩa nghiệp vụ tương ứng.
- Đoạn giải thích sau hình về vai trò của từng actor, quyền hạn và tác nhân/hệ thống ngoài.
- Mã use case ổn định để dùng trong 3.2, 3.3 và 3.4.

**Quan sát từ mẫu:** hình nằm trang 15; phần giải thích nêu User, Instructor, Student và Email System. Các nhóm đặc tả sau đó tổ chức theo User, Instructor, Student.

**Giới hạn:** không thay bằng sơ đồ kiến trúc hoặc sơ đồ cơ sở dữ liệu. Không đưa lớp nội bộ làm actor. Không sao chép máy móc quan hệ include/extend của mẫu vì có tham chiếu sai.

**Đạt khi:** actor xuất hiện trong các luồng chi tiết đều được biểu diễn hoặc giải thích ở tổng quan; chức năng trong phạm vi có use case tương ứng.

### G.2. 3.2. Use case Details - trang 16-31

**Mục tiêu:** biến mỗi use case thành một hợp đồng hành vi: ai khởi tạo, điều kiện nào cho phép chạy, hệ thống phản ứng thế nào và kết thúc ở trạng thái nào.

**Tổ chức:** nhóm theo actor/vai trò chính, cùng thứ tự ở phần Activity Diagram và Sequence Diagram. Bản mẫu có `3.2.1 User`, `3.2.2 Instructor`, `3.2.3 Student`.

#### G.2.1. Khuôn đặc tả bắt buộc khi bám mẫu

Mỗi use case có dòng tên `CODE: Use case name`, tiếp theo là bảng:

| Trường | Mục tiêu/nội dung phải ghi |
|---|---|
| **Use case code** | Mã duy nhất; không dùng một mã cho hai chức năng |
| **Use case name** | Tên hành động nhất quán với sơ đồ tổng quan |
| **Actor** | Vai trò khởi tạo/chính; tác nhân hỗ trợ xuất hiện rõ trong luồng nếu có |
| **Usage** | Mục tiêu nghiệp vụ hoặc khả năng use case cung cấp |
| **Activation Event** | Sự kiện hoặc thao tác khởi động |
| **Preconditions** | Trạng thái/quyền/dữ liệu cần tồn tại trước bước đầu |
| **Main Event Flow** | Bảng ba cột: `Index`, `Done by`, `Action` |
| **Postconditions** | Trạng thái hệ thống/dữ liệu và kết quả quan sát được khi hoàn thành |

**Luồng xử lý:** mỗi bước chỉ rõ người dùng, hệ thống hoặc hệ thống ngoài thực hiện. Bước hệ thống phải mô tả kiểm tra/xử lý/kết quả cụ thể, không chỉ ghi “process”. Có nhánh thì ghi điều kiện và kết quả cho từng nhánh.

**Giới hạn:** mẫu không có mục Alternative Flow/Exception Flow độc lập cho tất cả use case. Mặc định mô tả các nhánh cần thiết ngay trong Main Event Flow hoặc ghi chú đi kèm; không tự làm phát sinh một cấu trúc biểu mẫu khác. Không đưa câu SQL hoặc chi tiết cài đặt vào bảng.

**Đạt khi:** có thể dựng activity và sequence từ đặc tả; precondition, trigger, bước xử lý và postcondition tương thích; không để Postconditions rỗng như S4 của mẫu.

#### G.2.2. Danh mục use case của nguồn và mục tiêu từng use case

Bảng dưới phục vụ kiểm chứng mẫu và nhận diện mức chia nhỏ chức năng. Đây không phải danh mục áp đặt cho một đề tài khác. Cột Activity/Sequence ghi **trang chứa hình**, có thể khác trang chứa dòng tiêu đề trong mục lục.

| Nhóm/mục | Mã và tên use case | Mục tiêu nghiệp vụ trong mẫu | Trang đặc tả | Activity | Sequence |
|---|---|---|---|---:|---:|
| 3.2.1 User | U1 Register | Tạo và kích hoạt tài khoản qua xác nhận email | 16-17 | 32 | 53 |
| 3.2.1 User | U2 Log in | Xác thực và vào dashboard theo vai trò | 17 | 33 | 54 |
| 3.2.1 User | U3 Log out | Kết thúc phiên và chuyển về màn hình đăng nhập | 18 | 34 | 55 |
| 3.2.1 User | U4 Update profile information | Cập nhật thông tin cá nhân hợp lệ | 18-19 | 35 | 56 |
| 3.2.1 User | U5 Reset Password | Đặt lại mật khẩu qua email/token/code | 19-20 | 36 | 57 |
| 3.2.1 User | U6 Messenger | Truy cập chức năng trao đổi tin nhắn | 20 | 37 | 57 |
| 3.2.2 Instructor | I1 Manage Courses | Điều hướng quản lý và các thao tác tạo/sửa/xóa khóa học | 20-21 | 38 | Không có hình riêng |
| 3.2.2 Instructor | I2 Create a Course | Tạo khóa học mới | 21 | 39 | 58 |
| 3.2.2 Instructor | I3 Delete a Course | Xóa khóa học khi điều kiện ghi danh cho phép | 21-22 | 40 | 58 |
| 3.2.2 Instructor | I4 Update Course Content | Chỉnh sửa bài học, tài liệu và nội dung khóa học | 22-23 | 41 | 59 |
| 3.2.2 Instructor | I5 Track Students' Progress | Xem tiến độ/kết quả học viên và báo cáo | 23 | 42 | 59 |
| 3.2.2 Instructor | I6 Give Feedback | Ghi phản hồi/điểm cho bài nộp | 23-24 | 43 | 60 |
| 3.2.2 Instructor | I7 Create online events | Tạo sự kiện và xử lý chấp thuận theo luồng mô tả | 24-25 | 44 | 60 |
| 3.2.3 Student | S1 Enroll in a Course | Ghi danh và cập nhật trạng thái khóa học của sinh viên | 25-26 | 45 | 61 |
| 3.2.3 Student | S2 Unenroll from a Course | Rút khỏi khóa học và cập nhật trạng thái | 26 | 46 | 61 |
| 3.2.3 Student | S3 Search for a Course | Tìm khóa học theo truy vấn | 26-27 | 46 | 62 |
| 3.2.3 Student | S4 View Self Progress | Xem tiến độ cá nhân trong khóa học | 27 | 47 | 63 |
| 3.2.3 Student | S5 View and Download Certificate | Xem/tải chứng nhận đã được cấp | 28 | 47 | 64 |
| 3.2.3 Student | S6 Do Quiz/Assignment | Làm quiz hoặc nộp bài và cập nhật tiến độ | 28-29 | 49 | 65 |
| 3.2.3 Student | S7 Peer Reviews | Nhận xét bài của sinh viên khác | 29-30 | 50 | 66 |
| 3.2.3 Student | S8 Access Content | Truy cập và tương tác nội dung học tập | 30 | 51 | 67 |
| 3.2.3 Student | S9 Create Study Groups | Tạo nhóm học tập | 30-31 | 52 | 68 |

### G.3. 3.3. Activity Diagram - tiêu đề trang 31; hình trang 32-52

**Mục tiêu:** biểu diễn tiến trình thực hiện use case, phân công hành động và các nhánh nghiệp vụ.

**Cấu trúc quan sát:** `3.3.1 User`, `3.3.2 Instructor`, `3.3.3 Student`; mỗi use case có mã và tên trước hình. Các hình thường có tên quy trình, ghi chú precondition/postcondition và swimlane Actor/System.

**Đầu ra cần có:** activity cho từng use case cần mô tả; nút bắt đầu/kết thúc; hành động; hướng chuyển; nhánh quyết định có điều kiện; swimlane khi cần phân biệt trách nhiệm.

**Giới hạn:** mô tả luồng công việc, chưa phải lời gọi phương thức giữa lớp. Không dùng ký hiệu song song chỉ để trang trí hoặc biểu diễn các bước thực chất tuần tự. Không thêm nhánh nghiệp vụ không có ở đặc tả.

**Đạt khi:** các đường đi chính và nhánh quan trọng thống nhất với 3.2, kết thúc đúng postcondition, và không có hành động không rõ chủ thể. Có thể gom nhiều hình nhỏ trên một trang nhưng không bỏ hình để khớp số trang mẫu.

### G.4. 3.4. Sequence Diagram - tiêu đề trang 52; hình trang 53-68

**Mục tiêu:** mô tả tương tác theo thời gian để thực hiện use case, kết nối Analysis với các lớp thiết kế.

**Cấu trúc quan sát:** `3.4.1 User`, `3.4.2 Instructor`, `3.4.3 Student`. Hình sử dụng actor, đối tượng giao diện/boundary, controller/control, đối tượng dữ liệu/entity, lifeline, thông điệp và activation; một số hình có create/destroy.

**Đầu ra cần có:** mã use case; các đối tượng tham gia; lời gọi/thông điệp theo thứ tự; tham số hoặc dữ liệu quan trọng; kết quả/phản hồi; nhánh lỗi/điều kiện khi tác động đến hành vi.

**Giới hạn:** không thay bằng activity diagram thứ hai. Không cần tạo/destroy đối tượng chỉ để giống hình mẫu. Không để một phương thức xuất hiện trên sequence mà hoàn toàn không được giải thích trong thiết kế lớp.

**Đạt khi:** các bước đặc tả được giải thích bằng tương tác hợp lý; đối tượng ánh xạ được về 4.1/4.2; tên phương thức nhất quán. Use case tổng hợp như I1 có thể dẫn tới các sequence thành phần I2-I4, nhưng phải ghi rõ cách bao phủ; không im lặng bỏ sót.

### G.5. 3.5. Non-functional Requirements - trang 68-69

**Tên trong nguồn:** `3.4 Non-functional Requirements`; dùng số chuẩn `3.5` trong report mới.

**Mục tiêu:** xác định các điều kiện chất lượng mà thiết kế phải đáp ứng, bên cạnh chức năng.

| Nhóm phải giữ theo mẫu | Mục tiêu | Nội dung/đầu ra |
|---|---|---|
| **Performance Requirements** | Giới hạn về tải và thời gian phản hồi | Tải người dùng/giao dịch, thời gian phản hồi, điều kiện đo và phạm vi áp dụng |
| **Operational Requirements** | Điều kiện vận hành và môi trường sử dụng | Khả dụng, bảo trì, nền tảng hỗ trợ, tích hợp hệ thống ngoài |
| **Security Requirements** | Bảo vệ tài khoản, quyền và dữ liệu | Xác thực, phân quyền, bảo vệ thông tin khi lưu/truyền và các điều kiện liên quan nghiệp vụ |
| **Cultural and Political Requirements** | Sự phù hợp với ngôn ngữ, tiếp cận và bối cảnh áp dụng | Bản địa hóa, nhu cầu tiếp cận, các nghĩa vụ/quy định phù hợp có nguồn |

**Quan sát số liệu mẫu:** 5.000 người dùng đồng thời; thời gian tải không quá 2 giây cho 95% yêu cầu trong điều kiện bình thường; vận hành 24/7 với tối đa 1 giờ bảo trì/tháng. Đây là mục tiêu được report mẫu nêu, **không phải kết quả kiểm thử và không phải mặc định cho dự án mới**.

**Giới hạn:** không sao chép chỉ tiêu khi chưa xác định tải thực tế. Không coi tên nhóm cuối cùng là căn cứ để bàn luận chính trị ngoài nhu cầu thiết kế. Không thêm chương kiểm thử chỉ để giải thích cách đo.

**Đạt khi:** các yêu cầu đủ cụ thể để kiểm chứng hoặc được đánh dấu cần xác nhận; thiết kế có quyết định đáp ứng tương ứng; không mâu thuẫn với thời gian, nguồn lực và công nghệ.

## H. Chương 4.1 và 4.2: kiến trúc và đặc tả lớp

### H.1. 4.1. Architecture Design - trang 69-74

**Mục tiêu:** tổ chức hệ thống thành các nhóm trách nhiệm, làm cơ sở cho sequence và đặc tả lớp.

| Tiểu mục | Vị trí | Đầu ra cần có | Điều kiện đạt và giới hạn |
|---|---|---|---|
| **4.1.1. Package Diagram** | Tiêu đề 69; hình 70; giải thích 70-71 | Sơ đồ tổng quan MVC; mô tả trách nhiệm Model, View, Controller và hướng phụ thuộc/tương tác | Không chỉ chèn một hình MVC chung mà không giải thích ánh xạ vào hệ thống; không thay bằng sơ đồ triển khai |
| **4.1.2. Detailed Package Diagram** | 71-74 | Bộ sơ đồ chi tiết cho từng package | Là bước mở rộng của 4.1.1, không phải một kiến trúc khác |
| **4.1.2.1. Model Package** | Tiêu đề 71; hình 72 | Các lớp nghiệp vụ/dữ liệu, thuộc tính/phương thức chính và quan hệ liên quan | Tên lớp khớp 4.2.1; quan hệ có nghĩa; không mặc định mỗi lớp phải thành một bảng |
| **4.1.2.2. View Package** | 73 | Các lớp giao diện, form, thành phần hiển thị/tương tác | Khớp 4.2.2 và giao diện ở 4.4; không đưa toàn bộ xử lý nghiệp vụ vào View |
| **4.1.2.3. Controller Package** | 74 | Các lớp điều phối yêu cầu và tương tác nghiệp vụ | Khớp 4.2.3 và sequence; tránh trùng trách nhiệm không giải thích |

Mẫu dùng tên `Controller Package` ở 4.1.2.3 và `Control Package` ở 4.2.3. Có thể giữ cách viết của mẫu hoặc chuẩn hóa cả hai thành `Controller Package`; phải dùng nhất quán và vẫn giữ đủ ba nhóm.

### H.2. 4.2. Class Specification Design - trang 74-129

**Mục tiêu:** đặc tả từng lớp đủ để hiểu trạng thái, trách nhiệm, giao diện phương thức và quan hệ với các lớp khác.

**Tổ chức bắt buộc khi bám mẫu:** `4.2.1 Model Package -> 4.2.2 View Package -> 4.2.3 Control Package`; mỗi lớp là một mục con có số thứ tự.

#### H.2.1. Khuôn cho mỗi lớp

```text
4.2.[package].[index]. Class [ClassName]
Description: [Trách nhiệm ngắn, cụ thể của lớp]

Attributes:
| Attribute | Datatype | Accessibility | Description |

Methods:
| Method | Input | Output | Accessibility | Description |
```

**Yêu cầu từng thành phần:**

- Description giải thích lý do tồn tại của lớp và đối tượng/thao tác lớp quản lý.
- Attribute ghi đúng tên, kiểu dữ liệu, phạm vi truy cập và ý nghĩa; không thay kiểu bằng một mô tả mơ hồ.
- Method ghi tên/chữ ký đủ rõ; Input nêu tham số/kiểu hoặc `None`; Output nêu kiểu/kết quả hoặc `void`/`None`; Accessibility nêu phạm vi; Description giải thích hành vi.
- Phương thức trên sequence phải tìm thấy được trong đặc tả của lớp sở hữu hoặc được giải thích qua ánh xạ rõ ràng.
- Kiểu định danh và ý nghĩa dữ liệu phải phù hợp với các đối tượng liên quan và thiết kế lưu trữ. Kiểu đối tượng trong lớp và kiểu lưu trữ có thể khác nếu giải thích được cách ánh xạ.

**Giới hạn:** không thay bảng đặc tả bằng mã nguồn; không tự thêm lớp để đạt đúng 61 lớp; không tạo hàng loạt lớp chỉ đổi tên nhưng lặp nguyên Description/Attributes/Methods.

**Đạt khi:** mọi lớp được đưa vào bộ thiết kế đều có trách nhiệm rõ; các thuộc tính/phương thức sử dụng trong sơ đồ được giải thích; không có lớp hoặc phương thức mâu thuẫn giữa các phần.

#### H.2.2. 4.2.1. Model Package - 15 lớp trong mẫu

Trang là nơi bắt đầu mục lớp trong thân bài, không luôn trùng trang ghi trong mục lục.

| Mục | Lớp | Trang | Trách nhiệm/mục tiêu đặc tả |
|---|---|---:|---|
| 4.2.1.1 | M_User | 74 | Thông tin và trạng thái tài khoản, thao tác liên quan người dùng |
| 4.2.1.2 | M_Student | 76 | Thông tin/hành vi riêng của sinh viên; kế thừa M_User |
| 4.2.1.3 | M_Instructor | 78 | Thông tin/hành vi riêng của giảng viên; kế thừa M_User |
| 4.2.1.4 | M_Lesson | 79 | Nội dung và cấu trúc bài học |
| 4.2.1.5 | M_Module | 80 | Tổ chức module và các bài học |
| 4.2.1.6 | M_Course | 81 | Thông tin khóa học và nội dung liên quan |
| 4.2.1.7 | M_Assignment | 82 | Thông tin bài tập và thao tác quản lý bài tập |
| 4.2.1.8 | M_Submission | 83 | Bài nộp và kết quả bài nộp |
| 4.2.1.9 | M_Feedback | 84 | Phản hồi cho bài nộp |
| 4.2.1.10 | M_CourseContent | 85 | Nội dung và học liệu trong khóa học |
| 4.2.1.11 | M_Resource | 86 | Tài nguyên bổ sung và thông tin tài nguyên |
| 4.2.1.12 | M_Certificate | 87 | Chứng nhận hoàn thành khóa học |
| 4.2.1.13 | M_ProgressRecord | 88 | Bản ghi tiến độ học tập |
| 4.2.1.14 | M_Event | 89 | Thông tin và vòng đời sự kiện |
| 4.2.1.15 | M_StudyGroup | 90 | Thông tin, thành viên và tài nguyên nhóm học |

**Mục tiêu cấp package:** thể hiện được các thực thể nghiệp vụ và trạng thái mà hệ thống cần quản lý. Từ danh sách trên chỉ kế thừa cách phân loại/trình bày, không mang các thực thể học tập sang đề tài khác.

#### H.2.3. 4.2.2. View Package - 30 lớp trong mẫu

| Mục | Lớp | Trang | Trách nhiệm/mục tiêu đặc tả |
|---|---|---:|---|
| 4.2.2.1 | V_RegistrationForm | 91 | Giao diện nhập thông tin đăng ký |
| 4.2.2.2 | V_LoginForm | 92 | Giao diện đăng nhập |
| 4.2.2.3 | V_ConfirmationEmailSender | 93 | Thành phần xác nhận email theo cách tổ chức của mẫu |
| 4.2.2.4 | V_ErrorMessageDisplay | 94 | Hiển thị thông báo lỗi |
| 4.2.2.5 | V_ProfileForm | 95 | Giao diện hồ sơ người dùng |
| 4.2.2.6 | V_PasswordResetRequestForm | 95 | Nhập yêu cầu đặt lại mật khẩu |
| 4.2.2.7 | V_PasswordResetEmailSender | 96 | Thành phần email đặt lại mật khẩu trong mẫu |
| 4.2.2.8 | V_PasswordResetForm | 97 | Nhập và xác nhận mật khẩu mới |
| 4.2.2.9 | V_ProgressView | 98 | Hiển thị tiến độ của một sinh viên |
| 4.2.2.10 | V_CourseManagementForm | 98 | Giao diện quản lý khóa học |
| 4.2.2.11 | V_CreateCourseForm | 99 | Form tạo khóa học |
| 4.2.2.12 | V_CourseList | 100 | Hiển thị/lọc/tìm trong danh sách khóa học |
| 4.2.2.13 | V_ConfirmationDialog | 101 | Hộp thoại xác nhận thao tác |
| 4.2.2.14 | V_CourseContentForm | 102 | Form thêm hoặc sửa nội dung khóa học |
| 4.2.2.15 | V_StudentList | 102 | Danh sách sinh viên trong khóa học |
| 4.2.2.16 | V_FeedbackForm | 103 | Nhập phản hồi cho bài nộp |
| 4.2.2.17 | V_SubmissionViewer | 104 | Hiển thị bài nộp để xem/chấm |
| 4.2.2.18 | V_CourseSearchForm | 105 | Nhập truy vấn tìm khóa học |
| 4.2.2.19 | V_SearchResultsDisplay | 106 | Hiển thị kết quả tìm kiếm |
| 4.2.2.20 | V_SelfProgressView | 107 | Hiển thị tiến độ của chính người đang đăng nhập |
| 4.2.2.21 | V_CertificateDisplay | 107 | Hiển thị chứng nhận |
| 4.2.2.22 | V_CertificateDownloadOption | 108 | Tùy chọn/liên kết tải chứng nhận |
| 4.2.2.23 | V_AssignmentUploadForm | 109 | Giao diện tải bài nộp lên |
| 4.2.2.24 | V_CourseContentViewer | 110 | Hiển thị nội dung học tập |
| 4.2.2.25 | V_ModuleSelector | 110 | Chọn và điều hướng giữa các module |
| 4.2.2.26 | V_EventContentForm | 111 | Nhập/sửa thông tin sự kiện |
| 4.2.2.27 | V_EventViewer | 112 | Hiển thị thông tin sự kiện |
| 4.2.2.28 | V_MessageViewer | 113 | Hiển thị tin nhắn |
| 4.2.2.29 | V_GroupContentForm | 114 | Nhập/sửa thông tin nhóm |
| 4.2.2.30 | V_StudyGroupViewer | 114 | Hiển thị thông tin nhóm học |

**Mục tiêu cấp package:** xác định các thành phần trình bày và tương tác cần thiết. Một màn hình có thể dùng nhiều lớp View; số View không phải số màn hình. Việc mẫu đặt lớp gửi email trong View là lựa chọn của mẫu, không phải bằng chứng mọi kiến trúc MVC đều phải bố trí như vậy.

#### H.2.4. 4.2.3. Control Package - 16 lớp trong mẫu

| Mục | Lớp | Trang | Trách nhiệm/mục tiêu đặc tả |
|---|---|---:|---|
| 4.2.3.1 | C_RegistrationController | 115 | Điều phối đăng ký và xác nhận thông tin |
| 4.2.3.2 | C_LoginController | 116 | Điều phối xác thực và đăng nhập |
| 4.2.3.3 | C_ProfileController | 117 | Xem/cập nhật hồ sơ |
| 4.2.3.4 | C_PasswordResetController | 118 | Điều phối đặt lại mật khẩu |
| 4.2.3.5 | C_ProgressController | 118 | Truy xuất/cập nhật/báo cáo tiến độ |
| 4.2.3.6 | C_CourseController | 119 | Tạo, cập nhật và xóa khóa học |
| 4.2.3.7 | C_ProgressTrackingController | 120 | Ghi hoạt động, tính tiến độ và báo cáo |
| 4.2.3.8 | C_FeedbackController | 121 | Thu thập/quản lý phản hồi; cần thống nhất phản hồi bài nộp hay phản hồi khóa học |
| 4.2.3.9 | C_EnrollmentController | 122 | Ghi danh, rút khỏi và quản lý tham gia khóa học |
| 4.2.3.10 | C_CourseSearchController | 123 | Xử lý tìm kiếm và lọc khóa học |
| 4.2.3.11 | C_CertificateController | 124 | Tạo, cấp và xác minh chứng nhận |
| 4.2.3.12 | C_AssignmentController | 124 | Tạo bài tập, nhận và đánh giá bài nộp |
| 4.2.3.13 | C_ContentAccessController | 125 | Kiểm tra/cấp/thu hồi quyền truy cập nội dung |
| 4.2.3.14 | C_MessageController | 126 | Gửi và lưu tin nhắn |
| 4.2.3.15 | C_StudyGroupController | 127 | Quản lý nhóm, thành viên, tài nguyên theo các phương thức được liệt kê |
| 4.2.3.16 | C_EventController | 128 | Quản lý thông tin, người tham gia và nhắc việc sự kiện theo các phương thức được liệt kê |

**Mục tiêu cấp package:** mỗi yêu cầu từ giao diện có nơi điều phối rõ ràng và liên hệ được với Model. Hai lớp cuối có Description bị chép thành “Messenger” trong nguồn; trách nhiệm ở bảng trên được diễn giải từ tên lớp và phương thức, không coi câu Description sai đó là chuẩn.

## I. Chương 4.3: Data Storage Design

### I.1. 4.3.1. Overview - trang 129-132

**Mục tiêu:** giải thích cách dữ liệu hỗ trợ nghiệp vụ và mối liên hệ tổng thể giữa các thực thể.

**Đầu ra theo mẫu:** đoạn mô tả tổ chức dữ liệu -> hình lược đồ quan hệ/ERD ở trang 130 -> bảng danh mục gồm `Index | Table Name | Description`.

**Giới hạn:** không chỉ chèn ERD; không lặp nguyên các thuộc tính của toàn bộ lớp; không coi quan hệ lớp và quan hệ bảng luôn là một-một.

**Đạt khi:** bảng trong hình, bảng tổng quan và bảng chi tiết có thể đối chiếu được; các quan hệ chính và bảng liên kết được giải thích; không mất thực thể cần cho use case trong phạm vi.

### I.2. 4.3.2. Detailed Data Storage Design - trang 132-146

**Mục tiêu:** đặc tả lược đồ dữ liệu đủ rõ để triển khai lưu trữ và kiểm tra tính nhất quán.

**Khuôn mỗi bảng theo mẫu:** tên bảng, tiếp theo là bảng từ điển dữ liệu:

| Index | Fieldname | Datatype | Nullable | Constraint | Description |
|---|---|---|---|---|---|
| [STT] | [Tên trường] | [Kiểu và độ dài nếu có] | [Yes/No] | [PK/FK/Unique/ràng buộc] | [Ý nghĩa dữ liệu] |

**Yêu cầu:** nêu rõ khóa chính, khóa ngoại và đối tượng tham chiếu, tính bắt buộc, ràng buộc duy nhất/miền giá trị khi có. Với bảng liên kết, phải xác định cách định danh bản ghi và tránh trùng dữ liệu theo nghiệp vụ. Đây là làm rõ cột Constraint có sẵn, không phải thêm chương thiết kế mới.

**Giới hạn:** không thay bằng một khối SQL dài; không sao chép kiểu dữ liệu hoặc độ dài từ mẫu mà chưa xét miền dữ liệu của đề tài. Các lỗi như `BIT(0)`, tên `sumission_id`, độ dài khóa không khớp hoặc trường mật khẩu không phù hợp biểu diễn lưu trữ cần được rà soát, không kế thừa tự động.

**Đạt khi:** toàn bộ dữ liệu bền vững phục vụ luồng trong phạm vi có nơi lưu trữ; khóa/quan hệ/kiểu tương thích; tên và ràng buộc thống nhất với ERD và danh mục.

### I.3. Danh mục 20 bảng chi tiết của mẫu

Giữ thứ tự và tên dưới đây khi cần đối chiếu nguồn; khi viết đề tài khác, thay bằng danh mục thực tế. Một số tên trong hình ERD và danh mục dùng cách viết khác nhau; bản mới cần chuẩn hóa.

| STT đối chiếu | Tên mục trong phần chi tiết | Trang bắt đầu | Mục tiêu lưu trữ |
|---|---|---:|---|
| 1 | User Table | 132 | Tài khoản, vai trò và thông tin cá nhân |
| 2 | Student Table | 133 | Thông tin học tập riêng của sinh viên |
| 3 | Instructor Table | 134 | Thông tin riêng của giảng viên |
| 4 | Lesson Table | 134 | Thông tin bài học |
| 5 | LessonAndModule Table | 135 | Liên kết bài học-module và thứ tự bài học |
| 6 | Module Table | 135 | Thông tin module |
| 7 | ModuleAndCourse Table | 136 | Liên kết module-khóa học và thứ tự module |
| 8 | Course Table | 136 | Thông tin khóa học |
| 9 | ResourceAndCourseTable | 137 | Liên kết tài nguyên-khóa học |
| 10 | Resource Table | 138 | Đường dẫn, loại và mô tả tài nguyên |
| 11 | Progress Table | 139 | Ghi danh, tiến độ và trạng thái hoàn thành |
| 12 | InstructorAndCourse Table | 140 | Liên kết giảng viên-khóa học |
| 13 | Assignment Table | 140 | Thông tin bài tập và hạn nộp |
| 14 | Submission Table | 141 | Bài nộp, điểm, thời điểm nộp |
| 15 | Feedback Table | 142 | Phản hồi của giảng viên cho bài nộp |
| 16 | Certificates Table | 143 | Chứng nhận của sinh viên theo khóa học |
| 17 | Study Group Table | 143 | Thông tin nhóm học |
| 18 | StudentAndGroup Table | 144 | Thành viên, vai trò và thời điểm tham gia/rời nhóm |
| 19 | Event Table | 145 | Thông tin và thời gian sự kiện |
| 20 | Message Table | 146 | Người gửi/nhận, nội dung và thời điểm gửi tin |

**Chênh lệch cần lưu ý:** danh mục tổng quan chỉ có 18 bảng, thiếu hai mục nhóm học; ERD thể hiện chúng. Bản mới phải đồng bộ ba nơi, không lấy 18 hoặc 20 làm chỉ tiêu cố định.

## J. Chương 4.4: User Interface Design

### J.1. 4.4.1. Interface prototype - trang 147-156

**Mục tiêu:** cho thấy người dùng nhìn thấy gì và thao tác ở đâu để hoàn thành use case.

**Đầu ra cần có:** các mục con theo màn hình/nhóm thao tác; hình prototype hoặc wireframe; tên/mã use case liên quan; các trường, nút, thông tin và trạng thái thiết yếu. Một nhóm có thể có nhiều hình như phần sửa thông tin cá nhân của mẫu.

**Giới hạn:** không yêu cầu đã lập trình giao diện; không dùng ảnh trang trí thay mockup; không thêm chức năng mới chỉ vì xuất hiện trong ảnh tham khảo.

**Đạt khi:** có thể theo dõi đường thao tác của các use case chính từ hình; nhãn, dữ liệu và hành động phù hợp đặc tả; hình đủ rõ khi xuất report.

### J.2. 4.4.2. Interface specification - trang 156-159

**Mục tiêu:** giải thích chức năng và điều kiện truy cập của từng giao diện ở 4.4.1.

**Khuôn của mẫu là bảng hai cột, bốn trường:**

| Trường | Mục tiêu/nội dung |
|---|---|
| **Interface** | Tên giao diện chính xác |
| **Content** | Chức năng/nội dung giao diện phục vụ |
| **Condition** | Điều kiện, vai trò hoặc thao tác dẫn đến giao diện |
| **Complexity** | Mức độ phức tạp theo đánh giá được dùng nhất quán |

**Giới hạn:** giữ khuôn bốn trường, không tự biến thành tài liệu thành phần UI hoặc đặc tả API. Mẫu ghi Simple cho cả 14 mục; bản mới phải đánh giá theo thực tế, không tự động điền giống nhau.

**Đạt khi:** mỗi mục prototype có specification tương ứng; tên giao diện và điều kiện khớp use case; không lặp lỗi ghi Interface = Homepage cho màn hình Do Quiz/Assignment.

### J.3. Danh mục 14 nhóm màn hình trong nguồn

Hai bộ mục `4.4.1.i` và `4.4.2.i` dùng cùng thứ tự. Cột trang hình ghi vị trí ảnh thực tế, không chỉ vị trí tiêu đề.

| i | Tên nhóm màn hình | Mục tiêu | Trang hình prototype | Trang specification |
|---|---|---|---|---|
| 1 | Homepage | Điểm vào cho khách, dẫn tới đăng nhập/đăng ký | 147 | 156 |
| 2 | Register Form | Nhập và gửi yêu cầu đăng ký | 148 | 156-157 |
| 3 | Login Form | Xác thực tài khoản | 148 | 157 |
| 4 | Log Out / Logout Form | Truy cập thao tác kết thúc phiên | 149 | 157 |
| 5 | Update Information | Sửa hồ sơ, tài khoản hoặc ảnh | 150-151 | 157 |
| 6 | Reset Password | Khởi tạo đặt lại mật khẩu | 151 | 157 |
| 7 | Messenger | Xem/gửi tin nhắn | 152 | 158 |
| 8 | Enrollment | Xem khóa học và ghi danh | 152 | 158 |
| 9 | Do Quiz/Assignment | Làm bài hoặc nộp bài | 153 | 158 |
| 10 | Access Content | Xem/tải nội dung bài học | 154 | 158 |
| 11 | Course Management | Xem danh sách và truy cập tác vụ quản lý | 154 | 158-159 |
| 12 | Create Courses | Nhập thông tin khóa học mới | 155 | 159 |
| 13 | Delete Courses | Thao tác xóa khóa học | 155 | 159 |
| 14 | Update Course Content | Chỉnh sửa nội dung khóa học | 156 | 159 |

Danh sách màn hình không bằng danh sách 22 use case. Một màn hình có thể phục vụ nhiều use case và một use case có thể qua nhiều màn hình. Bản mới phải giải thích được sự bao phủ thay vì ép ánh xạ một-một.

### J.4. 4.4.3. Screen Flow - tiêu đề trang 159; hình trang 160-161

**Mục tiêu:** cho thấy cách người dùng chuyển giữa các màn hình khi thực hiện tác vụ theo vai trò.

**Đầu ra theo mẫu:** một flow cho Student và một flow cho Instructor; dùng các ảnh màn hình/khung màn hình nối bằng mũi tên. Với đề tài mới, thay bằng các vai trò chính thực tế.

**Nội dung cần rõ:** điểm bắt đầu, đường truy cập, thao tác dẫn tới màn hình tiếp theo, nhánh theo vai trò/trạng thái và đường quay lại khi cần.

**Giới hạn:** không thay bằng activity diagram nghiệp vụ. Không đưa vào flow màn hình chưa có trong prototype/specification mà không bổ sung tương ứng. Không cần sao chép các dấu chọn/khung biên tập vô tình có trong ảnh của mẫu.

**Đạt khi:** người đọc theo được ít nhất các hành trình chính của từng vai trò; mọi nút và đường chuyển có giải thích hoặc nhãn đủ rõ; không có màn hình bị cô lập vô cớ.

## K. Chương 5 và References

### K.1. 5.1. Conclusion - trang 161-162

**Mục tiêu:** đối chiếu công việc thực tế với vấn đề/mục tiêu ban đầu và tổng kết đóng góp.

**Cấu trúc quan sát:** nhắc lại hệ thống và kết quả -> công nghệ/phương pháp -> chức năng và giá trị -> các thách thức đã xử lý -> đánh giá tổng thể.

**Đầu ra cần có:** nội dung đã hoàn thành trong phạm vi, liên hệ với 1.1/1.2 và 2.2, quyết định thiết kế quan trọng, khó khăn/hạn chế có căn cứ và mức độ đạt mục tiêu.

**Giới hạn:** không chép nguyên phần Introduction; không thêm tính năng chưa có trong thiết kế. Nguồn có câu khẳng định đã phát triển và kiểm thử nghiêm ngặt, nhưng không có chương bằng chứng kiểm thử tương ứng. Không lặp kiểu khẳng định này khi dữ liệu không chứng minh.

**Đạt khi:** phân biệt được đã phân tích, đã thiết kế, đã hiện thực và đã xác minh; kết luận không vượt quá bằng chứng của report.

### K.2. 5.2. Future Work - trang 162-163

**Mục tiêu:** nêu những hướng phát triển có giá trị nằm ngoài phạm vi hoặc chưa hoàn tất.

**Dạng trình bày:** đoạn mở đầu về cơ hội cải thiện, rồi danh sách hướng phát triển có tên và giải thích ngắn. Mẫu nêu hỗ trợ thời gian thực bằng AI, gợi ý nội dung, mở rộng thanh toán, phân tích nâng cao và ứng dụng di động.

**Đầu ra cần có:** mỗi hướng gắn với hạn chế/nhu cầu còn lại, mô tả lợi ích và ranh giới với phiên bản hiện tại. Có thể thêm mức ưu tiên ngay trong mô tả nếu đã có căn cứ; không tạo một chương roadmap mới.

**Giới hạn:** không coi các ý tưởng AI/thanh toán/mobile của mẫu là yêu cầu mặc định. Không đưa chức năng cốt lõi đã hứa ở 1.2 vào Future Work mà không giải thích phạm vi và trạng thái.

**Đạt khi:** người đọc phân biệt rõ hệ thống hiện tại với đề xuất tương lai; không mâu thuẫn với Conclusion.

### K.3. References - trang 163

**Mục tiêu:** cho phép kiểm tra các nguồn đã dùng cho kiến thức, lập luận, quy định hoặc thiết kế.

**Quan sát:** đặt sau 5.2, tiêu đề riêng không có số chương; bên dưới là danh sách tham khảo dạng đánh số. Phần chữ của danh mục bị ảnh hưởng bởi font không đầy đủ trong bản PDF này; không tái tạo tên sách/tác giả/văn bản thành dữ kiện đã xác minh.

**Đầu ra cho report mới:** danh mục nguồn thực sự được dùng; thông tin nhận diện đủ để tra lại; trích dẫn trong thân bài theo một quy ước thống nhất.

**Giới hạn:** không sao chép nguyên danh mục mẫu cho đề tài khác; không bịa URL, tác giả, năm, số văn bản hoặc nguồn cho số liệu. Nếu phải dùng thông tin pháp lý/công nghệ hiện hành, cần kiểm chứng nguồn phù hợp ở thời điểm soạn report đó.

**Đạt khi:** mỗi khẳng định cần dẫn nguồn có nguồn phù hợp; nguồn có trong danh mục được sử dụng thực chất; các mục tham khảo không còn lỗi font hoặc thông tin thiếu không được đánh dấu.

## L. Quy cách trình bày và giới hạn độ dài

### L.1. Quan sát hình thức từ mẫu

| Thành phần | Đặc điểm quan sát được | Áp dụng khi soạn bản mới |
|---|---|---|
| Khổ trang | 612 x 792 pt, tương đương Letter, trang dọc | Nếu không có quy định học phần khác và cần giống hình thức, dùng cùng khổ; không mặc định mẫu là A4 |
| Kiểu chữ | Chủ yếu Times New Roman; một số chữ trong hình dùng font khác | Giữ font thân bài thống nhất |
| Thân bài | Chủ yếu 12 pt | Dùng làm mốc khi cần tái hiện hình thức |
| Mục lục | Chủ yếu 11 pt, tiêu đề riêng lớn hơn | Sinh từ heading để cập nhật tự động |
| Cấp tiêu đề | Chương khoảng 20 pt; cấp 2 khoảng 16 pt; cấp 3 khoảng 14 pt; cấp sâu thường 12 pt | Tái hiện phân cấp rõ ràng; không coi cỡ chữ là rubric chính thức |
| Màu tiêu đề | Xanh; nội dung chính đen | Dùng một màu nhất quán, tránh thêm hệ màu trang trí |
| Đoạn văn | Nhiều đoạn căn đều, có thụt đầu dòng; danh sách dùng gạch đầu dòng | Giữ nhịp trình bày học thuật dễ đọc |
| Bảng | Viền đen, hàng tiêu đề rõ, nhiều bảng kéo dài qua trang | Không để chữ bị bó quá hẹp; lặp hàng tiêu đề khi bảng sang trang |
| Sơ đồ/hình | Chèn theo use case/lớp/màn hình, có thể chiếm phần lớn trang | Ưu tiên khả năng đọc nhãn, không ép nhiều hình đến mức mất chi tiết |

Không xác lập chính xác lề hoặc giãn dòng bắt buộc chỉ từ nhận xét thị giác. Nếu có quy định định dạng chính thức, quy định đó được ưu tiên.

### L.2. Độ dài: mốc tham chiếu, không phải hạn mức được đề bài quy định

- Cover: một trang; mục lục dài theo số heading, trong mẫu là bốn trang.
- Introduction: khoảng 1-2 trang trong mẫu; chỉ cần đủ vấn đề và giải pháp cấp cao.
- Planning: khoảng 7-8 trang trong mẫu; phần lớn là văn bản đánh giá và kế hoạch.
- Use case details: khoảng 15-16 trang cho 22 use case; độ dài tăng theo số bước và nhánh.
- Activity và Sequence: khoảng 37 trang từ tiêu đề Activity đến hình sequence cuối; một số trang chỉ có tiêu đề hoặc khoảng trắng lớn. **Không tái tạo các trang trống để bắt chước độ dài.**
- NFR: khoảng 1-2 trang theo bốn nhóm.
- Architecture: khoảng 5-6 trang, gồm hình và giải thích.
- Class Specification: khoảng 55 trang cho 61 lớp; đây là phần đặc tả dài nhất.
- Data Storage: khoảng 17-18 trang gồm tổng quan, hình và 20 bảng chi tiết.
- User Interface: khoảng 14-15 trang gồm prototype, specification, screen flow.
- Conclusion/Future Work và References: nằm trong ba trang cuối, không phải mỗi phần ba trang.

Không có giới hạn từ, số trang tối thiểu/tối đa hoặc điểm số chính thức trong nguồn. Khi cần rút gọn, trước hết giảm lặp văn, trình bày hình/bảng hợp lý và thu hẹp phạm vi theo yêu cầu; không bỏ nhóm đầu ra cốt lõi hoặc chỉ giữ tiêu đề rỗng.

## M. Cơ chế dữ liệu thiếu và kiểm soát tính nhất quán cho AI

### M.1. Dữ liệu đầu vào cần thu thập

Trước khi viết nội dung khẳng định, xác định: tên đề tài; vấn đề/bối cảnh; actor; phạm vi chức năng; quy tắc nghiệp vụ; ràng buộc; trạng thái hiện thực; công nghệ được yêu cầu; nhóm và thời gian; nguồn tham khảo; yêu cầu định dạng/ngôn ngữ/độ dài nếu có.

Nếu thiếu dữ liệu, vẫn có thể lập cấu trúc và điền phần đã có căn cứ. Dùng các nhãn rõ ràng trong bản nháp:

- `[CHUA_CO_DU_LIEU: nội dung cần bổ sung]`: chưa có dữ kiện để viết.
- `[GIA_DINH_CAN_XAC_NHAN: giả định và tác động]`: lựa chọn tạm để hoàn thiện phân tích, chưa được xác nhận.
- `[KHONG_AP_DUNG: lý do]`: phần không áp dụng trong điều kiện cụ thể nhưng cần giữ vị trí cấu trúc.

Không chuyển giả định thành kết quả thật. Không dùng `[KHONG_AP_DUNG]` để bỏ qua một phần cốt lõi chỉ vì chưa làm xong. Trước khi coi report hoàn tất, xử lý hoặc công khai các nhãn còn tồn tại; dữ liệu thiếu quan trọng phải được báo lại.

### M.2. Bảng truy vết dùng để rà soát, không tự thêm thành chương report

| Requirement | UC code | Actor | Đặc tả 3.2 | Activity 3.3 | Sequence 3.4 | Class/method 4.2 | Data 4.3 | Screen 4.4 | Trạng thái/ghi chú |
|---|---|---|---|---|---|---|---|---|---|
| [Yêu cầu thực tế] | [Mã] | [Vai trò] | [Mục] | [Hình] | [Hình hoặc dẫn chiếu] | [Lớp.phương thức] | [Bảng/trường hoặc lý do không lưu] | [Màn hình hoặc tương tác khác] | [Đã đủ/thiếu/xung đột] |

**Cách kiểm tra:**

1. Mỗi yêu cầu trong phạm vi có use case hoặc lý do xử lý ở mức NFR.
2. Mỗi use case có mã duy nhất, mục tiêu, luồng và kết quả; không có actor ngoài tổng quan mà không giải thích.
3. Activity và sequence phản ánh cùng một hành vi với đặc tả; nhánh quan trọng không biến mất khi chuyển biểu diễn.
4. Đối tượng/thông điệp trên sequence ánh xạ được sang lớp/phương thức; lớp phục vụ một trách nhiệm có căn cứ.
5. Dữ liệu cần tồn tại sau giao dịch có chỗ lưu; dữ liệu tạm hoặc dịch vụ ngoài có thể không cần bảng riêng nhưng phải giải thích được.
6. ERD, danh mục bảng và từ điển dữ liệu đồng bộ; không ép một lớp tương ứng một bảng.
7. Prototype, specification và screen flow dùng cùng tên/định danh; các hành trình chính có màn hình tương ứng.
8. NFR liên hệ được với quyết định thiết kế; chỉ tiêu là mục tiêu hay kết quả kiểm chứng phải ghi đúng trạng thái.
9. Conclusion chỉ tổng kết phần đã có bằng chứng; Future Work không nhập nhằng với phạm vi hiện tại.
10. Tiến độ, nhân lực, chi phí, công nghệ và giả định phải thống nhất xuyên report.

### M.3. Ranh giới giữa các phần thường bị viết trùng

| Hai phần | Ranh giới nội dung cần giữ |
|---|---|
| Problem Definition / Motivation | Vấn đề và hậu quả / Lý do chọn và thực hiện đề tài |
| Proposed Solution / Business Requirements | Hướng giải quyết và nhóm khả năng / Danh sách khả năng được yêu cầu rõ hơn |
| Business Requirements / Use case Details | Cần cung cấp gì / Ai thực hiện, khi nào, các bước và kết quả |
| Special Issues or Constraints / NFR | Ràng buộc đầu vào / Điều kiện chất lượng cụ thể, có thể đánh giá |
| Activity / Sequence | Tiến trình công việc và nhánh / Tương tác đối tượng theo thời gian |
| Package Diagram / Class Specification | Tổ chức và quan hệ tổng thể / Chi tiết từng lớp, thuộc tính và phương thức |
| Model / Data Storage | Đối tượng và hành vi trong thiết kế / Cách dữ liệu bền vững được lưu và ràng buộc |
| Prototype / Interface specification / Screen Flow | Nhìn thấy và thao tác gì / Mục đích và điều kiện truy cập / Di chuyển giữa màn hình ra sao |
| Conclusion / Future Work | Kết quả đã đạt có căn cứ / Những gì còn lại hoặc đề xuất cho phiên bản sau |

## N. Lỗi, thiếu sót và điểm không nên kế thừa từ mẫu

Đây là danh sách kiểm soát chất lượng; giữ chúng trong hướng dẫn AI, không tự chèn nguyên danh sách này vào report mới.

| Vấn đề quan sát | Vị trí | Cách xử lý khi viết report mới |
|---|---|---|
| Trùng số `3.4` | Sequence trang 52; NFR trang 68 | Đổi NFR thành 3.5; giữ thứ tự |
| U6 Messenger nhưng hàng mã lại ghi U5 | 20 | Dùng một mã chuẩn trong mọi biểu diễn |
| I5 được ghi “Specializes U5”, trong khi U5 là Reset Password | 23 | Kiểm chứng lại ý nghĩa quan hệ, không sao chép tham chiếu |
| S4 ghi “Specialize U7” và nơi khác lại dẫn U5; không có U7 trong danh mục đặc tả | 27 và 46 | Loại tham chiếu sai; mô tả quan hệ theo nghiệp vụ thực tế |
| I6 có dòng “Extends I6”, ô tên ghi “Give case code” | 23 | Sửa mã đích và tên, không coi tự mở rộng chính nó là quan hệ hợp lệ để kế thừa |
| Postconditions của S4 bị để trống | 27 | Ghi rõ kết quả quan sát được và trạng thái dữ liệu |
| Admin có ở Business Requirements và luồng duyệt sự kiện nhưng không được giải thích cùng nhóm actor tổng quan | 8, 15-16, 25 | Xác định Admin có thuộc phạm vi; đồng bộ sơ đồ, đặc tả và phân quyền |
| Không có sequence riêng cho I1 | Nhóm sequence Instructor trang 58-60 | Nêu rõ I1 là use case tổng hợp, dẫn chiếu I2-I4 hoặc bổ sung sequence cần thiết trong cùng mục |
| Nhiều tiêu đề và hình nằm khác trang, mục lục có mục chưa khớp trang bắt đầu thực tế | Ví dụ ProfileForm: mục lục 94, thân bài 95 | Cập nhật mục lục sau khi hoàn tất dàn trang; không sao chép số trang |
| Danh mục dữ liệu 18 bảng nhưng chi tiết 20 bảng | 130-146 | Đồng bộ Study Group, StudentAndGroup và toàn bộ danh mục |
| Tên bảng/khóa và kiểu/độ dài có chỗ chưa thống nhất; thiếu hoặc mơ hồ ràng buộc | Ví dụ 132, 137-141, 144-146 | Rà soát ERD và từng cột; chỉ chốt kiểu/ràng buộc phù hợp dữ liệu |
| C_StudyGroupController và C_EventController lặp Description về Messenger | 127-128 | Viết Description theo đúng trách nhiệm của từng lớp |
| Phản hồi ở các phần chưa luôn cùng đối tượng: bài nộp hay khóa học | I6 trang 24, M_Feedback trang 84, C_FeedbackController trang 121 | Tách nghĩa hoặc thống nhất mô hình; không dùng chung tên che giấu hai nghiệp vụ khác nhau |
| Interface của Do Quiz/Assignment bị ghi là Homepage | 158 | Đồng bộ tên với prototype và đặc tả use case |
| Tính năng nâng cao như predictive analytics được nhắc ở đầu và kết luận nhưng mức truy vết vào thiết kế chưa tương xứng | 6-13, 161-163 so với bộ đặc tả | Hoặc thiết kế đủ trong khung có sẵn, hoặc hạ tuyên bố/đưa Future Work; không tự cho là đã hoàn thành |
| Timeline kỹ thuật và kế hoạch không thống nhất | 9, 13 | Chọn một cơ sở ước lượng và kiểm tra tổng thời gian |
| Kết luận khẳng định xây dựng/kiểm thử nhưng report không trình bày bằng chứng tương ứng | 161-162 | Viết đúng trạng thái dự án thực tế |
| Viện dẫn luật/tiêu chuẩn thuộc bối cảnh report cũ | 9, 11, 69 | Kiểm chứng lại nguồn và phạm vi áp dụng nếu dùng cho report mới |
| Bố cục có khoảng trống lớn và tiêu đề bị tách khỏi hình | Ví dụ 48, 52 | Dàn trang lại để đọc liền mạch; không bắt chước lỗi |
| References lỗi font trong bản được cung cấp | 163 | Chỉ dùng tài liệu tham khảo đã xác minh; không tự khôi phục nội dung thành khẳng định chắc chắn |

## O. Checklist hoàn thành cho AI

### O.1. Kết cấu

- [ ] Có bìa, mục lục, 5 chương và References theo đúng thứ tự.
- [ ] Giữ đủ 1.1-1.2, 2.1-2.4 và các mục con trong dàn ý chuẩn.
- [ ] Có 3.1-3.5, bao gồm cả activity, sequence và NFR; không trùng số.
- [ ] Có đủ 4.1-4.4; 4.2 chia ba package; 4.4 chia prototype, specification, screen flow.
- [ ] Có 5.1 Conclusion và 5.2 Future Work; không thêm chương ngoài yêu cầu.
- [ ] Mục lục và số trang phản ánh bản xuất cuối.

### O.2. Mục tiêu và đầu ra

- [ ] Vấn đề có chủ thể và hậu quả; giải pháp bám vấn đề.
- [ ] Nhu cầu, yêu cầu, giá trị và ràng buộc được phân biệt.
- [ ] Đánh giá đủ 5 loại khả thi, không chỉ tuyên bố khả thi.
- [ ] Phạm vi, thời gian, nhân lực và công cụ có căn cứ, nhất quán.
- [ ] Actor/use case được xác định, đặt mã và sử dụng thống nhất.
- [ ] Mỗi use case có đủ các trường bảng theo mẫu, đặc biệt precondition và postcondition.
- [ ] Activity và sequence bao phủ hành vi cần thiết; mọi phần không có hình riêng có giải thích.
- [ ] NFR có nội dung cụ thể theo 4 nhóm và không bị diễn đạt thành kết quả đo khi chưa đo.
- [ ] Có kiến trúc tổng quát và bộ package chi tiết gắn với đề tài.
- [ ] Mỗi lớp có Description, bảng Attributes và bảng Methods; không chỉ có tên lớp.
- [ ] Có ERD/lược đồ, danh mục bảng và từ điển dữ liệu; cả ba thống nhất.
- [ ] Có prototype, specification bốn trường và screen flow theo vai trò thực tế.
- [ ] Conclusion và Future Work phân biệt kết quả hiện tại với đề xuất tương lai.
- [ ] References gồm nguồn thật, phù hợp nội dung và đọc được.

### O.3. Giới hạn và độ trung thực

- [ ] Không nhập chức năng, actor, lớp, bảng hoặc thông tin cá nhân của mẫu sang đề tài mới ngoài căn cứ.
- [ ] Không ép số lượng 22 use case, 61 lớp, 20 bảng, 14 nhóm màn hình hoặc 163 trang.
- [ ] Không có số liệu, nguồn, tiến độ, công nghệ, kết quả kiểm thử hoặc trạng thái triển khai do AI tự bịa.
- [ ] Các giả định/dữ liệu thiếu được đánh dấu và xử lý hoặc công khai trước khi bàn giao.
- [ ] Không lặp các lỗi mã, tham chiếu, bảng, giao diện và kết luận của nguồn.
- [ ] Hình/bảng đọc được, không cắt chữ; tiêu đề gắn với nội dung, không tạo trang trống để tăng độ dài.

## P. Chỉ dẫn bàn giao ngắn cho AI soạn report sau này

Có thể dùng nguyên đoạn dưới đây kèm dữ liệu đề tài thực tế:

```text
Hãy đọc Example_Report_Structure_Guide.md và dùng làm đặc tả kết cấu report.
Giữ đúng thứ tự Cover, Table of Contents, 5 chương và References; giữ các mục cố định
trong phần D, dùng 3.5 cho Non-functional Requirements để sửa lỗi trùng số của mẫu.

Chỉ thay actor, use case, lớp, bảng, màn hình và dữ liệu theo đề tài được cung cấp.
Không sao chép nghiệp vụ Course Management System hoặc ép số lượng/trang của mẫu.
Mỗi phần phải đạt mục tiêu, có đầu ra và tuân thủ giới hạn đã mô tả trong hướng dẫn.

Trước khi viết chi tiết, khóa phạm vi tại 2.4.1 và lập bảng truy vết nội bộ theo M.2.
Sau đó hoàn thiện đặc tả use case, activity, sequence, kiến trúc MVC, lớp, dữ liệu và UI
theo cùng một tập tên/mã. Bảng truy vết là công cụ rà soát, không tự thêm thành chương.

Nếu thiếu thông tin, dùng nhãn trong M.1 và nêu rõ điều cần bổ sung; không bịa số liệu,
nguồn, kết quả hoặc trạng thái triển khai. Chỉ kết luận những gì có bằng chứng.
Rà soát các lỗi nguồn ở N và hoàn thành checklist O trước khi bàn giao.
```

**Phạm vi tài liệu này kết thúc ở việc phân tích và đặc tả cách bám mẫu. Tài liệu không tự xác lập chức năng hoặc yêu cầu riêng cho một đề tài mới chưa được cung cấp.**
