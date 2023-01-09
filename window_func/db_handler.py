import os.path

from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from constants.window_constant import ROOT_DIR, CREATE_BOOK_CASE_TABLE, CREATE_BOOK_CHAPTER_TABLE, DB_FILE, \
    INSERT_BOOK_CASE, SEARCH_BOOK_COUNT_SQL, SEARCH_BOOK_SQL, SEARCH_NO_CHAPTER_SQL, INSERT_CHAPTER_SQL, \
    UPDATE_CHAPTER_STATUS_SQL


class BookSqlHandler(object):
    def __init__(self, connect_name):
        self.connect_name = connect_name
        if QSqlDatabase.contains(connect_name):
            QSqlDatabase.removeDatabase(connect_name)
        self.db = QSqlDatabase.addDatabase("QSQLITE", self.connect_name)
        if os.path.exists(os.path.join(ROOT_DIR, DB_FILE)):
            self.db.setDatabaseName(os.path.join(ROOT_DIR, DB_FILE))
            self.db.open()
        else:
            self.db.setDatabaseName(os.path.join(ROOT_DIR, DB_FILE))
            self.db.open()
            self.init_db_data()

    def close(self):
        self.db.close()

    def init_db_data(self):
        query = QSqlQuery(self.db)
        query.exec_(CREATE_BOOK_CASE_TABLE)
        query.exec_(CREATE_BOOK_CHAPTER_TABLE)

    def search_count(self):
        query = QSqlQuery(self.db)
        query.exec_(SEARCH_BOOK_COUNT_SQL)
        count = 0
        while query.next():
            count += query.value(0)
        return count

    def insert_book(self, book: dict):
        query = QSqlQuery(self.db)
        query.exec_(SEARCH_BOOK_COUNT_SQL)
        count = 0
        while query.next():
            count += query.value(0)
        command = INSERT_BOOK_CASE.format(count + 1, book["title"], book["author"], book["update_chapter"],
                                          book["from"], book["status"], book["href"], 0, 0)
        return query.exec_(command)

    def search_book(self):
        book_list = []
        query = QSqlQuery(self.db)
        query.exec_(SEARCH_BOOK_SQL)
        while query.next():
            temp_book = []
            for i in range(0, 8):
                temp_book.append(query.value(i))
            book_list.append(temp_book)
        return book_list

    def delete_book(self, book_id):
        query = QSqlQuery(self.db)
        ret1 = query.exec_(f"delete from book_chapter where bookcase_id = {book_id};")
        ret = query.exec_(f"delete from bookcase where id = {book_id};")
        return ret

    def search_no_chapter(self):
        no_chapter_list = []
        query = QSqlQuery(self.db)
        query.exec_(SEARCH_NO_CHAPTER_SQL)
        while query.next():
            temp_list = []
            temp_list.append(query.value(0))
            temp_list.append(query.value(1))
            temp_list.append(query.value(2))
            no_chapter_list.append(temp_list)
        return no_chapter_list

    def insert_book_case(self, book_id, title_list, href_list) -> bool:
        query = QSqlQuery(self.db)
        temp_valuse = ""
        first = True
        for chapter_title, chapter_href in zip(title_list, href_list):
            if first:
                temp_valuse += "('{}', '{}', '{}')".format(chapter_title, chapter_href, book_id)
                first = False
            else:
                temp_valuse += ",('{}', '{}', '{}')".format(chapter_title, chapter_href, book_id)
        insert_result = query.exec_(INSERT_CHAPTER_SQL + temp_valuse + ";")
        return insert_result

    def update_book_chapter_state(self, book_id):
        query = QSqlQuery(self.db)
        return query.exec_(UPDATE_CHAPTER_STATUS_SQL.format(book_id))

    def query_book_info(self, book_id):
        book_dict = {}
        id_list = []
        title_list = []
        href_list = []
        query = QSqlQuery(self.db)
        query_result = query.exec_(
            f"select book_name, read_chapter_index, id, book_from from bookcase where id = {int(book_id)};")
        if query_result:
            while query.next():
                book_dict["book_name"] = query.value(0)
                book_dict["read_index"] = query.value(1)
                book_dict["id"] = query.value(2)
                book_dict["from"] = query.value(3)
            query.exec_(
                f"select id, chapter_name, chapter_href from book_chapter where bookcase_id = {int(book_id)} order by id;")
            while query.next():
                id_list.append(query.value(0))
                title_list.append(query.value(1))
                href_list.append(query.value(2))
            book_dict.update({"id_list": id_list, "title_list": title_list, "href_list": href_list})
            return book_dict
        return book_dict

    def update_book_read_index(self, book_id, read_index):
        query = QSqlQuery(self.db)
        return query.exec_(f"update bookcase set read_chapter_index = {read_index} where id = {int(book_id)};")

    def update_chapter_content(self, chapter_id, content):
        pass
