---
name: create-slides
description: Use when the user asks to create PowerPoint slides (.pptx) from thesis content, project documentation, or any structured content. Trigger on keywords like "tao slide", "create slides", "powerpoint", "pptx", "presentation", "trinh bay". Handles full workflow: read source content, generate PPTX with python-pptx, save to doandocs/.
---

# Skill: Create PowerPoint Slides

Use this skill when the user wants to generate a PowerPoint presentation from existing project content (thesis chapters, documentation, README, etc.).

## Workflow

1. **Identify source content**: Read the relevant files (`.docx`, `.md`, `.py`, etc.) to extract structure and key points.
2. **Plan slide structure**: Break content into logical slides (title, overview, per-chapter sections, conclusion).
3. **Generate PPTX**: Use `python-pptx` library to create slides with proper formatting.
4. **Save and inform**: Save to `doandocs/` directory and tell the user the file path.

## Slide Design Guidelines

- Use **16:9 widescreen** format (13.333 x 7.5 inches)
- Color scheme: Dark blue (#003366) for headers, white background
- Title slides: Blue background, white text, centered
- Content slides: White background, blue header bar at top
- Tables: Blue header row, alternating gray/white rows
- Font sizes: Title 28-36pt, body 14-18pt, tables 12pt
- Add footer with project name on every content slide

## python-pptx Template

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Add blank slide
slide = prs.slides.add_slide(prs.slide_layouts[6])

# Add text
txBox = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(11), Inches(1))
tf = txBox.text_frame
p = tf.paragraphs[0]
p.text = "Hello"
p.font.size = Pt(24)
p.font.bold = True

# Add table
table = slide.shapes.add_table(rows, cols, left, top, width, height).table

prs.save("output.pptx")
```

## Common Patterns

### Chapter Title Slide
- Blue background
- "CHUONG X: TEN CHUONG" in large white bold text

### Content Slide with Table
- Blue header bar at top with slide title
- Table below with data
- Footer at bottom

### Key Results Slide
- Bullet list of achievements
- Bold key numbers/metrics

## Output Location

Save generated PPTX files to: `doandocs/Slide_DATN_HUCE.pptx` (or as specified by user).

## Dependencies

- `python-pptx` (install via `pip install python-pptx`)
