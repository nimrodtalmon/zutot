# CLAUDE.md — Operating Manual for zutot

This file is the operating manual for Claude Code sessions on this repository.
Read it at the start of every session.

---

## Who

**Nimrod Talmon** — Faculty, Department of Computer Science, Ben-Gurion University of the Negev.
Research: computational social choice, AI & governance, decentralized systems (blockchain, DAOs, trust networks).
Also a home-recording musician. The site reflects both identities.

---

## Site

- **Stack**: Jekyll + [al-folio](https://github.com/alshedivat/al-folio)
- **URL**: `https://nimrodtalmon.github.io/zutot`
- **Repo**: `nimrodtalmon/zutot` on GitHub
- **Deploy**: push to `main` → GitHub Actions → `gh-pages` branch → live site
- **Local preview**: `bundle exec jekyll serve` → `http://localhost:4000/zutot`

---

## Author Identifiers

| Source | ID / URL |
|---|---|
| DBLP | `https://dblp.org/pid/53/11268` |
| Google Scholar | `https://scholar.google.com/citations?user=dSfOjCQAAAAJ` |
| arXiv | `https://arxiv.org/a/talmon_n_1.html` (verify this URL is correct) |

---

## Site Structure

| Page | Path | Nav order |
|---|---|---|
| Landing | `_pages/about.md` | — |
| News | `_pages/news.md` | 1 |
| Research | `_pages/research.md` | 2 |
| Publications | `_pages/publications.md` | 3 |
| People | `_pages/people.md` | 4 |
| Teaching | `_pages/teaching.md` | 5 |
| Resources | `_pages/resources.md` | 6 |
| Music | `_pages/music.md` | 7 |
| Supp | `_pages/music_supp.md` | 8 |

News items: `_news/` directory, one `.md` file per item.

---

## Weekly Sync (Friday Ritual)

Trigger: Friday Todoist reminder → open Claude Code web → say **"weekly sync"**.

**Steps:**

1. **Fetch new publications from DBLP**
   ```bash
   curl -L "https://dblp.org/pid/53/11268.bib?param=1" -o /tmp/dblp_fresh.bib
   ```
   Diff `/tmp/dblp_fresh.bib` against `_bibliography/papers.bib`.
   New entries: add them. Do not remove existing entries. Do not hallucinate venues or co-authors.

2. **Check arXiv for new preprints**
   Fetch `https://arxiv.org/a/talmon_n_1.html` and look for new preprints where Talmon is an author.
   Add any that are not already in `papers.bib` as `@misc` entries with `eprint` field.

3. **Read `_inbox/pending.md`**
   Process each line item:
   - News item → add a new file to `_news/` with today's date
   - People change → **do not auto-merge; create PR for review**
   - Paper accepted → add to `papers.bib` if not already there
   - Teaching/research update → update the relevant `_pages/` file

4. **Update footer year** if the year changed.

5. **Draft a PR** from a new branch.

**Auto-merge tier** (safe to merge directly):
- DBLP BibTeX entries, arXiv preprints where Talmon is listed author, footer year bump

**PR-review required**:
- All inbox items (news, teaching, research prose, resources)

**Never auto-merge**:
- People page changes about third parties

6. After PR is merged: clear `_inbox/pending.md` (delete lines below the `<!-- items -->` marker).

---

## Mid-Week Drops

User says: `inbox: <one-liner>` in any Claude Code session.

Claude appends the one-liner to `_inbox/pending.md` below the comment marker and commits:
```
git add _inbox/pending.md
git commit -m "inbox: <one-liner>"
git push
```

No separate context needed. The Friday sync picks it up.

---

## Explicit Don'ts

- **Do not hallucinate** co-authors, venues, paper titles, or dates. If uncertain, fail loudly and ask.
- **Do not touch** the Music section (`_pages/music.md`, `_pages/music_supp.md`) without explicit instruction.
- **Do not auto-merge** People page changes.
- **Do not ignore** `_inbox/pending.md` on Friday sync.
- **Do not copy Dropbox links** from any old sources — they rot. Find a permanent URL or host the file in-repo under `assets/`.
- **Do not link** to `sites.google.com/view/zutot` anywhere in the new site.

---

## Open Items (post-launch)

- [ ] Add actual profile photo: replace `assets/img/prof_pic.jpg`
- [ ] Confirm email address and uncomment in `_data/socials.yml`
- [ ] Verify arXiv author ID: check `https://arxiv.org/a/talmon_n_1.html`
- [ ] Populate `_bibliography/papers.bib` via weekly sync
- [ ] Expand Research prose in `_pages/research.md`
- [ ] Fill in Resources page
- [ ] Fill in Music pages
- [ ] Add course numbers, semesters, links to Teaching page

---

## Preferences (operating style)

- Concise, rigorous, structured output — Markdown sections + bullets
- Skeleton-first: ToC → sections → paragraphs
- Prefer clarifying questions over guesses
- If a source doesn't explain something, say so explicitly
- Brevity default; expand only when asked
