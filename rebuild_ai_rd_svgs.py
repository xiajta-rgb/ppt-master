from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape
from math import cos, pi, sin
import base64

ROOT = Path(r"c:\Users\xiajt\Documents\trae_projects\ppt-master\examples\ai-rd-system")
OUT = ROOT / "svg_final"
FONT = "Microsoft YaHei,Arial,sans-serif"
C = {"bg":"#F7F8FA","surface":"#FFFFFF","soft":"#F2F3F5","line":"#E5E6EB","ink":"#161823","muted":"#4E5969","dim":"#86909C","blue":"#1664FF","purple":"#6A4CFF","cyan":"#00B8D9","orange":"#FF8A34","green":"#00B42A","red":"#F53F3F","navy":"#0D1B3E"}

TITLES = ["AI双引擎产品智能研发体系","七大章节，体系化呈现","认知破局","传统研发与AI选品的核心底层问题","传统研发闭环死循环","双引擎架构解决的四大核心行业痛点","双引擎AI研发核心赋能逻辑","核心体系","创新选品引擎 vs 爆款选品引擎","创新选品引擎 · 五层结构化洞察流程","市场趋势洞察：新兴赛道取舍","消费者需求洞察：创新价值定调","市场缺口洞察：创新差异化定位","竞品趋势洞察：创新避坑与错位","创新产品定型：未来产品落地","爆款选品引擎 · 五层结构化洞察流程","爆款精准识别：成熟赛道取舍","爆款DNA深度拆解：成功基因定调","用户因果需求挖掘：痛点拆解优化","竞品对标超车：缺陷规避与错位升级","爆款迭代定型：成熟产品落地","双引擎数据融合 + 统一交叉推理建模","工程化打分体系","双模型核心权重体系","统一立项四级决策标准","流程对比","传统单一研发/单模型AI缺陷闭环","AI双引擎标准化高效研发流程","企业研发闭环","双机会池独立管理","统一产品决策池：双路径机会，进入同一投资语言","研发战略闭环定位","终审与归档","分层风控终审机制","双路径标准化物料归档清单","体系终复盘","双引擎分层研发 VS 传统单一研发","体系终极价值：六大核心目标","谢谢"]


def tx(x,y,s,size=20,fill=None,weight=400,anchor=None):
    a = f' text-anchor="{anchor}"' if anchor else ''
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill or C["ink"]}"{a}>{escape(str(s))}</text>'
def rect(x,y,w,h,fill,rx=12,stroke=None,sw=1):
    v=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'
    if stroke: v+=f' stroke="{stroke}" stroke-width="{sw}"'
    return v+'/>'
def ln(x1,y1,x2,y2,stroke,width=2,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}"{d}/>'
def circle(cx,cy,r,fill,stroke=None,sw=1):
    v=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"'
    if stroke: v+=f' stroke="{stroke}" stroke-width="{sw}"'
    return v+'/>'
def wrap(s,n=18): return [s[i:i+n] for i in range(0,len(s),n)]
def text_block(x,y,s,size=20,fill=None,lh=34,weight=400,n=20):
    return ''.join(tx(x,y+i*lh,line,size,fill,weight) for i,line in enumerate(wrap(s,n)))
def header(p,sub=None):
    title=TITLES[p-1]
    s=rect(0,0,1920,1080,C['bg'],0)
    s+=tx(80,88,f'{p:02d}',15,C['blue'],800)+ln(120,82,176,82,C['blue'],2)
    s+=tx(196,88,'AI PRODUCT INTELLIGENCE OS',12,C['dim'],700)
    s+=tx(80,174,title,52,C['ink'],800)
    if sub: s+=tx(80,228,sub,20,C['muted'])
    s+=ln(80,1016,1840,1016,C['line'])+tx(80,1050,'AI双引擎产品智能研发体系',13,C['dim'])+tx(1840,1050,f'{p:02d} / 39',13,C['dim'],400,'end')
    return s
def eyebrow(x,y,label,color=C['blue']):
    return tx(x,y+15,label,13,color,800)+ln(x,y+28,x+42,y+28,color,2)
def chip(x,y,label,color): return rect(x,y,len(label)*15+42,36,C['soft'],18)+tx(x+20,y+24,label,13,color,700)
def card(x,y,w,h,label,title,body,color=C['blue']):
    s=rect(x,y,w,h,C['surface'],14,C['line'])+rect(x,y,w,6,color,3)+eyebrow(x+28,y+31,label,color)+tx(x+28,y+92,title,27,C['ink'],800)
    return s+text_block(x+28,y+140,body,18,C['muted'],30,400,23)
def arrow(x1,y,x2,color=C['dim']): return ln(x1,y,x2-12,y,color,3)+f'<path d="M{x2-18} {y-8} L{x2-6} {y} L{x2-18} {y+8}" fill="none" stroke="{color}" stroke-width="3"/>'
def node(x,y,w,h,no,title,desc,color):
    return rect(x,y,w,h,C['surface'],14,C['line'])+eyebrow(x+28,y+32,f'步骤 {no}',color)+tx(x+28,y+94,title,23,C['ink'],800)+text_block(x+28,y+132,desc,16,C['muted'],26,400,15)

def image_data(filename):
    path = ROOT / 'assets' / filename
    return base64.b64encode(path.read_bytes()).decode('ascii')
def image_tag(filename):
    return f'<image href="data:image/jpeg;base64,{image_data(filename)}" x="0" y="0" width="1920" height="1080" preserveAspectRatio="xMidYMid slice"/>'

IMAGE_SLOT_LABELS = {
    2:'体系全景 / 研发运营场景', 4:'问题诊断 / 研发协作场景', 5:'研发闭环 / 团队协作场景',
    6:'机制升级 / 系统界面场景', 7:'战略价值 / 产品团队场景', 9:'双引擎 / 分流决策场景',
    10:'创新探索 / 信号洞察场景', 11:'趋势情报 / 多源数据场景', 12:'用户需求 / 生活方式场景',
    13:'市场机会 / 供需分析场景', 14:'竞品研究 / 产品对标场景', 15:'创新产品 / 通勤户外场景',
    16:'爆款识别 / 电商运营场景', 17:'销量分析 / 商品运营场景', 18:'产品 DNA / 设计拆解场景',
    19:'用户评价 / 评论分析场景', 20:'竞品超车 / 产品设计场景', 21:'升级产品 / 面料工艺场景',
    22:'数据融合 / AI 架构场景', 24:'模型评审 / 指标看板场景', 25:'决策评审 / 投资分配场景',
    27:'传统流程 / 低效协作场景', 28:'Agent 工作流 / 人机协同场景', 30:'机会池 / 产品组合场景',
    31:'统一决策 / 管理驾驶舱场景', 32:'战略闭环 / 企业研发场景', 34:'风险终审 / 合规评审场景',
    35:'知识归档 / 数字资产场景', 37:'体系复盘 / 管理评估场景', 38:'业务成效 / 经营复盘场景'
}

def visual_slot(p):
    label = IMAGE_SLOT_LABELS.get(p, '产品研发 / 数据洞察场景')
    x,y,w,h = 1470,52,370,184
    s=rect(x,y,w,h,C['surface'],12,C['line'])
    s+=rect(x+18,y+18,112,148,C['soft'],8)
    s+=f'<path d="M{ x+32 } { y+143 } L{ x+63 } { y+108 } L{ x+82 } { y+126 } L{ x+108 } { y+92 } L{ x+118 } { y+143 } Z" fill="{ C["line"] }"/>'
    s+=circle(x+101,y+48,9,C['line'])
    s+=tx(x+150,y+46,'VISUAL SLOT',12,C['blue'],800)+ln(x+150,y+59,x+202,y+59,C['blue'],2)
    s+=text_block(x+150,y+93,label,16,C['ink'],700,24,16)
    s+=tx(x+150,y+151,'待置入项目情境图',13,C['dim'])
    return s

def chapter(p,kicker,headline,desc,asset):
    s=image_tag(asset)
    s+=f'<rect x="0" y="0" width="1920" height="1080" fill="#FFFFFF" fill-opacity="0.82"/>'
    s+=rect(80,154,6,58,C['blue'],3)+tx(108,176,kicker,15,C['blue'],800)
    s+=tx(80,332,headline,78,C['ink'],800)+rect(80,376,82,4,C['blue'],2)
    s+=text_block(80,448,desc,27,C['muted'],44,400,26)
    s+=tx(80,958,'AI PRODUCT INTELLIGENCE OS',15,C['dim'],700)+tx(1840,958,f'{p:02d} / 39',14,C['dim'],700,'end')
    return s
def cover(p,title,one,two,asset='cover_bg.jpg'):
    s=image_tag(asset)+f'<rect x="0" y="0" width="1920" height="1080" fill="#0D1B3E" fill-opacity="0.57"/>'
    s+=tx(80,112,'战略升级 · 商业汇报',15,'#FFFFFF',700)+tx(1840,112,'2026',15,'#FFFFFF',700,'end')
    s+=rect(80,174,78,4,C['cyan'],2)
    lines=title.split('\n')
    for i,line in enumerate(lines): s+=tx(80,416+i*104,line,80,'#FFFFFF',800)
    s+=text_block(80,650,one,27,'#EAF2FF',42,400,25)+tx(80,770,two,21,'#D7E5FF')
    s+=ln(80,944,1840,944,'#FFFFFF',1)+tx(80,990,'AI PRODUCT INTELLIGENCE OS',15,'#FFFFFF',700)+tx(1840,990,f'{p:02d} / 39',14,'#FFFFFF',700,'end')
    return s
def flow_page(p,subtitle,items,colors=None,foot=None):
    s=header(p,subtitle); n=len(items); w=300 if n==5 else 340; gap=(1760-n*w)/(n-1) if n>1 else 0
    for i,(title,desc) in enumerate(items):
        x=80+i*(w+gap); color=(colors or [C['blue'],C['purple']])[i%len(colors or [C['blue'],C['purple']])]
        s+=node(x,400,w,190,f'{i+1:02d}',title,desc,color)
        if i<n-1:s+=arrow(x+w+10,495,x+w+gap-2)
    if foot:s+=rect(80,720,1760,90,C['soft'],12)+tx(112,778,foot,21,C['muted'])
    return s
def compare_page(p,subtitle,left,right):
    s=header(p,subtitle)
    for x,label,heading,items,color in [(80,'EXPLORE / 创新',left[0],left[1],C['cyan']),(1000,'UTILIZE / 爆款',right[0],right[1],C['orange'])]:
        s+=rect(x,320,840,560,C['surface'],16,C['line'])+rect(x,320,840,10,color,5)+tx(x+40,394,label,15,color,800)+tx(x+40,462,heading,32,C['ink'],800)
        for i,item in enumerate(items): s+=circle(x+48,535+i*61,6,color)+tx(x+70,542+i*61,item,19,C['muted'])
    return s
def metrics(x,y,items,cols=2):
    gap=20; w=(760-(cols-1)*gap)/cols; h=138
    s=''
    for i,(num,label,color) in enumerate(items):
        r,c=divmod(i,cols); xx=x+c*(w+gap); yy=y+r*(h+gap)
        s+=rect(xx,yy,w,h,C['surface'],12,C['line'])+tx(xx+24,yy+61,num,38,color,800)+tx(xx+24,yy+106,label,16,C['muted'])
    return s
def chart_axes(x,y,w,h,y_labels,title):
    s=rect(x,y,w,h,C['surface'],14,C['line'])+tx(x+28,y+40,title,16,C['muted'],800)
    plot_x=x+78; plot_y=y+84; plot_w=w-112; plot_h=h-132
    for i,label in enumerate(y_labels):
        yy=plot_y+plot_h-i*plot_h/(len(y_labels)-1)
        s+=ln(plot_x,yy,plot_x+plot_w,yy,C['line'],1)+tx(plot_x-18,yy+5,label,13,C['dim'],400,'end')
    return s,plot_x,plot_y,plot_w,plot_h

def line_series(x,y,w,h,values,color,fill_opacity=0.12):
    points=[]
    for i,value in enumerate(values):
        px=x+i*w/(len(values)-1); py=y+h-(value/100)*h; points.append((px,py))
    point_str=' '.join(f'{px:.1f},{py:.1f}' for px,py in points)
    area=f'{x},{y+h} '+point_str+f' {x+w},{y+h}'
    s=f'<polygon points="{area}" fill="{color}" fill-opacity="{fill_opacity}"/>'
    s+=f'<polyline points="{point_str}" fill="none" stroke="{color}" stroke-width="4"/>'
    return s+''.join(circle(px,py,5,color) for px,py in points)

def horizontal_bars(x,y,w,items,max_value=100):
    s=''
    for i,(label,value,color) in enumerate(items):
        yy=y+i*58
        s+=tx(x,yy+17,label,16,C['muted'],600)+rect(x+178,yy, w-258,18,C['soft'],9)
        s+=rect(x+178,yy,(w-258)*value/max_value,18,color,9)+tx(x+w,yy+16,str(value),16,C['ink'],800,'end')
    return s

def radar(p):
    s=header(p,'创新模型突出趋势、缺口与未来增长；爆款模型突出验证、优化与收益。')
    cx,cy,R=625,640,265; labs=['趋势 / 验证','需求 / 基因','缺口 / 竞争','可行 / 优化','未来增长','收益']
    for k in range(1,6):
        pts=[]
        for i in range(6):
            a=-pi/2+i*pi/3; pts.append(f'{cx+R*k/5*cos(a):.1f},{cy+R*k/5*sin(a):.1f}')
        s+=f'<polygon points="{" ".join(pts)}" fill="none" stroke="{C["line"]}" stroke-width="1"/>'
    for i,label in enumerate(labs):
        a=-pi/2+i*pi/3; ex,ey=cx+(R+44)*cos(a),cy+(R+44)*sin(a); s+=ln(cx,cy,cx+R*cos(a),cy+R*sin(a),C['line'])+tx(ex,ey+7,label,16,C['muted'],500,'middle')
    def poly(vals,color):
        pts=[]
        for i,v in enumerate(vals):
            a=-pi/2+i*pi/3; pts.append(f'{cx+R*v/100*cos(a):.1f},{cy+R*v/100*sin(a):.1f}')
        return f'<polygon points="{" ".join(pts)}" fill="{color}" fill-opacity="0.16" stroke="{color}" stroke-width="4"/>' + ''.join(circle(float(q.split(',')[0]),float(q.split(',')[1]),5,color) for q in pts)
    s+=poly([95,90,92,80,96,70],C['cyan'])+poly([90,92,78,85,65,90],C['orange'])
    s+=chip(1060,385,'创新选品模型',C['cyan'])+chip(1060,445,'爆款选品模型',C['orange'])
    s+=card(1060,535,680,250,'MODEL A','创新选品模型','趋势势能 95｜需求强度 90｜供需缺口 92｜未来增长 96',C['cyan'])
    s+=card(1060,810,680,130,'MODEL B','爆款选品模型','市场验证 90｜基因匹配 92｜利润收益 90',C['orange'])
    return s

def p01(): return cover(1,'AI双引擎\n产品智能研发体系','探索未来新品 · 复用成熟爆款','跨境服饰 AI 研发战略升级方案')
def p02():
    s=header(2,'从问题诊断到企业研发资产化的七章叙事。'); names=['认知破局','核心体系','工程化打分','流程对比','企业研发闭环','终审与归档','体系复盘']
    desc=['传统AI选品的战略缺陷','双引擎五层洞察体系','创新 / 爆款分层量化评审','AI分层研发 VS 传统研发','双机会池与战略迭代','风控终审与物料归档','终局能力升级对比']
    s+=ln(80,304,1840,304,C['line'])
    for i,(a,b) in enumerate(zip(names,desc)):
        col=i%2; row=i//2; x=80+col*890; y=352+row*158; w=1760 if i==6 else 850
        s+=rect(x,y,w,122,C['surface'],10,C['line'])
        s+=tx(x+32,y+43,f'0{i+1}',15,C['blue'],800)+ln(x+32,y+60,x+66,y+60,C['blue'],2)
        s+=tx(x+104,y+47,a,28,C['ink'],800)+tx(x+104,y+84,b,16,C['muted'])
    return s
def p04():
    s=header(4,'问题不在设计能力，而在任务、逻辑与评价体系没有按场景拆分。'); items=[('任务无分层','创新探索与爆款复用被同一逻辑覆盖'),('逻辑一刀切','单权重、单推理链、单评价体系'),('创新款评价失准','用成熟验证标准错杀无历史数据新品'),('爆款拆解浅层化','只复刻外观，未拆成功基因'),('风控无前置','主观审美驱动，研发投入不可控')]
    for i,(a,b) in enumerate(items):
        y=310+i*120;color=C['red'] if i>2 else C['blue'];s+=circle(116,y+26,18,color)+tx(116,y+32,f'{i+1:02d}',14,'#FFF',800,'middle')+tx(164,y+28,a,25,C['ink'],800)+tx(164,y+64,b,18,C['muted'])+ln(164,y+91,1760,y+91,C['line'])
    return s
def p05(): return flow_page(5,'单链路模型把两类任务强行压进同一条低效闭环。',[('单一逻辑','统一模型覆盖全场景'),('创新错杀','新机会被成熟标准淘汰'),('爆款跟风','只复刻表层外观'),('产品内卷','上市后缺乏竞争力'),('盲目试错','利润无法覆盖成本')],[C['red']], '结论：研发资源错配，最终造成战略停滞。')
def p06():
    s=header(6,'同一组行业痛点，需要由双引擎的独立数据、推理与权重共同解决。'); data=[('认知偏差','共用逻辑','独立数据、推理与权重'),('设计浅层','仅复刻外观','拆解产品DNA与因果需求'),('创新乏力','依赖成熟赛道','追踪趋势与供需缺口'),('决策无序','标准缺失、成果碎片','统一决策模型与日志沉淀')]
    for i,(a,b,c) in enumerate(data):
        x=80+(i%2)*890;y=320+(i//2)*240;s+=rect(x,y,850,204,C['surface'],14,C['line'])+tx(x+28,y+43,a,26,C['ink'],800)+tx(x+28,y+83,'传统',14,C['red'],800)+tx(x+105,y+83,b,17,C['muted'])+tx(x+28,y+140,'双引擎',14,C['blue'],800)+tx(x+105,y+140,c,17,C['ink'],600)
    return s
def p07():
    s=header(7,'一套研发系统，同时解决战略、效率与企业级资产沉淀。'); items=[('战略破局','稳存量、拓增量，形成长期产品矩阵','探索未来 + 复用成熟',C['blue']),('研发提效降本','AI 替代趋势筛查、拆解与风险研判','压缩 80% 前置调研时间',C['cyan']),('标准化沉淀','数据、推理链、物料与评价标准可复用','企业专属研发资产',C['purple'])]
    for i,(a,b,d,color) in enumerate(items): s+=card(80+i*594,340,570,410,f'0{i+1}',a,b,color)+chip(108+i*594,674,d,color)
    return s
def p09(): return compare_page(9,'双路径独立数据、独立推理、独立权重，最终使用同一投资语言决策。',('未知需求正向探索',['数据源：TikTok / WGSN / Google趋势','逻辑：趋势 → 需求 → 缺口 → 原创','权重：趋势 40%｜需求 30%｜缺口 20%｜可行 10%']),('成熟机会逆向解析',['数据源：BSR / 销量 / Review / Q&A','逻辑：验证 → DNA → 因果需求 → 优化','权重：验证 40%｜基因 30%｜竞争 20%｜优化 10%']))
def p10(): return flow_page(10,'创新引擎以五层证据链，将全球弱信号转化为可落地的原创方案。',[('市场趋势','识别增量萌芽赛道'),('消费者需求','拆解隐性诉求与场景'),('市场缺口','锁定高需低供空白'),('竞品趋势','借鉴趋势，规避误区'),('产品定型','输出原创研发方案')],[C['cyan']], '输出：新兴赛道取舍 → 创新价值定调 → 差异化蓝海 → 创新避坑 → 产品落地。')
def p11():
    s=header(11,'全球多源信号汇聚，以趋势势能、需求热度与供给密度确定“立项 / 观察 / 规避”。')
    s+=rect(80,310,460,510,C['navy'],16)+tx(120,374,'TREND SIGNALS',16,'#B8CCFF',800)+tx(120,442,'全球信号汇聚',34,'#FFF',800)
    s+=text_block(120,505,'社媒关键词\n行业报告\n搜索增量\n面料技术\n海外生活方式',19,'#D8E5FF',44,400,14)
    s+=tx(120,759,'5类外部证据源',16,'#B8CCFF',700)
    axes,px,py,pw,ph=chart_axes(580,310,1180,510,['100','75','50','25','0'],'趋势势能监测 / 近 6 个研判周期')
    s+=axes+line_series(px,py,pw,ph,[28,39,44,58,76,88],C['cyan'])+line_series(px,py,pw,ph,[46,48,51,49,55,61],C['blue'],0.06)
    for i,label in enumerate(['W1','W2','W3','W4','W5','W6']): s+=tx(px+i*pw/5,py+ph+30,label,13,C['dim'],400,'middle')
    s+=circle(1360,355,6,C['cyan'])+tx(1376,361,'新兴趋势势能',14,C['muted'])+circle(1510,355,6,C['blue'])+tx(1526,361,'成熟赛道热度',14,C['muted'])
    s+=rect(580,850,1180,74,C['soft'],12)+tx(612,896,'结论：新兴趋势势能升至 88，进入立项优先序列；成熟赛道维持观察。',19,C['ink'],700)
    return s
def p12():
    s=header(12,'从趋势跟风转向隐性刚需识别，建立可直接服务研发的需求字段库。'); s+=card(80,330,790,440,'AI INPUT','采集数据维度','社媒场景吐槽 · 新生活方式痛点 · 新生代审美 · 小众穿搭诉求',C['blue'])
    s+=rect(960,330,800,440,C['surface'],14,C['line'])+tx(1000,382,'OUTPUT / 隐性刚需层级字段库',16,C['cyan'],800)
    for i,(lab,color) in enumerate([('必须满足｜轻量化 · 防泼水 · 无夸张 Logo',C['green']),('场景加分｜通勤户外双适配 · 简约包容版型',C['blue']),('淘汰清单｜厚重面料 · 浮夸装饰 · 硬核户外',C['red'])]): s+=rect(1000,430+i*94,700,68,C['soft'],9)+circle(1030,464+i*94,6,color)+tx(1050,470+i*94,lab,18,C['ink'],600)
    return s
def p13():
    s=header(13,'以需求强度、供给覆盖和落地难度三维测算，锁定“高需低供”的创新窗口。')
    s+=rect(80,310,1120,570,C['surface'],14,C['line'])+tx(120,356,'供需机会矩阵 / Bubble size = 可落地性',16,C['muted'],800)
    x0,y0,w,h=190,770,850,330
    for i in range(5):
        xx=x0+i*w/4; yy=y0-i*h/4
        s+=ln(xx,y0-h,xx,y0,C['line'],1)+ln(x0,y0-i*h/4,x0+w,y0-i*h/4,C['line'],1)
    s+=tx(x0+w/2,y0+54,'供给覆盖率 →',17,C['muted'],600,'middle')+tx(112,y0-h/2,'需求强度',17,C['muted'],600,'middle')
    s+=circle(392,540,54,C['cyan'],C['cyan'],2)+tx(392,547,'城市轻户外',15,C['ink'],800,'middle')
    s+=circle(650,454,44,C['blue'],C['blue'],2)+tx(650,461,'通勤机能',14,C['ink'],800,'middle')
    s+=circle(882,652,35,C['orange'],C['orange'],2)+tx(882,658,'基础款',13,C['ink'],800,'middle')
    s+=rect(1270,310,490,570,C['surface'],14,C['line'])+tx(1310,356,'机会评估 / 排名',16,C['muted'],800)
    s+=horizontal_bars(1310,420,400,[('城市轻户外',94,C['cyan']),('通勤机能',78,C['blue']),('户外轻量',63,C['purple']),('基础款',41,C['orange'])])
    s+=rect(1310,695,400,120,C['soft'],10)+tx(1334,738,'关键判断',15,C['blue'],800)+tx(1334,782,'供给覆盖率仅 16%，优先立项。',18,C['ink'],700)
    return s
def p14():
    s=header(14,'用竞品早期反馈建立“可复用 / 应规避 / 可错位”的创新黑白名单。'); s+=card(80,330,770,430,'INPUT','AI 采集维度','早期趋势款反馈 · 小众创新短板 · 行业踩坑案例 · 跟风失败缺陷',C['blue'])
    s+=rect(940,330,820,430,C['surface'],14,C['line'])
    for i,(a,b,color) in enumerate([('可复用','通勤户外双适配、简约包容版型',C['green']),('应规避','硬核户外设计、厚重面料',C['red']),('错位空间','户外功能 + 通勤版型',C['purple'])]):s+=tx(980,392+i*112,a,17,color,800)+tx(980,428+i*112,b,22,C['ink'],700)+ln(980,462+i*112,1710,462+i*112,C['line'])
    return s
def product_page(p,case,left,right,color):
    s=header(p,'前序洞察最终沉淀为全参数结构化定型模型，直接进入研发交接。');s+=rect(80,320,720,470,C['surface'],14,C['line'])+tx(120,382,'PRODUCT CASE',15,color,800)+tx(120,448,case,36,C['ink'],800)
    for i,a in enumerate(left):s+=circle(128,510+i*52,5,color)+tx(148,517+i*52,a,19,C['muted'])
    for i,a in enumerate(right):
        x=910+(i%2)*410;y=320+(i//2)*150;s+=rect(x,y,370,120,C['surface'],12,C['line'])+tx(x+24,y+42,f'0{i+1}',14,color,800)+tx(x+24,y+86,a,21,C['ink'],700)
    return s
def p16(): return flow_page(16,'爆款引擎不是复刻外观，而是把成熟市场中的成功基因转化为可优化方案。',[('精准识别','排除泡沫与衰退款'),('DNA拆解','提炼关键参数'),('因果需求','锁定差评痛点'),('对标超车','复用、整改、微创新'),('迭代定型','输出升级新品')],[C['orange']], '输出：成熟赛道取舍 → 成功基因定调 → 痛点优化 → 错位升级 → 成熟产品落地。')
def p17():
    s=header(17,'“销量高”不等于“值得做”；以稳定、增长、利润、竞争四维筛出真实优质爆款。')
    axes,px,py,pw,ph=chart_axes(80,310,1030,510,['120','90','60','30','0'],'候选 SKU 销量稳定性 / 近 6 个周期')
    s+=axes+line_series(px,py,pw,ph,[48,56,63,71,76,82],C['orange'])+line_series(px,py,pw,ph,[62,58,51,44,38,34],C['dim'],0.05)
    for i,label in enumerate(['M1','M2','M3','M4','M5','M6']): s+=tx(px+i*pw/5,py+ph+30,label,13,C['dim'],400,'middle')
    s+=circle(760,355,6,C['orange'])+tx(776,361,'候选爆款',14,C['muted'])+circle(910,355,6,C['dim'])+tx(926,361,'衰退对照',14,C['muted'])
    s+=rect(1160,310,600,510,C['surface'],14,C['line'])+tx(1200,356,'爆款资质评分 / 100',16,C['muted'],800)
    s+=horizontal_bars(1200,425,500,[('销量稳定性',92,C['green']),('类目增长',86,C['blue']),('利润空间',81,C['orange']),('竞争密度',74,C['purple'])])
    s+=ln(1200,703,1660,703,C['line'])+tx(1200,747,'综合评分',16,C['muted'],600)+tx(1660,750,'84',42,C['orange'],800,'end')
    s+=rect(80,850,1680,74,C['soft'],12)+tx(112,896,'判定：销量连续增长且利润空间达标，进入爆款引擎深度 DNA 拆解。',19,C['ink'],700)
    return s
def p18():
    s=header(18,'把爆款从“外观复刻”升级为“产品基因组”拆解，形成可复用的参数资产。');cx,cy=960,570;s+=circle(cx,cy,115,C['navy'])+tx(cx,558,'PRODUCT',18,'#B8CCFF',800,'middle')+tx(cx,594,'DNA',36,'#FFF',800,'middle')
    data=[('版型基因',C['blue']),('面料基因',C['cyan']),('场景基因',C['orange']),('人群基因',C['purple']),('价格基因',C['green'])]
    for i,(a,col) in enumerate(data):
        ang=-pi/2+i*2*pi/5;x,y=cx+330*cos(ang),cy+250*sin(ang);s+=ln(cx+110*cos(ang),cy+110*sin(ang),x-75*cos(ang),y-50*sin(ang),C['line'],2)+circle(x,y,66,C['surface'],col,3)+tx(x,y+7,a,19,C['ink'],700,'middle')
    return s
def p19():
    s=header(19,'从万级 Review、Q&A 与退货原因中识别“复用优势—整改缺陷—付费痛点”。')
    s+=rect(80,310,1140,540,C['surface'],14,C['line'])+tx(120,356,'差评问题 Pareto / 高频问题占比',16,C['muted'],800)
    labels=[('面料透光',36,C['red']),('领型变形',24,C['orange']),('水洗缩水',18,C['orange']),('起球',12,C['blue']),('尺码偏差',10,C['blue'])]
    base_x,base_y,bar_w=160,748,680
    cumulative=0
    pts=[]
    for i,(label,value,col) in enumerate(labels):
        x=base_x+i*132; h=value*8
        s+=rect(x,base_y-h,76,h,col,5)+tx(x+38,base_y+30,label,14,C['muted'],500,'middle')+tx(x+38,base_y-h-13,f'{value}%',15,C['ink'],800,'middle')
        cumulative+=value; px=x+38; py=454-cumulative*1.9; pts.append((px,py))
    s+=f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" fill="none" stroke="{C["purple"]}" stroke-width="4"/>'+''.join(circle(x,y,5,C['purple']) for x,y in pts)
    s+=tx(1070,445,'累计问题覆盖率',14,C['purple'],700,'end')+tx(1070,480,'90%',42,C['purple'],800,'end')
    s+=rect(1280,310,480,540,C['surface'],14,C['line'])+tx(1320,356,'决策输出',16,C['muted'],800)
    for i,(a,b,col) in enumerate([('优先整改','面料透光 · 领型变形',C['red']),('体验加分','凉感持久 · 版型稳定',C['green']),('研发动作','面料升级 / 结构加固',C['blue'])]):
        y=425+i*118;s+=rect(1320,y,380,82,C['soft'],10)+circle(1348,y+28,6,col)+tx(1366,y+34,a,15,col,800)+tx(1348,y+63,b,17,C['ink'],700)
    return s
def p20():
    s=header(20,'结合供应链能力，形成“优势全复用、缺陷全优化、差异化微创新”的对标超车策略。');d=[('优势复用','凉感面料 · 合身版型',C['green']),('缺陷整改','不透肉 · 加固领型 · 抗皱水洗',C['red']),('微创新','差异化色彩 / 细节设计',C['purple'])]
    for i,(a,b,c) in enumerate(d):s+=card(80+i*594,360,570,330,f'STRATEGY 0{i+1}',a,b,c)
    return s
def p22():
    s=header(22,'创新与爆款先独立入库、独立推理，再由 FIOS 收敛为可解释的统一决策。');layers=[('双路径数据入库','创新：趋势势能 / 隐性需求 / 供需空白｜爆款：市场验证 / DNA / 差评痛点',C['cyan']),('FIOS 产品认知模型','双路径独立推理，标准化收敛为可解释、可留痕的分层决策',C['blue']),('统一输出','产品立项与研发参数｜自动推理、统一评分、资产沉淀',C['purple'])]
    for i,(a,b,col) in enumerate(layers):y=320+i*165;s+=rect(160,y,1600,126,C['surface'],14,C['line'])+rect(160,y,16,126,col,8)+tx(215,y+48,a,19,col,800)+tx(215,y+91,b,23,C['ink'],700)
    return s
def p25():
    s=header(25,'两套权重体系以同一组阈值映射研发动作，让评分直接服务资源配置。')
    s+=rect(80,310,1120,560,C['surface'],14,C['line'])+tx(120,356,'统一决策阈值 / 候选项目评分分布',16,C['muted'],800)
    bands=[('终止 <40',0,40,C['red']),('谨慎 40–59',40,20,C['orange']),('常规 60–79',60,20,C['blue']),('重仓 80–100',80,20,C['green'])]
    x0,y0,w,h=180,480,860,108
    for label,start,width,col in bands:
        xx=x0+w*start/100; ww=w*width/100
        s+=rect(xx,y0,ww,h,col,0)+tx(xx+ww/2,y0+64,label,17,'#FFFFFF',800,'middle')
    projects=[('A',94,C['cyan']),('B',84,C['cyan']),('C',72,C['blue']),('D',66,C['blue']),('E',53,C['orange']),('F',36,C['red'])]
    for i,(name,score,col) in enumerate(projects):
        xx=x0+w*score/100; s+=ln(xx,y0+130,xx,y0+190,col,2)+circle(xx,y0+206,18,col)+tx(xx,y0+212,name,14,'#FFF',800,'middle')+tx(xx,y0+248,str(score),14,C['ink'],800,'middle')
    s+=tx(180,800,'当前候选组合：2 个重仓 · 2 个常规 · 1 个谨慎 · 1 个终止',19,C['muted'],600)
    s+=rect(1270,310,490,560,C['surface'],14,C['line'])+tx(1310,356,'资源配置建议',16,C['muted'],800)
    for i,(tier,share,action,col) in enumerate([('重仓研发','45%','优先排产 / 全力打版',C['green']),('常规研发','30%','标准流程 / 小批试产',C['blue']),('谨慎研发','15%','极小批验证',C['orange']),('终止研发','10%','停止投入',C['red'])]):
        y=420+i*96;s+=tx(1310,y,tier,17,col,800)+tx(1690,y,share,20,C['ink'],800,'end')+rect(1310,y+20,380,10,C['soft'],5)+rect(1310,y+20,380*int(share[:-1])/45,10,col,5)+tx(1310,y+56,action,15,C['muted'])
    return s
def p27(): return flow_page(27,'传统研发的低效不是单点问题，而是一个不断放大风险的负向闭环。',[('数据堆叠','没有任务分层'),('单模型判断','逻辑一刀切'),('结果失真','创新错杀、爆款跟风'),('重复试错','上市后被迫改版'),('资源损耗','利润覆盖不了成本')],[C['red']], '对照下一页：用“扫描—分流—研判—决策—回流”替代负向循环。')
def p28():
    s=header(28,'从 Agent 执行界面到人工决策节点，让每一次研发操作可见、可控、可追溯。');d=[('01','数据扫描','趋势、竞品、用户反馈与供应链信息同步入库','全域数据分层扫描',C['cyan']),('02','Agent 研判','创新 / 爆款智能分流，完成五层研判、评分与风控','专属推理链',C['blue']),('03','决策落地','立项、打版、生产与数据回流形成闭环','统一评审与研发执行',C['purple'])]
    for i,(no,a,b,c,col) in enumerate(d):x=80+i*594;s+=rect(x,335,570,445,C['surface'],14,C['line'])+circle(x+56,395,28,col)+tx(x+56,401,no,15,'#FFF',800,'middle')+tx(x+32,493,a,30,C['ink'],800)+text_block(x+32,550,b,18,C['muted'],31,400,22)+chip(x+32,704,c,col)
    return s
def p30(): return compare_page(30,'创新与爆款各自保留来源、字段和上下文，在统一决策前不丢失差异。',('创新机会池',['趋势来源 · 趋势周期 · 新兴人群','生活方式 · 需求假设 · 缺口空间','创新方向 · 验证状态 · 创新得分']),('爆款机会池',['ASIN · BSR 排名 · 类目 · 销量趋势','价格区间 · 评论质量 · 爆款 DNA','差评痛点 · 优化方向 · 爆款得分']))
def p31():
    s=header(31,'双路径机会汇聚后仍保留上下文，并通过 6 项字段转化为管理层可比较的投资语言。');steps=[('机会汇聚','保留来源与研判上下文'),('统一评分','6 项关键决策字段'),('决策输出','重仓 / 常规 / 谨慎 / 终止')]
    for i,(a,b) in enumerate(steps):x=100+i*610;s+=circle(x+210,470,88,[C['cyan'],C['blue'],C['purple']][i])+tx(x+210,466,f'0{i+1}',22,'#FFF',800,'middle')+tx(x+210,508,a,25,'#FFF',800,'middle')+tx(x+210,625,b,19,C['muted'],600,'middle');
    s+=arrow(410,470,650,C['dim'])+arrow(1020,470,1260,C['dim'])+rect(340,760,1240,76,C['soft'],12)+tx(960,808,'价值 · 结构 · 市场适配 · 投资策略 · 落地优先级 · 可追溯理由',20,C['ink'],700,'middle')
    return s
def p32():
    s=header(32,'前端探索布局长期壁垒，中端利用保障短期盈利，后端防御控制全链路风险。');layers=[('前端探索｜创新引擎','挖掘未来增量机会，布局长期产品壁垒',C['cyan']),('中端利用｜爆款引擎','优化成熟机会，保障短期营收盈利',C['orange'])]
    for i,(a,b,col) in enumerate(layers):y=300+i*150;s+=rect(160,y,1600,110,C['surface'],14,C['line'])+rect(160,y,15,110,col,8)+tx(215,y+45,a,25,C['ink'],800)+tx(215,y+82,b,18,C['muted'])
    risk=[('竞品动态监控',C['blue']),('市场风险预警',C['purple']),('合规风险拦截',C['red'])]
    for i,(a,col) in enumerate(risk):x=160+i*540;s+=rect(x,635,500,108,C['surface'],12,C['line'])+circle(x+40,675,8,col)+tx(x+64,683,a,22,C['ink'],700)
    return s+rect(160,800,1600,70,C['soft'],12)+tx(190,845,'全域沉淀：双路径物料、日志、模型持续迭代，形成企业专属数字化研发资产。',19,C['muted'])
def p34(): return compare_page(34,'创新与爆款采用不同终审表；风险审查必须与机会类型匹配。',('创新款风控',['趋势真实性：是否可持续、非泡沫','技术可行性：面料 / 工艺 / 供应链','市场适配性：人群与场景是否成立','原创合规：知识产权与合规审查']),('爆款款风控',['侵权雷同：外观 / 专利 / 商标排查','市场竞争：竞品动态与价格战预判','利润空间：成本波动与定价测算','量产稳定：交付与品控能力']))
def p35(): return compare_page(35,'两条路径各沉淀 6 项证据链资料，形成可回溯、可复用的研发知识库。',('创新引擎归档',['趋势研判报告 · 隐性需求图谱','供需缺口矩阵 · 创新避坑清单','原创产品定型方案 · 创新评分报告']),('爆款引擎归档',['爆款资质筛选 · 产品 DNA 拆解库','用户因果痛点 · 迭代优化方案','爆款定型参数 · 爆款评分报告']))
def p37():
    s=header(37,'从单链路试错升级为分层研发资产：短期盈利有保障，长期创新有布局。');d=[('研发逻辑','一刀切单链路','探索 / 利用独立研判'),('评价体系','单一权重，创新易错杀','创新看趋势缺口，爆款看验证基因'),('产品产出','跟风内卷或创新无依据','原创创新与爆款优化形成梯队'),('风险控制','预判单一，试错成本高','分层前置风控，降本避险'),('长期价值','只能复刻存量','数据、规则与决策经验持续进化')]
    for i,(a,b,c) in enumerate(d):x=80+(i%2)*890;y=300+(i//2)*175;w=1760 if i==4 else 850;s+=rect(x,y,w,145,C['surface'],12,C['line'])+tx(x+25,y+42,a,20,C['ink'],800)+tx(x+25,y+83,'传统',14,C['red'],800)+tx(x+105,y+83,b,17,C['muted'])+tx(x+25,y+120,'双引擎',14,C['blue'],800)+tx(x+105,y+120,c,17,C['ink'],600)
    return s
def p38():
    s=header(38,'用六个可被管理、可被评估的目标，定义研发系统的最终业务价值。')
    s+=rect(80,310,820,560,C['surface'],14,C['line'])+tx(120,356,'研发效率对比 / AI 双引擎 VS 传统流程',16,C['muted'],800)
    stages=['趋势调研','竞品拆解','需求归因','立项评审','物料归档']; traditional=[100,88,72,64,52]; ai=[20,24,18,26,16]
    x0,y0=180,760
    for i,stage in enumerate(stages):
        y=y0-i*80;s+=tx(180,y+14,stage,16,C['muted'],600)+rect(340,y,430,16,C['soft'],8)+rect(340,y,430*traditional[i]/100,16,C['dim'],8)+rect(340,y+26,430,16,C['soft'],8)+rect(340,y+26,430*ai[i]/100,16,C['blue'],8)
    s+=circle(578,386,6,C['dim'])+tx(594,392,'传统流程',14,C['muted'])+circle(710,386,6,C['blue'])+tx(726,392,'AI 双引擎',14,C['muted'])
    s+=rect(980,310,780,560,C['surface'],14,C['line'])+tx(1020,356,'体系价值仪表盘',16,C['muted'],800)
    values=[('80%','前置调研时间压缩',C['blue']),('2×','双路径机会并行',C['cyan']),('6项','统一投资决策字段',C['purple']),('4级','研发投入阈值',C['orange']),('100%','决策过程可追溯',C['green']),('前置','风险识别与拦截',C['red'])]
    for i,(value,label,col) in enumerate(values):
        x=1020+(i%2)*350;y=420+(i//2)*130;s+=tx(x,y,value,40,col,800)+tx(x,y+34,label,16,C['muted'])+ln(x,y+56,x+270,y+56,C['line'])
    return s

RENDER={1:p01,2:p02,3:lambda:chapter(3,'CHAPTER · 01','认知破局','传统 AI 选品的战略缺陷与研发死局。','chapter_problem.jpg'),4:p04,5:p05,6:p06,7:p07,8:lambda:chapter(8,'CHAPTER · 02','核心体系','AI 双引擎五层递进研发洞察体系。','chapter_engine.jpg'),9:p09,10:p10,11:p11,12:p12,13:p13,14:p14,15:lambda:product_page(15,'城市轻户外通勤外套',['轻量化防泼水面料','简约无 Logo 设计','通勤包容版型','城市通勤 + 轻户外'],['面料参数','双场景工艺','版型结构','审美规范','场景定义'],C['cyan']),16:p16,17:p17,18:p18,19:p19,20:p20,21:lambda:product_page(21,'升级款凉感 T 恤',['复用：凉感面料、合身版型','优化：不透肉、加固领型、抗皱水洗','结果：优于市面爆款的迭代品'],['复用参数','优化参数','微创新','落地工艺','成本定价'],C['orange']),22:p22,23:lambda:chapter(23,'CHAPTER · 03','工程化打分体系','创新 / 爆款分层量化评审。','chapter_score.jpg'),24:lambda:radar(24),25:p25,26:lambda:chapter(26,'CHAPTER · 04','流程对比','AI 分层研发 VS 传统单一研发。','chapter_problem.jpg'),27:p27,28:p28,29:lambda:chapter(29,'CHAPTER · 05','企业研发闭环','双引擎全链路流转与战略迭代机制。','chapter_engine.jpg'),30:p30,31:p31,32:p32,33:lambda:chapter(33,'CHAPTER · 06','终审与归档','风控终审与分层物料归档。','chapter_score.jpg'),34:p34,35:p35,36:lambda:chapter(36,'CHAPTER · 07','体系终复盘','双引擎分层研发 VS 传统单一研发。','chapter_engine.jpg'),37:p37,38:p38,39:lambda:cover(39,'谢谢','探索未来新品 · 复用成熟爆款','全域溯源 · 分层决策 · 可迭代进化','closing_bg.jpg')}

IMAGE_BACKGROUND_PAGES = {1,3,8,23,26,29,33,36,39}

for p in range(1,40):
    file=next(OUT.glob(f'{p:02d}_*.svg'))
    content=RENDER[p]()
    if p not in IMAGE_BACKGROUND_PAGES:
        content+=visual_slot(p)
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">{content}</svg>'
    file.write_text(svg,encoding='utf-8')

invalid=[]
for f in OUT.glob('*.svg'):
    try:
        root=ET.parse(f).getroot()
        if root.attrib.get('viewBox')!='0 0 1920 1080': invalid.append(f.name)
    except ET.ParseError: invalid.append(f.name)
if invalid: raise SystemExit('Invalid SVG: '+', '.join(invalid))
print('Rebuilt 39 content-specific SVG pages with charts and data.')
