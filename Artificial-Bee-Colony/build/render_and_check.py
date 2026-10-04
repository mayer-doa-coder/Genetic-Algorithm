"""Open the deck in PowerPoint, add the click reveals, export PNG + PDF, and
report any text box whose text does not fit."""
from pathlib import Path
import json, re
import win32com.client
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "review"
SLIDES_DIR = REVIEW / "slides"
SLIDES_DIR.mkdir(parents=True, exist_ok=True)

app = win32com.client.Dispatch("PowerPoint.Application")
deck = app.Presentations.Open(str(ROOT / "Ackley_ABC_Presentation.pptx"),
                              ReadOnly=False, WithWindow=False)

warnings = []
REVEAL_SLIDES = (6, 8)
for slide in deck.Slides:
    slide.SlideShowTransition.AdvanceOnClick = True
    slide.SlideShowTransition.AdvanceOnTime = False

    if slide.SlideIndex in REVEAL_SLIDES:
        for sh in slide.Shapes:
            m = re.match(r"Reveal_(\d+)(.*)", sh.Name)
            if not m:
                continue
            # one click per logical block: the card triggers, the rest follow it
            trigger = 1 if m.group(2) == "" else 2
            effect = slide.TimeLine.MainSequence.AddEffect(sh, 1, 0, trigger)
            effect.Timing.Duration = 0.2

    for sh in slide.Shapes:
        if sh.HasTable:
            for row in range(1, sh.Table.Rows.Count + 1):
                for col in range(1, sh.Table.Columns.Count + 1):
                    cell = sh.Table.Cell(row, col).Shape
                    tr = cell.TextFrame2.TextRange
                    if tr.BoundHeight > cell.Height + 2 or tr.BoundWidth > cell.Width + 2:
                        warnings.append({"slide": slide.SlideIndex, "shape": sh.Name,
                                         "type": "table_cell", "row": row, "col": col,
                                         "text": cell.TextFrame.TextRange.Text})
        if sh.HasTextFrame and sh.TextFrame.HasText:
            tr = sh.TextFrame2.TextRange
            if tr.BoundHeight > sh.Height + 3:
                warnings.append({"slide": slide.SlideIndex, "shape": sh.Name,
                                 "type": "text_height", "shape_h": round(sh.Height, 1),
                                 "text_h": round(tr.BoundHeight, 1),
                                 "text": sh.TextFrame.TextRange.Text[:70]})
            if tr.BoundWidth > sh.Width + 4:
                warnings.append({"slide": slide.SlideIndex, "shape": sh.Name,
                                 "type": "text_width", "shape_w": round(sh.Width, 1),
                                 "text_w": round(tr.BoundWidth, 1),
                                 "text": sh.TextFrame.TextRange.Text[:70]})

deck.Save()
deck.Export(str(SLIDES_DIR), "PNG", 1920, 1080)
deck.SaveAs(str(ROOT / "Ackley_ABC_Presentation.pdf"), 32)
report = {"slides": deck.Slides.Count,
          "animations": {str(i): deck.Slides(i).TimeLine.MainSequence.Count
                         for i in REVEAL_SLIDES},
          "text_overflow_warnings": warnings}
deck.Close()
(REVIEW / "layout_check.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

files = sorted(SLIDES_DIR.glob("Slide*.PNG"),
               key=lambda f: int(re.search(r"\d+", f.stem).group()))
font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 19)
for start in range(0, len(files), 9):
    sheet = Image.new("RGB", (1500, 942), "#F3E7D2")
    draw = ImageDraw.Draw(sheet)
    for i, f in enumerate(files[start:start + 9]):
        im = Image.open(f); im.thumbnail((490, 276))
        x, y = (i % 3) * 500 + 5, (i // 3) * 314 + 5
        sheet.paste(im, (x, y))
        draw.text((x + 8, y + 283), f"Slide {start + i + 1:02d}", font=font, fill="#6F251B")
    sheet.save(REVIEW / f"contact_sheet_{start + 1:02d}-{min(start + 9, len(files)):02d}.jpg",
               quality=93)

print(json.dumps(report, indent=2))
