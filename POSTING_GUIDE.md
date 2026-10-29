# How to publish a blog post (flat repository)

All website files live in the GitHub repository root; there are no required folders.

## Option A — Upload one HTML article directly
Copy `article-template.html` to `post-your-topic.html`, replace title, description, canonical URL and body text, then upload it to your repository. Add a card linking to this article in `blog.html` and `library.html`, and its URL to `sitemap.xml`.

## Option B — Generate articles automatically
1. Add an item to `posts.json`, with `slug`, `title`, `description`, `topic`, and `body_html`.
2. Run `python build_blog.py` locally (requires `pip install beautifulsoup4`).
3. Upload changed `posts.json`, `blog.html`, `library.html`, `sitemap.xml`, and new `post-*.html` to GitHub.
4. Commit. GitHub Pages redeploys automatically.

`posts.json` begins as an empty array; no article is published yet. Always verify scientific claims and preview each post.

Example JSON item (replace and validate scientific content):
```json
{ "slug":"reading-scientific-evidence", "title":"How to Read Scientific Evidence", "description":"Learn how research study design shapes scientific claims.", "topic":"Research methods", "body_html":"<p>Describe your verified topic here.</p>" }
```

## GitHub
Settings > Pages > Deploy from a branch > main > / (root). Do not upload the ZIP itself. Extract it and upload all files. When uploading an update, replace older versions where GitHub prompts.
