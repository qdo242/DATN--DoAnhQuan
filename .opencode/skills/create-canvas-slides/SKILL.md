---
name: create-canvas-slides
description: Use when the user asks to create slides using Canvas, HTML slides, or web-based presentation. Trigger on keywords like "canvas", "tao slide canvas", "html slides", "reveal.js", "trinh bay web". Generates HTML slide deck that can be opened in browser and shared in chat.
---

# Skill: Create Canvas/HTML Slides

Use this skill when the user wants to generate a web-based slide presentation (HTML) that can be opened in any browser, rendered visually, and shared easily.

## Workflow

1. **Identify source content**: Read thesis chapters, docs, README, etc.
2. **Generate HTML**: Create a single-file HTML slide deck using reveal.js CDN.
3. **Save to disk**: Save as `doandocs/slides.html`
4. **Open in browser**: Use `start` command to open the file.
5. **Share in chat**: Return the HTML content or file path so user can share.

## HTML Slide Template (reveal.js)

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.6.0/dist/reveal.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.6.0/dist/theme/white.min.css">
  <style>
    .reveal h1, .reveal h2 { color: #003366; }
    .reveal table { margin: 0 auto; font-size: 0.6em; }
    .reveal table th { background: #003366; color: white; }
    .reveal table td { border: 1px solid #ddd; padding: 4px 8px; }
    .reveal .subtitle { color: #666; font-size: 0.7em; }
    .reveal section { text-align: left; }
  </style>
</head>
<body>
  <div class="reveal">
    <div class="slides">

      <!-- Slide 1: Title -->
      <section>
        <h1>TEN DE TAI</h1>
        <p class="subtitle">Sinh vien: A & B<br>HW: Thay Haihd</p>
      </section>

      <!-- Slide 2: Content -->
      <section>
        <h2>Tieu de</h2>
        <ul>
          <li>Item 1</li>
          <li>Item 2</li>
        </ul>
      </section>

      <!-- Slide 3: Table -->
      <section>
        <h2>Bang so lieu</h2>
        <table>
          <tr><th>Cot 1</th><th>Cot 2</th></tr>
          <tr><td>Data</td><td>Data</td></tr>
        </table>
      </section>

    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.6.0/dist/reveal.min.js"></script>
  <script>
    Reveal.initialize({ hash: true, slideNumber: true });
  </script>
</body>
</html>
```

## Slide Navigation

- **Space / Arrow keys**: Next/previous slide
- **Esc**: Overview mode
- **S**: Speaker notes
- **F**: Fullscreen
- **O**: Overview grid

## Output

Save to: `doandocs/slides.html`
Open command: `start doandocs/slides.html`

## Content Guidelines

- One main idea per slide
- Max 5 bullet points per slide
- Tables: keep under 6 columns
- Use visuals over text when possible
- Title slides for chapter transitions
- End with "Cam on" slide

## Dependencies

- Modern browser (Chrome, Firefox, Edge)
- Internet connection (for reveal.js CDN)
