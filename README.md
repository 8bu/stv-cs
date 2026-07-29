# TVKTĐGH/KHMT

**Tiếng Việt Kỹ thuật Đơn giản hóa cho Khoa học Máy tính**
*Simplified Technical Vietnamese for Computer Science (STV‑CS)*

Chuẩn ngôn ngữ kiểm soát để viết tài liệu khoa học máy tính (KHMT) bằng tiếng Việt. Mô hình theo [ASD‑STE100](https://www.asd-ste100.org/). Mục tiêu: tài liệu rõ, nhất quán, dễ đọc cho kỹ sư.

> **TVKTĐGH** = **T**iếng **V**iệt **K**ỹ **t**huật **Đ**ơn **g**iản **h**óa (lấy chữ cái đầu của từng tiếng). **/KHMT** = **K**hoa **h**ọc **M**áy **t**ính.

## Nguyên tắc cốt lõi

- Câu ngắn, một câu một lệnh, dùng câu chủ động.
- **Giữ thuật ngữ chuyên ngành ở tiếng Anh.** Chỉ dịch khi có từ tiếng Việt chuẩn và không mơ hồ.
- Thuật ngữ chia 3 tầng: **A** (giữ tiếng Anh), **B** (Anh + chú thích Việt lần đầu), **C** (ưu tiên Việt).

## Nội dung repo

| Đường dẫn | Nội dung |
|---|---|
| [`spec/TVKTDGH-KHMT.md`](spec/TVKTDGH-KHMT.md) | Toàn văn chuẩn: quy tắc viết, từ điển, **14 ví dụ trước/sau** (Phần 3), hướng dẫn áp dụng. |
| [`glossary/glossary.csv`](glossary/glossary.csv) | Từ điển máy đọc: thuật ngữ, tầng A/B/C, dạng dùng, chú thích. |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Cách góp ý và thêm thuật ngữ mới. |
| [`CHANGELOG.md`](CHANGELOG.md) | Lịch sử phiên bản. |
| [`typst/paper.typ`](typst/paper.typ) | Template Typst để build spec ra PDF. |
| [`.github/workflows/build-pdf.yml`](.github/workflows/build-pdf.yml) | CI: build PDF mỗi push/PR (lưu artifact để kiểm tra). |
| [`.github/workflows/release-please.yml`](.github/workflows/release-please.yml) | Tự động hóa release: version, CHANGELOG, tag, Release (đính PDF + Markdown). |

## Bắt đầu nhanh

1. Đọc [`spec/TVKTDGH-KHMT.md`](spec/TVKTDGH-KHMT.md), tập trung Phần 1 (quy tắc) và mục 2.1 (chính sách 3 tầng).
2. Lập glossary cho team dựa trên [`glossary/glossary.csv`](glossary/glossary.csv).
3. Dùng checklist tuân thủ (Phần 4) khi review tài liệu và pull request.

## Build PDF

PDF được build từ Markdown spec bằng [Typst](https://typst.app) (package `cmarker`).

Build tại máy:

```bash
make pdf        # hoặc: typst compile --root . typst/paper.typ TVKTDGH-KHMT.pdf
```

CI tự build mỗi lần push `main` hoặc mở PR — PDF nằm trong build artifacts để kiểm tra.

## Release (tự động, release-please)

Không cần gõ tay version hay tag. Chỉ cần commit theo [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`…):

1. Push commit lên `main`.
2. [release-please](https://github.com/googleapis/release-please) mở sẵn một **release PR** — gom thay đổi, tự tính version, cập nhật `CHANGELOG.md`.
3. Merge PR đó → nó tạo git tag + **GitHub Release**, và đính kèm **PDF + Markdown**.

Version hiển thị trong spec và title page (dòng có `x-release-please-version`) được bump tự động.

## Đóng góp

Xem [`CONTRIBUTING.md`](CONTRIBUTING.md). Mọi tài liệu và góp ý viết theo đúng chuẩn TVKTĐGH.

## License

[CC BY 4.0](https://github.com/8bu/stv-cs/blob/main/LICENSE) — © 2026 8bu. Free to use with attribution.
