---
name: create-slides
description: Use when the user wants to create PowerPoint slides for thesis defense or presentation. Trigger on "tao slide", "create slides", "powerpoint", "pptx", "presentation", "trinh bay", "bao cao", "slide bao ve". Generates PPTX with python-pptx.
---

# Create PowerPoint Slides

## Quick Start

```cmd
cd C:\ĐATN\server
python -c "from pptx import Presentation; print('python-pptx installed')"
```

If not installed:
```cmd
pip install python-pptx
```

## Create Slides

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Add title slide
slide = prs.slides.add_slide(prs.slide_layouts[0])
title = slide.shapes.title
title.text = "TEN DE TAI"

# Add content slide
slide = prs.slides.add_slide(prs.slide_layouts[1])
title = slide.shapes.title
title.text = "CHUONG 1: GIOI THIEU"
body = slide.placeholders[1]
body.text = "1.1 Boi canh\n1.2 Muc tieu\n1.3 Pham vi"

prs.save("doandocs/Slide_DATN_HUCE.pptx")
```

## Slide Structure

| Slide | Content |
|-------|---------|
| 1 | Title page |
| 2 | Table of contents |
| 3-5 | Chapter 1: Introduction |
| 6-9 | Chapter 2: Literature review |
| 10-13 | Chapter 3: Design |
| 14-20 | Chapter 4: Implementation |
| 21-23 | Chapter 5: Testing |
| 24 | Conclusion |
| 25 | Q&A |

## Styling Guide

| Element | Style |
|---------|-------|
| Background | White |
| Title Color | Blue (#003366) |
| Body Color | Black (#000000) |
| Font | Calibri |
| Title Size | 36pt |
| Body Size | 18pt |
| Slide Size | 13.333 x 7.5 inches |

## Thesis Structure

1. **Chuong 1: Gioi thieu**
   - 1.1 Boi canh
   - 1.2 Muc tieu
   - 1.3 Pham vi

2. **Chuong 2: Ngon ngu**
   - 2.1 ESP32
   - 2.2 AES-128-CBC
   - 2.3 Flask
   - 2.4 SQLite

3. **Chuong 3: Thiet ke**
   - 3.1 Kien truc
   - 3.2 Luong du lieu
   - 3.3 Protocol
   - 3.4 Database

4. **Chuong 4: Trien khai**
   - 4.1 Wokwi ESP32
   - 4.2 Server Flask
   - 4.3 AES Encrypt
   - 4.4 Anti-replay
   - 4.5 Android App
   - 4.6 Benchmark
   - 4.7 Test

5. **Chuong 5: Kiem thu**
   - 5.1 Muc tieu
   - 5.2 Test case
   - 5.3 Ket qua

## Common Issues

### python-pptx Not Installed
```cmd
pip install python-pptx
```

### File Not Saved
- Check `doandocs/` folder exists
- Verify write permissions

### Font Not Found
- Use Calibri or Times New Roman
- Avoid special fonts

## Output

Save to: `doandocs/Slide_DATN_HUCE.pptx`

## Related Files

| File | Purpose |
|------|---------|
| `doandocs/Slide_DATN_HUCE.pptx` | Generated slides |
| `doandocs/Chương 3.docx` | Thesis chapter |