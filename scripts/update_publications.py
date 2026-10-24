"""Import public OpenAlex outputs, cautiously matched to VCDRC members.
Run on GitHub Actions (internet available). Unresolved authors remain explicit gaps.
"""
import json, os, re, time, urllib.parse, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
db=json.loads((ROOT/'data.json').read_text())
people=db['people']
HEADERS={'User-Agent':'VCDRC-Research-Lab/1.0 (public academic research indexing)','Accept':'application/json'}

def get(path):
    req=urllib.request.Request('https://api.openalex.org/'+path,headers=HEADERS)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req,timeout=25) as response:return json.load(response)
        except Exception:
            if attempt==2:raise
            time.sleep(2**attempt)

def norm(x):
    return re.sub(r'[^a-z0-9]','',str(x).casefold().replace('ā','a').replace('’',"'"))

def abstract(inv):
    if not inv:return ''
    a=['']*(max((max(v) for v in inv.values() if v),default=-1)+1)
    for word,positions in inv.items():
        for p in positions:
            if p<len(a):a[p]=word
    return ' '.join(a)

records={}; coverage=[]
for index,name in enumerate(people):
    status={'name':name,'status':'unresolved','works':0,'source':'OpenAlex','notes':''}
    try:
        response=get('authors?'+urllib.parse.urlencode({'search':name,'per-page':12}))
        candidates=response.get('results',[])
        exact=[c for c in candidates if norm(c.get('display_name'))==norm(name)]
        affiliated=[c for c in exact if any('auckland university of technology' in (a.get('institution',{}).get('display_name','').lower()) for a in c.get('affiliations',[])) or any('auckland university of technology' in (a.get('display_name','').lower()) for a in c.get('last_known_institutions',[]))]
        if len(affiliated)!=1:
            status['notes']=f'{len(affiliated)} unambiguous exact-name AUT-affiliated author candidates; manual identity resolution required'
            coverage.append(status);continue
        author=affiliated[0];aid=author['id'].rsplit('/',1)[-1]
        status.update(status='matched',author_id=author['id'],orcid=author.get('orcid'),notes='Exact name + AUT affiliation; check identity if names collide')
        cursor='*';count=0
        while cursor and count<500:
            works=get('works?'+urllib.parse.urlencode({'filter':'authorships.author.id:'+aid,'per-page':100,'cursor':cursor,'select':'id,doi,display_name,publication_year,type,authorships,abstract_inverted_index,primary_location,topics'}))
            for w in works.get('results',[]):
                title=w.get('display_name','')
                if not title:continue
                key=w.get('doi') or w['id']
                authors=[a.get('author',{}).get('display_name','') for a in w.get('authorships',[])]
                item=records.setdefault(key,{'title':title,'authors':[],'year':w.get('publication_year'),'type':w.get('type'),'url':w.get('doi') or w['id'],'abstract':abstract(w.get('abstract_inverted_index')),'subjects':[t.get('display_name') for t in w.get('topics',[]) if t.get('display_name')][:5],'methods':[],'source':'OpenAlex','source_id':w['id'],'attribution':'AUT-affiliated exact-name author match'})
                if name not in item['authors']:item['authors'].append(name)
                count+=1
            cursor=works.get('meta',{}).get('next_cursor') if works.get('results') and count<500 else None
            time.sleep(.12)
        status['works']=count
        if count>=500:status['notes']+='; capped at 500 works, not a complete record'
    except Exception as e:
        status['status']='error';status['notes']=str(e)[:160]
    coverage.append(status)
    print(f'{index+1}/{len(people)} {name}: {status["status"]} {status["works"]}',flush=True)
    time.sleep(.12)
(ROOT/'publications.json').write_text(json.dumps(list(records.values()),ensure_ascii=False,indent=2))
(ROOT/'coverage.json').write_text(json.dumps({'members':coverage,'record_count':len(records),'note':'OpenAlex indexed works only; missing creative outputs and AUT-only records require further sources. Methods intentionally not guessed without text evidence.'},ensure_ascii=False,indent=2))
print('Saved',len(records),'unique records')
