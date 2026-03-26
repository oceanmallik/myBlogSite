---
layout: default
title: Home
---

# Welcome to my blog

I write about things I build, learn, and break while coding.

## Latest Posts

{% if site.posts.size > 0 %}
{% for post in site.posts %}
- [{{ post.title }}]({{ post.url | relative_url }})
	<span class="date">{{ post.date | date: "%B %d, %Y" }}</span>
	{% if post.excerpt %}
	<p>{{ post.excerpt | strip_html | truncate: 140 }}</p>
	{% endif %}
{% endfor %}
{% else %}
No posts yet. Add Markdown files to `_posts` using `YYYY-MM-DD-title.md`.
{% endif %}