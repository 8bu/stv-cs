# TVKTĐGH/KHMT — Tiếng Việt Kỹ thuật Đơn giản hóa cho Khoa học Máy tính

**Simplified Technical Vietnamese for Computer Science (STV‑CS)**
Phiên bản 0.1.0 — 2026-07-29 <!-- x-release-please-version -->

**TVKTĐGH** là viết tắt, lấy chữ cái đầu của **từng tiếng**: **T**iếng **V**iệt **K**ỹ **t**huật **Đ**ơn **g**iản **h**óa. Hậu tố **/KHMT** = **K**hoa **h**ọc **M**áy **t**ính.

Đây là chuẩn ngôn ngữ kiểm soát cho tài liệu KHMT. Mô hình theo ASD‑STE100. Đối tượng dùng: kỹ sư phần mềm, kỹ sư ML, kỹ sư hệ thống, người viết tài liệu kỹ thuật, người review.

Nguyên tắc cốt lõi của bản này: **giữ thuật ngữ chuyên ngành ở tiếng Anh**. Chỉ dịch khi có từ tiếng Việt chuẩn, ổn định, và không gây mơ hồ.

---

## 0. Giới thiệu

### 0.1 Mục đích

TVKTĐGH/KHMT làm cho tài liệu KHMT rõ ràng, nhất quán, và dễ đọc cho kỹ sư. Chuẩn này bỏ sự mơ hồ, giảm số cách nói cho cùng một ý, và giữ thuật ngữ ở dạng mà kỹ sư đọc mỗi ngày (dạng tiếng Anh).

### 0.2 Vì sao giữ tiếng Anh

Kỹ sư KHMT đọc code, log, API, và tài liệu gốc bằng tiếng Anh. Dịch thuật ngữ sang tiếng Việt thường gây ba vấn đề:

- **Mất khớp với công cụ.** Từ khóa trong IDE, thông báo lỗi, và tên hàm ở tiếng Anh. Bản dịch làm người đọc phải ánh xạ ngược.
- **Nhiều bản dịch cho một từ.** Ví dụ "pointer" từng được dịch là "con trỏ", "trỏ", "biến trỏ". Giữ `pointer` bỏ được sự phân mảnh này.
- **Sai nghĩa tinh tế.** "Thread", "process", "task" dịch chung thành "luồng"/"tiến trình" gây nhầm. Giữ tiếng Anh giữ đúng nghĩa.

Cách này khớp với thực tế viết của các chuyên gia KHMT Việt Nam: họ giữ `input`, `label`, `training set`, `framework`, `overfitting`, `feature engineering` ở tiếng Anh, và chỉ chú thích tiếng Việt trong ngoặc khi cần (xem mục Nguồn tham khảo).

### 0.3 Phạm vi áp dụng

Dùng chuẩn này cho: tài liệu thiết kế (design doc), README, hướng dẫn API, runbook vận hành, ghi chú review code (code review), báo cáo sự cố (incident report / postmortem), tài liệu ML (model card, data card), và commit message dạng mô tả.

Không bắt buộc cho: hợp đồng, văn bản pháp lý, nội dung tiếp thị.

---

# PHẦN 1 — QUY TẮC VIẾT

Áp dụng đủ 9 nhóm quy tắc của TVKTĐGH. Bản này chỉ nêu các quy tắc có điểm riêng cho KHMT. Các quy tắc còn lại giữ nguyên như bản gốc.

### QT 1.1 — Chỉ dùng từ được duyệt

Chỉ dùng từ trong Phần 2 hoặc trong glossary của dự án. Không tự dịch thuật ngữ đã có trong Phần 2.

| Không dùng | Dùng |
|---|---|
| Tiến hành triển khai dịch vụ lên môi trường sản xuất. | Deploy service lên production. |
| Thực hiện việc gộp nhánh. | Merge branch. |

### QT 1.5 — Tạo và giải thích từ viết tắt

**QT 1.5.1 — Cách tạo từ viết tắt tiếng Việt.** Từ viết tắt tiếng Việt lấy chữ cái đầu của **từng tiếng** (âm tiết), kể cả các tiếng nằm trong từ ghép. Không gộp một từ ghép thành một chữ cái.

| Cụm từ | Không dùng | Dùng |
|---|---|---|
| Tiếng Việt Kỹ thuật Đơn giản hóa | TVKĐ (gộp "Kỹ thuật"→K, "Đơn giản hóa"→Đ) | TVKTĐGH |
| Khoa học Máy tính | KHM (bỏ tiếng "tính") | KHMT |
| Cơ sở dữ liệu | CSD | CSDL |
| Trí tuệ nhân tạo | TTN | TTNT |

**QT 1.5.2 — Từ viết tắt tiếng Anh giữ nguyên.** Từ viết tắt gốc tiếng Anh giữ đúng dạng gốc, không tạo lại theo QT 1.5.1. Ví dụ: `API`, `SQL`, `HTTP`, `ML`, `CI/CD`, `SVM`. Đây là thuật ngữ Tầng A (xem Phần 2).

**QT 1.5.3 — Giải thích lần đầu.** Giải thích mỗi từ viết tắt ở lần xuất hiện đầu tiên. Viết cụm đầy đủ, rồi từ viết tắt trong ngoặc.

| Không dùng | Dùng |
|---|---|
| Kiểm tra CSDL trước khi deploy. | Kiểm tra cơ sở dữ liệu (CSDL) trước khi deploy. Sau đó chỉ dùng CSDL. |

### QT 3.1 — Dùng câu chủ động

| Không dùng | Dùng |
|---|---|
| Request được xử lý bởi middleware trước khi đến handler. | Middleware xử lý request trước handler. |

### QT 3.2 — Dùng động từ chỉ một hành động

Không dùng "thực hiện", "tiến hành", "xử lý" khi có động từ cụ thể (kể cả động từ tiếng Anh được duyệt).

| Không dùng | Dùng |
|---|---|
| Tiến hành thực hiện việc build lại image. | Build lại image. |
| Xử lý cái bug này. | Fix bug này. |

### QT 4.1 — Giới hạn độ dài câu

Câu hướng dẫn ≤ 20 từ. Câu mô tả ≤ 25 từ. Đếm mỗi thuật ngữ tiếng Anh là một từ.

| Không dùng | Dùng |
|---|---|
| Trước khi merge, hãy chạy full test suite, kiểm tra coverage, chạy linter, và bảo đảm CI pass để tránh làm hỏng build trên main. | Trước khi merge, làm bốn việc. Chạy full test suite. Kiểm tra coverage. Chạy linter. Bảo đảm CI pass. |

### QT 4.3 — Đặt điều kiện trước lệnh

| Không dùng | Dùng |
|---|---|
| Rollback deploy nếu error rate vượt 1%. | Nếu error rate vượt 1%, rollback deploy. |

### QT 7.3 — Cảnh báo đủ nguy cơ, hậu quả, cách tránh (áp dụng cho vận hành)

> **CẢNH BÁO:** Lệnh `DROP TABLE` chạy trực tiếp trên production. Xóa vĩnh viễn dữ liệu, không khôi phục được. Trước khi chạy, backup database và chạy trên staging trước.

### QT 8.2 — Định dạng token kỹ thuật

Viết tên định danh (identifier), lệnh, path, và tên hàm bằng `code style` (dấu nháy ngược). Giữ nguyên chữ hoa/thường như trong code.

| Không dùng | Dùng |
|---|---|
| Gọi hàm getUserById để lấy user. | Gọi `getUserById()` để lấy user. |
| Sửa file config chấm y a m l. | Sửa file `config.yaml`. |

---

# PHẦN 2 — TỪ ĐIỂN KIỂM SOÁT (KHMT)

## 2.1 Chính sách thuật ngữ: 3 tầng

Mỗi thuật ngữ thuộc một trong ba tầng. Tầng quyết định viết bằng tiếng Anh hay tiếng Việt.

### Tầng A — Giữ nguyên tiếng Anh, không dịch

Dùng cho thuật ngữ KHMT phổ biến mà bản dịch tiếng Việt gây mơ hồ, thiếu ổn định, hoặc lệch nghĩa. Viết y như tiếng Anh. Không chú thích tiếng Việt (trừ lần đầu, nếu người đọc mới).

Ví dụ Tầng A (danh từ): `framework`, `array`, `pointer`, `thread`, `process`, `cache`, `buffer`, `stack`, `heap`, `queue`, `hash`, `token`, `socket`, `endpoint`, `middleware`, `container`, `runtime`, `compiler`, `linker`, `boolean`, `enum`, `struct`, `interface`, `closure`, `callback`, `promise`, `deadlock`, `race condition`, `overfitting`, `gradient`, `tensor`, `embedding`, `epoch`, `batch`, `feature`, `label`, `checkpoint`, `latency`, `throughput`.

Ví dụ Tầng A (động từ): `commit`, `push`, `pull`, `merge`, `rebase`, `deploy`, `build`, `compile`, `debug`, `refactor`, `rollback`, `fork`, `mount`, `cache`, `parse`, `render`, `import`, `export`, `deprecate`, `spawn`, `throttle`, `benchmark`.

### Tầng B — Tiếng Anh chính, chú thích tiếng Việt lần đầu

Dùng cho thuật ngữ có bản dịch tiếng Việt được hiểu rộng, nhưng dạng tiếng Anh vẫn là dạng chính khi làm việc. Viết tiếng Anh, thêm tiếng Việt trong ngoặc **ở lần xuất hiện đầu tiên**, sau đó chỉ dùng tiếng Anh.

| Thuật ngữ (dạng dùng) | Chú thích lần đầu |
|---|---|
| machine learning | học máy |
| supervised learning | học có giám sát |
| unsupervised learning | học không giám sát |
| reinforcement learning | học tăng cường |
| deep learning | học sâu |
| training data | dữ liệu huấn luyện |
| feature extraction | trích xuất đặc trưng |
| classification | phân loại |
| regression | hồi quy |
| clustering | phân cụm |
| neural network | mạng nơ‑ron |

Ví dụ áp dụng: "Dùng **supervised learning** (học có giám sát) cho bài toán này. Supervised learning cần training data có label."

### Tầng C — Ưu tiên tiếng Việt, chú thích tiếng Anh lần đầu

Dùng cho khái niệm chung, ổn định, có từ tiếng Việt rõ nghĩa. Viết tiếng Việt, thêm tiếng Anh trong ngoặc ở lần đầu nếu cần.

| Tiếng Việt (dạng dùng) | Chú thích lần đầu |
|---|---|
| biến | variable |
| hàm | function |
| vòng lặp | loop |
| câu lệnh | statement |
| kiểu dữ liệu | data type |
| tệp | file |
| thư mục | directory |
| bộ nhớ | memory |
| mạng | network |
| máy chủ | server |
| cơ sở dữ liệu | database |
| bản ghi | record |
| hàng đợi (khi nói khái niệm chung) | queue |
| độ chính xác | accuracy |

**Quy tắc chọn tầng khi phân vân:** nếu từ xuất hiện trong code, log, hoặc tên API → Tầng A. Nếu là khái niệm học thuật có tên Việt phổ biến → Tầng B. Nếu là từ vựng cơ bản, dạy ở năm nhất → Tầng C.

## 2.2 Danh từ kỹ thuật được duyệt (Technical Names, mẫu KHMT)

| Từ | Tầng | Nghĩa dùng | Không dùng thay |
|---|---|---|---|
| `bug` | A | lỗi phần mềm | con bọ |
| `endpoint` | A | địa chỉ API nhận request | điểm cuối |
| `deploy` (dt) | A | lần đưa code lên môi trường chạy | sự triển khai |
| `commit` (dt) | A | một lần ghi thay đổi vào repo | bản giao nộp |
| `pull request` / `PR` | A | yêu cầu gộp code để review | yêu cầu kéo |
| `staging` | A | môi trường thử trước production | môi trường dàn dựng |
| `production` / `prod` | A | môi trường chạy thật | môi trường sản xuất |
| `overfitting` | A | mô hình khớp quá mức train data | quá khớp |
| `throughput` | A | số việc xử lý mỗi đơn vị thời gian | thông lượng |
| supervised learning | B | học có giám sát | — |
| cơ sở dữ liệu | C | nơi lưu dữ liệu có cấu trúc | — |

## 2.3 Động từ kỹ thuật được duyệt (Technical Verbs, mẫu KHMT)

| Động từ | Tầng | Nghĩa dùng | Ví dụ |
|---|---|---|---|
| `merge` | A | gộp nhánh code | Merge branch `feature/login` vào `main`. |
| `deploy` | A | đưa code lên môi trường chạy | Deploy service lên staging. |
| `rollback` | A | quay về phiên bản trước | Nếu lỗi, rollback về `v1.2.0`. |
| `build` | A | biên dịch và đóng gói | Build lại Docker image. |
| `parse` | A | phân tích cú pháp đầu vào | Parse response JSON. |
| `debug` | A | tìm và định vị lỗi | Debug hàm `handler()`. |
| `refactor` | A | sửa cấu trúc code, giữ hành vi | Refactor module `auth`. |
| train | B | huấn luyện mô hình | Train model trên tập mới. |
| kiểm thử | C | chạy test để tìm lỗi (test) | Kiểm thử API trước khi merge. |
| triển khai (nghĩa tổ chức, không phải deploy) | C | đưa vào áp dụng (rollout) | Triển khai quy trình review mới. |

## 2.4 Từ bị cấm và từ thay thế (KHMT)

| Từ bị cấm | Lý do | Dùng thay bằng |
|---|---|---|
| tiến hành / thực hiện | động từ rỗng | (bỏ, dùng động từ chính) |
| xử lý (khi mơ hồ) | nghĩa quá rộng | fix / parse / handle / lọc — chọn từ đúng |
| con trỏ (khi nói về pointer trong code) | nhiều biến thể dịch | `pointer` |
| sự triển khai (khi nói deploy) | dài, mơ hồ với rollout | `deploy` |
| khả dĩ | Hán‑Việt khó | có thể |
| tầm / cỡ / khoảng (cho số đo) | mơ hồ | từ … đến … |
| v.v. / vân vân | bỏ lửng | (liệt kê đủ, hoặc "và các mục khác trong danh sách X") |
| trộn lẫn tiếng Anh không nhất quán | phá nhất quán | theo đúng tầng A/B/C đã định |

## 2.5 Quy tắc hình thái cho thuật ngữ tiếng Anh

- **Số nhiều:** không thêm "s" tiếng Anh trong câu tiếng Việt. Viết "3 `pod`", không viết "3 `pods`". Số lượng do chữ số Việt quyết định.
- **Động từ tiếng Anh trong câu Việt:** dùng dạng nguyên thể, không chia thì. Viết "đã `deploy`", không viết "đã `deployed`".
- **Viết hoa:** giữ nguyên chữ hoa/thường của định danh trong code. `getUser` ≠ `getuser`.
- **Nối từ:** không ghép nửa Anh nửa Việt thành một từ. Viết "merge nhánh", không viết "merge‑nhánh" hay "mergenhánh".

---

# PHẦN 3 — VÍ DỤ KỸ THUẬT (Trước / Sau)

**Nguyên tắc:** cột **Sau** chỉ viết lại theo quy tắc và phải giữ **đúng, đủ** thông tin của cột **Trước**. Không thêm dữ kiện mới (số liệu, tên biến, tên lệnh, endpoint, bước xử lý). Nếu bản gốc thiếu thông tin mà quy tắc đòi hỏi, đánh dấu để tác giả bổ sung.

## 3.1 Ghi chú review code (Code review)

**Trước:**

> Chỗ này bạn nên tiến hành việc xử lý lại cái logic kiểm tra quyền vì hiện tại nó đang được thực hiện một cách lặp đi lặp lại ở nhiều nơi khác nhau trong codebase gây khó cho việc bảo trì về sau.

**Sau:**

> Logic kiểm tra quyền lặp ở nhiều nơi trong codebase. Việc này khó bảo trì. Nên refactor logic này vào một chỗ dùng chung.

## 3.2 Runbook vận hành

**Trước:**

> Khi hệ thống gặp sự cố quá tải thì cần phải tiến hành việc tăng số lượng bản sao của dịch vụ lên và đồng thời kiểm tra xem cơ sở dữ liệu có đang bị nghẽn hay không.

**Sau:**

> Khi service quá tải, làm hai việc. Tăng số replica của service. Kiểm tra xem database có bị nghẽn không.

## 3.3 Tài liệu ML

**Trước:**

> Chúng ta sẽ thực hiện việc huấn luyện mô hình học có giám sát với tập dữ liệu đã được gán nhãn và sau đó tiến hành đánh giá độ chính xác của nó ở trên tập kiểm thử để tránh việc mô hình bị quá khớp.

**Sau:**

> Train model bằng **supervised learning** (học có giám sát) trên training data có label. Đánh giá accuracy trên test set để tránh **overfitting** (quá khớp).

## 3.4 Hướng dẫn API

**Trước:**

> Người dùng sẽ gửi một yêu cầu đến điểm cuối và điểm cuối này sẽ trả về một phản hồi ở định dạng JSON chứa danh sách các đối tượng người dùng.

**Sau:**

> Người dùng gửi request đến endpoint. Endpoint trả response JSON chứa danh sách user.

## 3.5 Cảnh báo — bản gốc thiếu cách phòng tránh

**Trước:**

> Chú ý khi chạy lệnh này vì nó có thể sẽ xóa mất dữ liệu.

**Sau:**

> **CẢNH BÁO:** Lệnh này xóa mất dữ liệu. `[Cách phòng tránh — tác giả bổ sung]`.

*QT 7.3 đòi đủ nguy cơ – hậu quả – cách tránh, nhưng bản gốc thiếu "cách tránh" nên đánh dấu để tác giả điền, không tự bịa.*

## 3.6 Commit message

**Trước:**

> Đã thực hiện việc sửa lại cái hàm xử lý đăng nhập bởi vì nó đang bị lỗi khi mà người dùng nhập sai mật khẩu quá nhiều lần.

**Sau:**

> Fix hàm đăng nhập bị lỗi khi người dùng nhập sai mật khẩu quá nhiều lần.

## 3.7 Báo cáo sự cố (Incident report)

**Trước:**

> Vào lúc rạng sáng thì hệ thống đã gặp phải một sự cố và điều này đã dẫn đến việc là các người dùng không thể nào truy cập được vào ứng dụng trong một khoảng thời gian tương đối là dài.

**Sau:**

> Rạng sáng, hệ thống gặp sự cố. Người dùng không truy cập được ứng dụng trong thời gian dài.

*Không bịa giờ cụ thể hay số phút — bản gốc chỉ nói "rạng sáng", "thời gian dài".*

## 3.8 README — hướng dẫn cài đặt

**Trước:**

> Để có thể tiến hành việc cài đặt được thư viện này thì trước tiên bạn sẽ cần phải đảm bảo rằng là máy tính của bạn đã được cài đặt sẵn Python phiên bản 3 trở lên rồi sau đó mới chạy lệnh cài đặt.

**Sau:**

> Trước khi cài library này, máy phải có Python 3 trở lên. Sau đó chạy lệnh cài đặt.

*Điều kiện trước lệnh (QT 4.3). "Python 3 trở lên" giữ nguyên — có trong bản gốc.*

## 3.9 Tài liệu xử lý lỗi

**Trước:**

> Trong trường hợp mà API trả về mã lỗi thì hệ thống sẽ cần phải thực hiện việc ghi log lại và đồng thời gửi thông báo cho người quản trị được biết.

**Sau:**

> Nếu API trả về mã lỗi, hệ thống log lỗi và gửi thông báo cho admin.

## 3.10 Mô tả pull request

**Trước:**

> PR này được tạo ra nhằm mục đích là để giải quyết cái vấn đề liên quan tới việc trang chủ bị load chậm ở trên các thiết bị di động.

**Sau:**

> PR này fix vấn đề trang chủ load chậm trên thiết bị di động.

## 3.11 Ghi chú migration cơ sở dữ liệu

**Trước:**

> Chúng ta sẽ cần phải tiến hành việc thêm một cái cột mới vào trong bảng người dùng và cái cột này sẽ được dùng để lưu trữ thông tin về thời điểm mà người dùng đăng nhập lần cuối cùng.

**Sau:**

> Thêm một cột mới vào bảng người dùng. Cột này lưu thời điểm người dùng đăng nhập lần cuối.

## 3.12 Comment trong code

**Trước:**

> Cái hàm ở bên dưới đây được viết ra với mục đích chính là để thực hiện việc kiểm tra xem một cái chuỗi đầu vào có phải là một địa chỉ email hợp lệ hay là không.

**Sau:**

> Hàm này kiểm tra chuỗi đầu vào có phải email hợp lệ không.

## 3.13 Chuỗi danh từ dài

**Trước:**

> Tài liệu hướng dẫn cấu hình module xác thực người dùng hệ thống thanh toán.

**Sau:**

> Tài liệu hướng dẫn để cấu hình module xác thực người dùng của hệ thống thanh toán.

*Tách chuỗi danh từ dài bằng giới từ "để", "của" (QT 2.1). Không đổi nghĩa.*

## 3.14 Cảnh báo — bản gốc đủ thông tin

Ngược với 3.5: bản gốc đã có đủ nguy cơ – hậu quả – cách tránh; chỉ cần định dạng lại.

**Trước:**

> Lưu ý là nếu bạn xóa nhầm file config thì service sẽ không khởi động lại được nữa cho nên là bạn hãy nhớ sao lưu file đó ra một chỗ khác trước khi chỉnh sửa.

**Sau:**

> **CẢNH BÁO:** Xóa nhầm file config. Service sẽ không khởi động lại được. Trước khi sửa, sao lưu file config ra chỗ khác.

---

# PHẦN 4 — HƯỚNG DẪN ÁP DỤNG

## 4.1 Quy trình triển khai (4 bước)

1. **Lập glossary dự án.** Gán mỗi thuật ngữ vào Tầng A/B/C. Ghi dạng dùng chuẩn.
2. **Đào tạo.** Hướng dẫn kỹ sư quy tắc Phần 1 và chính sách 3 tầng.
3. **Viết và tự kiểm.** Dùng checklist mục 4.2 trước khi tạo PR.
4. **Review.** Người review ghi lỗi theo số hiệu quy tắc (ví dụ: QT 4.1) và theo tầng thuật ngữ.

## 4.2 Checklist tuân thủ

- [ ] Mỗi câu hướng dẫn ≤ 20 từ; mỗi câu mô tả ≤ 25 từ (QT 4.1).
- [ ] Câu ở dạng chủ động (QT 3.1).
- [ ] Không dùng "tiến hành / thực hiện / xử lý" khi có động từ cụ thể (QT 3.2).
- [ ] Mỗi thuật ngữ theo đúng Tầng A/B/C (mục 2.1); dùng nhất quán.
- [ ] Thuật ngữ Tầng A viết đúng dạng tiếng Anh; không tự dịch.
- [ ] Thuật ngữ Tầng B có chú thích tiếng Việt ở lần đầu.
- [ ] Định danh, lệnh, path viết `code style` (QT 8.2).
- [ ] Từ viết tắt tiếng Việt lấy chữ cái đầu của từng tiếng; giải thích ở lần đầu (QT 1.5).
- [ ] Không thêm "s" số nhiều tiếng Anh; động từ Anh không chia thì (mục 2.5).
- [ ] Điều kiện viết trước lệnh (QT 4.3).
- [ ] Cảnh báo đủ nguy cơ – hậu quả – cách tránh (QT 7.3).

## 4.3 Đo mức độ tuân thủ

> Tỷ lệ tuân thủ (%) = (số câu đạt ÷ tổng số câu) × 100

Mục tiêu đề xuất: ≥ 95% cho tài liệu phát hành.

## 4.4 Bảo trì chuẩn

- Giữ một glossary owner cho mỗi team.
- Xét duyệt thuật ngữ mới và cập nhật tầng mỗi quý.
- Khi một thuật ngữ Tầng A có bản dịch Việt trở nên phổ biến và ổn định, xét chuyển sang Tầng B.

---

## Phụ lục A — Bảng tra nhanh

| Hạng mục | Giá trị |
|---|---|
| Câu hướng dẫn | ≤ 20 từ |
| Câu mô tả | ≤ 25 từ |
| Chuỗi danh từ | ≤ 3 danh từ |
| Đoạn văn | ≤ 6 câu |
| Lệnh trong một câu | 1 |
| Tầng thuật ngữ | A (giữ Anh) / B (Anh + chú thích) / C (Việt) |

## Phụ lục B — Cây quyết định chọn tầng

```
Thuật ngữ này có xuất hiện trong code, log, API, hoặc CLI không?
├─ Có  → Tầng A (giữ tiếng Anh)
└─ Không
   ├─ Là khái niệm học thuật có tên Việt phổ biến (ML/AI/thuật toán)?
   │  └─ Có → Tầng B (Anh + chú thích Việt lần đầu)
   └─ Là từ vựng cơ bản, ổn định (biến, hàm, tệp, mạng)?
      └─ Có → Tầng C (Việt + chú thích Anh lần đầu)
```

## Phụ lục C — Nguồn tham khảo

Chính sách "giữ tiếng Anh + chú thích Việt trong ngoặc" trong bản này dựa trên phong cách viết thực tế của các tài liệu KHMT tiếng Việt:

- Nguyễn Văn Hiếu — "Machine learning là gì? Tổng quan về machine learning" (nguyenvanhieu.vn). Quan sát: giữ `input`, `label`, `training set`, `training example`, `framework`, `overfitting`, `feature engineering`, `confusion matrix` ở tiếng Anh; chú thích Việt trong ngoặc: học có giám sát (Supervised learning), phân loại (Classification), hồi quy (Regression).
- Vũ Hữu Tiệp — Machine Learning cơ bản (machinelearningcoban.com). Blog KHMT tiếng Việt tham chiếu rộng, giữ nguyên thuật ngữ toán/ML tiếng Anh.
- Tổng hợp thuật ngữ IT/lập trình (beelancer.vn, topdev.vn) — cho thấy hầu hết thuật ngữ lập trình giữ ở dạng tiếng Anh trong giao tiếp kỹ thuật.

---

*TVKTĐGH/KHMT v1.1 — chuẩn nội bộ, phỏng theo ASD‑STE100. Điều chỉnh glossary và tầng thuật ngữ theo nhu cầu team.*
