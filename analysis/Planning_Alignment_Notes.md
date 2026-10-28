# Ghi chú đồng bộ Introduction / Planning với Analysis

Ghi riêng các điểm cần nhóm rà soát khi hợp nhất report; không sửa PDF Introduction và Planning đã cung cấp. Analysis tuân theo MVP đã chốt. Đây không phải kết quả kiểm thử hay kết luận tuân thủ pháp lý.

## ALIGN01 — Tên hệ thống

Chuẩn hóa toàn bộ chương Analysis thành Escrow Payment System (EPS). Nếu Introduction/Planning dùng IPS hoặc tên khác, ghi đây là điểm cần đồng bộ khi nhóm chỉnh sửa bản nguồn; không tự sửa hai chương PDF đã có.

## ALIGN02 — Vision và MVP

Phân biệt tầm nhìn trong Introduction/Planning với phạm vi học phần tại 2.4.1. Chương Analysis chỉ đặc tả escrow giả lập VND, một buyer/một seller và thanh toán toàn phần một lần. Tiền thật, cross-border, đa tiền tệ, milestone, chia tiền, provider thật và tính phí được ghi là hướng phát triển; không âm thầm đưa vào MVP.

## ALIGN03 — Các phát biểu pháp lý

Các phát biểu pháp lý/quy định trong Planning chưa được xác minh bằng nguồn pháp lý hiện hành trong công việc này. Không dùng chúng để khẳng định MVP đã tuân thủ pháp luật hoặc đủ điều kiện vận hành tiền thật; nếu triển khai thực tế cần một đợt rà soát pháp lý riêng có nguồn.

## ALIGN04 — 21 tuần và công việc song song

Timeline nguồn tại trang PDF 9–10 (trang in 12–13) nêu Analysis 2 tuần; System/UI 3 tuần; Backend 7 tuần; Frontend 5 tuần và ghi rõ song song Backend; Dispute Workflow Integration 2 tuần; Testing/Security/Deployment 2 tuần, đồng thời kết luận tổng 21 tuần. Cộng các số theo tuần tự được 21, nhưng frontend song song backend khiến 21 tuần chưa được chứng minh là thời gian đường găng. Nhóm cần làm rõ phụ thuộc và mức độ chồng lấn; không tự tính lại một thời lượng cuối cùng khi chưa có phụ thuộc, và không sửa PDF gốc.

## ALIGN05 — Giới hạn kết cấu và bằng chứng

Giữ đúng 3.1→3.5 và cùng 22 mã use case trong đặc tả, activity, sequence; hai biến thể API dùng lại B1/U4. Tài liệu này là đặc tả phân tích và kịch bản nghiệm thu, không phải bằng chứng hệ thống đã được xây dựng hoặc kiểm thử. NFR p95 ≤ 2 giây là mục tiêu đề xuất, chưa phải số đo.

## Mặc định nghiệp vụ đã khóa

- Tiền giả lập, VND nguyên, một buyer/một seller khác nhau; hàng hóa hoặc dịch vụ; payout toàn phần một lần.
- Seller chấp thuận trước funding; buyer xác nhận điều khoản khi nạp tiền. Merchant là OAuth client được cấp sẵn, gắn với seller, chỉ tạo/tra cứu giao dịch của client.
- Đề nghị PENDING chặn ghi nhận bàn giao mới và giải ngân thường. Từ chối/rút khôi phục thao tác hợp lệ mà không đảo ngược bàn giao đã lưu.
- Chỉ một dispute; mở dispute vô hiệu hóa đề nghị chờ. Admin ghi lý do và chốt một hướng payout, sau đó chờ provider xác nhận.
- Timeout/UNKNOWN chỉ đối soát cùng attempt. Funding thất bại có xác nhận không thu tiền trả về AWAITING_FUNDING để buyer retry/hủy. Payout thất bại giữ trạng thái pending và chỉ retry cùng hướng sau xác nhận không chuyển tiền.

## Sơ đồ và tệp nguồn

Có 6 view use-case, 22 activity và 57 view sequence cho 24 luồng logic (22 use case chính và hai biến thể API). Continuation không làm tăng số use case.

- Giữ main.tex và sections/analysis.tex trong EPS_Report_LaTeX cùng toàn bộ nguồn .drawio và ảnh xuất.
- PDF được biên dịch và kiểm tra trình bày riêng. PNG phục vụ xem nhanh; PDF vector phục vụ LaTeX.
- EPS_Analysis.md là bản nội dung đồng hành. Traceability_and_Acceptance.md giữ truy vết/nghiệm thu bên ngoài chương 3, không tạo mục 3.6.
