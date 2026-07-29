# Đóng góp cho TVKTĐGH‑100/KHMT

Cảm ơn bạn góp sức. Tài liệu này là chuẩn sống; nó cải thiện theo phản hồi thực tế.

## Quy tắc chung

- Viết mọi issue, PR, và tài liệu theo đúng chuẩn TVKTĐGH.
- Một PR, một thay đổi rõ ràng. Không gộp nhiều thay đổi không liên quan.
- Mô tả PR nêu: thay đổi gì, vì sao, ảnh hưởng tới quy tắc/thuật ngữ nào.

## Thêm hoặc sửa thuật ngữ

1. Sửa `glossary/glossary.csv`. Giữ đúng thứ tự cột.
2. Gán tầng cho thuật ngữ theo cây quyết định (Phụ lục B của chuẩn):
   - Xuất hiện trong code/log/API/CLI → **A** (giữ tiếng Anh).
   - Khái niệm học thuật có tên Việt phổ biến → **B** (Anh + chú thích Việt).
   - Từ vựng cơ bản, ổn định → **C** (ưu tiên Việt).
3. Ghi lý do trong PR nếu chuyển tầng một thuật ngữ đã có.

## Sửa quy tắc viết

- Nêu số hiệu quy tắc (ví dụ: QT 4.1).
- Kèm ví dụ **Không dùng / Dùng** cho quy tắc mới hoặc sửa.

## Quy trình

1. Fork repo và tạo branch: `feature/<mô-tả-ngắn>`.
2. Commit message viết theo chuẩn (câu mệnh lệnh, ngắn). Ví dụ: `Thêm thuật ngữ "idempotent" vào tầng A`.
3. Mở pull request. Ít nhất một reviewer duyệt.
4. Cập nhật `CHANGELOG.md` nếu thay đổi ảnh hưởng người dùng.

## Báo lỗi

Mở issue. Nêu: vị trí (file, số hiệu quy tắc), lỗi là gì, đề xuất sửa.
