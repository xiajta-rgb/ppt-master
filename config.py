import os
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.resolve()
STATIC_DIR = PROJECT_DIR / 'public'

PORT = 5001

PROJECT_ALIASES = {
    'git-intro': 'ppt169_像素风_git_introduction',
    'tactical-clothing': 'ppt169_战术服装_市场分析',
    'yili-feng': 'ppt169_易理风_地山谦卦深度研究',
    'chan-yi-feng': 'ppt169_禅意风_金刚经第一品研究',
    'demo-project': 'demo_project_intro_ppt169_20251211',
    'dark-tech': 'ppt169_general_dark_tech_claude_code_auto_mode',
    'claude-code-auto-mode': 'ppt169_general_dark_tech_claude_code_auto_mode',
    'google-annual': 'ppt169_谷歌风_google_annual_report',
    'debug六步法': 'ppt169_通用灵活+代码_debug六步法',
    'ai-programming-tools': 'ppt169_通过灵活+代码_三大AI编程神器横向对比',
    'attachment-therapy': 'ppt169_顶级咨询风_心理治疗中的依恋',
    'chongqing-report': 'ppt169_顶级咨询风_重庆市区域报告_ppt169_20251213',
    'ganzi-economy': 'ppt169_顶级咨询风_甘孜州经济财政分析',
    'ai-agent-anthropic': 'ppt169_顶级咨询风_构建有效AI代理_Anthropic',
    'nam-ou-hydro': 'ppt169_高端咨询风_南欧江水电站战略评估',
    'car-certification': 'ppt169_高端咨询风_汽车认证五年战略规划',
    'customer-loyalty': 'ppt169_麦肯锡风_kimsoong_customer_loyalty',
    'tactical-clothing-report': 'TacticalClothingReport',
}

SCRIPTS_DIR = PROJECT_DIR / '.trae' / 'skills' / 'ppt-master' / 'scripts'
