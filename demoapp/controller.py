from flask import Flask, render_template

import json
from cassandra.cluster import Cluster
from faker import Factory

fake_data_src = Factory.create()

#Getting Cassandra connect params
with open('/opt/devopstz/demoapp/config.json') as f:
    conf_data = json.load(f)
    
contact_point = conf_data['ip']
keyspace = conf_data['keyspace']
cql_version = conf_data['cql_version']

cluster = Cluster(contact_points=contact_point, cql_version=cql_version)
session = cluster.connect(keyspace)

app = Flask(__name__)

def select():
    try:
        
        query_get_list = 'select * from users'
        query_get_list_result = session.execute(query_get_list)
        
        records = []
        for i in query_get_list_result:
            record = {}
            record['username'] = i.username
            record['email'] = i.email
            record['name'] = i.name
            record['ipaddr'] = i.ipaddr
            records.append(record)
        
        return(records)
    
    except Exception as e:
        
        return str(e)
        
@app.route('/')
def index():
        
    return render_template('list.html', records = select())
        
    
@app.route('/add_fake_record/', methods=['POST'])
def add_fake_record():
    
    query_add_record = 'insert into users (username, email, name, ipaddr) values (\'{username}\', \'{email}\', \'{name}\', \'{ipaddr}\')'.format(
        username = fake_data_src.user_name(),
        email = fake_data_src.email(),
        name = fake_data_src.name(),
        ipaddr = fake_data_src.ipv4())
    
    query_add_record_result = session.execute(query_add_record)
    
    return render_template('list.html', records = select())
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
