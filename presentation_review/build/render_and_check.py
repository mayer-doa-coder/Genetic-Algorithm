from pathlib import Path
import json, re
import win32com.client
from PIL import Image, ImageDraw, ImageFont

root=Path(__file__).resolve().parents[2]
app=win32com.client.Dispatch('PowerPoint.Application')
p=app.Presentations.Open(str(root/'Ackley_GA_Presentation_Updated.pptx'),ReadOnly=False,WithWindow=False)
warnings=[]
for slide in p.Slides:
    slide.SlideShowTransition.AdvanceOnClick=True
    slide.SlideShowTransition.AdvanceOnTime=False
    # Match named shapes to one click per logical diagram block.
    if slide.SlideIndex in (8,10,13):
        for sh in slide.Shapes:
            if sh.Name.startswith('Reveal_'):
                m=re.match(r'Reveal_(\d+)(.*)',sh.Name)
                trigger=1 if m and m.group(2)=='' else 2
                # Crossover blocks have numbered gene-shape suffixes.
                if slide.SlideIndex==10:trigger=1 if sh.Name in ('Reveal_1_0','Reveal_2_0') else 2
                effect=slide.TimeLine.MainSequence.AddEffect(sh,1,0,trigger)
                effect.Timing.Duration=.2
    for sh in slide.Shapes:
        if sh.HasTable:
            for row in range(1,sh.Table.Rows.Count+1):
                for col in range(1,sh.Table.Columns.Count+1):
                    cell=sh.Table.Cell(row,col).Shape
                    tr=cell.TextFrame2.TextRange
                    if tr.BoundHeight>cell.Height+2 or tr.BoundWidth>cell.Width+2:
                        warnings.append({'slide':slide.SlideIndex,'shape':sh.Name,'type':'table_cell','row':row,'col':col,'text':cell.TextFrame.TextRange.Text})
        if sh.HasTextFrame and sh.TextFrame.HasText:
            tr=sh.TextFrame2.TextRange
            if tr.BoundHeight>sh.Height+3:
                warnings.append({'slide':slide.SlideIndex,'shape':sh.Name,'type':'text_height','shape_h':sh.Height,'text_h':tr.BoundHeight,'text':sh.TextFrame.TextRange.Text})
            if tr.BoundWidth>sh.Width+4:
                warnings.append({'slide':slide.SlideIndex,'shape':sh.Name,'type':'text_width','shape_w':sh.Width,'text_w':tr.BoundWidth,'text':sh.TextFrame.TextRange.Text})
p.Save()
out=root/'presentation_review'/'slides';out.mkdir(exist_ok=True)
p.Export(str(out),'PNG',1920,1080)
p.SaveAs(str(root/'Ackley_GA_Presentation_Updated.pdf'),32)
report={'slides':p.Slides.Count,'animations':{str(i):p.Slides(i).TimeLine.MainSequence.Count for i in (8,10,13)},'text_overflow_warnings':warnings}
p.Close()
(root/'presentation_review'/'layout_check.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
files=sorted(out.glob('Slide*.PNG'),key=lambda f:int(re.search(r'\d+',f.stem).group()))
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19)
for start in (0,9):
    contact=Image.new('RGB',(1500,942),'#D9E2E3');d=ImageDraw.Draw(contact)
    for i,f in enumerate(files[start:start+9]):
        im=Image.open(f);im.thumbnail((490,276));x=(i%3)*500+5;y=(i//3)*314+5
        contact.paste(im,(x,y));d.text((x+8,y+283),f'Slide {start+i+1:02d}',font=font,fill='#163D50')
    contact.save(root/'presentation_review'/f'contact_sheet_{start+1:02d}-{start+9:02d}.jpg',quality=93)
print(json.dumps(report,indent=2))
