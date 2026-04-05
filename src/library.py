import sqlite3
import re
import json
import requests
from pathlib import Path
from typing import Optional
from mutagen import File as MutagenFile
from src.models import Track

PINYIN_MAP = {
    "啊": "a",
    "阿": "a",
    "啊": "a",
    "八": "ba",
    "巴": "ba",
    "拔": "ba",
    "把": "ba",
    "坝": "ba",
    "爸": "ba",
    "白": "bai",
    "百": "bai",
    "摆": "bai",
    "败": "bai",
    "拜": "bai",
    "班": "ban",
    "搬": "ban",
    "板": "ban",
    "版": "ban",
    "半": "ban",
    "办": "ban",
    "扮": "ban",
    "伴": "ban",
    "邦": "bang",
    "帮": "bang",
    "棒": "bang",
    "包": "bao",
    "宝": "bao",
    "报": "bao",
    "抱": "bao",
    "暴": "bao",
    "北": "bei",
    "被": "bei",
    "背": "bei",
    "倍": "bei",
    "杯": "bei",
    "奔": "ben",
    "本": "ben",
    "笨": "ben",
    "比": "bi",
    "笔": "bi",
    "必": "bi",
    "闭": "bi",
    "毕": "bi",
    "碧": "bi",
    "避": "bi",
    "鼻": "bi",
    "边": "bian",
    "便": "bian",
    "变": "bian",
    "编": "bian",
    "辩": "bian",
    "辨": "bian",
    "贬": "bian",
    "表": "biao",
    "别": "bie",
    "憋": "bie",
    "宾": "bin",
    "滨": "bin",
    "冰": "bing",
    "兵": "bing",
    "饼": "bing",
    "并": "bing",
    "病": "bing",
    "波": "bo",
    "博": "bo",
    "拨": "bo",
    "播": "bo",
    "伯": "bo",
    "不": "bu",
    "步": "bu",
    "部": "bu",
    "布": "bu",
    "猜": "cai",
    "才": "cai",
    "材": "cai",
    "采": "cai",
    "菜": "cai",
    "参": "can",
    "餐": "can",
    "残": "can",
    "惭": "can",
    "惨": "can",
    "苍": "cang",
    "藏": "cang",
    "操": "cao",
    "曹": "cao",
    "草": "cao",
    "测": "ce",
    "策": "ce",
    "册": "ce",
    "层": "ceng",
    "曾": "ceng",
    "查": "cha",
    "茶": "cha",
    "差": "cha",
    "察": "cha",
    "产": "chan",
    "颤": "chan",
    "常": "chang",
    "长": "chang",
    "场": "chang",
    "唱": "chang",
    "超": "chao",
    "车": "che",
    "彻": "che",
    "陈": "chen",
    "趁": "chen",
    "成": "cheng",
    "城": "cheng",
    "呈": "cheng",
    "承": "cheng",
    "诚": "cheng",
    "吃": "chi",
    "持": "chi",
    "赤": "chi",
    "尺": "chi",
    "充": "chong",
    "冲": "chong",
    "虫": "chong",
    "重": "chong",
    "春": "chun",
    "出": "chu",
    "初": "chu",
    "除": "chu",
    "处": "chu",
    "础": "chu",
    "储": "chu",
    "楚": "chu",
    "次": "ci",
    "词": "ci",
    "此": "ci",
    "刺": "ci",
    "辞": "ci",
    "慈": "ci",
    "磁": "ci",
    "从": "cong",
    "匆": "cong",
    "聪": "cong",
    "凑": "cou",
    "粗": "cu",
    "促": "cu",
    "醋": "cu",
    "窜": "cuan",
    "攒": "cuan",
    "催": "cui",
    "脆": "cui",
    "翠": "cui",
    "村": "cun",
    "存": "cun",
    "错": "cuo",
    "措": "cuo",
    "达": "da",
    "打": "da",
    "大": "da",
    "带": "dai",
    "待": "dai",
    "代": "dai",
    "袋": "dai",
    "大": "dai",
    "蛋": "dan",
    "但": "dan",
    "担": "dan",
    "党": "dang",
    "当": "dang",
    "刀": "dao",
    "倒": "dao",
    "到": "dao",
    "道": "dao",
    "得": "de",
    "德": "de",
    "的": "de",
    "等": "deng",
    "低": "di",
    "底": "di",
    "敌": "di",
    "弟": "di",
    "帝": "di",
    "递": "di",
    "点": "dian",
    "电": "dian",
    "店": "dian",
    "淀": "dian",
    "定": "dian",
    "钉": "ding",
    "东": "dong",
    "冬": "dong",
    "动": "dong",
    "懂": "dong",
    "都": "dou",
    "斗": "dou",
    "豆": "dou",
    "都": "du",
    "读": "du",
    "度": "du",
    "独": "du",
    "赌": "du",
    "段": "duan",
    "断": "duan",
    "锻": "duan",
    "对": "dui",
    "队": "dui",
    "吨": "dun",
    "顿": "dun",
    "多": "duo",
    "夺": "duo",
    "朵": "duo",
    "饿": "e",
    "恶": "e",
    "儿": "er",
    "而": "er",
    "二": "er",
    "发": "fa",
    "法": "fa",
    "翻": "fan",
    "凡": "fan",
    "烦": "fan",
    "反": "fan",
    "返": "fan",
    "范": "fan",
    "方": "fang",
    "房": "fang",
    "防": "fang",
    "访": "fang",
    "放": "fang",
    "非": "fei",
    "飞": "fei",
    "肥": "fei",
    "废": "fei",
    "肺": "fei",
    "分": "fen",
    "粉": "fen",
    "份": "fen",
    "奋": "fen",
    "愤": "fen",
    "粪": "fen",
    "风": "feng",
    "封": "feng",
    "丰": "feng",
    "峰": "feng",
    "锋": "feng",
    "疯": "feng",
    "佛": "fo",
    "否": "fou",
    "夫": "fu",
    "父": "fu",
    "服": "fu",
    "副": "fu",
    "复": "fu",
    "富": "fu",
    "府": "fu",
    "负": "fu",
    "妇": "fu",
    "附": "fu",
    "复": "fu",
    "嘎": "ga",
    "噶": "ga",
    "改": "gai",
    "盖": "gai",
    "概": "gai",
    "干": "gan",
    "感": "gan",
    "敢": "gan",
    "赶": "gan",
    "刚": "gang",
    "港": "gang",
    "高": "gao",
    "告": "gao",
    "歌": "ge",
    "个": "ge",
    "各": "ge",
    "给": "gei",
    "根": "gen",
    "跟": "gen",
    "更": "geng",
    "工": "gong",
    "公": "gong",
    "共": "gong",
    "功": "gong",
    "供": "gong",
    "够": "gou",
    "狗": "gou",
    "购": "gou",
    "古": "gu",
    "故": "gu",
    "顾": "gu",
    "姑": "gu",
    "骨": "gu",
    "估": "gu",
    "谷": "gu",
    "雇": "gu",
    "瓜": "gua",
    "挂": "gua",
    "乖": "guai",
    "怪": "guai",
    "关": "guan",
    "观": "guan",
    "管": "guan",
    "官": "guan",
    "馆": "guan",
    "惯": "guan",
    "光": "guang",
    "广": "guang",
    "贵": "gui",
    "规": "gui",
    "鬼": "gui",
    "归": "gui",
    "柜": "gui",
    "桂": "gui",
    "国": "guo",
    "果": "guo",
    "过": "guo",
    "哈": "ha",
    "还": "hai",
    "海": "hai",
    "害": "han",
    "含": "han",
    "寒": "han",
    "汉": "han",
    "行": "hang",
    "航": "hang",
    "好": "hao",
    "号": "hao",
    "浩": "hao",
    "和": "he",
    "河": "he",
    "何": "he",
    "合": "he",
    "喝": "he",
    "黑": "hei",
    "很": "hen",
    "恨": "hen",
    "红": "hong",
    "洪": "hong",
    "宏": "hong",
    "虹": "hong",
    "后": "hou",
    "厚": "hou",
    "候": "hou",
    "湖": "hu",
    "虎": "hu",
    "互": "hu",
    "户": "hu",
    "护": "hu",
    "花": "hua",
    "华": "hua",
    "化": "hua",
    "话": "hua",
    "画": "hua",
    "划": "hua",
    "黄": "huang",
    "慌": "huang",
    "灰": "hui",
    "回": "hui",
    "汇": "hui",
    "会": "hui",
    "惠": "hui",
    "毁": "hui",
    "活": "huo",
    "火": "huo",
    "获": "huo",
    "货": "huo",
    "基": "ji",
    "机": "ji",
    "积": "ji",
    "技": "ji",
    "际": "ji",
    "极": "ji",
    "即": "ji",
    "急": "ji",
    "几": "ji",
    "己": "ji",
    "记": "ji",
    "纪": "ji",
    "计": "ji",
    "家": "jia",
    "加": "jia",
    "假": "jia",
    "价": "jia",
    "架": "jia",
    "驾": "jia",
    "嫁": "jia",
    "甲": "jia",
    "监": "jian",
    "见": "jian",
    "件": "jian",
    "建": "jian",
    "减": "jian",
    "简": "jian",
    "将": "jiang",
    "江": "jiang",
    "奖": "jiang",
    "讲": "jiang",
    "匠": "jiang",
    "交": "jiao",
    "焦": "jiao",
    "角": "jiao",
    "脚": "jiao",
    "教": "jiao",
    "叫": "jiao",
    "较": "jiao",
    "接": "jie",
    "街": "jie",
    "节": "jie",
    "姐": "jie",
    "解": "jie",
    "借": "jie",
    "今": "jin",
    "金": "jin",
    "仅": "jin",
    "进": "jin",
    "近": "jin",
    "尽": "jin",
    "劲": "jin",
    "京": "jing",
    "经": "jing",
    "精": "jing",
    "静": "jing",
    "景": "jing",
    "竞": "jing",
    "久": "jiu",
    "九": "jiu",
    "酒": "jiu",
    "旧": "jiu",
    "救": "jiu",
    "就": "jiu",
    "具": "ju",
    "据": "ju",
    "聚": "ju",
    "举": "ju",
    "居": "ju",
    "局": "ju",
    "菊": "ju",
    "局": "ju",
    "矩": "ju",
    "巨": "ju",
    "句": "ju",
    "剧": "ju",
    "据": "ju",
    "捐": "juan",
    "卷": "juan",
    "决": "jue",
    "绝": "jue",
    "觉": "jue",
    "军": "jun",
    "均": "jun",
    "君": "jun",
    "卡": "ka",
    "开": "kai",
    "看": "kan",
    "坎": "kan",
    "砍": "kan",
    "抗": "kang",
    "考": "kao",
    "靠": "kao",
    "科": "ke",
    "可": "ke",
    "课": "ke",
    "克": "ke",
    "客": "ke",
    "空": "kong",
    "孔": "kong",
    "恐": "kong",
    "口": "kou",
    "扣": "kou",
    "苦": "ku",
    "库": "ku",
    "酷": "ku",
    "夸": "kua",
    "跨": "kua",
    "块": "kuai",
    "快": "kuai",
    "宽": "kuan",
    "款": "kuan",
    "狂": "kuang",
    "况": "kuang",
    "矿": "kuang",
    "亏": "kui",
    "愧": "kui",
    "昆": "kun",
    "困": "kun",
    "拉": "la",
    "腊": "la",
    "辣": "la",
    "来": "lai",
    "赖": "lai",
    "蓝": "lan",
    "兰": "lan",
    "拦": "lan",
    "篮": "lan",
    "懒": "lan",
    "烂": "lan",
    "浪": "lang",
    "郎": "lang",
    "朗": "lang",
    "老": "lao",
    "姥": "lao",
    "乐": "le",
    "勒": "le",
    "雷": "lei",
    "泪": "lei",
    "类": "lei",
    "累": "lei",
    "冷": "leng",
    "里": "li",
    "力": "li",
    "立": "li",
    "利": "li",
    "李": "li",
    "理": "li",
    "连": "lian",
    "联": "lian",
    "练": "lian",
    "恋": "lian",
    "良": "liang",
    "凉": "liang",
    "两": "liang",
    "量": "liang",
    "亮": "liang",
    "了": "le",
    "辽": "liao",
    "疗": "liao",
    "了": "liao",
    "料": "liao",
    "列": "lie",
    "烈": "lie",
    "裂": "lie",
    "林": "lin",
    "临": "lin",
    "邻": "lin",
    "磷": "lin",
    "灵": "ling",
    "岭": "ling",
    "另": "ling",
    "令": "ling",
    "留": "liu",
    "流": "liu",
    "刘": "liu",
    "六": "liu",
    "龙": "long",
    "隆": "long",
    "笼": "long",
    "弄": "long",
    "楼": "lou",
    "漏": "lou",
    "露": "lou",
    "路": "lu",
    "陆": "lu",
    "录": "lu",
    "鹿": "lu",
    "绿": "lv",
    "旅": "lv",
    "律": "lv",
    "虑": "lv",
    "率": "lv",
    "马": "ma",
    "吗": "ma",
    "麻": "ma",
    "妈": "ma",
    "马": "ma",
    "码": "ma",
    "骂": "ma",
    "吗": "ma",
    "吗": "ma",
    "买": "mai",
    "卖": "mai",
    "麦": "mai",
    "满": "man",
    "慢": "man",
    "忙": "mang",
    "盲": "mang",
    "毛": "mao",
    "猫": "mao",
    "冒": "mao",
    "贸": "mao",
    "么": "me",
    "没": "mei",
    "每": "mei",
    "美": "mei",
    "妹": "mei",
    "门": "men",
    "们": "men",
    "盟": "meng",
    "猛": "meng",
    "蒙": "meng",
    "梦": "meng",
    "米": "mi",
    "迷": "mi",
    "蜜": "mi",
    "密": "mi",
    "面": "mian",
    "免": "mian",
    "秒": "miao",
    "妙": "miao",
    "民": "min",
    "敏": "min",
    "名": "ming",
    "明": "ming",
    "鸣": "ming",
    "命": "ming",
    "摸": "mo",
    "末": "mo",
    "莫": "mo",
    "墨": "mo",
    "默": "mo",
    "母": "mu",
    "目": "mu",
    "墓": "mu",
    "幕": "mu",
    "慕": "mu",
    "木": "mu",
    "目": "mu",
    "那": "na",
    "拿": "na",
    "哪": "na",
    "纳": "na",
    "娜": "na",
    "那": "na",
    "南": "nan",
    "男": "nan",
    "难": "nan",
    "囊": "nang",
    "脑": "nao",
    "闹": "nao",
    "呢": "ne",
    "内": "nei",
    "能": "neng",
    "你": "ni",
    "尼": "ni",
    "泥": "ni",
    "拟": "ni",
    "逆": "ni",
    "年": "nian",
    "念": "nian",
    "娘": "niang",
    "鸟": "niao",
    "您": "nin",
    "牛": "niu",
    "农": "nong",
    "弄": "nong",
    "努": "nu",
    "怒": "nu",
    "女": "nv",
    "暖": "nuan",
    "挪": "nuo",
    "诺": "nuo",
    "欧": "ou",
    "怕": "pa",
    "爬": "pa",
    "帕": "pa",
    "派": "pai",
    "潘": "pan",
    "盘": "pan",
    "判": "pan",
    "叛": "pan",
    "旁": "pang",
    "胖": "pang",
    "跑": "pao",
    "炮": "pao",
    "泡": "pao",
    "培": "pei",
    "陪": "pei",
    "配": "pei",
    "盆": "pen",
    "朋": "peng",
    "碰": "peng",
    "批": "pi",
    "皮": "pi",
    "疲": "pi",
    "匹": "pi",
    "痞": "pi",
    "片": "pian",
    "偏": "pian",
    "骗": "pian",
    "票": "piao",
    "漂": "piao",
    "贫": "pin",
    "品": "pin",
    "平": "ping",
    "评": "ping",
    "屏": "ping",
    "乒": "ping",
    "迫": "po",
    "破": "po",
    "魄": "po",
    "剖": "pou",
    "扑": "pu",
    "葡": "pu",
    "普": "pu",
    "浦": "pu",
    "七": "qi",
    "期": "qi",
    "其": "qi",
    "奇": "qi",
    "骑": "qi",
    "起": "qi",
    "企": "qi",
    "气": "qi",
    "汽": "qi",
    "器": "qi",
    "弃": "qi",
    "砌": "qi",
    "掐": "qia",
    "恰": "qia",
    "千": "qian",
    "签": "qian",
    "前": "qian",
    "钱": "qian",
    "潜": "qian",
    "浅": "qian",
    "枪": "qiang",
    "墙": "qiang",
    "强": "qiang",
    "抢": "qiang",
    "桥": "qiao",
    "敲": "qiao",
    "悄": "qiao",
    "巧": "qiao",
    "撬": "qiao",
    "且": "qie",
    "切": "qie",
    "茄": "qie",
    "亲": "qin",
    "琴": "qin",
    "勤": "qin",
    "青": "qing",
    "轻": "qing",
    "清": "qing",
    "情": "qing",
    "请": "qing",
    "庆": "qing",
    "穷": "qiong",
    "秋": "qiu",
    "求": "qiu",
    "球": "qiu",
    "区": "qu",
    "曲": "qu",
    "取": "qu",
    "去": "qu",
    "趣": "qu",
    "全": "quan",
    "权": "quan",
    "泉": "quan",
    "圈": "quan",
    "劝": "quan",
    "券": "quan",
    "确": "que",
    "却": "que",
    "雀": "que",
    "群": "qun",
    "然": "ran",
    "燃": "ran",
    "染": "ran",
    "让": "rang",
    "饶": "rao",
    "扰": "rao",
    "热": "re",
    "人": "ren",
    "认": "ren",
    "任": "ren",
    "仁": "ren",
    "日": "ri",
    "如": "ru",
    "入": "ru",
    "软": "ruan",
    "锐": "rui",
    "瑞": "rui",
    "润": "run",
    "若": "ruo",
    "弱": "ruo",
    "撒": "sa",
    "洒": "sa",
    "萨": "sa",
    "赛": "sai",
    "三": "san",
    "散": "san",
    "桑": "sang",
    "嗓": "sang",
    "扫": "sao",
    "色": "se",
    "涩": "se",
    "森": "sen",
    "僧": "seng",
    "沙": "sha",
    "啥": "sha",
    "傻": "sha",
    "晒": "shai",
    "山": "shan",
    "删": "shan",
    "扇": "shan",
    "闪": "shan",
    "善": "shan",
    "伤": "shang",
    "商": "shang",
    "赏": "shang",
    "上": "shang",
    "尚": "shang",
    "捎": "shao",
    "烧": "shao",
    "少": "shao",
    "绍": "shao",
    "奢": "she",
    "蛇": "she",
    "舌": "she",
    "舍": "she",
    "射": "she",
    "社": "she",
    "设": "she",
    "涉": "she",
    "谁": "shui",
    "申": "shen",
    "身": "shen",
    "深": "shen",
    "什": "shen",
    "神": "shen",
    "审": "shen",
    "肾": "shen",
    "生": "sheng",
    "声": "sheng",
    "升": "sheng",
    "胜": "sheng",
    "盛": "sheng",
    "剩": "sheng",
    "失": "shi",
    "师": "shi",
    "十": "shi",
    "时": "shi",
    "食": "shi",
    "实": "shi",
    "识": "shi",
    "史": "shi",
    "使": "shi",
    "始": "shi",
    "市": "shi",
    "式": "shi",
    "事": "shi",
    "势": "shi",
    "试": "shi",
    "视": "shi",
    "是": "shi",
    "适": "shi",
    "室": "shi",
    "收": "shou",
    "手": "shou",
    "守": "shou",
    "首": "shou",
    "受": "shou",
    "授": "shou",
    "书": "shu",
    "术": "shu",
    "树": "shu",
    "数": "shu",
    "属": "shu",
    "鼠": "shu",
    "署": "shu",
    "蜀": "shu",
    "束": "shu",
    "竖": "shu",
    "恕": "shu",
    "刷": "shua",
    "耍": "shua",
    "摔": "shuai",
    "帅": "shuai",
    "率": "shuai",
    "双": "shuang",
    "爽": "shuang",
    "谁": "shui",
    "水": "shui",
    "税": "shui",
    "睡": "shui",
    "顺": "shun",
    "说": "shuo",
    "硕": "shuo",
    "朔": "shuo",
    "思": "si",
    "私": "si",
    "司": "si",
    "四": "si",
    "死": "si",
    "似": "si",
    "寺": "si",
    "饲": "si",
    "松": "song",
    "送": "song",
    "宋": "song",
    "搜": "sou",
    "苏": "su",
    "诉": "su",
    "速": "su",
    "素": "su",
    "塑": "su",
    "酸": "suan",
    "算": "suan",
    "虽": "sui",
    "随": "sui",
    "岁": "sui",
    "碎": "sui",
    "孙": "sun",
    "损": "sun",
    "笋": "sun",
    "缩": "suo",
    "所": "suo",
    "索": "suo",
    "琐": "suo",
    "锁": "suo",
    "他": "ta",
    "她": "ta",
    "它": "ta",
    "塔": "ta",
    "踏": "ta",
    "太": "tai",
    "态": "tai",
    "抬": "tai",
    "谈": "tan",
    "弹": "tan",
    "坦": "tan",
    "探": "tan",
    "叹": "tan",
    "炭": "tan",
    "汤": "tang",
    "糖": "tang",
    "堂": "tang",
    "唐": "tang",
    "逃": "tao",
    "桃": "tao",
    "淘": "tao",
    "套": "tao",
    "特": "te",
    "疼": "teng",
    "腾": "teng",
    "体": "ti",
    "提": "ti",
    "题": "ti",
    "踢": "ti",
    "替": "ti",
    "天": "tian",
    "田": "tian",
    "甜": "tian",
    "填": "tian",
    "挑": "tiao",
    "条": "tiao",
    "跳": "tiao",
    "铁": "tie",
    "贴": "tie",
    "听": "ting",
    "停": "ting",
    "庭": "ting",
    "挺": "ting",
    "通": "tong",
    "同": "tong",
    "铜": "tong",
    "统": "tong",
    "痛": "tong",
    "头": "tou",
    "投": "tou",
    "透": "tou",
    "突": "tu",
    "图": "tu",
    "途": "tu",
    "土": "tu",
    "吐": "tu",
    "兔": "tu",
    "团": "tuan",
    "推": "tui",
    "退": "tui",
    "吞": "tun",
    "托": "tuo",
    "拖": "tuo",
    "脱": "tuo",
    "驼": "tuo",
    "妥": "tuo",
    "挖": "wa",
    "瓦": "wa",
    "娃": "wa",
    "蛙": "wa",
    "哇": "wa",
    "外": "wai",
    "弯": "wan",
    "湾": "wan",
    "完": "wan",
    "玩": "wan",
    "晚": "wan",
    "万": "wan",
    "腕": "wan",
    "王": "wang",
    "往": "wang",
    "忘": "wang",
    "望": "wang",
    "为": "wei",
    "围": "wei",
    "伟": "wei",
    "卫": "wei",
    "未": "wei",
    "位": "wei",
    "味": "wei",
    "畏": "wei",
    "胃": "wei",
    "喂": "wei",
    "温": "wen",
    "文": "wen",
    "闻": "wen",
    "问": "wen",
    "翁": "weng",
    "我": "wo",
    "握": "wo",
    "卧": "wo",
    "沃": "wo",
    "巫": "wu",
    "无": "wu",
    "五": "wu",
    "午": "wu",
    "舞": "wu",
    "务": "wu",
    "物": "wu",
    "误": "wu",
    "西": "xi",
    "息": "xi",
    "希": "xi",
    "吸": "xi",
    "戏": "xi",
    "系": "xi",
    "细": "xi",
    "虾": "xia",
    "瞎": "xia",
    "峡": "xia",
    "下": "xia",
    "夏": "xia",
    "吓": "xia",
    "先": "xian",
    "仙": "xian",
    "鲜": "xian",
    "闲": "xian",
    "显": "xian",
    "险": "xian",
    "县": "xian",
    "现": "xian",
    "线": "xian",
    "限": "xian",
    "香": "xiang",
    "相": "xiang",
    "想": "xiang",
    "响": "xiang",
    "向": "xiang",
    "象": "xiang",
    "像": "xiang",
    "消": "xiao",
    "小": "xiao",
    "校": "xiao",
    "笑": "xiao",
    "效": "xiao",
    "孝": "xiao",
    "些": "xie",
    "写": "xie",
    "血": "xie",
    "鞋": "xie",
    "协": "xie",
    "斜": "xie",
    "胁": "xie",
    "谢": "xie",
    "心": "xin",
    "辛": "xin",
    "新": "xin",
    "信": "xin",
    "星": "xing",
    "兴": "xing",
    "行": "xing",
    "醒": "xing",
    "性": "xing",
    "姓": "xing",
    "凶": "xiong",
    "胸": "xiong",
    "雄": "xiong",
    "熊": "xiong",
    "修": "xiu",
    "休": "xiu",
    "秀": "xiu",
    "羞": "xiu",
    "须": "xu",
    "需": "xu",
    "徐": "xu",
    "许": "xu",
    "续": "xu",
    "宣传": "xuan",
    "选": "xuan",
    "旋": "xuan",
    "雪": "xue",
    "血": "xue",
    "寻": "xun",
    "讯": "xun",
    "训": "xun",
    "迅": "xun",
    "压": "ya",
    "牙": "ya",
    "呀": "ya",
    "哑": "ya",
    "雅": "ya",
    "亚": "ya",
    "烟": "yan",
    "淹": "yan",
    "严": "yan",
    "研": "yan",
    "盐": "yan",
    "眼": "yan",
    "演": "yan",
    "艳": "yan",
    "验": "yan",
    "央": "yang",
    "阳": "yang",
    "扬": "yang",
    "羊": "yang",
    "洋": "yang",
    "要": "yao",
    "腰": "yao",
    "摇": "yao",
    "遥": "yao",
    "咬": "yao",
    "药": "yao",
    "也": "ye",
    "业": "ye",
    "夜": "ye",
    "叶": "ye",
    "页": "ye",
    "一": "yi",
    "衣": "yi",
    "医": "yi",
    "依": "yi",
    "仪": "yi",
    "宜": "yi",
    "已": "yi",
    "以": "yi",
    "义": "yi",
    "艺": "yi",
    "易": "yi",
    "意": "yi",
    "益": "yi",
    "亿": "yi",
    "忆": "yin",
    "因": "yin",
    "银": "yin",
    "引": "yin",
    "印": "yin",
    "应": "ying",
    "英": "ying",
    "影": "ying",
    "映": "ying",
    "硬": "ying",
    "育": "yu",
    "元": "yuan",
    "园": "yuan",
    "圆": "yuan",
    "远": "yuan",
    "愿": "yuan",
    "约": "yue",
    "月": "yue",
    "乐": "yue",
    "阅": "yue",
    "云": "yun",
    "运": "yun",
    "孕": "yun",
    "韵": "yun",
    "杂": "za",
    "咱": "zan",
    "暂": "zan",
    "赞": "zan",
    "脏": "zang",
    "葬": "zang",
    "遭": "zao",
    "早": "zao",
    "枣": "zao",
    "噪": "zao",
    "造": "zao",
    "则": "ze",
    "责": "ze",
    "贼": "zei",
    "怎": "zen",
    "增": "zeng",
    "扎": "zha",
    "闸": "zha",
    "炸": "zha",
    "摘": "zhai",
    "宅": "zhai",
    "窄": "zhai",
    "债": "zhai",
    "沾": "zhan",
    "展": "zhan",
    "占": "zhan",
    "战": "zhan",
    "站": "zhan",
    "张": "zhang",
    "章": "zhang",
    "长": "zhang",
    "掌": "zhang",
    "涨": "zhang",
    "丈": "zhang",
    "杖": "zhang",
    "账": "zhang",
    "找": "zhao",
    "照": "zhao",
    "罩": "zhao",
    "兆": "zhao",
    "赵": "zhao",
    "照": "zhao",
    "折": "zhe",
    "者": "zhe",
    "这": "zhe",
    "着": "zhao",
    "真": "zhen",
    "镇": "zhen",
    "震": "zhen",
    "争": "zheng",
    "正": "zheng",
    "政": "zheng",
    "证": "zheng",
    "支": "zhi",
    "知": "zhi",
    "只": "zhi",
    "直": "zhi",
    "职": "zhi",
    "植": "zhi",
    "值": "zhi",
    "止": "zhi",
    "至": "zhi",
    "制": "zhi",
    "治": "zhi",
    "中": "zhong",
    "重": "zhong",
    "众": "zhong",
    "种": "zhong",
    "肿": "zhong",
    "州": "zhou",
    "周": "zhou",
    "洲": "zhou",
    "粥": "zhou",
    "轴": "zhou",
    "宙": "zhou",
    "皱": "zhou",
    "竹": "zhu",
    "主": "zhu",
    "住": "zhu",
    "注": "zhu",
    "助": "zhu",
    "著": "zhu",
    "柱": "zhu",
    "祝": "zhu",
    "筑": "zhu",
    "抓": "zhua",
    "专": "zhuan",
    "转": "zhuan",
    "赚": "zhuan",
    "撰": "zhuan",
    "庄": "zhuang",
    "装": "zhuang",
    "壮": "zhuang",
    "撞": "zhuang",
    "追": "zhui",
    "坠": "zhui",
    "准": "zhun",
    "桌": "zhuo",
    "卓": "zhuo",
    "捉": "zhuo",
    "灼": "zhuo",
    "资": "zi",
    "子": "zi",
    "自": "zi",
    "字": "zi",
    "紫": "zi",
    "宗": "zong",
    "总": "zong",
    "纵": "zong",
    "走": "zou",
    "奏": "zou",
    "租": "zu",
    "足": "zu",
    "族": "zu",
    "阻": "zu",
    "组": "zu",
    "祖": "zu",
    "钻": "zuan",
    "嘴": "zui",
    "最": "zui",
    "罪": "zui",
    "尊": "zun",
    "遵": "zun",
    "昨": "zuo",
    "左": "zuo",
    "作": "zuo",
    "坐": "zuo",
    "座": "zuo",
    "做": "zuo",
}


def to_pinyin(text: str) -> str:
    if not text:
        return ""
    result = []
    for char in text:
        if char in PINYIN_MAP:
            result.append(PINYIN_MAP[char])
        elif char.isalpha() or char.isdigit():
            result.append(char.lower())
    return "".join(result)


def to_pinyin_initials(text: str) -> str:
    pinyin = to_pinyin(text)
    if not pinyin:
        return ""
    return pinyin[0]


class Library:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tracks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE NOT NULL,
                title TEXT,
                artist TEXT,
                album TEXT,
                duration REAL DEFAULT 0.0,
                genre TEXT,
                year INTEGER,
                track_number INTEGER
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                track_id INTEGER PRIMARY KEY,
                FOREIGN KEY (track_id) REFERENCES tracks(id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS blacklist (
                track_id INTEGER PRIMARY KEY,
                FOREIGN KEY (track_id) REFERENCES tracks(id)
            )
        """)
        try:
            conn.execute("ALTER TABLE tracks ADD COLUMN cover TEXT DEFAULT ''")
        except sqlite3.OperationalError:
            pass
        conn.commit()
        conn.close()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        return conn

    def scan_local(self, path: str) -> list[Track]:
        music_extensions = {".mp3", ".flac", ".wav", ".ogg", ".m4a", ".wma"}
        tracks = []
        root = Path(path)

        if not root.exists():
            return tracks

        if root.is_file():
            if root.suffix.lower() in music_extensions:
                track = self._extract_metadata(root)
                self._save_track(track)
                tracks.append(track)
            return tracks

        for file_path in root.rglob("*"):
            if file_path.suffix.lower() in music_extensions:
                track = self._extract_metadata(file_path)
                self._save_track(track)
                tracks.append(track)

        return tracks

    def _extract_metadata(self, file_path: Path) -> Track:
        try:
            audio = MutagenFile(file_path)
            if audio is None:
                return Track(file_path=str(file_path), title=file_path.stem)

            tags = audio.tags or {}
            return Track(
                file_path=str(file_path),
                title=tags.get("title", [file_path.stem])[0]
                if tags
                else file_path.stem,
                artist=tags.get("artist", [""])[0] if tags else "",
                album=tags.get("album", [""])[0] if tags else "",
                duration=float(audio.info.length) if audio.info else 0.0,
                genre=tags.get("genre", [""])[0] if tags else "",
                year=int(tags.get("date", ["0"])[0][:4])
                if tags and tags.get("date")
                else None,
                track_number=int(tags.get("tracknumber", [0])[0]) if tags else None,
            )
        except Exception:
            return Track(file_path=str(file_path), title=file_path.stem)

    def _save_track(self, track: Track) -> None:
        conn = self._get_connection()
        cursor = conn.execute(
            """INSERT OR REPLACE INTO tracks 
               (file_path, title, artist, album, duration, genre, year, track_number, cover)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                track.file_path,
                track.title,
                track.artist,
                track.album,
                track.duration,
                track.genre,
                track.year,
                track.track_number,
                track.cover,
            ),
        )
        track.id = cursor.lastrowid
        conn.commit()
        conn.close()

    def _row_to_track(self, row: tuple) -> Track:
        return Track(
            id=row[0],
            file_path=row[1],
            title=row[2],
            artist=row[3],
            album=row[4],
            duration=row[5],
            genre=row[6],
            year=row[7],
            track_number=row[8],
            cover=row[9] if len(row) > 9 else "",
        )

    def get_all_tracks(self, offset: int = 0, limit: int = 100000) -> list[Track]:
        conn = self._get_connection()
        cursor = conn.execute(
            "SELECT id, file_path, title, artist, album, duration, genre, year, track_number, cover FROM tracks LIMIT ? OFFSET ?",
            (limit, offset),
        )
        tracks = [self._row_to_track(row) for row in cursor.fetchall()]
        conn.close()
        return tracks

    def get_total_count(self) -> int:
        conn = self._get_connection()
        cursor = conn.execute("SELECT COUNT(*) FROM tracks")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def search(self, query: str) -> list[Track]:
        conn = self._get_connection()
        pattern = f"%{query}%"

        cursor = conn.execute(
            """SELECT id, file_path, title, artist, album, duration, genre, year, track_number, cover
               FROM tracks 
               WHERE title LIKE ? OR artist LIKE ? OR album LIKE ?""",
            (pattern, pattern, pattern),
        )

        tracks = [self._row_to_track(row) for row in cursor.fetchall()]

        if not tracks:
            query_lower = query.lower()
            query_pinyin = to_pinyin(query)
            query_initials = to_pinyin_initials(query)

            all_tracks = self.get_all_tracks()
            for track in all_tracks:
                title_pinyin = to_pinyin(track.title).lower()
                artist_pinyin = to_pinyin(track.artist).lower()
                title_initials = to_pinyin_initials(track.title).lower()
                artist_initials = to_pinyin_initials(track.artist).lower()

                if (
                    query_lower in title_pinyin
                    or query_lower in artist_pinyin
                    or query_pinyin in title_pinyin
                    or query_pinyin in artist_pinyin
                    or query_initials in title_initials
                    or query_initials in artist_initials
                ):
                    if track not in tracks:
                        tracks.append(track)

        conn.close()
        return tracks

    def get_track_by_id(self, track_id: int) -> Optional[Track]:
        conn = self._get_connection()
        cursor = conn.execute(
            "SELECT id, file_path, title, artist, album, duration, genre, year, track_number, cover FROM tracks WHERE id = ?",
            (track_id,),
        )
        row = cursor.fetchone()
        conn.close()
        return self._row_to_track(row) if row else None

    def add_favorite(self, track_id: int) -> bool:
        conn = self._get_connection()
        try:
            conn.execute(
                "INSERT OR IGNORE INTO favorites (track_id) VALUES (?)", (track_id,)
            )
            conn.commit()
            result = True
        except Exception:
            result = False
        finally:
            conn.close()
        return result

    def remove_favorite(self, track_id: int) -> bool:
        conn = self._get_connection()
        try:
            conn.execute("DELETE FROM favorites WHERE track_id = ?", (track_id,))
            conn.commit()
            result = True
        except Exception:
            result = False
        finally:
            conn.close()
        return result

    def is_favorite(self, track_id: int) -> bool:
        conn = self._get_connection()
        cursor = conn.execute("SELECT 1 FROM favorites WHERE track_id = ?", (track_id,))
        result = cursor.fetchone() is not None
        conn.close()
        return result

    def get_favorites(self) -> list[Track]:
        conn = self._get_connection()
        cursor = conn.execute(
            """SELECT t.id, t.file_path, t.title, t.artist, t.album, t.duration, t.genre, t.year, t.track_number, t.cover
               FROM tracks t INNER JOIN favorites f ON t.id = f.track_id"""
        )
        tracks = [self._row_to_track(row) for row in cursor.fetchall()]
        conn.close()
        return tracks

    def add_to_blacklist(self, track_id: int) -> bool:
        conn = self._get_connection()
        try:
            conn.execute(
                "INSERT OR IGNORE INTO blacklist (track_id) VALUES (?)", (track_id,)
            )
            conn.commit()
            result = True
        except Exception:
            result = False
        finally:
            conn.close()
        return result

    def remove_from_blacklist(self, track_id: int) -> bool:
        conn = self._get_connection()
        try:
            conn.execute("DELETE FROM blacklist WHERE track_id = ?", (track_id,))
            conn.commit()
            result = True
        except Exception:
            result = False
        finally:
            conn.close()
        return result

    def is_blacklisted(self, track_id: int) -> bool:
        conn = self._get_connection()
        cursor = conn.execute("SELECT 1 FROM blacklist WHERE track_id = ?", (track_id,))
        result = cursor.fetchone() is not None
        conn.close()
        return result

    def get_tracks_excluding_blacklist(
        self, offset: int = 0, limit: int = 100000
    ) -> list[Track]:
        conn = self._get_connection()
        cursor = conn.execute(
            """SELECT id, file_path, title, artist, album, duration, genre, year, track_number, cover
               FROM tracks WHERE id NOT IN (SELECT track_id FROM blacklist) LIMIT ? OFFSET ?""",
            (limit, offset),
        )
        tracks = [self._row_to_track(row) for row in cursor.fetchall()]
        conn.close()
        return tracks

    def _parse_remote_content(self, content: str) -> list[Track]:
        """Parse remote content (JS or JSON format) to Track list"""
        if content.strip().startswith("["):
            return self._parse_json_format(content)
        return self._parse_js_format(content)

    def _parse_js_format(self, content: str) -> list[Track]:
        """Parse JS format: var list = [{name, artist, url, cover}, ...]"""
        tracks = []
        match = re.search(r"var\s+list\s*=\s*(\[.*?\]);", content, re.DOTALL)
        if not match:
            return tracks

        array_content = match.group(1)
        obj_matches = re.findall(r"\{([^}]+)\}", array_content)

        for obj in obj_matches:
            track = self._parse_js_object(obj)
            if track:
                tracks.append(track)

        return tracks

    def _parse_js_object(self, obj_str: str) -> Track | None:
        """Parse a single JS object"""
        try:
            name_match = re.search(r'name:\s*"([^"]+)"', obj_str)
            artist_match = re.search(r'artist:\s*"([^"]+)"', obj_str)
            url_match = re.search(r'url:\s*"([^"]+)"', obj_str)
            cover_match = re.search(r'cover:\s*"([^"]+)"', obj_str)

            if not name_match or not url_match:
                return None

            return Track(
                title=name_match.group(1),
                artist=artist_match.group(1) if artist_match else "",
                file_path=url_match.group(1),
                cover=cover_match.group(1) if cover_match else "",
            )
        except Exception:
            return None

    def _parse_json_format(self, content: str) -> list[Track]:
        """Parse JSON format"""
        tracks = []
        try:
            data = json.loads(content)
            if not isinstance(data, list):
                return tracks

            for item in data:
                if not isinstance(item, dict):
                    continue
                if not item.get("name") or not item.get("url"):
                    continue

                tracks.append(
                    Track(
                        title=item.get("name", ""),
                        artist=item.get("artist", ""),
                        file_path=item.get("url", ""),
                        cover=item.get("cover", ""),
                    )
                )
        except json.JSONDecodeError:
            pass

        return tracks

    def fetch_remote_list(self, url: str) -> list[Track]:
        """Fetch and parse song list from remote URL"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            content = response.text
            return self._parse_remote_content(content)
        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch: {str(e)}")

    def save_remote_tracks(self, tracks: list[Track]) -> int:
        """Save remote tracks to database, return count"""
        count = 0
        for track in tracks:
            self._save_track(track)
            count += 1
        return count
