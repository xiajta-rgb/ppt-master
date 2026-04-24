import React, { useEffect, useRef, useState } from 'react';
import {
  CalendarOutlined,
  FileTextOutlined,
  AimOutlined,
  TrophyOutlined,
  ShoppingOutlined,
  BugOutlined,
  ExperimentOutlined,
  ToolOutlined,
  PictureOutlined,
  ScheduleOutlined,
  RobotOutlined,
  TeamOutlined,
  HeartOutlined,
  CompassOutlined,
  BulbOutlined,
  BankOutlined,
  LineChartOutlined,
  GlobalOutlined,
} from '@ant-design/icons';
import './TacticalClothingReport.css';

const TacticalClothingReport: React.FC = () => {
  const [scrolled, setScrolled] = useState(false);
  const [activeSection, setActiveSection] = useState('hero');
  const activeSectionRef = useRef('hero');
  const sectionsRef = useRef<HTMLDivElement>(null);

  const isScrollingRef = useRef(false);

  useEffect(() => {
    const handleScroll = () => {
      if (isScrollingRef.current) return;
      setScrolled(window.scrollY > 50);

      const sections = ['hero', 'toc', 'market', 'product', 'hardware', 'visual', 'brand', 'future'];
      const sortedSections = [...sections].reverse();
      for (const section of sortedSections) {
        const el = document.getElementById(section);
        if (el && window.scrollY >= el.offsetTop - 150) {
          setActiveSection(section);
          break;
        }
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    activeSectionRef.current = activeSection;
  }, [activeSection]);

  useEffect(() => {
    const fadeElements = document.querySelectorAll('.tcr-fade-in');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    }, { threshold: 0.1 });
    fadeElements.forEach(el => observer.observe(el));

    return () => observer.disconnect();
  }, []);

  const scrollToSection = (id: string) => {
    const el = document.getElementById(id);
    const scrollContainer = document.querySelector('.main-layout') as HTMLElement;
    if (el && scrollContainer) {
      isScrollingRef.current = true;
      const headerOffset = 80;
      const targetPosition = el.offsetTop - headerOffset;
      scrollContainer.scrollTo({ top: targetPosition, behavior: 'smooth' });
      setTimeout(() => { isScrollingRef.current = false; }, 800);
    }
  };

  const scrollToNextSection = () => {
    const scrollContainer = document.querySelector('.main-layout') as HTMLElement;
    if (scrollContainer) {
      scrollContainer.scrollTo({ top: scrollContainer.scrollTop + window.innerHeight * 0.9, behavior: 'smooth' });
    }
  };

  const navItems = [
    { id: 'toc', label: '目录' },
    { id: 'market', label: '市场分析' },
    { id: 'product', label: '产品设计' },
    { id: 'hardware', label: '辅料五金' },
    { id: 'visual', label: '视觉呈现' },
    { id: 'brand', label: '品牌格局' },
    { id: 'future', label: '未来机遇' },
  ];

  const tocItems = [
    { id: 'market', num: '01', title: '市场现状与趋势', sub: '规模数据 / 增长驱动 / Gorpcore浪潮' },
    { id: 'product', num: '02', title: '核心产品设计DNA', sub: '面料科技 / 版型工学 / 功能细节' },
    { id: 'hardware', num: '03', title: '辅料与五金体系', sub: '拉链 / 扣具 / 织带 / 工艺标准' },
    { id: 'visual', num: '04', title: '产品视觉呈现', sub: 'Listing优化 / 色彩体系 / 摄影美学' },
    { id: 'brand', num: '05', title: '品牌竞争格局', sub: '头部品牌 / 定位矩阵 / 差异化策略' },
    { id: 'future', num: '06', title: '未来机遇与战略建议', sub: '市场切入 / 产品策略 / 品牌定位' },
  ];

  return (
    <div className="tcr-body" ref={sectionsRef}>
      <nav className={`tcr-nav ${scrolled ? 'scrolled' : ''}`}>
        <div className="tcr-nav-logo">TACTICAL REPORT</div>
        <ul className="tcr-nav-links">
          {navItems.map(item => (
            <li key={item.id}>
              <a
                className={activeSection === item.id ? 'active' : ''}
                onClick={() => scrollToSection(item.id)}
              >
                {item.label}
              </a>
            </li>
          ))}
        </ul>
      </nav>

      <section className="tcr-hero" id="hero">
        <div className="tcr-hero-bg" />
        <div className="tcr-hero-grid" />
        <div className="tcr-hero-content">
          <div className="tcr-hero-badge">Industry Research · 2025</div>
          <h1>
            亚马逊美国站<br />
            <span>休闲工装战术服装</span><br />
            市场深度分析
          </h1>
          <p className="tcr-hero-subtitle">
            从市场规模、竞争格局到产品设计DNA——面料科技、版型工学、辅料体系与视觉呈现的全方位专业解读
          </p>
          <div className="tcr-hero-meta">
            <span><CalendarOutlined /> 2025年4月</span>
            <span><GlobalOutlined /> Amazon US Market</span>
            <span><FileTextOutlined /> 课程研究报告</span>
          </div>
        </div>
      </section>

      <div className="tcr-toc" id="toc">
        <div className="tcr-toc-inner">
          <div className="tcr-toc-header">
            <div className="tcr-toc-title">CONTENTS</div>
            <h2 className="tcr-toc-heading">报告目录</h2>
          </div>
          <div className="tcr-toc-grid">
            {tocItems.map(item => (
              <div
                key={item.id}
                className="tcr-toc-item"
                onClick={() => scrollToSection(item.id)}
              >
                <div className="tcr-toc-num">{item.num}</div>
                <div>
                  <div className="tcr-toc-text">{item.title}</div>
                  <div className="tcr-toc-sub">{item.sub}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="tcr-section-alt" id="market">
        <section className="tcr-section tcr-fade-in">
          <div className="tcr-section-header">
            <span className="tcr-section-label">Chapter 01</span>
            <h2 className="tcr-section-title">市场现状与趋势</h2>
            <p className="tcr-section-desc">
              全球战术与户外服装市场正经历结构性增长，"城市战术"与Gorpcore风潮推动品类从专业领域向大众消费渗透
            </p>
          </div>

          <div className="tcr-grid-4" style={{ marginBottom: '64px' }}>
            <div className="tcr-stat-card">
              <div className="tcr-stat-value">$184<small>亿</small></div>
              <div className="tcr-stat-label">2025年全球市场规模</div>
              <div className="tcr-stat-sub">战术与户外服装</div>
            </div>
            <div className="tcr-stat-card">
              <div className="tcr-stat-value">5.1<small>%</small></div>
              <div className="tcr-stat-label">年复合增长率</div>
              <div className="tcr-stat-sub">2025-2033预测</div>
            </div>
            <div className="tcr-stat-card">
              <div className="tcr-stat-value">$274<small>亿</small></div>
              <div className="tcr-stat-label">2033年预计规模</div>
              <div className="tcr-stat-sub">持续稳健增长</div>
            </div>
            <div className="tcr-stat-card">
              <div className="tcr-stat-value">50<small>%+</small></div>
              <div className="tcr-stat-label">线上销售占比</div>
              <div className="tcr-stat-sub">电商渠道主导</div>
            </div>
          </div>

          <div className="tcr-content-block">
            <h3>1.1 市场规模与增长动力</h3>
            <p>
              根据 Global Growth Insights 数据，<strong>2024年全球战术与户外服装市场规模达175.57亿美元</strong>，2025年预计增长至184.45亿美元，到2033年有望突破273.77亿美元，期间复合年增长率（CAGR）约为5.06%。Technavio的独立研究给出更为乐观的预测：2025-2030年间市场增量将达30.3亿美元，CAGR为6.6%。
            </p>
            <p>
              美国作为全球最大消费市场，占区域需求的<strong>60%以上</strong>。2024年美国工装市场规模为34.5亿美元，预计到2035年将增长至52亿美元。北美市场的核心驱动力来自户外活动参与度的持续攀升（增长40%）、战术装备兴趣的爆发式增长（35%），以及城市战术时尚需求的强劲扩张（45%）。
            </p>

            <div className="tcr-highlight-box">
              <div className="tcr-box-title"><LineChartOutlined /> 关键增长驱动因素</div>
              <p><strong>户外活动参与度增长40%</strong> — 徒步、露营、狩猎、气枪运动等户外休闲活动持续升温</p>
              <p><strong>城市战术时尚需求增长45%</strong> — 军旅风格设计从专业领域渗透到日常消费，Gorpcore成为主流审美</p>
              <p><strong>面料科技需求增长30%</strong> — 吸湿排汗、防火、防撕裂等功能性面料成为消费者核心诉求</p>
              <p><strong>环保偏好增长45%</strong> — 再生聚酯、有机棉等可持续材料成为购买决策的关键因素</p>
            </div>

            <h3>1.2 消费结构与人群画像</h3>
            <p>战术服装的核心消费群体已经从传统的军事、执法专业人士扩展到多元化的日常用户群体：</p>
            <div className="tcr-grid-3" style={{ margin: '32px 0' }}>
              <div className="tcr-card" style={{ textAlign: 'center' }}>
                <div className="tcr-card-icon"><AimOutlined /></div>
                <h4 style={{ marginBottom: '8px' }}>专业用户</h4>
                <p style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>军事、执法、消防、急救等专业人士，强调功能性与耐用性</p>
              </div>
              <div className="tcr-card" style={{ textAlign: 'center' }}>
                <div className="tcr-card-icon"><CompassOutlined /></div>
                <h4 style={{ marginBottom: '8px' }}>户外爱好者</h4>
                <p style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>徒步、露营、狩猎、钓鱼爱好者，追求面料功能性与舒适性</p>
              </div>
              <div className="tcr-card" style={{ textAlign: 'center' }}>
                <div className="tcr-card-icon"><ShoppingOutlined /></div>
                <h4 style={{ marginBottom: '8px' }}>城市消费者</h4>
                <p style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>追求实用主义与时尚感融合的都市白领，Gorpcore风格拥趸</p>
              </div>
            </div>

            <div className="tcr-highlight-box">
              <div className="tcr-box-title"><BulbOutlined /> 核心洞察</div>
              <p><strong>"城市战术"(Urban Tactical) 是最大增量市场</strong>——这批用户不需要专业装备的专业性能，但对其"看起来专业"的设计语言有强烈偏好。品牌入局的最佳切入点。</p>
            </div>
          </div>
        </section>
      </div>

      <div id="product">
        <section className="tcr-section tcr-fade-in">
          <div className="tcr-section-header">
            <span className="tcr-section-label">Chapter 02</span>
            <h2 className="tcr-section-title">核心产品设计DNA</h2>
            <p className="tcr-section-desc">
              面料科技、版型工学与功能细节构成了战术服装的产品力三角——每一处设计决策都服务于"耐用性、功能性、舒适性"的核心诉求
            </p>
          </div>

          <div className="tcr-content-block">
            <h3>2.1 面料科技</h3>
            <p>面料是战术服装的"硬实力"。亚马逊头部品牌普遍采用以下面料技术建立竞争壁垒：</p>

            <div className="tcr-table-wrapper">
              <table className="tcr-table">
                <thead>
                  <tr>
                    <th>面料技术</th>
                    <th>功能特性</th>
                    <th>适用场景</th>
                    <th>代表品牌/产品</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Cordura 尼龙</strong></td>
                    <td>卓越耐磨性，比标准尼龙高10倍</td>
                    <td>高强度战术裤、背包</td>
                    <td>5.11全系列、Vertx Delta</td>
                  </tr>
                  <tr>
                    <td><strong>Ripstop 防撕裂</strong></td>
                    <td>菱形网格结构，轻量抗撕裂</td>
                    <td>常规战术裤、户外服装</td>
                    <td>Condor, BLACKHAWK!</td>
                  </tr>
                  <tr>
                    <td><strong>棉/聚酯混纺 (65/35)</strong></td>
                    <td>透气舒适，成本效益平衡</td>
                    <td>日常战术、工装裤</td>
                    <td>Dickies 874, Wrangler</td>
                  </tr>
                  <tr>
                    <td><strong>DWR 持久防泼水</strong></td>
                    <td>水珠在面料表面滑落，不浸透</td>
                    <td>几乎所有中高端战术裤标配</td>
                    <td>Vertx Delta, 5.11全系列</td>
                  </tr>
                  <tr>
                    <td><strong>Teflon 特氟龙涂层</strong></td>
                    <td>防水 + 防污渍双重保护</td>
                    <td>需要抗油污的工作环境</td>
                    <td>5.11 Stryke, Apex, XPRT</td>
                  </tr>
                  <tr>
                    <td><strong>37.5 温控技术</strong></td>
                    <td>活性炭粒子调节微气候温度</td>
                    <td>全天候温度管理</td>
                    <td>Vertx Fusion LT</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>2.2 版型与廓形工学</h3>
            <p>版型是战术服装"功能性"与"时尚感"的交汇点。当前亚马逊美国站主流品牌已发展出清晰的版型分级体系：</p>

            <div className="tcr-grid-3" style={{ margin: '32px 0' }}>
              <div className="tcr-card" style={{ textAlign: 'center' }}>
                <div className="tcr-card-icon"><TeamOutlined /></div>
                <h4 style={{ marginBottom: '8px' }}>Classic Fit 经典合身</h4>
                <p style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>传统工装版型，宽松舒适，适合体力劳动者和年长消费者</p>
              </div>
              <div className="tcr-card" style={{ textAlign: 'center' }}>
                <div className="tcr-card-icon"><AimOutlined /></div>
                <h4 style={{ marginBottom: '8px' }}>Athletic Fit 运动合身</h4>
                <p style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>针对健身人群优化，臀部/腿部收紧，适合标准体型年轻人</p>
              </div>
              <div className="tcr-card" style={{ textAlign: 'center' }}>
                <div className="tcr-card-icon"><TrophyOutlined /></div>
                <h4 style={{ marginBottom: '8px' }}>Slim Fit 修身裁剪</h4>
                <p style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>现代都市感，适合城市战术时尚消费者，融合功能与风格</p>
              </div>
            </div>

            <h3>2.3 功能细节设计</h3>
            <p>战术服装的功能细节是其区别于普通服装的核心标志，也是消费者识别产品专业性的关键触点：</p>

            <ul className="tcr-detail-list">
              <li>
                <div className="tcr-detail-icon"><BugOutlined /></div>
                <div className="tcr-detail-text">
                  <h5>口袋系统 Pocket System（8-14+口袋）</h5>
                  <p>大腿贴袋、隐藏弹匣/手机口袋、刀片/手电筒插槽、后臀Credential翻盖口袋。网布里衬增加透气性，褶裥设计实现容量扩展。</p>
                </div>
              </li>
              <li>
                <div className="tcr-detail-icon"><ExperimentOutlined /></div>
                <div className="tcr-detail-text">
                  <h5>通风系统 Ventilation System</h5>
                  <p>网眼通风口袋内衬、膝盖通风口、无衬育克、拉链通风口——战略性放置通风口促进空气流通，应对高温环境。</p>
                </div>
              </li>
              <li>
                <div className="tcr-detail-icon"><ScheduleOutlined /></div>
                <div className="tcr-detail-text">
                  <h5>腰部工学 Waistband Engineering</h5>
                  <p>弹力侧腰提供2-3英寸伸缩范围、可调节滑动腰带微调腰围、内置衬衫固定器防止滑出、加高后腰改善负重分配。</p>
                </div>
              </li>
              <li>
                <div className="tcr-detail-icon"><ToolOutlined /></div>
                <div className="tcr-detail-text">
                  <h5>加固工艺 Reinforcement</h5>
                  <p>双线缝合、打枣加固（Bar Tacks）关键受力点、YKK铆钉加固应力点、平缝/粘合缝减少摩擦。</p>
                </div>
              </li>
            </ul>
          </div>
        </section>
      </div>

      <div className="tcr-section-alt" id="hardware">
        <section className="tcr-section tcr-fade-in">
          <div className="tcr-section-header">
            <span className="tcr-section-label">Chapter 03</span>
            <h2 className="tcr-section-title">辅料与五金体系</h2>
            <p className="tcr-section-desc">
              拉链、扣具、织带、魔术贴——辅料五金是战术服装"专业感"与"可靠性"的具象化表达，也是品质差异化的关键维度
            </p>
          </div>

          <div className="tcr-content-block">
            <div className="tcr-table-wrapper">
              <table className="tcr-table">
                <thead>
                  <tr>
                    <th>五金类型</th>
                    <th>行业标杆品牌</th>
                    <th>材质与规格</th>
                    <th>采购成本区间</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>拉链</strong></td>
                    <td>YKK（70%市占率）、SBS</td>
                    <td>树脂/金属，抗腐蚀</td>
                    <td>$0.5-3/pcs</td>
                  </tr>
                  <tr>
                    <td><strong>扣具</strong></td>
                    <td>ITW Nexus、Cobra（军规）</td>
                    <td>acetyl、锌合金</td>
                    <td>$1-8/pcs</td>
                  </tr>
                  <tr>
                    <td><strong>织带</strong></td>
                    <td>YKK（织带）</td>
                    <td>尼龙/聚酯，军规级抗拉</td>
                    <td>$0.2-1/meter</td>
                  </tr>
                  <tr>
                    <td><strong>魔术贴</strong></td>
                    <td>3M Scotchcal</td>
                    <td>尼龙</td>
                    <td>$0.3-2/pcs</td>
                  </tr>
                  <tr>
                    <td><strong>铆钉/气眼</strong></td>
                    <td>YKK钉</td>
                    <td>铜/不锈钢，抗氧化</td>
                    <td>$0.05-0.2/pcs</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div className="tcr-highlight-box">
              <div className="tcr-box-title"><BulbOutlined /> 服装人专业洞察</div>
              <p>辅料五金是消费者感知"专业感"最直接的触点。YKK拉链的Logo、COBRA扣具的机械感、D型环的金属光泽——这些细节在产品图片和实物体验中都会产生强烈的品质暗示。</p>
              <p>对于新入局品牌，<strong>在辅料上对标行业标杆（YKK + 军规织带 + 不锈钢五金）是最小成本建立专业形象的有效策略</strong>。</p>
            </div>
          </div>
        </section>
      </div>

      <div id="visual">
        <section className="tcr-section tcr-fade-in">
          <div className="tcr-section-header">
            <span className="tcr-section-label">Chapter 04</span>
            <h2 className="tcr-section-title">产品视觉呈现</h2>
            <p className="tcr-section-desc">
              在亚马逊电商语境下，视觉呈现即产品力——从主图规范到A+内容，从色彩体系到摄影美学，每一帧画面都在传递品牌定位
            </p>
          </div>

          <div className="tcr-content-block">
            <h3>4.1 亚马逊Listing视觉规范与最佳实践</h3>
            <p>亚马逊的图片规范是所有品牌的"底线要求"，而头部品牌在此基础上发展出差异化的视觉策略。</p>

            <div className="tcr-img-block">
              <img src="/md_doc/tactical_clothing_report/images/amazon_listing_visual.jpg" alt="亚马逊产品Listing视觉呈现" />
              <div className="tcr-img-caption">品牌定位梯度 — 从大众工装到顶级军规，市场已形成清晰的分层格局</div>
            </div>

            <h3>4.2 色彩体系与品牌调性</h3>
            <p>战术服装的色彩策略反映品牌定位——从低调专业到张扬时尚：</p>

            <div className="tcr-table-wrapper">
              <table className="tcr-table">
                <thead>
                  <tr>
                    <th>风格定位</th>
                    <th>主色调</th>
                    <th>辅色调</th>
                    <th>设计语言</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>顶级军规 Tactical</strong></td>
                    <td>黑色、卡其色、OD绿</td>
                    <td>Coyote Brown、沙色</td>
                    <td>最低调务实，无logo外露</td>
                  </tr>
                  <tr>
                    <td><strong>执法专业</strong></td>
                    <td>黑色、Navy Blue</td>
                    <td>银色反光条</td>
                    <td>明确功能分区，反光安全标识</td>
                  </tr>
                  <tr>
                    <td><strong>户外工装</strong></td>
                    <td>棕色、Dark Navy</td>
                    <td>Hamilton Brown、Lily绿</td>
                    <td>都市街头化，鲜艳色调 + 做旧</td>
                  </tr>
                  <tr>
                    <td><strong>K-Techwear</strong></td>
                    <td>黑、灰、橄榄绿</td>
                    <td>亮橙（压胶撞色）</td>
                    <td>机能解构，"将功能通过时装化手段隐藏"</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div className="tcr-highlight-box accent-bg">
              <div className="tcr-box-title"><PictureOutlined /> 色彩战略建议</div>
              <p><strong>新手入局建议从中性色调切入</strong>——黑色、卡其、灰色是亚马逊战术服装的主流色，需求稳定，库存风险低。在建立一定体量后，再考虑通过亮色或联名款突破差异化。</p>
            </div>
          </div>
        </section>
      </div>

      <div className="tcr-section-alt" id="brand">
        <section className="tcr-section tcr-fade-in">
          <div className="tcr-section-header">
            <span className="tcr-section-label">Chapter 05</span>
            <h2 className="tcr-section-title">品牌竞争格局</h2>
            <p className="tcr-section-desc">
              从$25 Dickies到$322 Crye Precision，市场存在清晰的价格阶梯和对应的消费群体——品牌分层是品类成熟的核心标志
            </p>
          </div>

          <div className="tcr-img-block">
            <img src="/md_doc/tactical_clothing_report/images/brand_positioning.jpg" alt="品牌定位与竞争格局" />
            <div className="tcr-img-caption">品牌定位梯度 — 从大众工装到顶级军规，市场已形成清晰的分层格局</div>
          </div>

          <div className="tcr-content-block">
            <h3>5.1 价格分层与定位矩阵</h3>

            <div className="tcr-table-wrapper">
              <table className="tcr-table">
                <thead>
                  <tr>
                    <th>价格区间</th>
                    <th>代表品牌</th>
                    <th>核心竞争要素</th>
                    <th>目标客群</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>$20-40 大众工装</strong></td>
                    <td>Dickies, Wrangler, Carhartt</td>
                    <td>性价比、实用性、品牌认知</td>
                    <td>蓝领工人、日常休闲</td>
                  </tr>
                  <tr>
                    <td><strong>$40-80 中端战术</strong></td>
                    <td>5.11 Tactical, Condor</td>
                    <td>功能性强、面料可靠、款式多样</td>
                    <td>户外爱好者、执法从业者</td>
                  </tr>
                  <tr>
                    <td><strong>$80-150 专业战术</strong></td>
                    <td>Vertx, First Tactical</td>
                    <td>顶级面料、精密版型、细节工艺</td>
                    <td>专业用户、城市战术爱好者</td>
                  </tr>
                  <tr>
                    <td><strong>$150+ 顶级军规</strong></td>
                    <td>Crye Precision, Arc'teryx LEAF</td>
                    <td>军事级别耐用性、轻量化</td>
                    <td>特种部队、高端装备玩家</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div className="tcr-highlight-box">
              <div className="tcr-box-title"><BulbOutlined /> 竞争启示</div>
              <p><strong>中端市场 ($40-80) 是品牌入局的最佳切入点</strong>——既有足够的利润空间支撑品牌建设，又能通过功能差异化与大众工装拉开距离。这个价格带的消费者既有功能诉求，又有消费能力。</p>
            </div>
          </div>
        </section>
      </div>

      <div className="tcr-section-dark" id="future">
        <section className="tcr-section tcr-fade-in">
          <div className="tcr-section-header">
            <span className="tcr-section-label">Chapter 06</span>
            <h2 className="tcr-section-title">未来机遇与战略建议</h2>
            <p className="tcr-section-desc">
              基于市场数据、产品分析和趋势洞察，为品牌入局或升级提供可执行的战略方向
            </p>
          </div>

          <div className="tcr-content-block">
            <h3>6.1 战略机遇窗口</h3>

            <div className="tcr-grid-3" style={{ marginBottom: '48px' }}>
              <div className="tcr-card">
                <div className="tcr-card-icon"><BankOutlined /></div>
                <h4 style={{ marginBottom: '12px' }}>城市战术渗透</h4>
                <p style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>
                  Gorpcore风潮持续扩张，"看起来像战术装备"比"真的是战术装备"有更广阔的市场。城市战术风格溢价空间大。
                </p>
              </div>
              <div className="tcr-card">
                <div className="tcr-card-icon"><HeartOutlined /></div>
                <h4 style={{ marginBottom: '12px' }}>可持续升级</h4>
                <p style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>
                  40-45%消费者表示环保材料影响购买决策。再生面料、有机棉认证可以成为差异化切入点。
                </p>
              </div>
              <div className="tcr-card">
                <div className="tcr-card-icon"><RobotOutlined /></div>
                <h4 style={{ marginBottom: '12px' }}>智能功能融合</h4>
                <p style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>
                  抗菌面料、温度调节、智能收纳——科技赋能的面料创新是下一个十年的核心竞争维度。
                </p>
              </div>
            </div>

            <h3>6.2 市场进入建议</h3>

            <div className="tcr-highlight-box" style={{ marginBottom: '16px' }}>
              <p><strong>1. 从中端切入，逐步上探：</strong>$45-75价格带是最佳起点，有足够利润空间进行品牌建设。</p>
            </div>
            <div className="tcr-highlight-box" style={{ marginBottom: '16px' }}>
              <p><strong>2. "城市战术"是最大增量：</strong>45%的城市战术需求增长表明军旅风格已从专业领域渗透到日常消费。</p>
            </div>
            <div className="tcr-highlight-box" style={{ marginBottom: '16px' }}>
              <p><strong>3. Gorpcore是结构性转变：</strong>Arc'teryx 20亿美元+、Salomon 10亿美元鞋类销售的突破证明了户外功能服装已成为一代人的"制服"。</p>
            </div>
            <div className="tcr-highlight-box" style={{ marginBottom: '16px' }}>
              <p><strong>4. 亚马逊是核心战场：</strong>线上销售占比超50%，A+内容可提升20%销售额，视觉呈现即产品力。</p>
            </div>
            <div className="tcr-highlight-box" style={{ marginBottom: '16px' }}>
              <p><strong>5. 功能与时尚融合加速：</strong>技术面料不再仅服务于专业场景，而是成为日常时尚的表达载体。</p>
            </div>
            <div className="tcr-highlight-box">
              <p><strong>6. 可持续性是必选项：</strong>40-45%消费者环保偏好 + PFAS法规收紧，要求品牌在材料创新上持续投入。</p>
            </div>

            <h3>6.3 核心增长指标</h3>

            <div className="tcr-progress-section">
              <div className="tcr-progress-item">
                <div className="tcr-progress-label">
                  <span>城市战术时尚需求增长</span>
                  <span>45%</span>
                </div>
                <div className="tcr-progress-bar">
                  <div className="tcr-progress-fill" style={{ width: '45%' }} />
                </div>
              </div>
              <div className="tcr-progress-item">
                <div className="tcr-progress-label">
                  <span>户外活动参与度增长</span>
                  <span>40%</span>
                </div>
                <div className="tcr-progress-bar">
                  <div className="tcr-progress-fill" style={{ width: '40%' }} />
                </div>
              </div>
              <div className="tcr-progress-item">
                <div className="tcr-progress-label">
                  <span>面料科技需求增长</span>
                  <span>30%</span>
                </div>
                <div className="tcr-progress-bar">
                  <div className="tcr-progress-fill" style={{ width: '30%' }} />
                </div>
              </div>
              <div className="tcr-progress-item">
                <div className="tcr-progress-label">
                  <span>环保材料偏好增长</span>
                  <span>45%</span>
                </div>
                <div className="tcr-progress-bar">
                  <div className="tcr-progress-fill" style={{ width: '45%' }} />
                </div>
              </div>
              <div className="tcr-progress-item">
                <div className="tcr-progress-label">
                  <span>社交媒体驱动品牌互动增长</span>
                  <span>35%</span>
                </div>
                <div className="tcr-progress-bar">
                  <div className="tcr-progress-fill" style={{ width: '35%' }} />
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>

      <footer className="tcr-footer">
        <div className="tcr-footer-divider" />
        <p>亚马逊美国站 · 休闲工装战术服装市场深度分析报告</p>
        <p>数据来源：Global Growth Insights · Technavio · Workwear.org · Amazon公开数据</p>
        <p>报告日期：2025年4月 | 仅供内部课程研究使用</p>
      </footer>

      <button className="tcr-page-scroll-indicator" onClick={scrollToNextSection} type="button">
        <span className="tcr-scroll-arrow">↓</span>
        <span>SCROLL</span>
      </button>
    </div>
  );
};

export default TacticalClothingReport;