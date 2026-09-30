# Editable CV

Edit `content.json`, then run:

```bash
python3 -m pip install -r cv/requirements.txt
python3 cv/build_cv.py
```

The script writes `assets/Xia_Su_CV_2026.pdf`, the stable download linked by the website. It uses standard PDF fonts and checks for content extending beyond the page body. `archive/Xia_Su_CV_2026_before_update.pdf` preserves the original CV.

## Editorial basis

- The September 2026 revision describes the current Google role using the owner's account. Start date: August 31, 2026; shown at month precision. Role: Software Engineer. No unconfirmed team name, product, deployment result, or performance metrics are added.
- Research profile emphasizes AI as a bridge between people and spaces, linking architecture, HCI, accessibility, and computer vision.
- UW doctoral defense is reported without asserting formal degree conferral. The original website independently lists an M.S. in Computer Science & Engineering in 2024.
- The original website and CV disagree on the Tsinghua master's degree title. The public CV uses “master's degree” pending confirmation.
- CapNav and DepthScape are listed at their 2026 publication venues. The original CV's DepthScape author list was corrected to the paper's four authors.
- The published Adobe audio patent application is identified by publication number; it is not represented as a granted patent. The two other inventions retain their original names, inventors, and affiliations without repeating unverifiable “in process” statuses or assigning a new legal classification.
- Mentoring start dates are retained without asserting that the engagements are still active.

## Verification

After every substantive edit, render all three pages and inspect the resulting PNGs. For example, with Poppler:

```bash
pdftoppm -r 140 -png assets/Xia_Su_CV_2026.pdf cv/qa/page
```

Check title wrapping, section spacing, links, page numbers, and text extraction. Rendered QA files are local intermediates, not website assets.

The September 2026 version was rendered with PDFium (`pypdfium2`) after the bundled Poppler encountered a font-cache configuration error. All three pages were visually inspected; no clipping, overlap, missing glyphs, or pagination defects were found. PDF text extraction and all 17 link annotations were also checked.
