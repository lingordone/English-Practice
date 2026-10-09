import asyncio
import json
import os
import subprocess
import random

# === DATA ===
words_data = [
    ("passenger", "/ˈpæsɪndʒər/", "乘客，旅客"),
    ("conductor", "/kənˈdʌktər/", "售票员，列车长"),
    ("driver", "/ˈdraɪvər/", "驾驶员，司机"),
    ("inspector", "/ɪnˈspektər/", "检查员"),
    ("staff", "/stæf/", "工作人员"),
    ("guard", "/ɡɑːrd/", "守卫，看守"),
    ("tourist", "/ˈtʊrɪst/", "游客，观光者"),
    ("officer", "/ˈɔːfɪsər/", "官员，干事"),
    ("operator", "/ˈɑːpəreɪtər/", "操作员，接线员"),
    ("personnel", "/ˌpɜːrsəˈnel/", "全体人员，职员"),
    ("guide", "/ɡaɪd/", "导游，向导"),
    ("agent", "/ˈeɪdʒənt/", "代理人，代理商"),
    ("manager", "/ˈmænɪdʒər/", "经理，管理人"),
    ("cashier", "/kæˈʃɪr/", "出纳，收银员"),
    ("clerk", "/klɜːrk/", "办事员，职员"),
    ("porter", "/ˈpɔːrtər/", "搬运工，门卫"),
    ("messenger", "/ˈmesɪndʒər/", "信使，送信者"),
    ("customer", "/ˈkʌstəmər/", "顾客，客户"),
    ("mechanic", "/məˈkænɪk/", "机械师，技工"),
    ("engineer", "/ˌendʒɪˈnɪr/", "工程师，技师"),
]

# === PHRASES ===
phrases = {
    "passenger": [
        ("passenger train", "The passenger train arrives at 8 AM. （客运列车早上8点到达。）"),
        ("passenger seat", "The passenger seat is empty. （乘客座位是空的。）"),
    ],
    "conductor": [
        ("train conductor", "The conductor checks our tickets. （列车长检查我们的票。）"),
        ("bus conductor", "The bus conductor sells tickets on the bus. （公共汽车售票员在车上卖票。）"),
    ],
    "driver": [
        ("train driver", "The train driver starts the engine. （列车司机启动引擎。）"),
        ("driver's seat", "The driver's seat is at the front. （驾驶座在前面。）"),
    ],
    "inspector": [
        ("ticket inspector", "The ticket inspector checks every passenger. （检票员检查每位乘客。）"),
        ("health inspector", "The health inspector visits the station restaurant. （卫生检查员视察车站餐厅。）"),
    ],
    "staff": [
        ("station staff", "The station staff wear uniforms. （车站工作人员穿制服。）"),
        ("staff room", "The staff room is on the second floor. （员工休息室在二楼。）"),
    ],
    "guard": [
        ("security guard", "The security guard watches the entrance. （保安看守入口。）"),
        ("guard dog", "The guard dog patrols the station. （警犬在车站巡逻。）"),
    ],
    "tourist": [
        ("tourist information", "Tourist information is available at the counter. （咨询台提供旅游信息。）"),
        ("tourist season", "The tourist season makes the station busier. （旅游季节让车站更繁忙。）"),
    ],
    "officer": [
        ("police officer", "A police officer helps lost tourists. （警察帮助迷路的游客。）"),
        ("station officer", "The station officer manages daily operations. （车站官员管理日常运营。）"),
    ],
    "operator": [
        ("machine operator", "The machine operator controls the escalator. （机器操作员控制自动扶梯。）"),
        ("telephone operator", "The telephone operator connects your call. （接线员为你转接电话。）"),
    ],
    "personnel": [
        ("all personnel", "All personnel must wear ID badges. （所有人员必须佩戴工牌。）"),
        ("medical personnel", "Medical personnel are available during emergencies. （紧急情况下有医护人员待命。）"),
    ],
    "guide": [
        ("tour guide", "The tour guide explains the route. （导游讲解路线。）"),
        ("guide map", "Take a guide map from the information desk. （从咨询台拿一张导览图。）"),
    ],
    "agent": [
        ("travel agent", "The train agent sells tickets at the counter. （售票代理在柜台卖票。）"),
        ("agent's office", "The agent's office is near the ticket counter. （代理办公室在售票柜台附近。）"),
    ],
    "manager": [
        ("station manager", "The station manager oversees all operations. （车站经理监督所有运营。）"),
        ("duty manager", "The duty manager is available 24 hours a day. （值班经理24小时待命。）"),
    ],
    "cashier": [
        ("ticket cashier", "The ticket cashier gives you change. （售票收银员给你找零。）"),
        ("cashier's window", "The cashier's window is next to the gate. （收银窗口在闸机旁边。）"),
    ],
    "clerk": [
        ("booking clerk", "The booking clerk sells tickets. （售票员卖票。）"),
        ("office clerk", "The office clerk handles paperwork. （办公室职员处理文书工作。）"),
    ],
    "porter": [
        ("station porter", "The station porter carries luggage. （车站搬运工搬运行李。）"),
        ("head porter", "The head porter manages the luggage room. （行李员主管管理行李房。）"),
    ],
    "messenger": [
        ("station messenger", "The station messenger delivers packages. （车站信使送包裹。）"),
        ("messenger bag", "The messenger carries a messenger bag. （信使背着挎包。）"),
    ],
    "customer": [
        ("customer service", "Customer service is at the information counter. （客户服务在咨询台。）"),
        ("customer satisfaction", "The station values customer satisfaction. （车站重视客户满意度。）"),
    ],
    "mechanic": [
        ("train mechanic", "The train mechanic repairs the engine. （列车机械师修理引擎。）"),
        ("garage mechanic", "The garage mechanic fixes the bus. （修车厂技工修理公交车。）"),
    ],
    "engineer": [
        ("chief engineer", "The chief engineer designs the new platform. （总工程师设计新站台。）"),
        ("software engineer", "The software engineer updates the ticket system. （软件工程师更新票务系统。）"),
    ],
}

# === DIALOGUE ===
dialogue_lines = [
    ("Staff Member", "Welcome to Central Station. How can I help you today?"),
    ("Passenger", "Hi, I'm a tourist here. Could you guide me to the right platform?"),
    ("Staff Member", "Of course! The agent at the counter can sell you a ticket. The cashier will give you change."),
    ("Passenger", "Great! Is there a porter who can carry my luggage?"),
    ("Staff Member", "Yes, the station porter is near the entrance. The head porter will help you."),
    ("Passenger", "Wonderful. Who do I ask about train times?"),
    ("Staff Member", "The booking clerk at the ticket office has the schedule. The conductor on the platform can also help."),
    ("Passenger", "Is there a customer service desk?"),
    ("Staff Member", "Yes, the customer service clerk is next to the information counter."),
    ("Passenger", "What about the driver? Can I speak to the train driver?"),
    ("Staff Member", "No, the driver stays in the cabin. But the inspector checks tickets on the train."),
    ("Passenger", "I see. Who manages the station?"),
    ("Staff Member", "The station manager oversees all personnel. The duty manager is here 24 hours a day."),
    ("Passenger", "Are there security guards?"),
    ("Staff Member", "Yes, the security guard patrols the area. The guard dog helps at night."),
    ("Passenger", "What about the mechanic? My friend is an engineer."),
    ("Staff Member", "The train mechanic works in the garage. The chief engineer is designing the new line."),
    ("Passenger", "Is there a telephone operator?"),
    ("Staff Member", "The operator connects calls at the office. The machine operator controls the escalator."),
    ("Passenger", "Thank you! The staff here are very helpful."),
    ("Staff Member", "You're welcome! Enjoy your trip."),
]

# === GRAMMAR ===
grammar_title = "职业名词后缀 -er/-or/-ist/-ant"
grammar_content = """
### 规则说明

英语中表示"人"的名词常由动词/名词加后缀构成：

| 后缀 | 含义 | 示例 |
|------|------|------|
| **-er** | 做某事的人 | driver（司机），passenger（乘客），manager（经理） |
| **-or** | 做某事的人 | conductor（售票员），inspector（检查员），operator（操作员） |
| **-ist** | 专业人员 | tourist（游客），mechanic（机械师） |
| **-ant** | 做某事的人 | agent（代理人），cashier（收银员） |

### √ 正确用法

- The **driver** drives the train. — 正确。（司机驾驶列车。）
- The **conductor** checks tickets. — 正确。（售票员检票。）
- The **inspector** inspects the train. — 正确。（检查员检查列车。）

### × 错误用法

- The **driver** drive the train. — 错误。（第三人称单数动词需加-s。）
- The **conductor** check tickets. — 错误。（第三人称单数动词需加-s。）
"""

# === QUIZZES ===
quizzes = [
    ("The ___ checks tickets on the train.", "conductor", "售票员", ["driver", "guard", "porter"]),
    ("The train ___ drives the train every day.", "driver", "司机", ["conductor", "inspector", "clerk"]),
    ("The security ___ watches the entrance.", "guard", "守卫", ["guide", "agent", "porter"]),
    ("The station ___ manages all operations.", "manager", "经理", ["clerk", "cashier", "officer"]),
    ("The ___ carries luggage for passengers.", "porter", "搬运工", ["driver", "guard", "guide"]),
]

# === GENERATE MARKDOWN ===
def generate_markdown():
    lines = []
    lines.append("# Day 3 · 地铁站 Subway Station · 单元 C · Who — 地铁站有谁？")
    lines.append("")
    lines.append("> **Part:** 交通")
    lines.append("> **PDF Pages:** 59-68")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 今日词汇 (20 词)")
    lines.append("")
    lines.append("| 单词 | 音标 | 中文 |")
    lines.append("|------|------|------|")
    for word, ipa, meaning in words_data:
        lines.append(f"| {word} | [{ipa}] | {meaning} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🎧 单词音频")
    lines.append("")
    for word, ipa, meaning in words_data:
        lines.append(f"- **{word}** [{ipa}] — {meaning}")
        lines.append(f'  <audio controls preload="none" style="width:100%;max-width:300px;height:32px;"><source src="../audio/{word}.mp3" type="audio/mpeg"></audio>')
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 短语延伸")
    lines.append("")
    for word in [w for w, _, _ in words_data]:
        if word in phrases:
            lines.append(f"### {word}")
            lines.append("")
            for phrase, sentence in phrases[word]:
                lines.append(f"- **{phrase}**: {sentence}")
                safe_phrase = phrase.replace(" ", "_").replace("'", "")
                lines.append(f'  <audio controls preload="none" style="width:100%;max-width:300px;height:32px;"><source src="../audio/{word}_{safe_phrase}.mp3" type="audio/mpeg"></audio>')
                lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 语境对话")
    lines.append("")
    lines.append("**场景**: 地铁站内 — 乘客与车站工作人员交流")
    lines.append("")
    lines.append('<audio controls preload="none" style="width:100%;max-width:400px;height:32px;"><source src="../audio/dialogue_subway_station_C.mp3" type="audio/mpeg"></audio>')
    lines.append("")
    for role, text in dialogue_lines:
        lines.append(f"**{role}:** {text}")
        lines.append(f"（{get_chinese_translation(text)}）")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 语法点")
    lines.append("")
    lines.append(f"### {grammar_title}")
    lines.append("")
    lines.append(grammar_content.strip())
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 填空练习")
    lines.append("")
    for i, (sentence, answer, meaning, options) in enumerate(quizzes, 1):
        all_options = [answer] + options
        # Shuffle but keep track
        import random
        random.seed(42 + i)
        shuffled = all_options[:]
        random.shuffle(shuffled)
        labels = ["A", "B", "C", "D"]
        lines.append(f'{i}. "{sentence}"')
        for j, opt in enumerate(shuffled):
            lines.append(f"   {labels[j]}. {opt}")
        answer_label = labels[shuffled.index(answer)]
        lines.append(f"   → 答案：{answer_label} （{answer} — {meaning}）")
        lines.append("")
    return "\n".join(lines)

def get_chinese_translation(text):
    translations = {
        "Welcome to Central Station. How can I help you today?": "欢迎来到中央车站。今天我能帮您什么？",
        "Hi, I'm a tourist here. Could you guide me to the right platform?": "你好，我是这里的游客。你能引导我去正确的站台吗？",
        "Of course! The agent at the counter can sell you a ticket. The cashier will give you change.": "当然！柜台的代理人可以卖给你票。收银员会给你找零。",
        "Great! Is there a porter who can carry my luggage?": "太好了！有搬运工能帮我搬行李吗？",
        "Yes, the station porter is near the entrance. The head porter will help you.": "有，车站搬运工在入口附近。行李员主管会帮你。",
        "Wonderful. Who do I ask about train times?": "太好了。我该问谁关于火车时间？",
        "The booking clerk at the ticket office has the schedule. The conductor on the platform can also help.": "售票处的售票员有时刻表。站台上的售票员也能帮忙。",
        "Is there a customer service desk?": "有客户服务台吗？",
        "Yes, the customer service clerk is next to the information counter.": "有，客户服务职员在咨询台旁边。",
        "What about the driver? Can I speak to the train driver?": "司机呢？我能和列车司机说话吗？",
        "No, the driver stays in the cabin. But the inspector checks tickets on the train.": "不能，司机待在车厢里。但检票员在列车上检票。",
        "I see. Who manages the station?": "我明白了。谁管理车站？",
        "The station manager oversees all personnel. The duty manager is here 24 hours a day.": "车站经理监督所有人员。值班经理24小时在这里。",
        "Are there security guards?": "有保安吗？",
        "Yes, the security guard patrols the area. The guard dog helps at night.": "有，保安巡逻区域。警犬在晚上帮忙。",
        "What about the mechanic? My friend is an engineer.": "机械师呢？我朋友是工程师。",
        "The train mechanic works in the garage. The chief engineer is designing the new line.": "列车机械师在车库工作。总工程师在设计新线路。",
        "Is there a telephone operator?": "有电话接线员吗？",
        "The operator connects calls at the office. The machine operator controls the escalator.": "接线员在办公室转接电话。机器操作员控制自动扶梯。",
        "Thank you! The staff here are very helpful.": "谢谢！这里的工作人员都很乐于助人。",
        "You're welcome! Enjoy your trip.": "不客气！祝你旅途愉快！",
    }
    return translations.get(text, "")

# === TTS GENERATION ===
async def generate_tts():
    import edge_tts
    
    voice = "en-US-JennyNeural"
    audio_dir = "C:/Users/admin/Documents/Obsidian Vault/audio"
    os.makedirs(audio_dir, exist_ok=True)
    
    tts_tasks = []
    
    # Word audio
    for word, _, _ in words_data:
        tts_tasks.append((word, word))
    
    # Phrase audio (strip Chinese for TTS)
    for word, _, _ in words_data:
        if word in phrases:
            for phrase, sentence in phrases[word]:
                safe_phrase = phrase.replace(" ", "_").replace("'", "")
                # Extract English only (before Chinese parenthesis)
                english_only = sentence.split("（")[0].strip()
                tts_tasks.append((f"{word}_{safe_phrase}", english_only))
    
    # Dialogue audio
    dialogue_text = " ".join([text for _, text in dialogue_lines])
    tts_tasks.append(("dialogue_subway_station_C", dialogue_text))
    
    print(f"Generating {len(tts_tasks)} TTS files...")
    
    for filename, text in tts_tasks:
        ogg_path = os.path.join(audio_dir, f"{filename}.ogg")
        mp3_path = os.path.join(audio_dir, f"{filename}.mp3")
        
        # Skip if mp3 already exists
        if os.path.exists(mp3_path):
            print(f"  SKIP (exists): {filename}.mp3")
            continue
        
        try:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(ogg_path)
            
            # Convert to mp3
            subprocess.run(
                ["ffmpeg", "-y", "-i", ogg_path, "-acodec", "libmp3lame", "-q:a", "2", mp3_path],
                check=True,
                capture_output=True
            )
            
            # Remove ogg
            if os.path.exists(ogg_path):
                os.remove(ogg_path)
            
            print(f"  OK: {filename}.mp3")
        except Exception as e:
            print(f"  FAIL: {filename} - {e}")
    
    # Count files
    mp3_files = [f for f in os.listdir(audio_dir) if f.endswith('.mp3')]
    print(f"\nTotal mp3 files in audio/: {len(mp3_files)}")

# === MAIN ===
if __name__ == "__main__":
    # Generate markdown
    md_content = generate_markdown()
    
    # Write markdown
    md_path = "C:/Users/admin/Documents/Obsidian Vault/美国人都在用的英语/Day3-Subway-Station-C.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Written: {md_path}")
    
    # Generate TTS
    asyncio.run(generate_tts())
    
    # Update progress
    progress_path = "C:/Users/admin/Documents/Obsidian Vault/美国人都在用的英语/scene_lesson_progress.json"
    with open(progress_path, 'r', encoding='utf-8') as f:
        progress = json.load(f)
    
    progress["section"] = "C"
    progress["total_lessons"] = 3
    progress["last_lesson_date"] = "2026-10-09"
    progress["last_status"] = "completed"
    
    # Add to daily_log
    today = "2026-10-09"
    progress["daily_log"][today] = {
        "scene": "subway",
        "section": "C",
        "words": [w for w, _, _ in words_data],
        "audio_count": 61,
        "lesson_file": "Day3-Subway-Station-C.md"
    }
    
    with open(progress_path, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)
    print(f"Updated: {progress_path}")
    
    print("\nDone!")
