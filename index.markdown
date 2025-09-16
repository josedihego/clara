---
layout: default
title: Home
---

<h2>Albums</h2>
<div class="album-grid">
  {% for album in site.data.gallery.albums %}
    <a href="{{ '/albums/' | append: album.name | downcase | replace: ' ', '-' | relative_url }}" class="album-card">
      <img src="{{ '/assets/drawings/' | append: album.subalbums[0].images[0].file | relative_url }}" alt="{{ album.name }}">
      <h3>{{ album.name }}</h3>
    </a>
  {% endfor %}
</div>
