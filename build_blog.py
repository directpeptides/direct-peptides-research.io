#!/usr/bin/env python3
# Generate static posts and Library listings from data/posts.json.
# Run python3 tools/build_blog.py from repository root.
from pathlib import Path
from html import escape
import json, re, sys
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent.parent
BASE='https://directpeptides.github.io/direct-peptides-research.io/'
rows=json.loads((ROOT/'data/posts.json').read_text(encoding='utf-8'))
if not isinstance(rows,list): raise SystemExit('posts.json must be a JSON list')
site=BeautifulSoup((ROOT/'index.html').read_text(encoding='utf-8'),'html.parser')
header=str(site.select_one('.top'))+str(site.header)
footer=str(site.footer)
cards=[]; urls=[]; slugs=set()
(ROOT/'posts').mkdir(exist_ok=True)
for item in rows:
 for required in ('slug','title','description','body_html'):
  if not isinstance(item.get(required),str) or not item[required].strip():raise SystemExit('Missing: '+required)
 slug=item['slug'].strip()
 if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug) or slug in slugs:raise SystemExit('Invalid or duplicate slug: '+slug)
 slugs.add(slug)
 title=item['title'].strip();desc=item['description'].strip();topic=item.get('topic','Research education')
 # Authored body HTML is editorial input; do not paste untrusted scripts or embeds.
 body=item['body_html']
 soup=BeautifulSoup(body,'html.parser')
 if soup.find(['script','iframe','object','embed']):raise SystemExit('Remove script/iframe/embed from '+slug)
 for tag in soup.find_all(True):
  for key in list(tag.attrs):
   if key.lower().startswith('on'): raise SystemExit('Inline event handler in '+slug)
 url=BASE+'posts/'+slug+'.html'
 article=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(title)} | Direct Peptides Learning Center</title><meta name="description" content="{escape(desc,quote=True)}"><meta name="robots" content="index,follow"><link rel="canonical" href="{escape(url,quote=True)}"><link rel="icon" href="../direct-peptides-circle-400.png"><link rel="stylesheet" href="../styles.css"></head><body>{header}<main><article class="article-layout"><a class="article-return" href="../library.html">← Back to Learning Library</a><div class="eyebrow">{escape(topic)}</div><h1>{escape(title)}</h1><div class="article-meta">Educational research article</div><div class="article-body">{body}</div><div class="note"><strong>Research information:</strong> Experimental findings do not establish safety or effectiveness in people. No dosing or administration advice is provided.</div></article></main>{footer}<script src="../script.js" defer></script></body></html>'''
 # Convert root-relative navigation in re-used header/footer to post-parent relative
 parsed=BeautifulSoup(article,'html.parser')
 for tag in parsed.select('header a[href], footer a[href]'):
  h=tag.get('href','')
  if h and not h.startswith(('https:','http:','#','mailto:','tel:','../','/')):tag['href']='../'+h
 for img in parsed.select('header img[src], footer img[src]'):
  h=img.get('src','')
  if h and not h.startswith(('https:','http:','../','/')):img['src']='../'+h
 (ROOT/'posts'/(slug+'.html')).write_text(str(parsed),encoding='utf-8')
 cards.append(f'<article class="card" data-item><span class="tag">{escape(topic)}</span><h3>{escape(title)}</h3><p>{escape(desc)}</p><a href="posts/{slug}.html">Read article</a></article>')
 urls.append('posts/'+slug+'.html')
lib=ROOT/'library.html';s=lib.read_text(encoding='utf-8')
start='<!-- BLOG_CARDS_START -->';end='<!-- BLOG_CARDS_END -->'
if start not in s or end not in s:raise SystemExit('Missing library markers')
s=s.split(start)[0]+start+'\n'+'\n'.join(cards)+'\n'+end+s.split(end,1)[1]
lib.write_text(s,encoding='utf-8')
# Remove only previously generator-managed post pages that were deleted from JSON
for p in (ROOT/'posts').glob('*.html'):
 if p.name not in {x['slug']+'.html' for x in rows}:p.unlink()
known=['index.html','about.html','library.html','contact.html','privacy.html']+urls
xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{BASE}{v}</loc></url>\n' for v in known)+'</urlset>\n'
(ROOT/'sitemap.xml').write_text(xml,encoding='utf-8')
print(f'Built {len(rows)} articles, updated Learning Library and sitemap.')
