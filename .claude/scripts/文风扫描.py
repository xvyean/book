#!/usr/bin/env python3
# 文风铁律 v2 扫描器（2026-09-06）
# 用法: python3 .claude/scripts/文风扫描.py [章号区间, 如 25 42]
import re, sys, glob
ADV=['挺','蛮','十分','非常','极其','格外','相当','有些','有点','稍稍','稍微','渐渐','缓缓','慢慢','轻轻','微微','默默','静静','淡淡','悄悄','偷偷','隐隐','略微','颇为','愈发','这么','那么','如此','很','一直']
OLD=['仿佛','然而','嘴角','瞬间','这一刻','犹如','宛如','随着','映入眼帘','一丝','一缕','眨眼']
re_adv=re.compile('('+'|'.join(sorted(ADV,key=len,reverse=True))+')')
re_vv=re.compile(r'([\u4e00-\u9fff]{1,2})了\1')                       # 看了看/想了想/拍了拍
re_vnum=re.compile(r'了(好)?[一两三四五六七八九十半廿]{1,2}(下|口|步|遍|眼|回|趟|次|勺|碗|杯|圈|阵|声|息|刻|会儿|瞬|句|躬|夜|天|月)')  # 看了一眼/说了一句/鞠了一躬
re_exp=re.compile(r'那意思是|意思是|像在说|也就是说|换言之|潜台词|仿佛在说|言下之意|说白了')
rng=[int(x) for x in sys.argv[1:3]] or [1,999]
hits={}
for f in sorted(glob.glob('06-CHAPTERS/ch-0*.md')):
    n=int(f.split('-')[-1].split('.')[0])
    if not(rng[0]<=n<=rng[1]): continue
    b=open(f).read().split('# ',1)[1]
    row={}
    for name,rx in [('adv',re_adv),('vv',re_vv),('vnum',re_vnum),('expl',re_exp)]:
        m=rx.findall(b); row[name]=len(m)
        if m: hits.setdefault(f,{})[name]=m
    tot=sum(row.values())
    print(f'{n:03d} adv={row["adv"]} vv={row["vv"]} vnum={row["vnum"]} expl={row["expl"]}  Σ={tot}')
print('--- 命中明细 ---')
for f,d in hits.items():
    for k,v in d.items():
        print(f, k, v[:6])
