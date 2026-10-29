#!/usr/bin/env python3
"""Run: python build_blog.py after editing posts.json. All generated files stay in root."""
from pathlib import Path
from html import escape
import json, re
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent
BASE='https://directpeptides.github.io/direct-peptides-research.io/'
rows=json.loads((ROOT/'posts.json').read_text(encoding='utf-8'))
if not isinstance(rows,list): raise SystemExit('posts.json must be a JSON array')
site=BeautifulSoup((ROOT/'index.html').read_text(encoding='utf-8'),'html.parser')
header=str(site.select_one('.top'))+str(site.header)
footer=str(site.footer)
cards=[]; urls=[]; slugs=set()
for item in rows:
 for required in ('slug','title','description','body_html'):
  if not isinstance(item.get(required),str) or not item[required].strip(): raise SystemExit('Missing '+required)
 slug=item['slug'].strip()
 if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug) or slug in slugs: raise SystemExit('Invalid or duplicate slug: '+slug)
 slugs.add(slug)
 title=item['title'].strip(); desc=item['description'].strip(); topic=item.get('topic','Research education'); body=item['body_html']
 dom=BeautifulSoup(body,'html.parser')
 if dom.find(['script','iframe','object','embed']): raise SystemExit('No script, iframe or embed allowed in article')
 for tag in dom.find_all(True):
  for key in tag.attrs:
   if key.lower().startswith('on'): raise SystemExit('Remove inline event handlers')
 filename='post-'+slug+'.html';url=BASE+filename
 article=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | Direct Peptides Learning Center</title><meta name="description" content="{escape(desc,quote=True)}"><link rel="canonical" href="{url}"><link rel="icon" type="image/png" href="favicon.png"><link rel="stylesheet" href="styles.css"></head><body>{header}<main><article class="article-layout"><a class="article-return" href="blog.html">← Back to Blog</a><div class="eyebrow">{escape(topic)}</div><h1>{escape(title)}</h1><div class="article-meta">Educational research article</div><div class="article-body">{body}</div><div class="note"><strong>Research information:</strong> Experimental findings do not establish safety or effectiveness in people. No dosing or administration advice is provided.</div></article></main>{footer}<script src="script.js" defer></script></body></html>'''
 (ROOT/filename).write_text(article,encoding='utf-8')
 cards.append(f'<article class="card" data-item><span class="tag">{escape(topic)}</span><h3>{escape(title)}</h3><p>{escape(desc)}</p><a href="{filename}">Read article</a></article>')
 urls.append(filename)
for filename in ('blog.html','library.html'):
 p=ROOT/filename;s=p.read_text(encoding='utf-8');start='<!-- BLOG_CARDS_START -->';end='<!-- BLOG_CARDS_END -->'
 if start not in s or end not in s:raise SystemExit('Missing BLOG_CARDS markers in '+filename)
 s=s.split(start,1)[0]+start+'\n'+'\n'.join(cards)+'\n'+end+s.split(end,1)[1]
 p.write_text(s,encoding='utf-8')
for p in ROOT.glob('post-*.html'):
 if p.name not in set(urls):p.unlink()
known=['index.html','about.html','library.html','blog.html','contact.html','privacy.html']+urls
xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{BASE}{v}</loc></url>\n' for v in known)+'</urlset>\n'
(ROOT/'sitemap.xml').write_text(xml,encoding='utf-8')
print(f'Generated {len(rows)} post pages and updated blog.html, library.html, sitemap.xml')
