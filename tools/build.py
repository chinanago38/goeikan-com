#!/usr/bin/env python3
"""護衛艦.com のページを tools/content/*.html から生成する。
ファイル名 <dir>__<slug>.html → /<dir>/<slug>/、<dir>__index.html → /<dir>/、<name>.html → /<name>/、index.html → /
1行目 title、2行目 description、3行目以降 本文（h1・p.updated・h2 …・section.sources）。"""
import glob, html, os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://xn--ef1ay5jhyc.com"
CSS_VER = "20261125a"
AD = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1061443138303693" crossorigin="anonymous"></script>'
NAV = [("一般公開", "/koukai/"), ("護衛艦", "/kan/"), ("海戦", "/kaisen/"), ("戦艦", "/senkan/"), ("人物", "/jinbutsu/")]
SECTION_NAME = {"kaisen": ("海戦", "/kaisen/"), "senkan": ("戦艦", "/senkan/"), "jinbutsu": ("人物", "/jinbutsu/"),
                "kan": ("護衛艦", "/kan/"), "koukai": ("一般公開", "/koukai/"), "minato": ("港", "/minato/")}

def esc(s): return html.escape(s, quote=True)
def strip(s): return re.sub(r"<[^>]+>", "", s).strip()

def url_of(fname):
    b = os.path.basename(fname)[:-5]
    if b == "index": return "/"
    if "__" in b:
        d, s = b.split("__", 1)
        return f"/{d}/" if s == "index" else f"/{d}/{s}/"
    return f"/{b}/"

def wrap_tables(s):
    return re.sub(r"(?<!<div class=\"table-wrap\">)(<table\b.*?</table>)", r'<div class="table-wrap">\1</div>', s, flags=re.S)

def blockify(body):
    tail = ""
    k = body.find('<section class="sources">')
    if k >= 0:
        tail = body[k:].replace('<section class="sources">', '<section class="sources block">', 1)
        body = body[:k]
    out = []
    for p in re.split(r"(?=<h2[ >])", body):
        if not p.strip(): continue
        if p.lstrip().startswith("<h2"): out.append(f'<section class="block">{p.rstrip()}</section>\n')
        elif strip(p): out.append(f'<div class="block lead-block">{p.strip()}</div>\n')
    return "".join(out) + tail

def render(url, title, desc, body):
    m = re.search(r"<h1>(.*?)</h1>\s*(<p class=\"updated\">.*?</p>)?", body, re.S)
    hero = ""
    if m:
        hero = f'<div class="page-hero"><h1>{m.group(1)}</h1>{m.group(2) or ""}</div>\n'
        body = body[:m.start()] + body[m.end():]
    crumbs = [("護衛艦.com", "/")]
    seg = url.strip("/").split("/")
    if url != "/":
        if len(seg) == 2 and seg[0] in SECTION_NAME: crumbs.append(SECTION_NAME[seg[0]])
        crumbs.append((strip(m.group(1)) if m else title, None))
    crumb = " › ".join(f'<a href="{u}">{esc(t)}</a>' if u else esc(t) for t, u in crumbs)
    main = (f'  <div class="crumb">{crumb}</div>\n' if url != "/" else "") + hero + blockify(wrap_tables(body))
    nav = "".join(f'<a href="{u}">{t}</a>' for t, u in NAV)
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{DOMAIN}{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="{'website' if url == '/' else 'article'}">
<meta property="og:url" content="{DOMAIN}{url}">
<link rel="stylesheet" href="/assets/style.css?v={CSS_VER}">
{AD}
</head>
<body>
<header class="site"><div class="wrap">
  <a class="logo" href="/">護衛艦<span>.com</span></a>
  <nav class="global">{nav}</nav>
</div></header>

<main><div class="wrap">
{main}</div></main>

<footer class="site"><div class="wrap">
  <p>護衛艦.com は、護衛艦の一般公開や海の歴史をまとめた個人運営の情報サイトです。防衛省・海上自衛隊の公式サイトではありません。</p>
  <p>{" ・ ".join(f'<a href="{u}">{t}</a>' for t, u in [("トップ", "/")] + NAV)}</p>
  <p><a href="/operator/">運営者情報</a> ・ <a href="/editorial-policy/">編集方針</a> ・ <a href="/contact/">お問い合わせ</a> ・ <a href="/privacy/">プライバシーポリシー</a> ・ <a href="/disclaimer/">免責事項</a></p>
  <p>© 2026 護衛艦.com</p>
</div></footer>
</body>
</html>
"""

def main():
    urls = []
    for f in sorted(glob.glob(os.path.join(ROOT, "tools", "content", "*.html"))):
        lines = open(f, encoding="utf-8").read().split("\n", 2)
        if len(lines) < 3: continue
        url = url_of(f)
        out = os.path.join(ROOT, url.strip("/"), "index.html") if url != "/" else os.path.join(ROOT, "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        title = strip(lines[0])
        dm = re.search(r'content="([^"]*)"', lines[1])
        desc = html.unescape(dm.group(1)) if dm else strip(lines[1])
        open(out, "w", encoding="utf-8").write(render(url, html.unescape(title), desc, lines[2]))
        urls.append(url)
    today = datetime.date.today().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{DOMAIN}{u}</loc><lastmod>{today}</lastmod></url>" for u in urls]
    sm.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    print("pages", len(urls))

if __name__ == "__main__":
    main()
