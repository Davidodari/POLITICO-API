from api.db_conn import db_connect


class ResultsModel:
    def __init__(self, office_id):
        self.office_id = office_id
        self.db_conn = db_connect()

    def get_results(self):
        query = """SELECT candidate,COUNT(*) FROM votes WHERE office = %s GROUP BY candidate ;"""
        cursor = self.db_conn.cursor()
        cursor.execute(query, (self.office_id,))
        self.db_conn.commit()
        tally = cursor.fetchall()
        if len(tally) < 1:
            return 'Empty'
        return tally
