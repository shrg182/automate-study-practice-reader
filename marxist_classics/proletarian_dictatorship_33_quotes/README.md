# 《马克思恩格斯列宁论无产阶级专政（33条语录及注释）》

## Classification

This is a supplementary anthology, not one of the nine primary works in the Marxist Classics reading sequence. The webpage was published in 2011 and identifies the underlying compilation as the work of the Shandong University Theory Group in April 1975. During editing, quotations from Marx, Engels, and Lenin should therefore be kept distinct from the compiler's introductions, notes, source attributions, and historical claims.

Source: [乌有之乡移动版](https://m.wyzxwk.com/Article/shushe/2011/08/250089.html)

## Measured processing quota

- 33 numbered quotation-and-commentary units stated by the title
- 242 extracted paragraphs
- 46,441 non-whitespace characters
- approximately 52 reading pages at 900 Chinese characters per page
- recommended quota: 8 review batches, approximately 5,800 characters per batch

A practical division is: preliminary material and items 1–4, then 5–8, 9–12, 13–16, 17–20, 21–24, 25–28, and 29–33. The editor remains a single file so searches, the project dictionary, backups, and exports cover the entire article.

## Files

- `sources/page.html`: saved source-page snapshot
- `source.txt`: reproducibly extracted source text
- `proletarian_dictatorship_33_quotes_clean.txt`: editable clean-text baseline
- `source_metadata.json`: measured source metadata and quota
- `reading_terms.csv`: article-specific dictionary entries
- `editor.html`: self-contained browser editor
- `extract_source.py`: extraction utility; it does not overwrite an existing clean-text baseline
- `build_editor.py`: editor generator

The source transcript preserves the webpage's missing separator in `30我们`. The editable clean-text baseline normalizes this evident numbering typo to `30、我们`.

Rebuild the editor with:

```bash
python3 practice/marxist_classics/proletarian_dictatorship_33_quotes/build_editor.py
```


