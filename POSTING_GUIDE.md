# Posting guide — Direct Peptides Learning Center

## Before upload
Upload the CONTENTS of this ZIP to the repository root (not the enclosing folder). Make sure `index.html`, `direct-peptides-circle-400.png`, `assets/`, and `posts/` retain their exact paths. Existing matching files should be replaced; do not delete unrelated articles.

## Add future blog posts
1. Open `data/posts.json` and add an item following this JSON schema:
```json
[
  {
    "slug": "example-research-article",
    "title": "Example Research Article",
    "description": "A short original summary of the article, around 140 characters.",
    "topic": "Research methods",
    "body_html": "<p>Write your original opening paragraph here.</p><h2>What the evidence says</h2><p>Explain research findings with appropriate context.</p>"
  }
]
```
This is only an example: DO NOT publish it as a real article. Replace it with checked original content.
2. Install Python and `beautifulsoup4` on a computer: `python -m pip install beautifulsoup4`.
3. Run `python tools/build_blog.py` in this folder.
4. Upload changed `data/posts.json`, `library.html`, `sitemap.xml` and new `posts/<slug>.html` files to GitHub. Future new posts are automatically added to the Learning Library and sitemap when the script runs. Existing articles remain intact.
5. Verify the article, navigation, logo, and Library link on GitHub Pages after publishing.

## Optional no-Python workflow
Copy a previously generated article HTML file into `posts/` and edit the title, meta description, canonical URL and article body. Then manually add a matching card to `library.html` and the URL to `sitemap.xml`. Never upload articles to `posts/` without updating the Library.

## GitHub Pages settings
Repository: `directpeptides/direct-peptides-research.io`.
Settings > Pages > Deploy from a branch > `main` > `/ (root)`.
Expected project URL: https://directpeptides.github.io/direct-peptides-research.io/

## Notes
- The source screenshot showed the logo uploaded at root while the previous HTML pointed to `/assets/`. This ZIP includes the icon in BOTH places; all HTML now points to the root copy.
- This is a STATIC site. Blog posts do NOT appear automatically when writing a WordPress.com article; run the generator or edit the HTML pages manually.
- Each piece needs human factual, regulatory and link review before it is published.
- Publishing and indexing cannot be guaranteed by a ZIP.
- `privacy.html` is a draft and needs owner review.
- The website's relationship to the Direct Peptides brand needs confirmation before changing the independently educational wording.
