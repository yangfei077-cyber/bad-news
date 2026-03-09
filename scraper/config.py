import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", "")
if not DATABASE_URL:
    DATABASE_PATH = ROOT_DIR / "platform" / "prisma" / "dev.db"
    DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
FINE_TUNED_MODEL = os.getenv("FINE_TUNED_MODEL", "gpt-4o-mini")

SCRAPE_INTERVAL_MINUTES = 60

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

KEYWORDS_EN = [
    "gender violence", "femicide", "domestic violence",
    "sexual assault", "rape", "FGM", "female genital mutilation",
    "reproductive rights", "abortion ban", "forced marriage",
    "honor killing", "intimate partner violence", "sex trafficking",
    "sexual harassment", "misogyny", "gender discrimination",
    "maternal mortality", "child marriage", "dowry death",
    "women's rights", "gender-based violence", "marital rape",
    "period poverty", "menstrual taboo", "pay gap",
    "motherhood penalty", "workplace harassment",
]

KEYWORDS_ZH = [
    "家暴", "性侵", "强奸", "性别暴力", "性别歧视",
    "厌女", "堕胎", "生育权", "杀女婴", "女性割礼",
    "强迫婚姻", "拐卖妇女", "性骚扰", "彩礼", "家庭暴力",
    "女性权益", "产假", "职场歧视", "月经羞耻", "荡妇羞辱",
    "性别薪资差距", "母职惩罚", "女权", "代孕",
    "婚内强奸", "冥婚", "重男轻女",
]
