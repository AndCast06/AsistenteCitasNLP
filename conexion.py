import mariadb

class ConexionDB:
    def __init__(self):
        try:
            # Establecer la conexión a la base de datos
            self.conn = mariadb.connect(
                user="root",  # Usuario de la base de datos
                password="",  # Contraseña de la base de datos
                host="127.0.0.1",  # Host de la base de datos
                port=3306,  # Puerto de la base de datos
                database="AgenteChatBot"  # Nombre de la base de datos
            )
            self.cursor = self.conn.cursor()
            print("Conexión a la base de datos exitosa")
        except mariadb.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.cursor = None

    def ejecutar_query(self, query, params=None, fetch_one=False):
        if self.cursor:
            try:
                # Ejecutar la consulta
                self.cursor.execute(query, params) if params else self.cursor.execute(query)

                # Si la consulta requiere obtener datos, retornar el resultado
                if fetch_one:
                    return self.cursor.fetchone()
                else:
                    return self.cursor.fetchall()
            except mariadb.Error as e:
                print(f"Error al ejecutar la consulta: {e}")
                return None

    def cerrar_conexion(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Conexión cerrada correctamente")
