// Build the TVKTĐGH/KHMT standard PDF from the Markdown spec.
// Compile: typst compile --root . typst/paper.typ TVKTDGH-KHMT.pdf
#import "@preview/cmarker:0.1.6"

#let title = "TVKTĐGH/KHMT"
#set document(title: title, author: "8bu")

#set page(
  paper: "a4",
  margin: (x: 2.2cm, top: 2.3cm, bottom: 2cm),
  numbering: "1",
  number-align: center,
)
#set text(font: "New Computer Modern", size: 10.5pt, lang: "vi")
#set par(justify: true, leading: 0.62em, spacing: 0.95em)
#show heading.where(level: 1): set text(size: 15pt)
#show heading.where(level: 2): set text(size: 12.5pt)
#show link: set text(fill: rgb("#1a5fb4"))
#show raw: set text(font: "DejaVu Sans Mono", size: 8.5pt)
#show table.cell.where(y: 0): set text(weight: "bold")

// ---- Title page ----
#page(numbering: none)[
  #set align(center)
  #v(4.5cm)
  #text(size: 30pt, weight: "bold")[TVKTĐGH/KHMT]
  #v(8pt)
  #line(length: 38%, stroke: 0.6pt)
  #v(12pt)
  #text(size: 13pt)[Tiếng Việt Kỹ thuật Đơn giản hóa \ cho Khoa học Máy tính]
  #v(8pt)
  #text(size: 11pt, style: "italic", fill: luma(35%))[Simplified Technical Vietnamese for Computer Science]
  #v(2.2cm)
  #text(size: 11pt)[Phiên bản 0.1.0 · 29-07-2026] // x-release-please-version
  #v(5pt)
  #text(size: 10pt, fill: luma(35%))[© 2026 8bu · Giấy phép CC BY 4.0]
  #v(1fr)
  #text(size: 9pt, fill: luma(45%))[Phỏng theo ASD-STE100]
]

// ---- Table of contents ----
#outline(title: [Mục lục], depth: 2, indent: auto)
#pagebreak()

// ---- Body: render Markdown, stripping the leading title block ----
#let src = read("/spec/TVKTDGH-KHMT.md")
#let body = src.split("\n---\n").slice(1).join("\n---\n")
#cmarker.render(body, h1-level: 1)
