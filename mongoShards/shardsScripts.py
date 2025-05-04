import os
import subprocess
import time
import signal
import argparse
from pymongo import MongoClient

# Paths and ports configuration
CONFIG_RS = 'cfgRS'
SHARD_RS = ['shardRS1', 'shardRS2']
CONFIG_PORTS = [26050, 26051, 26052]
SHARD_PORTS = [27017, 27018]
DATA_DIR = os.path.join(os.getcwd(), 'data')

processes = []

def launch_mongod(repl_set, port, dbpath, configsvr=False, shardsvr=False):
    cmd = [
        'mongod',
        '--replSet', repl_set,
        '--port', str(port),
        '--dbpath', dbpath,
        '--bind_ip', 'localhost'
    ]
    if configsvr:
        cmd.insert(1, '--configsvr')
    if shardsvr:
        cmd.insert(1, '--shardsvr')
    os.makedirs(dbpath, exist_ok=True)
    return subprocess.Popen(cmd)


def launch_mongos(configdb, port=27019):
    cmd = [
        'mongos',
        '--configdb', configdb,
        '--port', str(port),
        '--bind_ip', 'localhost'
    ]
    return subprocess.Popen(cmd)


def initiate_rs(client, repl_set, members, configsvr=False):
    cfg = {
        '_id': repl_set,
        'members': [{'_id': i, 'host': m} for i, m in enumerate(members)]
    }
    if configsvr:
        cfg['configsvr'] = True
    client.admin.command('replSetInitiate', cfg)


def add_shards(client, shards):
    for repl_set, port in shards:
        client.admin.command('addShard', f"{repl_set}/localhost:{port}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['start', 'stop', 'status', 'test'], help='Action to perform')
    args = parser.parse_args()

    if args.action == 'start':
        # Launch config servers
        for port in CONFIG_PORTS:
            p = launch_mongod(CONFIG_RS, port, os.path.join(DATA_DIR, f'cfg{port-26050+1}'), configsvr=True)
            processes.append(p)
        # Launch shards
        for rs, port in zip(SHARD_RS, SHARD_PORTS):
            p = launch_mongod(rs, port, os.path.join(DATA_DIR, f'sh{port-27017+1}'), shardsvr=True)
            processes.append(p)
        # Wait for mongod instances
        time.sleep(5)
        # Initiate config RS
        cfg_client = MongoClient(f'localhost:{CONFIG_PORTS[0]}')
        initiate_rs(cfg_client, CONFIG_RS, [f"localhost:{p}" for p in CONFIG_PORTS], configsvr=True)
        # Initiate shards
        for rs, port in zip(SHARD_RS, SHARD_PORTS):
            client = MongoClient(f'localhost:{port}')
            initiate_rs(client, rs, [f"localhost:{port}"])
        # Launch mongos
        configdb = CONFIG_RS + '/' + ','.join([f'localhost:{p}' for p in CONFIG_PORTS])
        p_mongos = launch_mongos(configdb)
        processes.append(p_mongos)
        time.sleep(3)
        # Add shards
        mongos_client = MongoClient('localhost:27019')
        add_shards(mongos_client, list(zip(SHARD_RS, SHARD_PORTS)))
        print("Cluster started. Connect via mongo --port 27019")

    elif args.action == 'stop':
        # Terminate all
        for p in processes:
            p.send_signal(signal.SIGINT)
        print("Cluster stopped.")

    elif args.action == 'status':
        client = MongoClient('localhost:27019')
        print(client.admin.command('replSetGetStatus'))

    elif args.action == 'test':
        # Simple test: insert and read
        client = MongoClient('localhost:27019')
        db = client.testdb
        col = db.testcol
        col.insert_one({'x': 1})
        print(col.find_one({'x': 1}))

if __name__ == '__main__':
    main()