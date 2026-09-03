# Historical build / patch scripts

These are the one-off Python scripts that were used to generate and patch the site's HTML
during the March 2026 build. They are kept for reference only.

**Do not re-run them.** The HTML has been hand-edited since, and most scripts append or
re-inject markup/CSS, so running them again would duplicate nav/footer/CSS blocks or
re-introduce the encoding damage that has since been repaired.

This directory (and `docs/`) is blocked from being served by Netlify via `netlify.toml`.
