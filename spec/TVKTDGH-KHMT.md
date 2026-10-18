# TVKTĐGH/KHMT — Tiếng Việt Kỹ thuật Đơn giản hóa cho Khoa học Máy tính

**Simplified Technical Vietnamese for Computer Science (STV-CS)**  
Phiên bản 0.1.0 <!-- x-release-please-version -->

TVKTĐGH/KHMT là chuẩn ngôn ngữ kiểm soát cho tài liệu khoa học máy tính bằng tiếng Việt.
Chuẩn này phỏng theo nguyên tắc của ASD-STE100 Issue 9. Chuẩn này không phải bản dịch của ASD-STE100.

TVKTĐGH là viết tắt của **T**iếng **V**iệt **K**ỹ **t**huật **Đ**ơn **g**iản **h**óa.
KHMT là viết tắt của **K**hoa **h**ọc **M**áy **t**ính.

<!-- BEGIN STANDARD -->

---

## 0. Phạm vi và kiến trúc

### 0.1 Mục đích

Chuẩn này giúp tác giả và agent tạo tài liệu rõ ràng, nhất quán và dễ kiểm tra.
Chuẩn giảm cách diễn đạt cho cùng một ý. Chuẩn không làm đơn giản nội dung kỹ thuật.

### 0.2 Phạm vi

Dùng chuẩn này cho các loại nội dung sau:

- Tài liệu thiết kế.
- README và hướng dẫn API.
- Runbook và báo cáo sự cố.
- Ghi chú review code và mô tả pull request.
- Tài liệu machine learning (học máy) và dữ liệu.
- Câu trả lời kỹ thuật do agent tạo.

Không mặc định dùng chuẩn này cho hợp đồng, văn bản pháp lý hoặc nội dung tiếp thị.

### 0.3 Ba lớp của chuẩn

1. **Chuẩn lõi** quy định từ, câu, thủ tục, mô tả và cảnh báo.
2. **KHMT profile** quy định thuật ngữ và cách viết token kỹ thuật.
3. **Agent profile** quy định cấu trúc và độ tin cậy của output do agent tạo.

### 0.4 Từ khóa quy phạm

- **PHẢI**: yêu cầu bắt buộc.
- **KHÔNG ĐƯỢC**: hành vi bị cấm.
- **NÊN**: khuyến nghị. Tác giả cần lý do khi không làm theo.
- **ĐƯỢC PHÉP**: hành vi được cho phép.

`Có khả năng` chỉ mô tả năng lực hoặc xác suất. Không dùng cụm này để cấp quyền.

### 0.5 Nguyên tắc ưu tiên

Nếu hai quy tắc xung đột, áp dụng thứ tự sau:

1. Giữ đúng thông tin và ý nghĩa.
2. Giữ nguyên token kỹ thuật và nội dung được trích dẫn.
3. Loại bỏ sự mơ hồ.
4. Rút ngắn câu và chuẩn hóa thuật ngữ.

---

# PHẦN 1 — CHUẨN LÕI

## Nhóm 1 — Từ và thuật ngữ

### QT 1.1 — Dùng dạng chuẩn của thuật ngữ

Tác giả PHẢI dùng dạng `canonical` trong từ điển kiểm soát.
Tác giả PHẢI dùng thuật ngữ với nghĩa và từ loại đã được duyệt.

Nếu từ điển chưa có thuật ngữ, tác giả PHẢI đề xuất entry mới. Tác giả KHÔNG ĐƯỢC tự dịch thuật ngữ trong tài liệu phát hành.

### QT 1.2 — Dùng một thuật ngữ cho một khái niệm

Trong cùng một tài liệu, tác giả PHẢI dùng một dạng chuẩn cho một khái niệm.
Không đổi từ chỉ để tránh lặp.

| Không dùng | Dùng |
|---|---|
| `service`, `dịch vụ`, `hệ thống phục vụ` | `service` |
| lỗi, bug, sự cố phần mềm | bug |

### QT 1.3 — Dùng từ phổ biến và trực tiếp

Tác giả NÊN dùng từ phổ biến khi từ đó giữ đúng nghĩa.
Tác giả KHÔNG ĐƯỢC dùng thành ngữ, lối nói bóng hoặc từ trang trí.

| Không dùng | Dùng |
|---|---|
| trong một tương lai không xa | sau khi deploy |
| khả dĩ | có khả năng |

### QT 1.4 — Giải thích từ viết tắt

Tác giả PHẢI giải thích từ viết tắt tại lần xuất hiện đầu tiên.
Viết cụm đầy đủ trước. Viết từ viết tắt trong ngoặc sau cụm đầy đủ.

Entry trong glossary được phép miễn quy tắc này bằng ghi chú `Không cần giải thích lần đầu`.
Giữ nguyên từ viết tắt tiếng Anh. Không tạo lại từ viết tắt tiếng Anh theo tiếng Việt.

Ví dụ: `cơ sở dữ liệu (CSDL)` và `continuous integration (CI)`.

### QT 1.5 — Tạo từ viết tắt tiếng Việt

Từ viết tắt tiếng Việt PHẢI lấy chữ cái đầu của từng tiếng.

| Cụm từ | Không dùng | Dùng |
|---|---|---|
| Tiếng Việt Kỹ thuật Đơn giản hóa | TVKĐ | TVKTĐGH |
| Khoa học Máy tính | `KHM` | KHMT |
| Cơ sở dữ liệu | `CSD` | CSDL |

## Nhóm 2 — Cụm danh từ và tham chiếu

### QT 2.1 — Giới hạn cụm danh từ không có từ nối

Một cụm danh từ không có từ nối NÊN có tối đa ba thành phần nghĩa.
Dùng `của`, `cho`, `trong`, `trên` hoặc một mệnh đề để tách cụm dài.

| Không dùng | Dùng |
|---|---|
| module xác thực người dùng hệ thống thanh toán | module xác thực người dùng của hệ thống thanh toán |

### QT 2.2 — Giữ danh từ chính rõ ràng

Đặt danh từ chính gần phần bổ nghĩa trực tiếp của nó.
Không để người đọc phải thử nhiều cách nhóm từ.

### QT 2.3 — Tránh tham chiếu mơ hồ

Không dùng `nó`, `cái này`, `việc này` hoặc `thành phần đó` khi có nhiều đối tượng có thể được nhắc đến.
Lặp lại danh từ chuẩn khi cần.

| Không dùng | Dùng |
|---|---|
| Service ghi cache vào database. Nó hết hạn sau 10 phút. | Service ghi cache vào cơ sở dữ liệu. Cache hết hạn sau 10 phút. |

## Nhóm 3 — Động từ, thời và thể

### QT 3.1 — Dùng câu chủ động

Trong câu hướng dẫn, tác giả PHẢI nêu tác nhân hoặc dùng động từ mệnh lệnh.
Trong câu mô tả, tác giả NÊN dùng câu chủ động khi biết tác nhân.

| Không dùng | Dùng |
|---|---|
| Request được xử lý bởi middleware. | Middleware xử lý request. |

### QT 3.2 — Dùng động từ chỉ hành động cụ thể

Không dùng `tiến hành`, `thực hiện` hoặc `xử lý` khi có động từ cụ thể.

| Không dùng | Dùng |
|---|---|
| Thực hiện việc cấu hình webhook. | Cấu hình webhook. |
| Xử lý response JSON. | Parse response JSON. |

### QT 3.3 — Dùng thời và thể đơn giản

Dùng hiện tại để mô tả hành vi ổn định.
Chỉ dùng `đã`, `đang`, `sẽ` hoặc `xong` khi quan hệ thời gian có ý nghĩa kỹ thuật.

### QT 3.4 — Tách yêu cầu, khuyến nghị, quyền và khả năng

Dùng `phải` cho yêu cầu. Dùng `nên` cho khuyến nghị.
Dùng `được phép` cho quyền. Dùng `có khả năng` cho năng lực hoặc xác suất.
Không dùng `có thể` khi người đọc không phân biệt được quyền và khả năng.

### QT 3.5 — Dùng `bị` và `được` có chủ ý

Được phép dùng `bị` để mô tả sự cố hoặc tác động bất lợi.
Không dùng cấu trúc `được ... bởi ...` khi có thể đặt tác nhân làm chủ ngữ.

| Không dùng | Dùng |
|---|---|
| Image được xóa bởi script. | Script xóa image. |
| Pod bị crash khi hết bộ nhớ. | Pod bị crash khi hết bộ nhớ. |

## Nhóm 4 — Câu

### QT 4.1 — Giới hạn độ dài câu

Câu thủ tục PHẢI có tối đa 20 token. Câu mô tả NÊN có tối đa 25 token.
Mục 8.4 định nghĩa cách đếm token.

### QT 4.2 — Viết một ý trong một câu

Một câu mô tả PHẢI có một chủ đề chính.
Tách các nguyên nhân, kết quả hoặc ngoại lệ độc lập thành câu riêng.

### QT 4.3 — Đặt điều kiện trước lệnh

Nếu người đọc cần biết điều kiện trước khi hành động, đặt điều kiện trước lệnh.

| Không dùng | Dùng |
|---|---|
| Rollback deploy nếu error rate vượt 1%. | Nếu error rate vượt 1%, rollback deploy. |

### QT 4.4 — Dùng từ nối theo một quan hệ

- Dùng `nếu` cho điều kiện logic.
- Dùng `khi` cho thời điểm hoặc sự kiện.
- Dùng `vì` cho nguyên nhân.
- Dùng `để` cho mục đích có chủ ý.
- Dùng `dẫn đến` cho kết quả.
- Dùng `sau đó` cho thứ tự thời gian.

### QT 4.5 — Dùng danh sách dọc

Dùng danh sách dọc cho ba mục trở lên, các bước theo thứ tự hoặc các lựa chọn loại trừ nhau.
Mỗi mục PHẢI có cùng cấu trúc ngữ pháp.

## Nhóm 5 — Viết thủ tục

### QT 5.1 — Dùng câu mệnh lệnh

Bắt đầu mỗi bước bằng động từ chỉ hành động.
Không thêm chủ ngữ giả như `bạn`, `chúng ta` hoặc `người dùng` khi tác nhân là người làm thủ tục.

### QT 5.2 — Viết một lệnh trong một bước

Mỗi bước PHẢI chứa một hành động bắt buộc.
Tách bước nếu hai hành động có thể xảy ra độc lập.

Hai hành động được phép ở cùng một bước khi chúng phải xảy ra đồng thời.

### QT 5.3 — Viết các bước theo thứ tự thực hiện

Sắp xếp bước theo thứ tự thời gian.
Không yêu cầu người đọc quay lại bước trước để tìm điều kiện hoặc dữ liệu.

### QT 5.4 — Tách điều kiện, hành động và kết quả

Viết điều kiện trước hành động. Viết kết quả cần kiểm tra sau hành động.
Dùng bước hoặc câu riêng cho từng phần.

### QT 5.5 — Không đặt lệnh trong ghi chú

Ghi chú chỉ cung cấp thông tin.
Nếu nội dung yêu cầu hành động, chuyển nội dung đó thành một bước.

## Nhóm 6 — Viết mô tả

### QT 6.1 — Giới thiệu chủ đề trước chi tiết

Câu đầu của đoạn PHẢI nêu chủ đề của đoạn.
Các câu sau bổ sung thông tin cho chủ đề đó.

### QT 6.2 — Mỗi đoạn chỉ có một chủ đề

Tách đoạn khi chủ đề thay đổi.
Không dùng một đoạn để mô tả đồng thời kiến trúc, cách cài đặt và cách khắc phục lỗi.

### QT 6.3 — Giới hạn độ dài đoạn

Một đoạn mô tả NÊN có tối đa sáu câu.
Dùng danh sách hoặc tiêu đề phụ nếu đoạn cần nhiều thông tin hơn.

### QT 6.4 — Trình bày thông tin theo quan hệ logic

Dùng một thứ tự ổn định: tổng quan đến chi tiết, nguyên nhân đến kết quả hoặc đầu vào đến đầu ra.
Không đổi thứ tự trong cùng một đoạn.

### QT 6.5 — Nêu chủ thể của trạng thái

Nêu rõ module, dữ liệu hoặc tiến trình có trạng thái được mô tả.
Không dùng câu như `Có lỗi xảy ra` khi biết thành phần phát sinh lỗi.

## Nhóm 7 — Cảnh báo vận hành

### QT 7.1 — Chọn đúng loại thông báo

- **CẢNH BÁO**: nguy cơ mất dữ liệu, lộ bí mật, thay đổi không thể đảo ngược hoặc gián đoạn production.
- **CHÚ Ý**: nguy cơ giảm hiệu năng, cạn tài nguyên hoặc tạo công việc khôi phục.
- **GHI CHÚ**: thông tin hỗ trợ, không có hành động bắt buộc.

Không dùng nhãn sự cố như `SEV-1` thay cho loại thông báo. Hai hệ thống phục vụ hai mục đích khác nhau.

### QT 7.2 — Viết đủ ba phần của cảnh báo

CẢNH BÁO và CHÚ Ý PHẢI nêu ba phần theo thứ tự sau:

1. Hành động hoặc điều kiện gây nguy cơ.
2. Hậu quả kỹ thuật.
3. Cách tránh hoặc điều kiện tiên quyết.

Nếu nguồn thiếu một phần, dùng `[CẦN BỔ SUNG: ...]`. Không tự tạo thông tin.

### QT 7.3 — Không đặt lệnh trong ghi chú

GHI CHÚ KHÔNG ĐƯỢC chứa lệnh hoặc điều kiện tiên quyết.
Đổi GHI CHÚ thành bước, CẢNH BÁO hoặc CHÚ Ý nếu người đọc phải hành động.

## Nhóm 8 — Dấu câu, token và nội dung kỹ thuật

### QT 8.1 — Dùng dấu câu đơn giản

Dùng dấu chấm để tách ý độc lập.
Không dùng dấu chấm phẩy để nối nhiều lệnh.
Không dùng dấu ba chấm để thay thông tin bị thiếu.

### QT 8.2 — Định dạng token kỹ thuật

Viết identifier, lệnh, path, endpoint cụ thể và tên hàm bằng code style.
Giữ nguyên chữ hoa, chữ thường và dấu câu của token.

| Không dùng | Dùng |
|---|---|
| Gọi hàm getUserById. | Gọi `getUserById()`. |
| Sửa file config chấm yaml. | Sửa tệp `config.yaml`. |

### QT 8.3 — Viết số và đơn vị rõ ràng

Dùng chữ số cho giá trị kỹ thuật. Viết một khoảng trắng giữa số và đơn vị.
Dùng khoảng có hai đầu mút thay cho `khoảng`, `tầm` hoặc `cỡ` khi cần giới hạn chính xác.

Ví dụ: `10 ms`, `5 GiB`, `từ 3 đến 5 replica`.

### QT 8.4 — Đếm token

Validator đếm token theo khoảng trắng sau khi bỏ dấu câu ở đầu và cuối token.
Identifier, path, URL và số phiên bản không chứa khoảng trắng được tính là một token.
Lệnh có nhiều phần được tính theo từng token.
Validator bỏ qua code block và nội dung trích dẫn nguyên văn.

### QT 8.5 — Giữ nguyên nội dung trích dẫn

Không sửa code, log, thông báo lỗi hoặc câu trích dẫn để làm chúng tuân thủ chuẩn.
Đặt nội dung đó trong code style, code block hoặc blockquote.

## Nhóm 9 — Thực hành viết

### QT 9.1 — Giữ đúng và đủ thông tin

Khi viết lại, tác giả PHẢI giữ nguyên điều kiện, dữ kiện, giá trị và quan hệ nhân quả.
Không thêm bước, số liệu, tên hoặc kết luận không có trong nguồn.

### QT 9.2 — Đổi cấu trúc khi thay từ chưa đủ

Nếu thay từng từ làm câu sai nghĩa hoặc khó đọc, viết lại cấu trúc câu.
Câu mới PHẢI giữ nguyên ý của câu nguồn.

### QT 9.3 — Đánh dấu thông tin thiếu

Nếu quy tắc yêu cầu thông tin nhưng nguồn không có, dùng `[CẦN BỔ SUNG: nội dung cần có]`.
Không dùng marker chung như `TODO` hoặc `TBD`.

### QT 9.4 — Đánh dấu suy luận

Nếu nội dung không được quan sát trực tiếp hoặc không có trong nguồn, bắt đầu nội dung đó bằng `[SUY LUẬN]`.
Không trình bày suy luận như sự thật đã kiểm chứng.

### QT 9.5 — Ưu tiên tính nhất quán

Dùng cùng một thuật ngữ, cấu trúc bước và mức cảnh báo trong toàn bộ tài liệu.
Không thay đổi cách viết chỉ để tạo phong cách đa dạng.

---

# PHẦN 2 — KHMT PROFILE

## 2.1 Chính sách ngôn ngữ cho thuật ngữ

Mỗi entry có một `language_policy`.
Chính sách này độc lập với nghĩa và từ loại của entry.

### Tầng A — Giữ dạng tiếng Anh

Dùng dạng tiếng Anh làm `canonical`.
Không dịch dạng chuẩn trong nội dung kỹ thuật.

### Tầng B — Dùng tiếng Anh và chú thích tiếng Việt lần đầu

Dùng dạng tiếng Anh làm `canonical`.
Tại lần xuất hiện đầu tiên, dùng đúng `first_use_form` trong glossary.
Sau đó, chỉ dùng dạng tiếng Anh.

### Tầng C — Dùng dạng tiếng Việt

Dùng dạng tiếng Việt làm `canonical`.
Dạng tiếng Anh chỉ là thông tin đối chiếu. Không trộn hai dạng trong cùng một tài liệu.

## 2.2 Thứ tự chọn thuật ngữ

1. Tìm khái niệm trong glossary.
2. Chọn entry đúng nghĩa, từ loại và phạm vi.
3. Dùng đúng `canonical` và `first_use_form`.
4. Nếu không có entry phù hợp, đề xuất entry mới.

Không tự gán tầng dựa trên việc từ xuất hiện trong code, log hoặc API.
Token xuất hiện nguyên văn trong code, log hoặc API luôn giữ nguyên theo QT 8.5.

## 2.3 Hình thái của thuật ngữ tiếng Anh

- Không thêm `s` để tạo số nhiều trong câu tiếng Việt. Viết `3 pod`, không viết `3 pods`.
- Dùng dạng nguyên thể cho động từ tiếng Anh. Viết `đã deploy`, không viết `đã deployed`.
- Không ghép nửa Anh nửa Việt thành một từ. Viết `merge nhánh`, không viết `merge-nhánh`.
- Giữ nguyên chữ hoa và chữ thường của identifier.

## 2.4 Schema của controlled dictionary

`glossary/glossary.csv` là nguồn sự thật duy nhất cho thuật ngữ.
Mỗi row chứa các trường sau:

| Trường | Nội dung |
|---|---|
| `canonical` | Dạng bắt buộc dùng. |
| `english_equivalent` | Dạng tiếng Anh để đối chiếu. |
| `language_policy` | A, B hoặc C. |
| `part_of_speech` | Từ loại được duyệt. |
| `approved_meaning` | Nghĩa duy nhất của entry. |
| `scope` | Phạm vi kỹ thuật của nghĩa. |
| `first_use_form` | Dạng bắt buộc tại lần xuất hiện đầu tiên. |
| `forbidden_alternatives` | Các dạng không được dùng cho nghĩa này. |
| `approved_example` | Ví dụ đúng. |
| `non_approved_example` | Ví dụ sai. |
| `note` | Ghi chú quản trị. |

Một dạng có nhiều từ loại hoặc nghĩa PHẢI có nhiều row.
Không sửa bảng sinh tự động bên dưới bằng tay. Chạy `make sync` sau khi sửa CSV.

## 2.5 Controlled dictionary

<!-- BEGIN GENERATED GLOSSARY -->
<!-- Sinh tự động từ glossary CSV bằng `python3 tools/validate.py sync`. Không sửa tay. -->

#### Chính sách A — Giữ nguyên tiếng Anh

| Dạng chuẩn | Từ loại | Nghĩa được duyệt | Phạm vi | Dạng lần đầu | Không dùng | Ví dụ đúng | Ví dụ sai |
| --- | --- | --- | --- | --- | --- | --- | --- |
| framework | noun | bộ khung code có sẵn để xây ứng dụng | software |  | khung phần mềm | Dự án dùng framework Django. | Dự án dùng khung phần mềm Django. |
| array | noun | dãy phần tử cùng kiểu, truy cập theo chỉ số | data structure |  | mảng | Duyệt array từ đầu đến cuối. | Duyệt mảng từ đầu đến cuối. |
| pointer | noun | biến lưu địa chỉ bộ nhớ của một giá trị | programming |  | con trỏ, biến trỏ | `pointer` trỏ đến đầu array. | Con trỏ trỏ đến đầu array. |
| thread | noun | luồng chạy trong một process, dùng chung bộ nhớ với các thread khác | operating system |  |  | Mỗi request chạy trên một thread riêng. | Mỗi request chạy trên một luồng riêng. |
| process | noun | chương trình đang chạy, có không gian bộ nhớ riêng | operating system |  |  | Process con thoát khi process cha dừng. | Tiến trình con thoát khi tiến trình cha dừng. |
| cache | noun | vùng lưu tạm dữ liệu để đọc lại nhanh | performance |  | bộ nhớ đệm | Xóa cache sau khi deploy. | Xóa bộ nhớ đệm sau khi deploy. |
| buffer | noun | vùng nhớ tạm giữ dữ liệu trong lúc chuyển giữa hai bên | programming |  | bộ đệm | Buffer đầy thì dừng ghi. | Bộ đệm đầy thì dừng ghi. |
| stack | noun | cấu trúc dữ liệu lấy phần tử vào sau ra trước | data structure |  | ngăn xếp | Dùng stack để kiểm tra dấu ngoặc. | Dùng ngăn xếp để kiểm tra dấu ngoặc. |
| heap | noun | vùng bộ nhớ cấp phát động khi chương trình chạy | memory |  |  | Object lớn nằm trên heap. | Object lớn nằm trên vùng nhớ động. |
| queue | noun | cấu trúc dữ liệu lấy phần tử vào trước ra trước | data structure |  |  | Dùng queue để duyệt đồ thị theo chiều rộng. | Dùng hàng đợi để duyệt đồ thị theo chiều rộng. |
| hash | noun | giá trị cố định tính từ dữ liệu bằng hash function | programming |  | giá trị băm, mã băm | So sánh hash của hai tệp. | So sánh giá trị băm của hai tệp. |
| token | noun | đơn vị nhỏ nhất của chuỗi đầu vào mà parser hoặc model đọc | language processing |  |  | Compiler tách mã nguồn thành token. | Compiler tách mã nguồn thành thẻ. |
| token | noun | chuỗi ký tự chứng minh quyền truy cập | security |  | mã thông hành | Gửi token trong header của request. | Gửi mã thông hành trong header của request. |
| socket | noun | điểm đầu cuối của kết nối mạng trong chương trình | networking |  | ổ cắm | Đóng socket sau khi gửi xong. | Đóng ổ cắm sau khi gửi xong. |
| endpoint | noun | địa chỉ API nhận request | api |  | điểm cuối | Endpoint trả response JSON. | Điểm cuối trả response JSON. |
| middleware | noun | lớp code xử lý request trước hoặc sau handler | software |  | phần mềm trung gian | Middleware kiểm tra token trước handler. | Phần mềm trung gian kiểm tra token trước handler. |
| container | noun | môi trường chạy cô lập chứa ứng dụng và phụ thuộc của nó | infrastructure |  | thùng chứa | Chạy service trong một container. | Chạy service trong một thùng chứa. |
| runtime | noun | môi trường thực thi chương trình | programming |  | thời gian chạy | Cài runtime Python 3 trước khi chạy script. | Cài môi trường thời gian chạy Python 3 trước khi chạy script. |
| compiler | noun | chương trình dịch mã nguồn sang mã máy hoặc bytecode | programming |  | trình biên dịch | Compiler báo lỗi ở dòng 12. | Trình biên dịch báo lỗi ở dòng 12. |
| linker | noun | chương trình ghép các tệp object thành một tệp chạy được | programming |  | trình liên kết | Linker báo thiếu symbol. | Trình liên kết báo thiếu symbol. |
| boolean | noun | kiểu dữ liệu chỉ có hai giá trị đúng và sai | programming |  | giá trị luận lý | Hàm trả về một boolean. | Hàm trả về một giá trị luận lý. |
| enum | noun | kiểu dữ liệu gồm một tập giá trị có tên cố định | programming |  | kiểu liệt kê | Khai báo một enum cho trạng thái đơn hàng. | Khai báo một kiểu liệt kê cho trạng thái đơn hàng. |
| struct | noun | kiểu dữ liệu gom nhiều trường thành một khối | programming |  |  | Struct `Point` có hai trường. | Cấu trúc `Point` có hai trường. |
| interface | noun | tập chữ ký hàm mà một kiểu phải cài đặt | programming |  |  | Class cài đặt interface `Reader`. | Class cài đặt giao diện `Reader`. |
| closure | noun | hàm giữ lại biến của phạm vi nơi nó được tạo | programming |  | hàm đóng | Closure giữ biến `count` sau khi hàm ngoài kết thúc. | Hàm đóng giữ biến `count` sau khi hàm ngoài kết thúc. |
| callback | noun | hàm được truyền vào hàm khác để gọi lại sau | programming |  | hàm gọi lại | Truyền callback vào `fetchUser()`. | Truyền hàm gọi lại vào `fetchUser()`. |
| promise | noun | đối tượng đại diện cho kết quả của một việc chạy bất đồng bộ | programming |  | lời hứa | `fetch()` trả về một promise. | `fetch()` trả về một lời hứa. |
| deadlock | noun | tình trạng các thread chờ nhau mãi nên không thread nào chạy tiếp | concurrency |  | khóa chết, bế tắc | Hai thread giữ lock của nhau gây deadlock. | Hai thread giữ lock của nhau gây khóa chết. |
| race condition | noun | lỗi xảy ra khi kết quả phụ thuộc vào thứ tự chạy của các thread | concurrency |  | điều kiện tranh đua | Race condition làm bộ đếm sai. | Điều kiện tranh đua làm bộ đếm sai. |
| overfitting | noun | tình trạng model khớp quá mức với training data | machine learning |  | quá khớp | Thêm dữ liệu để giảm overfitting. | Thêm dữ liệu để giảm quá khớp. |
| gradient | noun | vector đạo hàm riêng của hàm mất mát | machine learning |  |  | Gradient lớn làm training không ổn định. | Độ dốc lớn làm training không ổn định. |
| tensor | noun | mảng nhiều chiều dùng để chứa dữ liệu của model | machine learning |  | ten-xơ | Chuyển ảnh thành tensor. | Chuyển ảnh thành ten-xơ. |
| embedding | noun | vector số biểu diễn một đối tượng như từ hoặc ảnh | machine learning |  | vector nhúng | Lưu embedding của mỗi câu. | Lưu vector nhúng của mỗi câu. |
| epoch | noun | một lượt model học qua toàn bộ training data | machine learning |  | kỷ nguyên | Train model trong 10 epoch. | Train model trong 10 kỷ nguyên. |
| batch | noun | nhóm mẫu dữ liệu xử lý cùng lúc trong một bước train | machine learning |  | kích thước lô | Chọn batch size là 32. | Chọn kích thước lô là 32. |
| feature | noun | biến đầu vào mô tả một mẫu dữ liệu của model | machine learning |  | đặc trưng | Thêm một feature cho model. | Thêm một đặc trưng cho model. |
| label | noun | giá trị đúng gán cho một mẫu training data | machine learning |  |  | Mỗi mẫu có một label. | Mỗi mẫu có một nhãn. |
| checkpoint | noun | bản lưu trạng thái của model trong lúc train | machine learning |  | điểm kiểm tra | Lưu checkpoint sau mỗi epoch. | Lưu điểm kiểm tra sau mỗi epoch. |
| latency | noun | khoảng thời gian từ lúc gửi request đến lúc nhận response | performance |  | độ trễ | Latency của endpoint vượt 200 ms. | Độ trễ của endpoint vượt 200 ms. |
| throughput | noun | số việc xử lý mỗi đơn vị thời gian | performance |  | thông lượng | Tăng throughput của queue. | Tăng thông lượng của queue. |
| bug | noun | lỗi phần mềm | software |  | con bọ | Bug này làm app đóng đột ngột. | Con bọ này làm app đóng đột ngột. |
| staging | noun | môi trường thử trước production | infrastructure |  | môi trường dàn dựng | Deploy service lên staging trước. | Deploy service lên môi trường dàn dựng trước. |
| production | noun | môi trường chạy thật | infrastructure |  | môi trường sản xuất | Không chạy lệnh này trên production. | Không chạy lệnh này trên môi trường sản xuất. |
| prod | noun | dạng ngắn của production | infrastructure |  |  | Log trên prod có lỗi mới. | Log trên môi trường chạy thật có lỗi mới. |
| deploy | noun | lần đưa code lên môi trường chạy | release |  | sự triển khai | Deploy tối qua gây lỗi. | Sự triển khai tối qua gây lỗi. |
| commit | noun | một lần ghi thay đổi vào repo | version control |  | bản giao nộp | Commit này sửa hàm đăng nhập. | Bản giao nộp này sửa hàm đăng nhập. |
| pull request | noun | yêu cầu gộp code để review | version control |  | yêu cầu kéo | Mở pull request cho nhánh `feature/login`. | Mở yêu cầu kéo cho nhánh `feature/login`. |
| PR | noun | dạng viết tắt của pull request | version control |  | yêu cầu kéo | PR này fix lỗi đăng nhập. | Yêu cầu kéo này fix lỗi đăng nhập. |
| repo | noun | kho lưu mã nguồn và lịch sử thay đổi | version control |  | kho mã | Clone repo về máy. | Clone kho mã về máy. |
| branch | noun | dòng phát triển riêng trong repo | version control |  |  | Tạo branch `feature/login` từ `main`. | Tạo nhánh `feature/login` từ `main`. |
| service | noun | chương trình chạy độc lập và nhận request qua mạng | architecture |  | dịch vụ | Deploy service lên staging. | Triển khai dịch vụ lên môi trường dàn dựng. |
| replica | noun | bản chạy giống hệt của một service | infrastructure |  | bản sao | Tăng số replica của service. | Tăng số bản sao của service. |
| pod | noun | đơn vị chạy nhỏ nhất của Kubernetes, chứa một hoặc nhiều container | infrastructure |  |  | Chạy 3 `pod`. | Chạy 3 `pods`. |
| request | noun | thông điệp client gửi đến server để yêu cầu một việc | api |  |  | Middleware xử lý request trước handler. | Yêu cầu được gửi đến điểm cuối. |
| response | noun | thông điệp server trả lại cho client | api |  |  | Parse response JSON. | Phân tích phản hồi JSON. |
| handler | noun | hàm nhận và xử lý một request hoặc một event | software |  |  | Debug hàm `handler()`. | Debug hàm xử lý. |
| image | noun | tệp đóng gói sẵn dùng để tạo container | infrastructure |  | ảnh Docker | Build lại Docker image. | Build lại ảnh Docker. |
| log | noun | bản ghi sự kiện do hệ thống tạo ra | operations |  | nhật ký | Đọc log của service. | Đọc nhật ký của service. |
| user | noun | tài khoản hoặc đối tượng người dùng trong code và dữ liệu | software |  |  | Endpoint trả danh sách user. | Endpoint trả danh sách người dùng. |
| admin | noun | người có quyền quản trị hệ thống | operations |  | người quản trị | Gửi thông báo cho admin. | Gửi thông báo cho người quản trị. |
| library | noun | bộ code có sẵn để chương trình khác gọi | software |  | thư viện | Cài library này bằng `pip`. | Cài thư viện này bằng `pip`. |
| codebase | noun | toàn bộ mã nguồn của một dự án | software |  | cơ sở mã | Logic này lặp ở nhiều nơi trong codebase. | Logic này lặp ở nhiều nơi trong cơ sở mã. |
| module | noun | đơn vị code có tên, gom các hàm liên quan | software |  | mô-đun | Refactor module `auth`. | Refactor mô-đun `auth`. |
| logic | noun | phần code quyết định hành vi của chương trình | software |  |  | Logic kiểm tra quyền lặp ở nhiều nơi. | Lô-gic kiểm tra quyền lặp ở nhiều nơi. |
| coverage | noun | tỷ lệ code được test chạy qua | testing |  | độ phủ | Coverage của module `auth` là 80%. | Độ phủ của module `auth` là 80%. |
| linter | noun | công cụ kiểm tra style và lỗi thường gặp của code | tooling |  |  | Chạy linter trước khi commit. | Chạy công cụ kiểm tra style trước khi commit. |
| test | noun | kịch bản tự động kiểm tra hành vi của code | testing |  | bài kiểm tra | Thêm test cho hàm `parse()`. | Thêm bài kiểm tra cho hàm `parse()`. |
| test suite | noun | tập các test chạy cùng nhau | testing |  | bộ kiểm thử | Chạy full test suite trước khi merge. | Chạy toàn bộ bộ kiểm thử trước khi merge. |
| model | noun | hàm đã được train để dự đoán hoặc sinh đầu ra từ đầu vào | machine learning |  | mô hình | Train model trên tập mới. | Huấn luyện mô hình trên tập mới. |
| input | noun | dữ liệu đưa vào chương trình hoặc model | programming |  |  | Kiểm tra input trước khi parse. | Kiểm tra dữ liệu nhập trước khi parse. |
| error rate | noun | tỷ lệ request lỗi trên tổng số request | operations |  | tỷ lệ lỗi | Nếu error rate vượt 1%, rollback deploy. | Nếu tỷ lệ lỗi vượt 1%, rollback deploy. |
| code review | noun | việc người khác đọc và nhận xét thay đổi code | process |  | xét duyệt mã | Ghi chú code review nêu rõ file và dòng. | Ghi chú xét duyệt mã nêu rõ file và dòng. |
| design doc | noun | tài liệu mô tả thiết kế trước khi viết code | documentation |  |  | Viết design doc trước khi code. | Viết tài liệu thiết kế trước khi code. |
| README | noun | tệp giới thiệu và hướng dẫn dùng một dự án | documentation |  |  | Thêm bước cài đặt vào README. | Thêm bước cài đặt vào tệp đọc tôi. |
| runbook | noun | tài liệu hướng dẫn từng bước vận hành hệ thống | operations |  | sổ tay vận hành | Cập nhật runbook sau sự cố. | Cập nhật sổ tay vận hành sau sự cố. |
| incident report | noun | báo cáo mô tả một sự cố vận hành | operations |  |  | Viết incident report trong 48 giờ. | Viết báo cáo sự cố trong 48 giờ. |
| postmortem | noun | bản phân tích nguyên nhân sau một sự cố | operations |  |  | Họp postmortem sau sự cố. | Họp phân tích hậu kiểm sau sự cố. |
| model card | noun | tài liệu mô tả mục đích, dữ liệu, và giới hạn của model | machine learning |  | thẻ mô hình | Cập nhật model card sau mỗi lần train lại. | Cập nhật thẻ mô hình sau mỗi lần train lại. |
| data card | noun | tài liệu mô tả nguồn gốc và đặc điểm của một bộ dữ liệu | machine learning |  | thẻ dữ liệu | Thêm nguồn dữ liệu vào data card. | Thêm nguồn dữ liệu vào thẻ dữ liệu. |
| commit message | noun | đoạn mô tả đi kèm một commit | version control |  |  | Viết commit message ở dạng mô tả. | Viết thông điệp commit ở dạng mô tả. |
| agent | noun | chương trình dùng LLM để tự chọn và gọi công cụ nhằm hoàn thành việc | agent |  | tác tử, đại lý | Agent chạy test rồi báo kết quả. | Tác tử chạy test rồi báo kết quả. |
| prompt | noun | văn bản đầu vào đưa cho LLM | agent |  |  | Ghi rõ mục tiêu trong prompt. | Ghi rõ mục tiêu trong lời nhắc. |
| IDE | abbreviation | môi trường phát triển tích hợp gồm editor, debugger và công cụ build | tooling |  |  | IDE đánh dấu lỗi cú pháp. | Môi trường phát triển tích hợp đánh dấu lỗi cú pháp. |
| commit | verb | ghi một thay đổi vào repo | version control |  | giao nộp | Commit thay đổi này vào `main`. | Giao nộp thay đổi này vào `main`. |
| push | verb | gửi commit từ repo cục bộ lên repo từ xa | version control |  |  | Push branch lên remote. | Đẩy nhánh lên remote. |
| pull | verb | lấy commit mới từ repo từ xa về repo cục bộ | version control |  |  | Pull `main` trước khi tạo branch. | Kéo `main` trước khi tạo branch. |
| merge | verb | gộp nhánh code | version control |  |  | Merge branch `feature/login` vào `main`. | Thực hiện việc gộp nhánh. |
| rebase | verb | đặt lại các commit của một branch lên đầu một branch khác | version control |  |  | Rebase branch lên `main`. | Gắn lại nền nhánh lên `main`. |
| deploy | verb | đưa code lên môi trường chạy | release |  | sự triển khai | Deploy service lên staging. | Triển khai service lên môi trường dàn dựng. |
| build | verb | biên dịch và đóng gói | release |  |  | Build lại Docker image. | Dựng lại Docker image. |
| build | noun | kết quả hoặc lần chạy biên dịch và đóng gói | release |  |  | Build trên `main` đang đỏ. | Bản dựng trên `main` đang đỏ. |
| compile | verb | dịch mã nguồn sang mã máy hoặc bytecode | programming |  |  | Compile module `core` với cờ debug. | Biên dịch module `core` với cờ debug. |
| debug | verb | tìm và định vị lỗi | software |  | gỡ lỗi | Debug hàm `handler()`. | Gỡ lỗi hàm `handler()`. |
| refactor | verb | sửa cấu trúc code, giữ hành vi | software |  | tái cấu trúc | Refactor module `auth`. | Tái cấu trúc module `auth`. |
| rollback | verb | quay về phiên bản trước | release |  |  | Nếu lỗi, rollback về `v1.2.0`. | Nếu lỗi, quay lui về `v1.2.0`. |
| fork | verb | sao chép một repo thành bản riêng của mình | version control |  |  | Fork repo rồi sửa trên bản của bạn. | Rẽ nhánh repo rồi sửa trên bản của bạn. |
| mount | verb | gắn một ổ đĩa hoặc volume vào hệ thống tệp | operating system |  |  | Mount volume vào `/data`. | Gắn volume vào `/data`. |
| cache | verb | lưu tạm dữ liệu để đọc lại nhanh | performance |  | lưu đệm | Cache kết quả truy vấn trong 5 phút. | Lưu đệm kết quả truy vấn trong 5 phút. |
| parse | verb | phân tích cú pháp đầu vào | programming |  |  | Parse response JSON. | Phân tích response JSON. |
| render | verb | tạo ra hình ảnh hoặc HTML từ dữ liệu | programming |  | kết xuất | Render trang từ template. | Kết xuất trang từ template. |
| import | verb | nạp code hoặc dữ liệu từ nơi khác vào | programming |  |  | Import module `auth`. | Nhập module `auth`. |
| export | verb | xuất code hoặc dữ liệu ra để nơi khác dùng | programming |  |  | Export dữ liệu ra tệp CSV. | Xuất khẩu dữ liệu ra tệp CSV. |
| deprecate | verb | đánh dấu một API hoặc tính năng sắp bị bỏ | software |  |  | Deprecate endpoint `/v1/login`. | Đánh dấu lỗi thời endpoint `/v1/login`. |
| spawn | verb | tạo một process hoặc thread mới | operating system |  |  | Spawn một thread cho mỗi request. | Sinh ra một thread cho mỗi request. |
| throttle | verb | giới hạn tốc độ xử lý hoặc gửi request | performance |  |  | Throttle request về 100 mỗi giây. | Bóp nghẹt request về 100 mỗi giây. |
| benchmark | verb | đo hiệu năng của code trong điều kiện cố định | performance |  |  | Benchmark hàm `parse()` trước và sau khi refactor. | Đánh giá chuẩn hàm `parse()` trước và sau khi refactor. |
| fix | verb | sửa một lỗi cho chương trình chạy đúng | software |  |  | Fix bug này. | Xử lý cái bug này. |
| handle | verb | nhận và trả lời một request hoặc event trong code | software |  |  | Hàm `handler()` handle lỗi timeout. | Hàm `handler()` xử lý lỗi timeout. |
| log | verb | ghi một sự kiện vào log | operations |  |  | Log lỗi và gửi thông báo cho admin. | Ghi log lại lỗi và gửi thông báo cho admin. |
| review | verb | đọc và nhận xét thay đổi code hoặc tài liệu | process |  |  | Review PR này trước 17 giờ. | Thực hiện việc review PR này trước 17 giờ. |
| backup | verb | sao lưu dữ liệu để khôi phục khi mất | operations |  |  | Backup cơ sở dữ liệu trước khi chạy lệnh. | Tiến hành backup cơ sở dữ liệu trước khi chạy lệnh. |
| load | verb | tải dữ liệu hoặc trang vào bộ nhớ để dùng | software |  |  | Trang chủ load chậm trên thiết bị di động. | Trang chủ tải chậm trên thiết bị di động. |
| pass | verb | chạy xong và đạt mọi kiểm tra | testing |  |  | Bảo đảm CI pass. | Bảo đảm CI vượt qua. |
| API | abbreviation | giao diện để chương trình này gọi chương trình khác | api |  |  | API trả về mã lỗi 404. | Giao diện lập trình ứng dụng trả về mã lỗi 404. |
| JSON | abbreviation | định dạng văn bản trao đổi dữ liệu theo cặp khóa và giá trị | api |  |  | Endpoint trả response JSON. | Endpoint trả response Jây-xân. |
| SQL | abbreviation | ngôn ngữ truy vấn cơ sở dữ liệu quan hệ | database |  |  | Viết câu truy vấn SQL cho báo cáo. | Viết câu truy vấn ngôn ngữ hỏi có cấu trúc cho báo cáo. |
| HTTP | abbreviation | giao thức truyền dữ liệu giữa client và server trên web | networking |  |  | Endpoint chỉ nhận HTTP POST. | Endpoint chỉ nhận giao thức truyền siêu văn bản POST. |
| CI | abbreviation | hệ thống tự build và test mỗi lần có commit mới | tooling |  |  | CI chạy test cho mỗi PR. | Tích hợp liên tục chạy test cho mỗi PR. |
| CI/CD | abbreviation | quy trình tự build, test, và deploy code | tooling |  |  | CI/CD tự deploy lên staging. | Tích hợp và phân phối liên tục tự deploy lên staging. |
| CLI | abbreviation | chương trình điều khiển bằng lệnh gõ trong terminal | tooling |  |  | Chạy `tool --help` trong CLI. | Chạy `tool --help` trong giao diện dòng lệnh. |
| ML | abbreviation | ngành cho máy học từ dữ liệu | machine learning |  |  | Tài liệu ML gồm model card và data card. | Tài liệu HM gồm model card và data card. |
| SVM | abbreviation | thuật toán phân loại tìm ranh giới rộng nhất giữa các lớp | machine learning |  |  | Dùng SVM cho bài toán classification này. | Dùng máy vector hỗ trợ cho bài toán classification này. |
| LLM | abbreviation | model ngôn ngữ cỡ lớn, train trên lượng văn bản rất lớn | agent |  |  | Agent gọi LLM để sinh patch. | Tác tử gọi mô hình ngôn ngữ lớn để sinh patch. |

#### Chính sách B — Tiếng Anh kèm giải thích tiếng Việt ở lần đầu

| Dạng chuẩn | Từ loại | Nghĩa được duyệt | Phạm vi | Dạng lần đầu | Không dùng | Ví dụ đúng | Ví dụ sai |
| --- | --- | --- | --- | --- | --- | --- | --- |
| machine learning | noun | ngành cho máy học từ dữ liệu | machine learning | machine learning (học máy) |  | Machine learning (học máy) cần training data. | Học máy cần training data. |
| supervised learning | noun | học từ dữ liệu có label | machine learning | supervised learning (học có giám sát) |  | Dùng supervised learning (học có giám sát) cho bài toán này. | Dùng học có giám sát cho bài toán này. |
| unsupervised learning | noun | học từ dữ liệu không có label | machine learning | unsupervised learning (học không giám sát) |  | Unsupervised learning (học không giám sát) tìm cấu trúc trong dữ liệu. | Học không giám sát tìm cấu trúc trong dữ liệu. |
| reinforcement learning | noun | học bằng cách thử hành động và nhận phần thưởng | machine learning | reinforcement learning (học tăng cường) |  | Reinforcement learning (học tăng cường) dùng phần thưởng làm tín hiệu. | Học tăng cường dùng phần thưởng làm tín hiệu. |
| deep learning | noun | học bằng neural network nhiều tầng | machine learning | deep learning (học sâu) |  | Deep learning (học sâu) cần nhiều dữ liệu. | Học sâu cần nhiều dữ liệu. |
| training data | noun | dữ liệu dùng để train model | machine learning | training data (dữ liệu huấn luyện) |  | Training data (dữ liệu huấn luyện) có label. | Dữ liệu huấn luyện có label. |
| training set | noun | phần dữ liệu dùng để train model | machine learning | training set (tập huấn luyện) |  | Chia training set (tập huấn luyện) và test set. | Chia tập huấn luyện và test set. |
| test set | noun | phần dữ liệu dùng để đánh giá model sau khi train | machine learning | test set (tập kiểm thử) |  | Đánh giá accuracy trên test set (tập kiểm thử). | Đánh giá accuracy trên tập kiểm thử. |
| feature extraction | noun | biến dữ liệu thô thành feature | machine learning | feature extraction (trích xuất đặc trưng) |  | Feature extraction (trích xuất đặc trưng) chạy trước khi train. | Trích xuất đặc trưng chạy trước khi train. |
| feature engineering | noun | việc chọn và tạo feature cho model | machine learning | feature engineering (kỹ thuật đặc trưng) |  | Feature engineering (kỹ thuật đặc trưng) giúp tăng accuracy. | Kỹ thuật đặc trưng giúp tăng accuracy. |
| classification | noun | bài toán gán mỗi mẫu vào một lớp | machine learning | classification (phân loại) |  | Classification (phân loại) ảnh thành mèo hoặc chó. | Phân loại ảnh thành mèo hoặc chó. |
| regression | noun | bài toán dự đoán một giá trị số liên tục | machine learning | regression (hồi quy) |  | Regression (hồi quy) dự đoán giá nhà. | Hồi quy dự đoán giá nhà. |
| clustering | noun | bài toán chia mẫu thành các nhóm giống nhau | machine learning | clustering (phân cụm) |  | Clustering (phân cụm) nhóm khách hàng theo hành vi. | Phân cụm nhóm khách hàng theo hành vi. |
| neural network | noun | model gồm các tầng nút nối với nhau | machine learning | neural network (mạng nơ-ron) |  | Neural network (mạng nơ-ron) có ba tầng. | Mạng nơ-ron có ba tầng. |
| train | verb | điều chỉnh tham số của model từ dữ liệu | machine learning | train (huấn luyện) |  | Train (huấn luyện) model trên tập mới. | Huấn luyện model trên tập mới. |

#### Chính sách C — Dùng tiếng Việt

| Dạng chuẩn | Từ loại | Nghĩa được duyệt | Phạm vi | Dạng lần đầu | Không dùng | Ví dụ đúng | Ví dụ sai |
| --- | --- | --- | --- | --- | --- | --- | --- |
| biến | noun | tên chỉ một vùng nhớ lưu giá trị | programming |  |  | Khai báo biến `count` trước vòng lặp. | Khai báo variable `count` trước vòng lặp. |
| hàm | noun | khối code có tên, nhận tham số và trả về giá trị | programming |  |  | Gọi hàm `parse()` hai lần. | Gọi function `parse()` hai lần. |
| vòng lặp | noun | cấu trúc chạy lặp một khối code | programming |  |  | Thoát vòng lặp khi hết phần tử. | Thoát loop khi hết phần tử. |
| câu lệnh | noun | một lệnh hoàn chỉnh trong chương trình | programming |  |  | Câu lệnh `return` kết thúc hàm. | Statement `return` kết thúc hàm. |
| kiểu dữ liệu | noun | loại giá trị mà một biến có thể giữ | programming |  |  | Kiểu dữ liệu của `count` là số nguyên. | Data type của `count` là số nguyên. |
| tệp | noun | đơn vị lưu dữ liệu có tên trong hệ thống tệp | operating system |  |  | Đọc tệp `config.yaml`. | Đọc file `config.yaml`. |
| thư mục | noun | nơi chứa tệp và thư mục con | operating system |  |  | Tạo thư mục `build/`. | Tạo directory `build/`. |
| bộ nhớ | noun | nơi chương trình lưu dữ liệu khi chạy | operating system |  |  | Chương trình dùng 2 GB bộ nhớ. | Chương trình dùng 2 GB memory. |
| mạng | noun | hệ thống kết nối các máy để trao đổi dữ liệu | networking |  |  | Máy mất kết nối mạng. | Máy mất kết nối network. |
| máy chủ | noun | máy hoặc chương trình nhận và trả lời request | networking |  |  | Máy chủ trả response sau 50 ms. | Server trả response sau 50 ms. |
| cơ sở dữ liệu | noun | nơi lưu dữ liệu có cấu trúc | database |  |  | Kiểm tra cơ sở dữ liệu có bị nghẽn không. | Kiểm tra database có bị nghẽn không. |
| CSDL | abbreviation | dạng viết tắt của cơ sở dữ liệu | database |  | CSD | Cơ sở dữ liệu (CSDL) lưu đơn hàng. CSDL chạy trên máy chủ riêng. | Dùng CSDL trước khi giải thích. |
| KHMT | abbreviation | dạng viết tắt của Khoa học Máy tính | education |  | KHM | Khoa học Máy tính (KHMT) là ngành học này. | Dùng KHM cho Khoa học Máy tính. |
| TTNT | abbreviation | dạng viết tắt của trí tuệ nhân tạo | education |  | TTN | Trí tuệ nhân tạo (TTNT) gồm cả học máy. | Dùng TTN cho trí tuệ nhân tạo. |
| bản ghi | noun | một dòng dữ liệu trong cơ sở dữ liệu | database |  |  | Xóa bản ghi cũ. | Xóa record cũ. |
| độ chính xác | noun | tỷ lệ dự đoán đúng của model | machine learning |  |  | Đo độ chính xác của model trên test set (tập kiểm thử). | Đo accuracy của model trên test set (tập kiểm thử). |
| kiểm thử | verb | chạy test để tìm lỗi | testing |  |  | Kiểm thử API trước khi merge. | Test API trước khi merge. |
| hàng đợi | noun | dãy người hoặc việc xếp chờ theo thứ tự, không nói về cấu trúc dữ liệu | general |  |  | Có 12 việc trong hàng đợi chờ duyệt. | Có 12 việc trong queue chờ duyệt. |
| người dùng | noun | người dùng sản phẩm hoặc hệ thống | general |  |  | Người dùng nhập sai mật khẩu quá nhiều lần. | User nhập sai mật khẩu quá nhiều lần. |
| triển khai | verb | đưa một quy trình hoặc chính sách vào áp dụng trong tổ chức | organization |  |  | Triển khai quy trình review mới cho cả nhóm. | Triển khai service lên production. |

<!-- END GENERATED GLOSSARY -->

---

# PHẦN 3 — AGENT PROFILE

Agent profile áp dụng cùng Chuẩn lõi và KHMT profile.
Các quy tắc trong phần này bổ sung hành vi cho output do agent tạo.

### AG 1 — Trả lời trực tiếp trước

Agent PHẢI đưa kết quả, quyết định hoặc bước tiếp theo trước phần giải thích.
Không mở đầu bằng câu xã giao không có thông tin.

### AG 2 — Tách sự thật và suy luận

Agent PHẢI dùng `[SUY LUẬN]` cho kết luận chưa được quan sát hoặc chưa có nguồn.
Agent KHÔNG ĐƯỢC dùng marker này cho sự thật đã được kiểm tra.

### AG 3 — Không tạo dữ kiện còn thiếu

Agent PHẢI dùng `[CẦN BỔ SUNG: ...]` khi thiếu dữ liệu bắt buộc.
Agent KHÔNG ĐƯỢC tạo số liệu, path, tên lệnh, trạng thái hoặc kết quả kiểm tra.

### AG 4 — Viết một hành động trong một mục

Trong checklist và hướng dẫn, mỗi mục PHẢI có một hành động chính.
Tách điều kiện, hành động và kết quả khi chúng cần được kiểm tra riêng.

### AG 5 — Giữ nguyên dữ liệu máy đọc

Agent PHẢI giữ nguyên code, identifier, path, URL, log và lỗi được trích dẫn.
Không dịch hoặc sửa chính tả các giá trị này.

### AG 6 — Tách loại nội dung

Nếu output trộn nhiều loại nội dung, dùng các nhãn phù hợp:

- **Kết quả** cho điều đã quan sát.
- **Khuyến nghị** cho lựa chọn được đề xuất.
- **Quyết định** cho phương án đã chọn.
- **Rủi ro** cho hậu quả cần xem xét.

Không lặp cùng một nội dung dưới nhiều nhãn.

### AG 7 — Báo phạm vi kiểm tra

Agent chỉ được báo các lệnh, test hoặc tình huống đã chạy.
Kết quả chưa quan sát PHẢI có marker `[SUY LUẬN]` hoặc không được nêu.

### AG 8 — Giữ output ngắn nhưng đầy đủ

Agent NÊN bỏ câu đệm, lời nhắc lại yêu cầu và kết luận trùng lặp.
Agent KHÔNG ĐƯỢC bỏ điều kiện, ngoại lệ, rủi ro hoặc bước bắt buộc để rút ngắn output.

---

# PHẦN 4 — VÍ DỤ TRƯỚC VÀ SAU

Cột **Sau** chỉ sửa cách diễn đạt. Cột này giữ đúng và đủ thông tin của cột **Trước**.

## 4.1 Review code

**Không dùng:**

> Chỗ này bạn nên tiến hành việc xử lý lại logic kiểm tra quyền vì logic đang lặp ở nhiều nơi trong codebase.

**Dùng:**

> Logic kiểm tra quyền lặp ở nhiều nơi trong codebase. Nên refactor logic này vào một hàm dùng chung.

Áp dụng QT 3.2, QT 4.2 và QT 9.1.

## 4.2 Runbook vận hành

**Không dùng:**

> Khi service quá tải thì cần tăng replica và kiểm tra cơ sở dữ liệu có bị nghẽn hay không.

**Dùng:**

> Nếu service quá tải, làm hai bước:
>
> 1. Tăng số replica của service.
> 2. Kiểm tra cơ sở dữ liệu có bị nghẽn không.

Áp dụng QT 4.3, QT 4.5 và QT 5.2.

## 4.3 Tài liệu machine learning

**Không dùng:**

> Chúng ta sẽ thực hiện việc huấn luyện model và sau đó đánh giá nó để tránh quá khớp.

**Dùng:**

> Train (huấn luyện) model bằng supervised learning (học có giám sát). Dùng training data (dữ liệu huấn luyện) có label. Đo độ chính xác trên test set (tập kiểm thử) để tránh overfitting.

Áp dụng QT 1.1, QT 1.2 và QT 3.2.

## 4.4 Hướng dẫn API

**Không dùng:**

> Người dùng sẽ gửi một yêu cầu đến điểm cuối và điểm cuối sẽ trả về một phản hồi JSON.

**Dùng:**

> Ứng dụng gửi request đến endpoint. Endpoint trả response JSON chứa danh sách người dùng.

Áp dụng QT 1.1 và QT 4.2.

## 4.5 Cảnh báo thiếu cách tránh

**Không dùng:**

> Chú ý khi chạy lệnh này vì lệnh có thể xóa dữ liệu.

**Dùng:**

> **CẢNH BÁO:** Lệnh này xóa dữ liệu. Dữ liệu không khôi phục được. `[CẦN BỔ SUNG: cách tránh mất dữ liệu]`

Áp dụng QT 7.1, QT 7.2 và QT 9.3.

## 4.6 Commit message

**Không dùng:**

> Đã thực hiện việc sửa hàm đăng nhập vì hàm bị lỗi khi người dùng nhập sai mật khẩu nhiều lần.

**Dùng:**

> `fix: sửa lỗi đăng nhập sau nhiều lần nhập sai mật khẩu`

Áp dụng QT 3.2 và QT 8.5.

## 4.7 Báo cáo sự cố

**Không dùng:**

> Vào lúc rạng sáng thì hệ thống đã gặp sự cố và người dùng không thể truy cập trong một khoảng thời gian tương đối dài.

**Dùng:**

> Rạng sáng, hệ thống gặp sự cố. Người dùng không truy cập được ứng dụng trong thời gian dài.

Không thêm giờ bắt đầu hoặc thời lượng vì nguồn không có các giá trị đó. Áp dụng QT 4.2 và QT 9.1.

## 4.8 Hướng dẫn cài đặt

**Không dùng:**

> Để cài library này thì trước tiên máy của bạn cần có Python 3 trở lên rồi sau đó chạy lệnh cài đặt.

**Dùng:**

> Trước khi cài library, cài Python 3 trở lên. Sau đó, chạy lệnh cài đặt.

Áp dụng QT 4.3 và QT 5.3.

## 4.9 Xử lý lỗi API

**Không dùng:**

> Trong trường hợp API trả mã lỗi thì hệ thống cần ghi log và đồng thời gửi thông báo cho admin.

**Dùng:**

> Nếu API trả mã lỗi, ghi log. Sau đó, gửi thông báo cho admin.

Áp dụng QT 4.4 và QT 5.2.

## 4.10 Mô tả pull request

**Không dùng:**

> PR này được tạo ra nhằm mục đích giải quyết vấn đề trang chủ tải chậm trên thiết bị di động.

**Dùng:**

> PR này giảm thời gian tải trang chủ trên thiết bị di động.

Áp dụng QT 3.1 và QT 3.2.

## 4.11 Ghi chú migration

**Không dùng:**

> Chúng ta cần tiến hành thêm một cột vào bảng người dùng và cột này lưu thời điểm đăng nhập cuối.

**Dùng:**

> Thêm một cột vào bảng người dùng. Cột mới lưu thời điểm đăng nhập cuối.

Áp dụng QT 2.3, QT 3.2 và QT 4.2.

## 4.12 Comment trong code

**Không dùng:**

> Cái hàm bên dưới được viết ra để thực hiện việc kiểm tra một chuỗi có phải email hợp lệ hay không.

**Dùng:**

> Hàm này kiểm tra chuỗi đầu vào có phải email hợp lệ không.

Áp dụng QT 3.2 và QT 4.2.

## 4.13 Cụm danh từ dài

**Không dùng:**

> Tài liệu cấu hình module xác thực người dùng hệ thống thanh toán.

**Dùng:**

> Tài liệu cấu hình module xác thực người dùng của hệ thống thanh toán.

Áp dụng QT 2.1.

## 4.14 Cảnh báo đủ thông tin

**Không dùng:**

> Lưu ý là nếu xóa nhầm tệp config thì service không khởi động nên hãy sao lưu tệp trước khi sửa.

**Dùng:**

> **CẢNH BÁO:** Xóa nhầm tệp config. Service không khởi động lại được. Trước khi sửa, sao lưu tệp config.

Áp dụng QT 7.1 và QT 7.2.

## 4.15 Output của agent

**Không dùng:**

> Có vẻ lỗi chắc chắn do cache. Bạn chỉ cần xóa cache là được.

**Dùng:**

> `[SUY LUẬN]` Cache có khả năng chứa dữ liệu cũ. Kiểm tra thời điểm tạo cache trước khi xóa.

Áp dụng AG 2, AG 3 và AG 4.

---

# PHẦN 5 — ÁP DỤNG VÀ TUÂN THỦ

## 5.1 Quy trình áp dụng

1. Chọn Chuẩn lõi và profile phù hợp.
2. Kiểm tra thuật ngữ trong glossary.
3. Viết hoặc sửa nội dung.
4. Chạy `make check` và validator cho tài liệu.
5. Review các warning cần đánh giá ngữ nghĩa.

## 5.2 Mức chẩn đoán

| Mức | Ý nghĩa | Điều kiện phát hành |
|---|---|---|
| `error` | Vi phạm xác định được, như sai thuật ngữ hoặc thiếu dạng lần đầu. | PHẢI bằng 0. |
| `warning` | Cần người review, như câu dài. | PHẢI được xem xét. |
| `info` | Gợi ý không chặn phát hành. | ĐƯỢC PHÉP giữ nguyên. |

Một tài liệu tuân thủ khi không có `error` và mọi `warning` đã được review.
Chuẩn không dùng tỷ lệ phần trăm để thay điều kiện này.

## 5.3 Phạm vi của validator

Validator kiểm tra các quy tắc xác định được:

- Schema và tính duy nhất của glossary.
- Dạng thuật ngữ bị cấm.
- Dạng lần đầu của thuật ngữ Tầng B.
- Độ dài câu theo cách đếm tại QT 8.4.
- Reference đến số hiệu quy tắc.
- Bảng glossary được sinh từ CSV.

Người review kiểm tra các quy tắc ngữ nghĩa:

- Câu có đúng một ý hay không.
- Đại từ có tham chiếu rõ hay không.
- Cảnh báo có đúng loại hay không.
- Bản viết lại có giữ nguyên ý hay không.

## 5.4 Quản trị glossary

Mỗi thay đổi glossary PHẢI có các nội dung sau:

1. Nghĩa và phạm vi của entry.
2. Lý do chọn chính sách A, B hoặc C.
3. Ví dụ đúng và ví dụ sai.
4. Tác động đến entry hiện có.

Một reviewer PHẢI duyệt thay đổi trước khi merge.
Không đổi tầng chỉ để phù hợp với một tài liệu riêng.

## 5.5 Quản trị quy tắc

Mỗi thay đổi quy tắc PHẢI có:

- Số hiệu ổn định.
- Lý do thay đổi.
- Ví dụ trước và sau.
- Fixture nếu validator kiểm tra quy tắc.
- Ghi chú migration nếu thay đổi output hợp lệ trước đây.

## 5.6 Checklist review

- [ ] Thuật ngữ dùng đúng `canonical`, nghĩa và từ loại.
- [ ] Thuật ngữ Tầng B dùng đúng dạng lần đầu.
- [ ] Mỗi câu hướng dẫn có một lệnh.
- [ ] Mỗi câu mô tả có một ý chính.
- [ ] Điều kiện đứng trước lệnh.
- [ ] Đại từ không gây mơ hồ.
- [ ] Cảnh báo có nguy cơ, hậu quả và cách tránh.
- [ ] Code, log, path và lỗi được giữ nguyên.
- [ ] Nội dung không thêm dữ kiện mới.
- [ ] Suy luận và thông tin thiếu có marker đúng.
- [ ] Validator không báo `error`.
- [ ] Mọi `warning` đã được review.

---

# PHỤ LỤC A — ĐỐI CHIẾU ASD-STE100

TVKTĐGH/KHMT dùng các nguyên tắc chung sau của ASD-STE100 Issue 9:

- Tách quy tắc viết và controlled dictionary.
- Dùng dạng chuẩn, nghĩa chuẩn và từ loại chuẩn.
- Tách procedural writing và descriptive writing.
- Giới hạn câu thủ tục và câu mô tả.
- Viết một lệnh trong một bước.
- Đặt điều kiện trước lệnh.
- Dùng một chủ đề trong một đoạn mô tả.

TVKTĐGH/KHMT có các điều chỉnh riêng:

- Quy tắc thời, thể và câu bị động phù hợp với tiếng Việt.
- Quy tắc cụm danh từ phù hợp với cấu trúc danh từ chính đứng trước.
- Chính sách A/B/C xử lý nội dung trộn tiếng Việt và tiếng Anh.
- Cảnh báo vận hành bao gồm dữ liệu, bảo mật và availability.
- Agent profile quy định độ tin cậy của output.

Nguồn chính:

- ASD-STE100, Issue 9, January 2025: <https://asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf>
- ASD-STE100 official portal: <https://www.asd-ste100.org/>

---

# PHỤ LỤC B — BẢNG TRA NHANH

| Hạng mục | Quy tắc |
|---|---|
| Câu thủ tục | Tối đa 20 token; một lệnh. |
| Câu mô tả | Tối đa 25 token; một ý chính. |
| Đoạn mô tả | Một chủ đề; tối đa sáu câu. |
| Điều kiện | Đặt trước lệnh. |
| Thuật ngữ | Dùng entry trong glossary. |
| Dữ kiện thiếu | `[CẦN BỔ SUNG: ...]` |
| Suy luận | `[SUY LUẬN]` |
| Tuân thủ | Không có `error`; review mọi `warning`. |
