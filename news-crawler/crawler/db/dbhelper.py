import pymysql


class DbHelper:

    db_params = {
        'host' : '127.0.0.1',
        'user' : 'newsmailer',
        'passwd' : '123456',
        'db' : 'news',
        'charset' : 'utf8',
        'cursorclass' : pymysql.cursors.DictCursor,
    }

    def __init__(self):
        self.connection = pymysql.connect(**self.db_params)

    def insert_qsbk(self, item):
        joke_id = self.insert_jokes(item)
        self.insert_images(item, joke_id)

    def insert_jokes(self, item):
        sql = 'INSERT INTO `jokes` (`link`, `text`, `votes`, `comments`)' \
              ' VALUES (%s, %s, %s, %s)'
        values = (item['link'], item['text'], item['votes'], item['comments'])
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, values)
                joke_id = cursor.lastrowid
                self.connection.commit()
                return joke_id
        except:
            self.connection.rollback()

    def insert_images(self, item, joke_id):
        sql = 'INSERT INTO `images` (`url`, `joke_id`) VALUES (%s, %s)'
        for url in item['img_urls']:
            values = (url, joke_id)
        try:
            with self.connection.cursor() as cursor:
                for url in item['img_urls']:
                    values = (url, joke_id)
                    cursor.execute(sql, values)
                self.connection.commit()
        except:
            self.connection.rollback()



