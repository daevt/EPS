# Hướng dẫn AI tiếp tục report EPS

Đọc tài liệu này trước khi sửa report. Mục tiêu là duy trì một chương **Analysis bằng tiếng Anh**, ngắn gọn, bám mẫu và nhất quán với MVP đã được duyệt; phần giải thích/ghi chú cho nhóm dùng tiếng Việt. Không tự mở rộng phạm vi, tuyên bố hệ thống đã triển khai hay biến kịch bản nghiệm thu thành kết quả kiểm thử.

**Yêu cầu mới nhất:** Analysis phải ngắn gọn và chỉ giữ kết cấu có trong mẫu. Không thêm lại các mục 3.1.1–3.1.5, bảng FR/BR, bảng trạng thái, hợp đồng tích hợp hoặc chỉ mục NFR vào báo cáo. Các mô hình hỗ trợ vẫn được lưu riêng để kiểm tra nghiệp vụ, không phải nội dung cần chèn lại. Tuyệt đối không sửa Introduction/Planning.

## Nguồn có thẩm quyền và tệp cần đọc

Ưu tiên yêu cầu mới nhất của người dùng, sau đó phạm vi MVP đã khóa và các nguồn sau. Nếu có mâu thuẫn nghiệp vụ thực sự, ghi rõ điểm mâu thuẫn và giải quyết trước khi phát sinh đặc tả/sơ đồ mới.

| Nguồn | Cách sử dụng |
| --- | --- |
| [Introduction và Planning nguồn chuẩn](EPS_Report_LaTeX/source/Introduction_Planning.pdf) | Căn cứ đề tài; trọng tâm 2.4.1, trang PDF 9–10, trang in 12–13. Giữ PDF nguyên bản. |
| [Hướng dẫn kết cấu mẫu](Example_Report_Structure_Guide.md) | Giữ thứ tự, mục đích, độ chi tiết và giới hạn từng phần; không sao chép nghiệp vụ giáo dục của mẫu. |
| [Đặc tả User/Buyer](analysis/content_user_buyer.json), [Seller/Admin/Payment](analysis/content_seller_admin_payment.json) | Nguồn nội dung 22 use case và hai biến thể API; giữ mã, actor, điều kiện, luồng ngoại lệ và hậu điều kiện nhất quán. |
| [Nội dung rút gọn dùng trong report](analysis/report_concise.py) | Câu ngắn cho 22 use case và NFR; builder dùng bản này để tránh đưa lại diễn giải dài vào báo cáo. |
| [Controls](analysis/analysis_controls.json) | FR01–FR12, BR01–BR27, trạng thái/guard, NFR và các tình huống nghiệm thu. |
| [Manifest overview](analysis/overview_manifest.json), [activity](analysis/activity_models.json), [sequence](analysis/sequence_models.json) | Danh mục hình, tên tệp, main/continuation và tham chiếu hiện hành. Lấy số lượng view từ manifest, không cố định trong quá trình tinh chỉnh sơ đồ. |
| [Truy vết/nghiệm thu](analysis/Traceability_and_Acceptance.md), [đồng bộ Planning](analysis/Planning_Alignment_Notes.md), [rà soát ngữ nghĩa](analysis/Semantic_Review.md) | Kiểm tra độ phủ, quy tắc và các điểm chưa đồng bộ; không dùng làm bằng chứng chạy ứng dụng. |

[main.tex](EPS_Report_LaTeX/main.tex) điều phối báo cáo; [sections/analysis.tex](EPS_Report_LaTeX/sections/analysis.tex) điều phối nội dung; mục 3.4 dùng chung từ [sections/sequence.tex](EPS_Report_LaTeX/sections/sequence.tex), cũng được biên dịch độc lập qua [EPS_Sequence_Diagrams.tex](EPS_Report_LaTeX/EPS_Sequence_Diagrams.tex). Introduction/Planning chỉ có **nguồn PDF được giữ nguyên**, được chèn từ `EPS_Report_LaTeX/source/Introduction_Planning.pdf`; không mô tả hai chương này là đã chuyển thành LaTeX chỉnh sửa được.

## MVP và các mặc định không được âm thầm thay đổi

- EPS là mô phỏng học phần: GOODS hoặc SERVICES, một buyer và một seller khác nhau, số tiền VND nguyên dương, funding toàn phần và một kết quả payout toàn phần duy nhất. Không tự thêm tiền thật, FX/cross-border, milestone, chia tiền, tự giải ngân, phí/subscription, provider KYC/logistics thật hay trọng tài ngoài.
- Seller chấp thuận trước funding; buyer chấp nhận điều khoản đã lưu khi nạp tiền. Điều khoản đã chấp thuận không sửa; nếu đủ điều kiện thì hủy trước funding và tạo escrow mới. User đăng nhập MFA; Admin cấp sẵn. Merchant là OAuth client cấp sẵn, gắn với một seller, chỉ tạo và tra cứu escrow thuộc client.
- Hai phương thức funding là Bank mock và Gateway mock. Chỉ receipt hợp lệ của provider mới tạo HELD. Mọi release dùng Bank mock đến seller đã chốt; refund qua provider và nguồn funding ban đầu. Redirect, nút bấm hoặc Admin không thể xác nhận tiền thành công.
- Seller ghi nhận bàn giao theo policy snapshot lúc tạo escrow; mặc định GOODS không bắt buộc bằng chứng, SERVICES bắt buộc. Policy chỉ cấu hình cờ evidence-required cho escrow tạo sau đó. Release thường luôn cần delivery và buyer xác nhận; Admin quyết định dispute là nhánh thẩm quyền riêng.
- Refund proposal PENDING chặn ghi nhận delivery mới và release thường. Chỉ đối tác chấp thuận/từ chối, chỉ người đề nghị được rút trước chấp thuận. Từ chối/rút khôi phục thao tác còn hợp lệ, không đảo ngược delivery đã lưu.
- Chỉ một dispute mỗi escrow. Mở dispute vô hiệu hóa proposal đang chờ; hai bên thêm bằng chứng đến trước quyết định cuối. Admin ghi lý do và chọn release/refund toàn phần; không appeal, dispute thứ hai hay đảo hướng payout sau khi đã nhận quyết định.
- Gate trạng thái phải nguyên tử: yêu cầu hợp lệ đến trước được chấp nhận; thao tác lặp không tạo chuyển tiền lặp. Timeout/UNKNOWN giữ pending và chỉ query cùng attempt. Chỉ provider xác nhận FAILED và không chuyển tiền mới cho retry. Funding thất bại trả AWAITING_FUNDING để buyer retry/hủy; payout thất bại giữ RELEASE_PENDING/REFUND_PENDING và khóa cùng hướng/đích cho A5 retry. Admin không nạp thay buyer hoặc đánh dấu thành công thủ công.
- Mười trạng thái chuẩn: AWAITING_SELLER, AWAITING_FUNDING, FUNDING_PENDING, HELD, DELIVERED, RELEASE_PENDING, REFUND_PENDING, RELEASED, REFUNDED, CANCELLED. Proposal/dispute/attempt là các chiều riêng; không tạo thêm lifecycle chỉ để biểu diễn dispute.
- p95 ≤ 2 giây cho create/query nội bộ, 20 phiên đồng thời và 1.000 escrow là **mục tiêu đề xuất, chưa đo**; loại thời gian người dùng/provider. Các phát biểu pháp lý từ Planning chưa được xác minh cho triển khai tiền thật. Không tự thêm nghiên cứu pháp lý hoặc kết luận tuân thủ vào lần chỉnh sửa này.

## Kết cấu và mã cố định

Giữ đúng năm mục, không thêm 3.6 Testing, Design, API implementation, database schema hay wireframe vào chương Analysis:

1. **3.1 General Use cases Diagram** — sơ đồ và giải thích actor ngắn gọn; không thêm mục con. Chỉ dùng sáu view UML cần thiết, không đưa bản đồ điều hướng vào report.
2. **3.2 Use case Details** — 22 use case; bảng tám trường Use Case Code, Use Case Name, Actor, Usage, Activation Event, Preconditions, Main Event Flow, Postconditions như mẫu. Luồng dùng Index–Done by–Action; viết gọn và giữ nhánh lỗi cần thiết. Biến thể API nằm trong luồng chung, không thêm bảng hợp đồng riêng.
3. **3.3 Activity Diagram** — nhóm theo vai trò rồi đến hình; không thêm danh mục điều hướng hoặc bảng truy vết.
4. **3.4 Sequence Diagram** — nhóm tương ứng với 3.2/3.3, gồm 22 case và hai biến thể API; các module tiếp nối có tham chiếu rõ. Không thêm danh mục điều hướng hoặc mục thiết kế.
5. **3.5 Non-functional Requirements** — bốn nhãn in đậm Performance Requirements, Operational Requirements, Security Requirements, Cultural and Political Requirements với các gạch đầu dòng như mẫu. Không đánh số 3.5.x, không chèn mã NFR hoặc nhãn Acceptance/Verification.

| Nhóm dùng đồng nhất ở 3.2/3.3/3.4 | Mã |
| --- | --- |
| User/shared | U1 Register; U2 Login with MFA; U3 Logout; U4 View/Track Escrows; U5 Open Dispute; U6 Submit Dispute Evidence; U7 Propose/Withdraw Full Refund; U8 Accept/Reject Refund Proposal |
| Buyer | B1 Create Escrow; B2 Cancel Unfunded Escrow; B3 Fund Escrow; B4 Confirm Acceptance and Request Release |
| Seller | S1 Accept/Reject Escrow Terms; S2 Record Delivery/Service Completion |
| Admin | A1 Review and Resolve Dispute; A2 Configure Escrow Policy Parameters; A3 View Basic Analytics; A4 View Audit Trail; A5 Reconcile Pending Transactions/Retry Confirmed-Failed Transfers |
| Payment Integration | P1 Confirm Funding; P2 Execute and Confirm Release; P3 Execute and Confirm Refund |

B1.API và U4.API là biến thể kênh Merchant của B1/U4, không tăng số use case thành 24. Các continuation sequence cũng không làm tăng số use case. Ma trận nghiệm thu có 16 đường cơ bản = 2 loại giao dịch × 2 funding × 4 kết quả, kèm các tình huống ngoại lệ/concurrency trong Controls.

## Quy trình sửa và tái tạo

1. Sửa đúng JSON đặc tả/Controls và bản diễn đạt ngắn trong `analysis/report_concise.py`; rà soát tác động lên toàn bộ điều kiện và trạng thái. Các mô hình/ngôn từ sơ đồ cũng được khai báo trong các builder, nên sửa JSON **không tự bảo đảm** mọi label/guard trong hình đã đổi. Cập nhật builder tương ứng khi nghiệp vụ thay đổi; không chỉ vá ảnh xuất hoặc TeX sinh tự động.
2. Chỉnh native `.drawio` trên đây làm nguồn chuẩn cho các hình hiện hành. Không chạy fresh-generation builders trên các nguồn hiện hành; sequence builder giữ cơ chế bảo vệ nguồn đã duyệt. Chỉ chạy builder khi thực sự tạo view mới hoặc tái tạo view được chọn từ JSON/builder đã cập nhật.
3. Dùng [render_diagrams.cjs](analysis/render_diagrams.cjs) với `--current` để render **native draw.io** đúng danh sách trong ba manifest: 7 overview (6 được report dùng),22 activity,57 sequence views/24 logical sequences. Giữ thư viện chính thức và giấy phép trong `analysis/vendor/drawio`; renderer tạo PNG/SVG/PDF cùng tên và dữ liệu kiểm tra theo SHA-256. Không thay bằng ảnh chứa toàn bộ sơ đồ như một bitmap trong file `.drawio`.
4. Chạy [finalize_assets.py](analysis/finalize_assets.py): kiểm tra ID/edge và export còn khớp nguồn, ghép board 86 trang và board sequence 57 trang, sao chép asset vào project LaTeX. Script chỉ chấp nhận PDF nguồn chuẩn trong project nếu SHA-256 khớp `1cf077ae8e1794a04857f9e48fe70f965f5d57c56b2384854cf8e112d74b7435`; không thay bằng file khác. Kiểm tra `analysis/Artifact_Validation.json`; đây là kiểm tra artifact, không phải test hệ thống EPS.
5. Chạy [build_report_content.py](analysis/build_report_content.py): sinh lại `sections/analysis.tex`, dùng chung `sections/sequence.tex` cho mục 3.4, [EPS_Analysis.md](EPS_Analysis.md), ma trận truy vết và ghi chú Planning. Builder tự lấy số view hiện hành và kiểm tra tám trường/22 case, nhãn hình/tham chiếu. LaTeX dùng `diagrams/...pdf`; Markdown dùng `analysis/diagrams/...png`.
6. Chạy `python EPS_Report_LaTeX/build_pdf.py` (cần pypdf và pdflatex). Script biên dịch **hai lượt** cho cả ba PDF để cập nhật tham chiếu, rồi ghép các page object PDF gốc với Analysis để giữ nguyên trang Introduction/Planning. Xem diagnostics, sửa lỗi nguồn, biên dịch lại; kiểm tra PDF thực tế về tràn bảng, cỡ chữ, hình cắt/mờ và trang chỉ có tiêu đề. Giữ tùy chọn `clip` ở macro hình để nội dung vector ngoài khung không che đầu trang. Chạy `analysis/verify_report_pdf.py` sau khi biên dịch; giữ toàn bộ `.tex`, `.drawio`, ảnh xuất và ba PDF cuối khi bàn giao. Project hiện có 7 overview, 22 activity, 57 sequence views; report có 85 hình (không tính overview map).

Ví dụ thứ tự chạy (AI lấy đường dẫn Python/Node từ `load_workspace_dependencies`, gán vào `$epsPython` và `$epsNode` trước; thư mục hiện hành là workspace EPS):

```powershell
& $epsNode analysis/render_diagrams.cjs --current
& $epsPython analysis/finalize_assets.py
& $epsPython analysis/build_report_content.py
& $epsPython EPS_Report_LaTeX/build_pdf.py
& $epsPython analysis/verify_report_pdf.py
& $epsPython analysis/finish_delivery.py --pack
```

Nguồn native hiện hành là chuẩn cho các lần bảo trì tiếp theo. Quy trình thường dùng là sửa `.drawio` được chọn, render lại các trang hiện hành, finalize exports, sinh lại nội dung báo cáo, biên dịch ba PDF, xác minh và đóng gói. Không tái tạo toàn bộ thư viện hoặc đổi nghiệp vụ khi không được yêu cầu. Checkpoint và thư mục trial đầy đủ được giữ trong workspace; gói portable chỉ chứa chứng cứ in B3 và các tệp đo lường/so sánh được liên kết.
