#-*-coding:utf-8-*-
import MySQLdb
import time
conn=-1
cur=-1
def connect_database():
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='data',port=3306,charset='utf8')
        cur=conn.cursor()    
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return [-1,-1]
    return [conn,cur]
    

def close_database(conn,cur):
    try:
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print '\n' #"Mysql Error %d: %s" % (e.args[0], e.args[1])  

def update_data(link='',name='',ori_price='',pro_price='',img='',desc='',source='',table='temp_table',ack_time='',call_flag=0):
        db=connect_database()
        conn=db[0]
        cur=db[1]
        if table == 'temp_table':
            value=[None,name,img,link,source,desc,ori_price,pro_price,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))]
            cur.execute('insert into temp_table values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',value)
        if table == 'data_table':
            value=[None,name,img,link,source,desc,ori_price,pro_price,ack_time]
            cur.execute('insert into data_table values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',value)
        conn.commit()
        close_database(conn,cur)  


def look_temp_data(page=0):
    db=connect_database()
    conn=db[0]
    cur=db[1]
    cur.execute('select * from temp_table')
    try:
        cur.scroll(9*page, mode='absolute')
        lines=cur.fetchmany(size=9)
    except IndexError as e:
        close_database(conn,cur)
        return ()
    close_database(conn,cur)
    return lines

def look_data_data(page=0):
    db=connect_database()
    conn=db[0]
    cur=db[1]
    cur.execute('select * from data_table')
    try:
        cur.scroll(9*page, mode='absolute')
        lines=cur.fetchmany(size=9)
    except IndexError as e:
        close_database(conn,cur)
        return ()
    close_database(conn,cur)
    return lines

def delete(product_id='',table='',call_flag=0):
    db=connect_database()
    conn=db[0]
    cur=db[1]
    cur.execute('delete from '+table+' where product_code = '+product_id)
    conn.commit()
    close_database(conn,cur)
   

def ack(product_id,table=''):   
    if table == 'temp_table':
        db=connect_database()
        conn=db[0]
        cur=db[1]
        cur.execute('select * from temp_table where product_code ='+product_id)
        lines=cur.fetchone()
        update_data(name=lines[1],img=lines[2],link=lines[3],source=lines[4],desc=lines[5],ori_price=lines[6],pro_price=lines[7],table='data_table',ack_time=lines[8],call_flag=1)
        delete(product_id,'temp_table',call_flag=1)
        close_database(conn,cur)
        return 0
    else:
        return -1

def main():    
    print len(look_temp_data(7))
if __name__ == '__main__':
    main()
      