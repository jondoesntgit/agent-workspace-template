# Writing standards

Applies to notebook markdown, docs, and papers. Replace with your team's conventions.

- Lead with the answer or finding, then the supporting detail.
- Active voice; define every acronym on first use.
- Numbers carry units and a sensible number of significant figures.
- Every figure is referenced in the text and has a caption that states what to
  notice **and** lists the settings that produced it (see `plotting.md`).
- In LaTeX, use sidenotes (`\sidenote{}`) for asides and citations, and margin notes
  (`\marginnote{}`) for unnumbered remarks. Keep the main text column for the argument.
- Citations render as margin sidenotes, so put `\cite{}` after the punctuation that ends
  the clause (`…prior work.\cite{key}`), never as a noun in the sentence ("see~\cite{key}").
- Don't claim more than the data shows; state assumptions and limitations explicitly.
- Cite sources (Confluence page titles, papers, ticket keys); never invent a citation.
- Mark anything unresolved as an open question rather than guessing.
