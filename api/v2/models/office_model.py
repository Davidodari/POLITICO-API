from api.db_conn import db_connect
import psycopg2
from api.validator import OfficeValidator


class OfficesModelDb:
    """Offices Model Class"""

    def __init__(self, office=None, office_id=None):
        # Setup connection to db
        self.db_conn = db_connect()
        # Office object being worked on
        self.office = office
        self.office_id = office_id

    def create_office(self):
        """Function to create an office in db"""
        # Passed to validator
        validated_office = OfficeValidator(self.office).all_checks()
        if 'Invalid' in validated_office:
            return 'Invalid Data'
        office_type = validated_office['type']
        office_name = validated_office['name']
        # Add Office to table
        data = (office_type, office_name)
        query = "INSERT INTO offices (office_type,office_name) " \
                "VALUES(%s,%s);"
        try:
            cursor = self.db_conn.cursor()
            cursor.execute(query, data)
            self.db_conn.commit()
            return office_name
        except psycopg2.IntegrityError:
            return 'Office Exists'

    def get_all_offices(self):
        query = "SELECT * from offices"
        cursor = self.db_conn.cursor()
        cursor.execute(query)
        self.db_conn.commit()
        # Result of tables in list as tuples
        rows = cursor.fetchall()
        return rows

    def edit_office(self, new_name):
        if isinstance(self.office_id, int):
            query = "UPDATE offices SET office_name = %s WHERE _id = %s;"
            cursor = self.db_conn.cursor()
            # Validate data to be updated
            if len(new_name) < 4 or isinstance(new_name, str) == False:
                return 'Invalid Data'
            # Execute function works with iterable
            try:
                # Cant put existing data when editing
                cursor.execute(query, (new_name, self.office_id,))
                self.db_conn.commit()
            except psycopg2.IntegrityError:
                return 'Office Exists'
            # Look Up To Confirm was saved
            query = "SELECT * FROM offices WHERE _id=%s"
            cursor.execute(query, (self.office_id,))
            user_row = cursor.fetchall()
            return user_row
        return 'Invalid Id'

    def delete_office(self):
        pass

