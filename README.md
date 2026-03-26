## Ocean Mallik Blog

Live site: `https://blog.oceanmallik.com`

This blog is powered by Jekyll and GitHub Pages.

## Features

✨ **Complete blogging platform** with:

- 🌓 **Multi-theme support** - Dark, Light, and Sepia themes with system preference detection
- 📝 **Post management** - Automatic reading time estimates
- 🏷️ **Tags system** - Categorize and browse posts by tag
- 📚 **Archive** - Browse all posts organized by year
- 📡 **RSS Feed** - `/feed.xml` for subscriptions
- 🗺️ **SEO optimized** - Automated sitemap, robots.txt, meta tags, and social sharing
- 💾 **Persistent preferences** - Theme choice saved in localStorage

## How to add a new post

1. Create a file in `_posts/` named `YYYY-MM-DD-title.md`.
2. Add front matter at the top:

```md
---
title: "Your Post Title"
tags: [tag1, tag2]
---
```

3. Write the post content in Markdown below the front matter.
4. The reading time will be calculated automatically.
5. Commit and push to GitHub.

## Post front matter options

```md
---
layout: post
title: "Your Post Title"
tags: [optional, tags]
author: "Your Name" # Optional, defaults to site author
---
```

## Site pages

- **Home** `/` - Latest posts feed
- **Archive** `/archive/` - All posts organized by year
- **About** `/about/` - About page
- **RSS Feed** `/feed.xml` - Subscribe to updates
- **Sitemap** `/sitemap.xml` - For search engines

## Local preview (optional)

If you have Ruby and Bundler installed:

```bash
bundle install
bundle exec jekyll serve
```

Then open `http://127.0.0.1:4000`.

## Customization

- **Theme colors**: Edit `assets/css/style.css` CSS variables
- **Site info**: Update `_config.yml` with your title, description, author
- **Post author**: Set in `_config.yml` or override per-post in front matter