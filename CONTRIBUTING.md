# Đóng góp cho TVKTĐGH/KHMT

Mọi thay đổi PHẢI giữ spec, glossary và validator đồng bộ.

## Nguyên tắc chung

- Một pull request chỉ chứa một thay đổi có mục đích rõ ràng.
- Mô tả pull request nêu thay đổi, lý do và phạm vi ảnh hưởng.
- Dùng số hiệu quy tắc hoặc dạng `canonical` của thuật ngữ khi có thể.
- Không sửa phần glossary được sinh trong spec bằng tay.

## Sửa thuật ngữ

`glossary/glossary.csv` là nguồn sự thật duy nhất.

1. Thêm hoặc sửa row trong CSV.
2. Chọn đúng `language_policy`, từ loại, nghĩa và phạm vi.
3. Thêm ví dụ đúng và ví dụ sai.
4. Ghi lý do nếu thay đổi dạng chuẩn hoặc policy hiện có.
5. Chạy `make sync`.
6. Chạy `make check` và `make test`.

Một dạng có nhiều từ loại hoặc nghĩa PHẢI có nhiều row.
Dùng `|` để phân tách nhiều giá trị trong `forbidden_alternatives`.

## Sửa quy tắc

Mỗi thay đổi quy tắc PHẢI có:

- Số hiệu ổn định.
- Lý do thay đổi.
- Ví dụ **Không dùng / Dùng**.
- Ghi chú migration nếu output hợp lệ trước đây trở thành không hợp lệ.
- Fixture nếu validator kiểm tra quy tắc.

Không đổi số hiệu của quy tắc không liên quan.

## Sửa Agent profile

Nêu rõ thay đổi ảnh hưởng đến cấu trúc output hay độ tin cậy của output.
Không biến quy tắc an toàn hoặc hành vi sản phẩm thành quy tắc ngôn ngữ nếu hai nội dung không liên quan.

## Kiểm tra trước pull request

```bash
make sync
make check
make test
make pdf
```

`make sync` KHÔNG ĐƯỢC tạo diff sau khi đã commit bảng glossary mới.

## Commit và release

Dùng Conventional Commits. Ví dụ:

```text
feat: thêm quy tắc cho modal tiếng Việt
fix: đồng bộ nghĩa của queue trong glossary
docs: giải thích quy trình thêm thuật ngữ
```

Không sửa `CHANGELOG.md`, version hoặc tag bằng tay. Release-please quản lý các giá trị này.

## Báo lỗi

Issue PHẢI nêu:

- File và số hiệu quy tắc hoặc thuật ngữ.
- Hành vi hiện tại.
- Hành vi mong muốn.
- Ví dụ tối thiểu tái hiện vấn đề.
