# TVKTĐGH/KHMT

**Tiếng Việt Kỹ thuật Đơn giản hóa cho Khoa học Máy tính**  
*Simplified Technical Vietnamese for Computer Science (STV-CS)*

TVKTĐGH/KHMT là chuẩn ngôn ngữ kiểm soát cho tài liệu khoa học máy tính bằng tiếng Việt. Chuẩn phỏng theo nguyên tắc của [ASD-STE100 Issue 9](https://asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf), nhưng không phải bản dịch của ASD-STE100.

## Kiến trúc

Chuẩn có ba lớp trong một tài liệu phát hành:

1. **Chuẩn lõi** quy định từ, câu, thủ tục, mô tả và cảnh báo.
2. **KHMT profile** quy định thuật ngữ và token kỹ thuật.
3. **Agent profile** quy định cấu trúc và độ tin cậy của output do agent tạo.

`glossary/glossary.csv` là nguồn sự thật duy nhất cho thuật ngữ. `make sync` sinh controlled dictionary trong spec từ CSV.

## Nội dung repo

| Đường dẫn | Nội dung |
|---|---|
| [`spec/TVKTDGH-KHMT.md`](spec/TVKTDGH-KHMT.md) | Toàn văn chuẩn và controlled dictionary đã sinh. |
| [`glossary/glossary.csv`](glossary/glossary.csv) | Nguồn thuật ngữ máy đọc. |
| [`tools/validate.py`](tools/validate.py) | Công cụ đồng bộ, kiểm tra repo và lint tài liệu. |
| [`tests/`](tests/) | Fixture và test hành vi của validator. |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Quy trình sửa quy tắc và thuật ngữ. |
| [`typst/paper.typ`](typst/paper.typ) | Template PDF của bản chuẩn. |

## Bắt đầu nhanh

```bash
make sync   # Sinh bảng thuật ngữ trong spec từ glossary.csv
make check  # Kiểm tra glossary, spec và reference quy tắc
make test   # Chạy test của validator
make pdf    # Build TVKTDGH-KHMT.pdf
```

Lint một tài liệu:

```bash
python3 tools/validate.py lint path/to/document.md
```

Validator báo ba mức:

- `error`: vi phạm xác định được và chặn phát hành.
- `warning`: vấn đề cần người review.
- `info`: gợi ý không chặn phát hành.

## Quy trình sửa thuật ngữ

1. Sửa `glossary/glossary.csv`.
2. Chạy `make sync`.
3. Chạy `make check` và `make test`.
4. Commit cả CSV và spec đã đồng bộ.

Không sửa bảng glossary được sinh trong spec bằng tay.

## Build PDF

Cài [Typst](https://typst.app), sau đó chạy:

```bash
make pdf
```

CI kiểm tra validator, test và PDF trên mỗi pull request.

## Release

Repo dùng [release-please](https://github.com/googleapis/release-please). Dùng [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` cho thay đổi quy tắc hoặc khả năng mới.
- `fix:` cho sửa lỗi chuẩn, glossary hoặc validator.
- `docs:` cho thay đổi không làm đổi hành vi chuẩn.

Sau khi release PR được merge, workflow tạo tag và GitHub Release. Release đính kèm Markdown, glossary và PDF.

## License

[CC BY 4.0](LICENSE) — © 2026 8bu.

ASD-STE100 là tài sản của ASD. Repo này chỉ tham khảo các nguyên tắc công khai và không tái bản nội dung chuẩn ASD-STE100.
