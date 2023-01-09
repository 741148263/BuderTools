import os

# 图书URL
SEARCH_BOOK_BASE_URL = "https://www.book123.info"
SEARCH_BOOK_URL = "https://www.book123.info/list?key={}"

# 盘api列表
HOST_LIST = [
    'https://api.upyunso2.com',
    'https://upapi.juapp9.com',
    'https://api.upyunso1.com'
]

# 项目根路径
ROOT_DIR = os.getcwd()

# 配置文件
CONFIG_DIR = os.path.join(ROOT_DIR, "setting/config.ini")

# 窗口常量
SOFTWARE_TITLE = "BuderTools"
SOFTWARE_VERSION = "2022.12.1"
SOFTWARE_WIDTH = 1200

DB_FILE = "database.db"

# 创建表语句
CREATE_BOOK_CASE_TABLE = """
CREATE TABLE "bookcase" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "book_name" varchar(150) NOT NULL,
    "book_auther" varchar(150) not null ,
    "book_new_chapter" varchar(200) not null ,
    "book_from" varchar(100) NOT NULL,
    "book_status" varchar(100),
    "book_href" varchar(500) NOT NULL,
    "read_chapter_index" integer,
    "has_chapter_status" integer,
    UNIQUE ("book_href" ASC)
);
"""
# 创建章节表语句
CREATE_BOOK_CHAPTER_TABLE = """
CREATE TABLE "book_chapter" (
"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
"chapter_name" varchar(250) NOT NULL,
"chapter_href" varchar(500) NOT NULL,
"bookcase_id" bigint NOT NULL,
"chapter_content" text,
FOREIGN KEY ("bookcase_id") REFERENCES "bookcase" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED
);
"""
# 插入书
INSERT_BOOK_CASE = 'insert into "bookcase" values ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'

# 查询当前书架的数量
SEARCH_BOOK_COUNT_SQL = "SELECT MAX(id) FROM bookcase"

# 查询书架所有书
SEARCH_BOOK_SQL = "select * from bookcase;"

# 查询没有章节信息的书
SEARCH_NO_CHAPTER_SQL = "select id, book_from, book_href from bookcase where has_chapter_status == 0"

# 插入章节表
INSERT_CHAPTER_SQL = "insert into book_chapter(chapter_name, chapter_href, bookcase_id) values "

# 更新书架表章节收集状态
UPDATE_CHAPTER_STATUS_SQL = "update bookcase set has_chapter_status = 1 where id = {};"

# 搜索表格表头常量
SEARCH_RESULT_TABLE_COLUMN = ["序号", "书名", "作者", "最新章节", "来源", "状态", "操作"]

# 图书搜索表头常量
SEARCH_BOOK_TABLE_COLUMN = ["序号", "书名", "作者", "评分", "下载状态", "操作"]

# 盘表头
NETWORK_DISK_TABLE_COLUMN = ["序号", "资源名", "资源来源", "有效期", "收录时间", "操作"]

# music请求头
MUSIC_SEARCH_TABLE_COLUMN = ["序号", "歌曲名称", "歌手", "分类", "音质"]

SEARCH_RULES = {
    "龙坛书网": {
        "sourceName": "龙坛书网",
        "searchUrl": "https://www.longtanshuw.net/modules/article/search.php?searchkey={}",
        "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "searchCharSet": "gbk",
        "chapterListCharSet": "gbk",
        "baseUrl": "https://www.longtanshuw.net",
        "searchXpath": {
            "titleRuleXpath": '//*[@id="nr"]/td[1]/a/text()',
            "hrefRuleXpath": '//*[@id="nr"]/td[1]/a/@href',
            "updateChapterXpath": '//*[@id="nr"]/td[2]/a/text()',
            "autherXpath": '//*[@id="nr"]/td[3]/text()',
            "statusXpath": '//*[@id="nr"]/td[6]/text()',
        },
        "chapterXpath": {
            "chapterTitleXpath": '//*[@id="list"]/dl/dd/a/text()',
            "chapterHrefXpath": '//*[@id="list"]/dl/dd/a/@href',
        },
        "chapterHrefJoin": False,
        "chapterStartIndex": 9,
        "chapterContentXpath": '//*[@id="content"]/text()',
        "chapterContentStopIndex": -2
    },
    "笔趣阁": {
        "sourceName": "笔趣阁",
        "searchUrl": "https://so.biqusoso.com/s1.php?ie=utf-8&siteid=qu-la.com&q={}",
        "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 "
                 "Safari/537.36",
        "searchCharSet": "utf-8",
        "chapterListCharSet": "gbk",
        "baseUrl": "http://www.qu-la.com",
        "searchXpath": {
            "titleRuleXpath": '//*[@id="search-main"]/div[1]/ul/li/span[2]/a/text()',
            "hrefRuleXpath": '//*[@id="search-main"]/div[1]/ul/li/span[2]/a/@href',
            "updateChapterXpath": None,
            "autherXpath": '//*[@id="search-main"]/div[1]/ul/li/span[3]/text()',
            "statusXpath": None,
        },
        "chapterXpath": {
            "chapterTitleXpath": '//*[@id="list"]/div[3]/ul[2]/li/a/text()',
            "chapterHrefXpath": '//*[@id="list"]/div[3]/ul[2]/li/a/@href',
        },
        "chapterHrefJoin": True,
        "chapterStartIndex": 0,
        "chapterContentXpath": '//*[@id="txt"]/text()',
        "chapterContentStopIndex": -1
    }
}
