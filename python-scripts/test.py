import json
import os
import subprocess

from conf2orgs import conf

org_name = 'owkin'

org = conf['orgs'][org_name]
org_user_home = org['users']['user']['home']
org_user_msp_dir = org_user_home + '/msp'
peer = org['peers'][0]
args = '{"Args":["queryChallenges"]}'

# update config path for using right core.yaml
os.environ['FABRIC_CFG_PATH'] = peer['docker_core_dir']
# update mspconfigpath for getting one in /data
os.environ['CORE_PEER_MSPCONFIGPATH'] = org_user_msp_dir

channel_name = conf['misc']['channel_name']
chaincode_name = conf['misc']['chaincode_name']

print('Querying chaincode in the channel \'%(channel_name)s\' on the peer \'%(peer_host)s\' ...' % {
    'channel_name': channel_name,
    'peer_host': peer['host']
}, flush=True)

output = subprocess.run(['peer',
                         '--logging-level=debug',
                         'chaincode', 'query',
                         '-x',
                         '-C', channel_name,
                         '-n', chaincode_name,
                         '-c', args],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

data = output.stdout.decode('utf-8')
if data:
    try:
        data = json.loads(bytes.fromhex(data.rstrip()).decode('utf-8'))
    except:
        pass
    else:
        msg = 'Query of channel \'%(channel_name)s\' on peer \'%(peer_host)s\' was successful\n' % {
            'channel_name': channel_name,
            'peer_host': peer['host']
        }
        print(msg, flush=True)
        print(data, flush=True)
else:
    try:
        msg = output.stderr.decode('utf-8').split('Error')[2].split('\n')[0]
        data = {'message': msg}
    except:
        msg = output.stderr.decode('utf-8')
        data = {'message': msg}
    finally:
        print(data)
