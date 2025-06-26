from mini_db.conexion import conectar_db

def findByUserName(username):
    conexion = conectar_db()
    if not conexion:
        return None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin WHERE v_userName = %s", (username,))
        return cursor.fetchone()
    finally:
        conexion.close()

def findById(admin_id):
    conexion = conectar_db()
    if not conexion:
        return None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin WHERE id = %s", (admin_id,))
        return cursor.fetchone()
    finally:
        conexion.close()

def create(id, username, email, password):
    conexion = conectar_db()
    try:
        userExist = findByUserName(username)
        if userExist:
            return None
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO admin (id, v_userName, v_email, v_password) VALUES (%s, %s, %s, %s)", (id, username, email, password))
        conexion.commit()
        return cursor.lastrowid
    finally:
        conexion.close()

def update(admin_id, username, email, password):
    conexion = conectar_db()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE admin SET v_userName = %s, v_email = %s, v_password = %s WHERE id = %s
        """, (username, email, password, admin_id))
        conexion.commit()
        return cursor.rowcount
    finally:
        conexion.close()

def delete(admin_id):
    conexion = conectar_db()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM admin WHERE id = %s", (admin_id,))
        conexion.commit()
        return cursor.rowcount
    finally:
        conexion.close()


def resetPassword(username, email, password):
    conexion = conectar_db()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE admin SET v_password = %s WHERE v_userName = %s AND v_email = %s
        """, (password, username, email))
        conexion.commit()
        return cursor.rowcount
    finally:
        conexion.close()