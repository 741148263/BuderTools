import os.path
from configparser import ConfigParser

from constants.window_constant import CONFIG_DIR


def init_config():
    """
    初始化配置文件
    """
    if not os.path.exists(CONFIG_DIR):
        writer = ConfigParser()
        writer.add_section("read")
        writer.set("read", "book_id", "")
        with open(CONFIG_DIR, "w") as fp:
            writer.write(fp)


def read_info(module, key):
    """
    读取配置文件
    """
    reader = ConfigParser()
    reader.read(CONFIG_DIR)
    return reader.get(module, key)


def write_info(module, key, value):
    """
    写入配置文件
    """
    writer = ConfigParser()
    writer.read(CONFIG_DIR)
    writer.set(module, key, value)
    with open(CONFIG_DIR, "w") as fp:
        writer.write(fp)


def add_book_info(book_id):
    """
    更新配置文件，禁止重复内容
    """
    writer = ConfigParser()
    writer.read(CONFIG_DIR)
    id_list_str = writer.get("read", "book_id")
    id_list = id_list_str.split(",")
    if str(book_id) not in id_list:
        id_list_str += f"{book_id},"
        writer.set("read", "book_id", id_list_str)
        with open(CONFIG_DIR, "w") as fp:
            writer.write(fp)


def delete_book_info(book_id):
    """
    删除配置
    """
    writer = ConfigParser()
    writer.read(CONFIG_DIR)
    id_list_str = writer.get("read", "book_id")
    id_list_str = id_list_str.replace(f"{book_id},", "")
    writer.set("read", "book_id", id_list_str)
    with open(CONFIG_DIR, "w") as fp:
        writer.write(fp)
