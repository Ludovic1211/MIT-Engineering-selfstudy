# Engineering Notes — MIT OCW

A self-study notebook in engineering, built from the courses of
[MIT OpenCourseWare](https://ocw.mit.edu). Each lecture is rewritten in my own
words and paired with a Python demonstration.

Built with **[Quarto](https://quarto.org)** and published on **GitHub Pages**.

## Repository structure

```
.
├── _quarto.yml            # Global configuration (theme, navbar, footer)
├── theme.scss             # Typography customization (the font)
├── _include/fonts.html    # Web font loading
├── index.qmd              # Home page
├── about.qmd              # The approach
├── requirements.txt       # Python dependencies (to render the demos)
├── LICENSE                # CC BY-NC-SA 4.0
├── .github/workflows/     # Build & deploy automation
└── courses/
    ├── 18.02/             # Multivariable Calculus (in progress)
    ├── 8.01SC/ 18.03/ ... # Upcoming courses (placeholders)
    └── ...
```

## Working locally

Requirements: [Quarto](https://quarto.org/docs/get-started/) and Python (with the
packages in `requirements.txt`: `pip install -r requirements.txt`).

```bash
quarto preview     # live preview in the browser (auto-reload)
quarto render      # build the whole site into _site/
```

## Publishing

A push to `main` triggers the GitHub Actions workflow, which rebuilds the site
and deploys it to GitHub Pages. No manual step is needed once the initial setup
is done.

## License

Content licensed under [CC BY-NC-SA 4.0](./LICENSE), derived from MIT
OpenCourseWare materials. Non-commercial use.
