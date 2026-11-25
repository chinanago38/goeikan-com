# 護衛艦.com（xn--ef1ay5jhyc.com）作業ルール

GitHub Pages で公開する静的サイト。tools/build.py が tools/content/*.html から全ページを生成する。

## ページの元ファイル
- tools/content/<dir>__<slug>.html → /<dir>/<slug>/ に出力（例 kaisen__nihonkai.html → /kaisen/nihonkai/）。一覧ページは <dir>__index.html → /<dir>/
- 1行目：<title>（末尾「｜護衛艦.com」）、2行目：meta description（120字以内）、3行目以降：本文HTML
- 本文は `<h1>`、`<p class="updated">最終確認日：2026年11月25日</p>`、導入の `<p>`、そのあと素の `<h2>` 見出しと <p>/<ul>/<h3>/<table>/<dl> だけ（<section> や装飾は build.py が付ける）
- 最後は `<section class="sources"><h2>出典</h2><ul>…</ul></section>`

## 守ること
- 事実は公的・公式の情報源で確かめたものだけ書く：防衛省・海上自衛隊・防衛研究所、国立公文書館アジア歴史資料センター（JACAR）、国立国会図書館、自治体、記念館・博物館の公式サイト（記念艦三笠、大和ミュージアム、山本五十六記念館、鹿屋航空基地史料館など）。Wikipedia・個人ブログ・まとめサイトは使わない
- 確かめられない数字・日付は書かない。資料によって数字が違うときは、そのことを書く
- 戦争の歴史は中立に書く。美化も過度な非難もしない。日本側・相手側の損害や犠牲も事実として書く
- 写真は Wikimedia Commons の自由ライセンス、または海上自衛隊サイトの写真（出典表示つき）だけ（build 側で入れる）
- 1ページ本文3,000文字以上。同じ文章の使い回し・数合わせのページは作らない
- 公式サイトと誤解されない書き方にする（個人運営・非公式）
