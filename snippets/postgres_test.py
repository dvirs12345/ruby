import psycopg2

conn = psycopg2.connect(
    database="postgres",
    user='postgres',
    password='vn3fxpugx',
    host='localhost',
    port='5432'
)

# conn.autocommit = True

cursor = conn.cursor()

# query = "select * from public.\"Blocks\""
# cursor.execute(query)

camid = "1"
platenum = "9700594"
long = "35.168947"
lat = "31.858142"
drawing = open("download.jpg", 'rb').read()

# query = "INSERT INTO public.sensors(camid, platenum, \"long\", lat, image) VALUES (?, ?, ?, ?, ?);"
#cursor.execute("INSERT INTO sensors (camid, platenum, \"long\", lat, image) " + "VALUES(%s,%s,%s,%s,%s)",
#               (camid, platenum, long, lat, psycopg2.Binary(drawing)))\

#conn.commit()

cursor.execute("SELECT * FROM sensors")
data = cursor.fetchall()
open("FromDB.jpg", 'wb').write(data[0][-1])
print(type(data[0][-1]))

