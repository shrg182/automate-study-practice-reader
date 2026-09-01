# Reader Articles Studio

This directory is reserved for articles written or edited by the reader. It is
separate from `news_reports/`, whose existing PDF reports remain unchanged.

Open `index.html` to write in the left pane and review the print-ready article
in the right pane. Work is autosaved in the browser. Use **Export backup** for
a portable JSON copy and **Generate PDF** to open the browser print dialog.

The browser-local **Draft library** retains multiple new or imported articles,
supports search and switching, and automatically migrates the former single
active draft. Published catalog articles remain a separate collection.

The backup format is described by `article_manifest.json`. Images are stored as
data URLs inside the backup so the article remains portable.
