# Xia Su — personal research website

A dependency-free static website for GitHub Pages. The main page connects spatial AI, human–AI interaction, and accessibility research with Xia's current computer vision work at Google.

## Preview

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open `http://127.0.0.1:8765`. No build step is required. GitHub Pages serves the repository's default branch.

## Update

- `index.html`: biography, current work, research, links, and search/social metadata.
- `assets/css/style.css`: responsive layout and visual system.
- `assets/js/script.js`: keyboard-accessible research perspective tabs.
- `assets/images/`: original research and profile imagery from the previous site, plus the favicon.
- `cv/content.json`: editable CV content; see `cv/README.md` to regenerate the linked PDF.
- `sitemap.xml`: update the modification date after substantial content changes.

Research media link to the authors' existing demonstration videos. The homepage diagram is conceptual, not a visualization of experimental results or an internal Google system. Content remains readable without JavaScript; motion respects the visitor's reduced-motion preference.

The CapNav overview image is reproduced from the [official project page](https://makeabilitylab.github.io/CapNav/). Other project images and video links were retained from the original site.
