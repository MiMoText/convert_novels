# HTML Source Dialects

The HTML sources from Hub18cfrench alone come in at least three varieties, when looking at the content of `<span class="xml-text">`, respectively:

1. `.xml-text` contains `.xml-front` with the frontmatter and a single `.xml-div0`, which in turn contains a heading section (`<b class="headword">`) and one or multiple `.xml-div1`, which can again start with a heading section before the regular text content. This is handled by 'HUB18CFRENCH_A'.
2. `.xml-text` contains a single `.xml-div1`, which in turn contains a heading section and one or more `.xml-div2`, which again can start with a heading section before the regular text content. This is handled by 'HUB18CFRENCH_B'.
3. `.xml-text` contains one or more `.xml-div1`, each with an optional heading section and the regular text content. This is handled by 'HUB18CFRENCH_C'.

Sometimes, when no dedicated front matter is given, and no encompassing div is given, some kind of titlepage content is simply placed before the first `<div class="xml-div1>`, acompagnied by manual formatting with br tags, empty paragraphs etc. The different dialects basically only differ in the way they interpret the sources' structure i.e. how to split chapters etc.
