"""Check local Markdown and HTML file links; no remote availability claims."""
import re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def check():
 errors=[];n=0
 files=[R/'README.md',*list((R/'docs').glob('*.md')),R/'site/index.html']
 for p in files:
  text=p.read_text()
  links=re.findall(r'(?:href|src)="([^"]+)"',text) if p.suffix=='.html' else re.findall(r'\]\(([^)]+)\)',text)
  for link in links:
   if link.startswith(('http:','https:','mailto:','#')):continue
   target=link.split('#')[0]
   if target:
    n+=1
    if not (p.parent/target).exists():errors.append(str(p.relative_to(R))+': '+target)
 assert not errors,'Broken internal links: '+str(errors)
 print('PASS:',n,'internal document/site file links')
if __name__=='__main__':check()
