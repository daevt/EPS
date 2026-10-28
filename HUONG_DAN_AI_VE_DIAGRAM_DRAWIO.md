# Hướng dẫn AI vẽ diagram bằng draw.io theo cách đã dùng trong EPS

Tài liệu này có thể gửi cho một AI khác để tạo hoặc chỉnh diagram có cùng cách trình bày và quy trình kiểm tra như thư viện EPS. Hướng dẫn viết bằng tiếng Việt; tiêu đề, actor, action, message và ghi chú nằm trong diagram dùng tiếng Anh, trừ khi người dùng yêu cầu khác.

## 1. Chỉ dẫn cốt lõi cho AI

Bạn phải tạo **file `.drawio` chỉnh sửa được bằng từng shape, text và connector**, kèm bản xuất để người dùng xem. Dùng draw.io/diagrams.net làm định dạng nguồn. Không chỉ trả về mô tả, mã Mermaid hoặc một ảnh phẳng.

Thực hiện trọn quy trình: đọc yêu cầu → xác định nội dung/ngữ nghĩa → chọn bố cục → tạo hoặc sửa native draw.io → kiểm tra cấu trúc → render → xem hình thực tế → sửa lỗi trong phạm vi cần thiết → bàn giao.

- Ưu tiên yêu cầu mới nhất của người dùng. Giữ nguyên mẫu đang được dùng nếu chỉ được yêu cầu sửa cục bộ.
- Tách rõ **đổi nội dung nghiệp vụ** và **đổi cách trình bày**. Yêu cầu làm đẹp, tăng khoảng cách hoặc ghép trang không cho phép tự bỏ nhánh lỗi, guard, message hay business rule.
- Tạo file thật trong thư mục làm việc. Không dừng ở việc hướng dẫn người dùng tự vẽ.
- Hỏi bổ sung khi thiếu thông tin làm thay đổi đáng kể ý nghĩa sơ đồ. Với lựa chọn nhỏ về căn chỉnh, khoảng cách và tên file, tự xử lý theo mẫu.
- Không tuyên bố đã mở file, render hoặc kiểm tra thành công nếu chưa thực hiện. Kiểm tra diagram không phải kiểm thử ứng dụng.

## 2. File mẫu và nguồn chuẩn

Nếu đang làm trong project EPS, đọc các file sau theo nhu cầu. Đường dẫn bên dưới tính từ thư mục gốc của project.

| File | Vai trò |
| --- | --- |
| `AI_Reuse_Guide.md` | Phạm vi, nguồn nội dung, mã use case và quy tắc nghiệp vụ hiện hành. |
| `analysis/diagrams/overview/UC_Buyer.drawio` và `.png` | Ví dụ use case: actor bên ngoài, use case trong system boundary, màu dịu và nhãn rõ. |
| `analysis/diagrams/activity/AD_B3.drawio` và `.png` | Ví dụ activity: lane theo trách nhiệm, action, decision, guard và đường đi ngoại lệ. |
| `analysis/diagrams/sequence/SD_B3.drawio` và `.png` | Ví dụ sequence đã chỉnh: chữ nghiệp vụ 14 px, actor/boundary/control/entity, `alt`, `ref`, activation và note. |
| `analysis/diagrams/sequence/SD_B3_funding.drawio` | Ví dụ phần sequence tiếp nối được giữ riêng. |
| `analysis/overview_manifest.json`, `activity_models.json`, `sequence_models.json` | Danh sách view đang dùng, tên file và liên hệ giữa main/continuation. |
| `analysis/Selective_Sequence_Implementation.md` | Quyết định ghép/tách sequence và bằng chứng khả năng đọc khi in A4. |
| `analysis/render_diagrams.cjs` | Xuất PNG, SVG, PDF bằng thư viện draw.io chính thức đã lưu trong project. |
| `analysis/finalize_assets.py` | Kiểm tra, ghép board và đồng bộ asset sang project báo cáo. |

**Nguồn chuẩn để bảo trì hình hiện hành là native `.drawio` cùng manifest hiện hành.** JSON đặc tả/controls là căn cứ nghiệp vụ; builder lưu cách sinh hình ban đầu nhưng có thể chưa chứa các chỉnh sửa native đã được chấp nhận sau đó.

Không chọn bản trong `tmp/`, `checkpoint/`, `sequence_trials/` hoặc thư mục đóng gói làm nguồn mới nhất chỉ vì tên gần giống. Không ghi đè nguồn hiện hành bằng một bản sinh lại từ builder cũ.

Nếu dùng hướng dẫn này cho project khác, áp dụng quy trình và style dưới đây với nguồn nghiệp vụ của project đó. Nếu muốn bám chính xác mẫu EPS, gửi kèm ít nhất một file `.drawio` và ảnh preview tương ứng; đừng phụ thuộc vào đường dẫn trên máy cũ.

## 3. Chuẩn bị nội dung trước khi vẽ

1. Xác định loại diagram: use case, activity hay sequence; đối tượng đọc; phạm vi; định dạng bàn giao và nơi sử dụng, nhất là khi chèn vào báo cáo A4.
2. Đọc đặc tả hoặc nguồn được chỉ định. Lập danh sách actor/participant, action/message, quan hệ, điều kiện và kết quả.
3. Với luồng nghiệp vụ, giữ đủ trigger, tiền điều kiện, nhánh chính, nhánh lỗi, trạng thái chờ và hậu điều kiện có trong nguồn.
4. Gắn mã ổn định để đối chiếu giữa đặc tả và các loại diagram. Một use case xuất hiện trên nhiều view vẫn giữ cùng mã.
5. Xác định những gì chưa rõ. Không tự thêm module, API, database table, quyền hạn hay chức năng chỉ để làm hình trông đầy đủ hơn.
6. Dự kiến số cột/lane/lifeline và khoảng trống dành cho connector trước khi đặt shape.

Với EPS, xem `AI_Reuse_Guide.md` để lấy đầy đủ quy tắc. Ví dụ bắt buộc: funding chỉ thành công sau xác nhận provider hợp lệ; redirect không tạo `HELD`; `UNKNOWN` giữ pending; retry chỉ sau confirmed failure; release/refund là toàn phần. Khi đổi bố cục, giữ nguyên các điều kiện này.

## 4. Style hình ảnh cần giữ

Mục tiêu là diagram sáng, dễ đọc, ít trang trí, phù hợp báo cáo học thuật. Dùng nền trắng, chữ đậm màu, các khối có chức năng rõ và legend ngắn khi cần.

| Thành phần | Quy ước theo mẫu EPS |
| --- | --- |
| Font | Helvetica; có thể dùng Arial nếu môi trường không có Helvetica, nhưng dùng nhất quán. |
| Nhãn nội dung chính | Mốc 14 px ở native source: action, decision, participant, message, guard và ref. |
| Tiêu đề | Activity/sequence thường 16 px, đậm. Overview có hệ tiêu đề riêng lớn hơn; giữ theo file mẫu của đúng loại. |
| Subtitle / legend | Thường 12 px / 11 px; không dùng cỡ phụ này để thu nhỏ message hoặc guard cho vừa trang. |
| Nội dung xanh | Fill `#dae8fc`, stroke `#6c8ebf`: action chính, EPS boundary/control hoặc use case chính tùy loại hình. |
| Nội dung vàng | Fill `#fff2cc`, stroke `#d6b656`: decision hoặc business constraint tùy loại hình. |
| Nội dung xám | Fill `#f5f5f5`, stroke `#666666`: exception, entity, external mock hoặc use case tham chiếu tùy loại hình. |
| Chữ | Màu tối như `#243447` hoặc `#222222`, theo mẫu đang chỉnh. |
| Activation sequence | Thân trắng, viền xanh `#6c8ebf`, thanh hẹp gắn với lifeline. |
| Connector | Nét mảnh, rõ hướng; ưu tiên đường thẳng hoặc gấp khúc dễ theo dõi. |

Màu có nghĩa theo **từng loại diagram**, không phải một bộ nghĩa chung cho mọi hình. Legend phải mô tả đúng những gì có trên trang.

Không đồng loạt đổi font hoặc màu của các hình đã duyệt khi chỉ sửa một hình. Với note cũ có cỡ chữ riêng, giữ mẫu trừ khi đang được yêu cầu đồng bộ; note nghiệp vụ trong bản B3 đã chỉnh dùng 14 px.

Ưu tiên mở rộng shape, ngắt dòng có chủ đích, tăng khoảng cách và chuyển vị trí. Không tăng chữ lên quá lớn rồi để đè nhau; không thu nhỏ toàn bộ nội dung để ép vào một trang.

## 5. Quy tắc theo từng loại diagram

### 5.1. Use case diagram

- Actor dùng shape UML actor và đặt ngoài system boundary; use case dùng ellipse, nằm trong boundary tương ứng.
- Nhãn có mã và tên, ví dụ `B3  Fund Escrow`. Các view theo vai trò vẫn giữ identity của use case được tham chiếu.
- Association actor–use case theo mẫu là nét liền, không mũi tên. Không biến quan hệ này thành luồng tuần tự.
- Chỉ dùng `«include»`, `«extend»` hoặc generalization khi nguồn thực sự có quan hệ đó. Nếu có, dùng đúng hướng: include trỏ tới use case được bao gồm; extend trỏ tới use case cơ sở; tam giác generalization trỏ tới actor/use case tổng quát.
- Chia thành các view tập trung khi hình tổng quá nhiều cạnh. Overview map có thể dùng để điều hướng, không thay thế các view UML chi tiết.

### 5.2. Activity diagram

- Dùng các lane đặt cạnh nhau theo actor/hệ thống chịu trách nhiệm; thời gian/luồng chính đi từ trên xuống.
- Action là hình chữ nhật bo góc; decision là hình thoi; initial là chấm đen; activity final là vòng tròn có chấm đen bên trong.
- Action nằm trong đúng lane. Dùng parent là lane và tọa độ tương đối để kéo lane vẫn giữ được nội dung bên trong.
- Decision có guard rõ trên nhánh đi ra, ví dụ `[valid]`, `[invalid]`, `[confirmed success]`, `[pending / unknown]`. Không để đường rẽ không có ý nghĩa.
- Bố trí nhánh lỗi ở cột bên cạnh; chừa hành lang connector; tránh đưa cạnh qua action hoặc nhãn khác.
- Chỉ nối lại các nhánh nếu nghiệp vụ thực sự hội tụ. Không tự tạo đường trở về luồng chính sau kết quả lỗi.
- Theo mẫu B3, action thường khoảng 240 × 80, decision khoảng 240 × 100, header lane 40 đơn vị; đây là điểm bắt đầu bố cục, có thể điều chỉnh theo nội dung.

### 5.3. Sequence diagram

- Participant đặt theo vai trò từ trái sang phải: actor → boundary/UI → control → entity; thêm external provider khi thực sự tham gia luồng. Không thêm participant chỉ để trang cân đối.
- Dùng native lifeline có đường sống nét đứt; thời gian đi xuống. Giữ thứ tự và định danh participant nhất quán giữa main và continuation.
- Có thể dùng stereotype `«boundary»`, `«control»`, `«entity»` như mẫu EPS. Đây là mức tương tác phân tích, không tự chuyển thành thiết kế lớp hoặc implementation API.
- Message phải nối đúng sender/receiver hoặc activation tương ứng. Không dùng một đường trang trí đặt cạnh text để giả làm connector.
- Request trong mẫu dùng nét liền, đầu mũi tên đặc (`endArrow=block`). Return dùng nét đứt, đầu mở, đường màu xám. Các async event hiện có phải giữ loại message, nhãn và legend của nguồn; không suy diễn mọi nét đứt đều là return.
- Activation là cell con của lifeline tương ứng, không parent nhầm sang `alt`/`ref`. Điều chỉnh đầu/cuối thanh theo khoảng xử lý của luồng.
- `alt`, `opt`, `loop`, `ref` phải phản ánh cấu trúc thật. Guard thuộc đúng operand; message nằm dưới guard; separator không đè lên chữ hoặc ref frame.
- Dành đủ hàng cho message nhiều dòng. Thay đổi vị trí hàng và kích thước frame trước khi thay đổi cỡ chữ.
- Khi tạo sequence mới, ưu tiên engine bố cục như `drawio-skill/scripts/seqlayout.py` cho lifeline/message/activation, rồi xử lý fragment/ref theo nội dung. Đọc schema của engine trước khi cấp JSON; không tự đoán tham số.

**Sequence dài và phần tiếp nối:**

- Một logical sequence có thể có main và nhiều continuation. Dùng ref có mã đích rõ, ví dụ `SD B3_funding — ...`, kèm điều kiện khi gọi phần đó.
- Tách view ở ranh giới nghiệp vụ có nghĩa, không cắt giữa một nhóm message khiến guard hoặc kết quả mất liên hệ.
- Ghép view chỉ khi giữ nguyên message, sender/receiver, guard, thứ tự, nesting, note và ref còn cần thiết; đồng thời bản in vẫn dễ đọc.
- Trong EPS hiện hành, chỉ `B3 + B3_outcomes` đã được chấp nhận ghép; `B3_funding` vẫn riêng. Không tự ghép lại các cặp khác đã được giữ riêng.
- Không tự tái tạo toàn bộ sequence hiện hành: fresh builder có cơ chế chống ghi đè; các merge/trial/promotion script lịch sử đã thành no-write stub. Sửa nguồn native được chọn rồi render lại.

## 6. Native draw.io và cách sửa XML

AI có thể dùng UI draw.io hoặc viết/sửa XML trực tiếp. Viết XML là cách hợp lệ nếu file mở được bằng draw.io và các thành phần vẫn chỉnh sửa riêng lẻ.

- Dùng cấu trúc `mxfile → diagram → mxGraphModel → root`.
- Có cell gốc `id="0"` và layer `id="1" parent="0"`. Các shape/edge khác dùng ID riêng, ổn định và không trùng trong trang.
- Shape dùng `vertex="1"`; connector nghiệp vụ dùng `edge="1"`, `source`, `target` trỏ tới cell tồn tại. Đường separator tự do có thể dùng `sourcePoint`/`targetPoint` thay cho endpoints gắn cell; không tự gắn chúng vào participant hoặc action.
- Mỗi edge phải có `<mxGeometry relative="1" as="geometry"/>`.
- Geometry của cell con tính theo parent. Khi đổi parent, đổi tọa độ tương ứng để giữ vị trí và ngữ nghĩa.
- Escape XML đúng: `&amp;`, `&lt;`, `&gt;`, `&quot;`. Nếu `html=1`, nội dung HTML trong attribute cũng phải được escape, ví dụ `&lt;br&gt;`.
- Có thể dùng waypoint và pin entry/exit để tránh vật cản. Kiểm tra đường đã render, không kết luận từ tọa độ nguồn.
- Giữ metadata đang có như `data-model-id`, `data-ref`, `data-source-view`, `data-source-index` và provenance; không đổi ID tùy tiện khi sửa cục bộ.
- Không nhúng PNG của cả sơ đồ vào một cell rồi gọi đó là native diagram. Không nhúng dữ liệu bí mật vào metadata.

Ví dụ XML tối thiểu để thấy cấu trúc shape và connector; đây là minh họa kỹ thuật, không thay cho template UML:

```xml
<mxfile host="app.diagrams.net">
  <diagram id="example" name="Example">
    <mxGraphModel grid="1" gridSize="10" background="#ffffff">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="start" value="Validate request"
          style="rounded=1;whiteSpace=wrap;html=1;fontFamily=Helvetica;fontSize=14;fillColor=#dae8fc;strokeColor=#6c8ebf;"
          vertex="1" parent="1">
          <mxGeometry x="100" y="80" width="240" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="result" value="Return permitted result"
          style="rounded=1;whiteSpace=wrap;html=1;fontFamily=Helvetica;fontSize=14;fillColor=#dae8fc;strokeColor=#6c8ebf;"
          vertex="1" parent="1">
          <mxGeometry x="100" y="240" width="240" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="flow" style="edgeStyle=orthogonalEdgeStyle;html=1;endArrow=block;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"
          edge="1" parent="1" source="start" target="result">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## 7. Quy trình tạo mới và chỉnh sửa

**Khi tạo mới:** lập mô hình nội dung trước, chọn file mẫu cùng loại, rồi tạo file mới với ID và nội dung của tác vụ. Nếu đồ thị lớn, dùng bố cục tự động hoặc theo lane/hàng; không đặt thủ công mọi node một cách tùy hứng. Có skill draw.io thì đọc `SKILL.md` và reference đúng loại diagram trước khi dùng script.

**Khi chỉnh file hiện có:**

1. Chọn đúng native file từ manifest; đọc cả XML và preview để hiểu cấu trúc, style và điểm cần sửa.
2. Lưu bản trước sửa hoặc bản candidate riêng nếu đổi bố cục đáng kể. Không dùng thư mục checkpoint cũ làm nơi ghi output.
3. Chỉ đổi cell liên quan; giữ hình không thuộc phạm vi và tránh auto-layout toàn trang khi chỉ cần một sửa nhỏ.
4. So sánh trước/sau về nội dung, endpoints, guard, fragment, note và ref. Đổi bố cục phải giữ nguyên nghĩa.
5. Nếu thêm/tách/ghép view, cập nhật manifest, ref và nơi dùng liên quan. Không để trang mồ côi hoặc ref trỏ tới file đã bỏ.
6. Render candidate, kiểm tra rồi mới thay vào bộ nguồn hiện hành. Ghi rõ những file thực sự thay đổi.

## 8. Render và kiểm tra bằng công cụ

### Trong project EPS

Các ví dụ chạy từ thư mục gốc EPS bằng PowerShell. Cần Python, Node.js, `playwright-core` và Chrome cho các công cụ tương ứng. Xác định executable thực tế trước khi chạy; trong Codex có thể dùng `load_workspace_dependencies` để tìm runtime. Không giả định AI trên máy khác có cùng đường dẫn cài đặt.

```powershell
# Chỉ chạy sau khi đã xác nhận Python và Node thực sự có sẵn.
$epsPython = (Get-Command python -ErrorAction Stop).Source
$epsNode = (Get-Command node -ErrorAction Stop).Source

# Thay đường dẫn skill nếu đang dùng máy khác.
$drawioSkill = 'C:/Users/lenovo/.codex/skills/drawio-skill'
& $epsPython "$drawioSkill/scripts/validate.py" 'analysis/diagrams/sequence/SD_B3.drawio' --score

# Render một nguồn native được chọn; ghi PNG/SVG/PDF cạnh file nguồn.
& $epsNode 'analysis/render_diagrams.cjs' 'analysis/diagrams/sequence/SD_B3.drawio'

# Chỉ khi cần refresh toàn bộ bộ hình hiện hành theo ba manifest.
& $epsNode 'analysis/render_diagrams.cjs' --current
```

- Renderer EPS dùng `analysis/vendor/drawio/viewer.html` và official viewer bundle được lưu kèm; giữ `NOTICE.md` và `LICENSE`. Script chặn HTTP/HTTPS khi render.
- Renderer ghi DOM evidence vào `analysis/.render-cache/dom/`, gồm text bounding boxes, edge paths và `sourceSha256`. Dùng hash để kiểm tra preview có thực sự khớp XML vừa sửa.
- Nếu Chrome ở vị trí khác, đặt biến môi trường `CHROME_PATH` tới executable thực tế mà script hỗ trợ.
- **Chỉ đưa nguồn single-view vào renderer này.** Nó đọc `mxGraphModel` đầu tiên, nên không dùng trực tiếp để xuất mọi trang của board nhiều trang như `EPS_Analysis_Diagrams.drawio`.
- Khi xuất cả bộ, dùng `--current`; không quét thư mục lịch sử rồi coi tất cả trial/superseded view là hiện hành.
- `analysis/check_sequence_render.py` là công cụ kiểm tra bổ sung: mặc định cũ yêu cầu 58 view, trong khi bộ hiện hành có 57. Nếu dùng, lấy số lượng từ manifest và truyền `--require-views` đúng giá trị. Không xem báo cáo audit cũ là bằng chứng cho lần sửa mới; nhãn có ID được prefix khi ghép cũng cần kiểm tra DOM/ảnh riêng.

Nếu tác vụ bao gồm đồng bộ thư viện hoặc báo cáo, sau khi nguồn/export đã đạt yêu cầu mới chạy các bước tương ứng. `finalize_assets.py` cần `pypdf`; chuỗi dựng và xác minh report còn cần `pdflatex` cùng các thư viện Python `pypdf`, `pypdfium2`, `Pillow`, `pdfplumber`. Kiểm tra môi trường trước khi chạy:

```powershell
& $epsPython 'analysis/finalize_assets.py'

# Chỉ cần khi phải cập nhật và bàn giao cả report.
& $epsPython 'analysis/build_report_content.py'
& $epsPython 'EPS_Report_LaTeX/build_pdf.py'
& $epsPython 'analysis/verify_report_pdf.py'
& $epsPython 'analysis/finish_delivery.py' --pack
```

`finalize_assets.py` cập nhật các board và bản sao asset của báo cáo. Không chạy các bước sửa/sinh report chỉ để trả lời một yêu cầu vẽ hình độc lập. Số view phải lấy từ manifest; tại thời điểm viết hướng dẫn, EPS có 7 overview, 22 activity và 57 sequence view cho 24 logical sequence.

### Khi không có bộ script EPS

Mở file bằng draw.io Desktop/diagrams.net và export, hoặc dùng CLI draw.io đã được xác nhận có trên máy. Với CLI, thay `drawio` bằng đúng executable tìm được:

```powershell
# Draft PNG để kiểm tra; không nhúng XML vào bản dùng để xem hình.
drawio -x -f png --width 2000 -o diagram.preview.png diagram.drawio

# Bản xuất vector.
drawio -x -f svg -o diagram.svg diagram.drawio
drawio -x -f pdf -o diagram.pdf diagram.drawio
```

Không kết hợp `--width` và scale `-s`. Nếu cần PNG có nhúng nguồn, dùng quy trình riêng của skill và `repair_png.py`; file `.drawio` gốc vẫn là deliverable bắt buộc. Nếu chưa render được, bàn giao native file và nói rõ phần kiểm tra còn thiếu, không giả lập kết quả xuất.

## 9. Checklist trước khi bàn giao

### Nội dung và cấu trúc

- [ ] Actor, use case code, message, trạng thái, guard và kết quả khớp nguồn nghiệp vụ.
- [ ] Không mất nhánh lỗi, timeout/pending, quyền hạn, note hay ref quan trọng khi làm gọn.
- [ ] XML hợp lệ; ID không trùng; các parent/source/target được khai báo đều tồn tại; edge có relative geometry; separator tự do có tọa độ endpoint hợp lệ.
- [ ] Mở được bằng draw.io và chọn/sửa được từng shape, label, connector.
- [ ] Main/continuation, manifest và tham chiếu thống nhất nếu tác vụ có thay đổi chúng.

### Hình đã render

- [ ] Đã xem ảnh export thực tế của các view vừa sửa, không chỉ đọc XML hoặc log validator.
- [ ] Chữ không đè chữ, shape, mũi tên, header hoặc fragment separator; label không bị cắt.
- [ ] Connector không xuyên shape không liên quan; không có cạnh chồng nhau khiến mất hướng đi.
- [ ] Guard/ref đúng vùng, activation đúng lifeline, note đủ chỗ và legend mô tả đúng trang.
- [ ] Font nội dung nhất quán, màu theo mẫu; không dùng cỡ chữ nhỏ để che vấn đề bố cục.
- [ ] SVG/PDF thực sự có chất lượng vector phù hợp; nếu cần, kiểm tra text trong PDF có chọn được.
- [ ] Hash nguồn/export còn khớp sau lần sửa cuối.

Validator chỉ kiểm tra được một phần. Các cảnh báo overlap có thể là lồng ghép hợp lệ của lane/frame/lifeline; phải phân loại bằng ảnh hoặc DOM, không bỏ qua hàng loạt và cũng không di chuyển mọi container chỉ để xóa cảnh báo.

Sau tối đa hai vòng tự sửa bố cục bằng đánh giá ảnh, không lặp auto-layout vô hạn. Chọn bố cục/tách view đã kiểm chứng hoặc báo rõ điểm chưa đạt; sửa cục bộ có bằng chứng khi cần.

### Khi đưa vào báo cáo A4

Phải kiểm tra trang PDF cuối với khung hình, lề, header/footer và caption thực tế. `14 px` trong native source không bảo đảm khi in vẫn đọc được. Không dùng riêng công thức `px × 0.75` để kết luận cỡ chữ sau khi hình bị scale; đo glyph từ PDF đã biên dịch hoặc kiểm chứng tương đương.

EPS dùng ngưỡng đã thống nhất là **ít nhất 9 pt cho chữ nghiệp vụ trong proof sequence**. Ngưỡng này là yêu cầu của project, không phải tiêu chuẩn mặc định của draw.io. Với B3 đã chấp nhận, proof A4 portrait dùng khung `510 × 700 bp` và đo được minimum `9.103 pt`; đây là số của bản đã kiểm chứng, phải đo lại nếu sửa hình hoặc cách chèn. Những view không đạt thì giữ/tách continuation thay vì bỏ nội dung hoặc ép ghép.

## 10. Bàn giao

Với một diagram độc lập, tối thiểu cung cấp:

- `diagram.drawio`: nguồn native chỉnh sửa được.
- `diagram.preview.png`: ảnh xem nhanh đã kiểm tra.
- `diagram.svg` hoặc `diagram.pdf` nếu cần chèn báo cáo/in; trong EPS giữ đủ PNG/SVG/PDF theo renderer.
- Ghi chú ngắn: đã vẽ/sửa gì, đã kiểm tra bằng cách nào và điểm nào còn chưa xác minh.

Không cập nhật ZIP, toàn bộ report hoặc nguồn nghiệp vụ ngoài phạm vi chỉ vì chúng nằm cùng thư mục. Khi yêu cầu có bao gồm thư viện/report, đồng bộ các artifact liên quan để tránh ảnh cũ và ref sai.

## 11. Prompt mẫu gửi cho AI khác

Copy phần sau, điền yêu cầu và gửi kèm file hướng dẫn này cùng file mẫu/đặc tả liên quan:

```text
Hãy dùng hướng dẫn trong HUONG_DAN_AI_VE_DIAGRAM_DRAWIO.md để tạo hoặc chỉnh
diagram bằng draw.io, theo style của các file mẫu tôi gửi kèm.

Nhiệm vụ cụ thể: [loại diagram, nội dung hoặc phần cần sửa].
Nguồn nghiệp vụ: [đặc tả / code / tài liệu].
File mẫu hoặc file hiện hành: [đường dẫn hoặc attachment].
Nơi dùng và đầu ra: [xem màn hình / báo cáo A4; thư mục; định dạng cần thêm].

Tạo file .drawio native có thể chỉnh từng thành phần, kèm PNG preview.
Nhãn trong diagram bằng tiếng Anh. Giữ font, màu, mã định danh và quy ước UML
theo đúng loại hình trong mẫu. Với yêu cầu đổi bố cục, giữ nguyên nghiệp vụ.
Nếu sequence quá dài, dùng continuation/ref rõ ràng để bảo đảm đọc được.
Render và xem hình thực tế, sửa lỗi chữ/connector/frame rồi bàn giao file.
Nếu có bước chưa chạy được, nói rõ bước đó; không tuyên bố đã kiểm tra.
```
