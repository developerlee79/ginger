from app.search.device_info_finder import DeviceInfoFinder
from app.db import get_db

class AzureDatabaseFinder(DeviceInfoFinder):

    def get_device_list(self, category, page, size):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        offset = page * size

        if category == 0:
            query = """
                    SELECT *
                    FROM ELECTRONIC_DEVICE LIMIT %s \
                    OFFSET %s \
                    """
            cursor.execute(query, (size, offset))
        else:
            query = """
                    SELECT *
                    FROM ELECTRONIC_DEVICE
                    WHERE category = %s
                        LIMIT %s \
                    OFFSET %s \
                    """
            cursor.execute(query, (category, size, offset))

        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def get_recommend_devices(self, search_query):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        size = 5

        query = ["SELECT * FROM ELECTRONIC_DEVICE"]

        if search_query["where"]:
            query.append(" WHERE ")
            for where_query in search_query["where"]:
                query.append(where_query)
                query.append(" AND ")
            query.pop()

        if search_query["sort"]:
            query.append(" ORDER BY ")
            for sort_query in search_query["sort"]:
                query.append(sort_query)
                query.append(", ")
            query.pop()

        query.append(" LIMIT %s")
        cursor.execute(''.join(query), (size,))

        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def get_device_info(self, device_id):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        query = """
                SELECT *
                FROM ELECTRONIC_DEVICE
                WHERE id = %s
                """
        cursor.execute(query, (device_id,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            return result
        else:
            raise Exception("Device not found")

    def find_device_info(self, manufacturer, model_code):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        query = """
                SELECT model_name, power_consumption
                FROM ELECTRONIC_DEVICE
                WHERE manufacturer = %s \
                  AND model_code = %s \
                """
        cursor.execute(query, (manufacturer, model_code))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            return result["model_name"], result["power_consumption"]
        else:
            raise Exception("Device not found")
