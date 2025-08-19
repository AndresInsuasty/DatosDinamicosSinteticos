import io

def preparar_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def preparar_excel(df):
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)
    return buffer

def preparar_json(df):
    return df.to_json(orient="records", force_ascii=False).encode('utf-8')

def preparar_parquet(df):
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)
    return buffer

def preparar_sqlite(df, tabla_nombre='datos_sinteticos'):
    import sqlite3
    import tempfile
    import os
    
    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as temp_file:
        temp_path = temp_file.name
    
    try:
        # Crear conexión a archivo temporal
        conn = sqlite3.connect(temp_path)
        
        # Insertar DataFrame en la tabla
        df.to_sql(tabla_nombre, conn, index=False, if_exists='replace')
        
        # Cerrar conexión
        conn.close()
        
        # Leer archivo binario
        with open(temp_path, 'rb') as f:
            buffer_sqlite = io.BytesIO(f.read())
        
        buffer_sqlite.seek(0)
        
        return buffer_sqlite
    
    finally:
        # Limpiar archivo temporal
        if os.path.exists(temp_path):
            os.unlink(temp_path)
