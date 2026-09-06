#!/usr/bin/env python3
# 文风铁律 v3 扫描器：逐章扫出所有违规行。用法: python3 .claude/scripts/文风扫描.py [起] [止]  (默认全卷)
# 输出: 每章计数 + 每处命中(带行号/段落前缀)。修复目标: 每章 Σ=0。
import re, sys, glob
ADV=['挺','蛮','十分','非常','极其','格外','相当','有些','有点','稍稍','稍微','渐渐','缓缓','慢慢','轻轻','微微','默默','静静','淡淡','悄悄','偷偷','隐隐','略微','颇为','愈发','这么','那么','如此','一直','仿佛','犹如','宛如','越来越','更加','很','太']
OLD=['然而','嘴角','瞬间','这一刻','随着','映入眼帘','一丝','一缕','眨眼']
V=['一','两','二','三','四','五','六','七','八','九','十','几','半','好','廿']
Q='下|口|步|遍|眼|回|趟|次|勺|碗|杯|圈|阵|声|句|躬|会儿|瞬|炷香'
re_word=re.compile('('+'|'.join(sorted(ADV+OLD,key=len,reverse=True))+')')
re_vv=re.compile(r'([\u4e00-\u9fff]{1,2})了\1')
re_num=re.compile('(?<![第这])(好)?[一二两三四五六七八九十半几]{1,3}(?=(?:下|口|步|遍|眼|回|趟|次|勺|碗|杯|圈|阵|声|句|躬|会儿|瞬|炷香))')
re_expl=re.compile(r'那意思是|意思是|像在说|也就是说|换言之|潜台词|仿佛在说|言下之意|说白了')
def ctx(txt,sp,ep,pad=16):
    s=max(0,sp-pad); e=min(len(txt),ep+pad)
    return txt[s:e].replace('\n','⏎')
rng=[int(x) for x in sys.argv[1:3]] if len(sys.argv)>2 else [1,999]
for f in sorted(glob.glob('06-CHAPTERS/ch-0*.md')):
    n=int(f.split('-')[-1].split('.')[0])
    if not(rng[0]<=n<=rng[1]): continue
    b=open(f).read().split('# ',1)[1]
    counts={k:0 for k in ('adv','vv','vnum','expl')}; rows=[]
    for m in re_word.finditer(b):
        if m.group(1)=='太' and b[max(0,m.start()-1):m.start()] in ('老','太'): continue
        counts['adv']+=1; rows.append(('adv',m.group(1),ctx(b,m.start(),m.end())))
    for m in re_vv.finditer(b):
        counts['vv']+=1; rows.append(('vv',m.group(0),ctx(b,m.start(),m.end())))
    for m in re.finditer(r'(?<=了)(好)?[一二两三四五六七八九十半几]{1,3}(?=(?:夜|天|晌|息|刻|程))',b):
        counts['vnum']+=1; rows.append(('vnum',m.group(0)+b[m.end():m.end()+1],ctx(b,m.start(),m.end()+1)))
    for m in re_num.finditer(b):
        w=m.group(0)+b[m.end():m.end()+2].lstrip()
        pre=b[max(0,m.start()-4):m.start()]
        nx=b[m.end():m.end()+2]
        p1=b[max(0,m.start()-1):m.start()]
        if ('钟敲' in pre or '敲过' in pre) or p1 in ('小','老','太') or nx=='下午': continue
        if '年' in pre and nx[:1]=='回': continue
        counts['vnum']+=1; rows.append(('vnum',w,ctx(b,m.start(),m.end()+2)))
    for m in re_expl.finditer(b):
        counts['expl']+=1; rows.append(('expl',m.group(0),ctx(b,m.start(),m.end())))
    tot=sum(counts.values())
    print(f'== ch-{n:03d}  adv={counts["adv"]} vv={counts["vv"]} vnum={counts["vnum"]} expl={counts["expl"]} Σ={tot}')
    if n not in rng or not rows: continue
    for k,w,c in rows:
        print(f'   [{k}:{w}] …{c}…')
