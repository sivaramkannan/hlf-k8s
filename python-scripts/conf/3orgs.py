import json
import os
from misc import misc
from orderer import orderer
from owkin import owkin
from chunantes import chunantes
from clb import clb


SUBSTRA_PATH = os.getenv('SUBSTRA_PATH', '/substra')

misc.update({
    'fixtures_path': 'fixtures2orgs.py'
})


def main():

    orderer.update({
        'misc': {k: misc[k] for k in ['system_channel_name', 'system_channel_block', 'channel_name', 'channel_block', 'chaincode_name',
                                      'chaincode_version', 'genesis_bloc_file', 'channel_tx_file',
                                      'config_block_file', 'config_update_envelope_file']},
    })

    service_name = orderer['name']
    orderer['misc']['setup_logfile'] = f'{SUBSTRA_PATH}/data/log/setup-{service_name}.log',
    orderer['misc']['configtx-config-path'] = f'{SUBSTRA_PATH}/data/orgs/{service_name}'
    orderer['misc']['setup_success_file'] = f'{SUBSTRA_PATH}/data/log/setup-{service_name}.successful'

    with open(f'{SUBSTRA_PATH}/conf/config/conf-{service_name}.json', 'w+') as write_file:
        json.dump(orderer, write_file, indent=4)

    for org in [owkin, chunantes, clb]:
        org.update({
            'misc': dict(misc),
        })

        service_name = org['name']
        org['misc']['configtx-config-path'] = f'{SUBSTRA_PATH}/data/orgs/{service_name}'

        org['misc']['setup_logfile'] = f'{SUBSTRA_PATH}/data/log/setup-{service_name}.log',
        org['misc']['setup_success_file'] = f'{SUBSTRA_PATH}/data/log/setup-{service_name}.successful'

        org['misc']['run_logfile'] = f'{SUBSTRA_PATH}/data/log/run-{service_name}.log'
        org['misc']['run_sumfile'] = f'{SUBSTRA_PATH}/data/log/run-{service_name}.sum'
        org['misc']['run_success_file'] = f'{SUBSTRA_PATH}/data/log/run-{service_name}.successful'
        org['misc']['run_fail_file'] = f'{SUBSTRA_PATH}/data/log/run-{service_name}.fail'

        org['misc']['fixtures_logfile'] = f'{SUBSTRA_PATH}/data/log/fixtures-{service_name}.log'
        org['misc']['fixtures_success_file'] = f'{SUBSTRA_PATH}/data/log/fixtures-{service_name}.sum'
        org['misc']['fixtures_fail_file'] = f'{SUBSTRA_PATH}/data/log/fixtures-{service_name}.successful'

        org['misc']['revoke_logfile'] = f'{SUBSTRA_PATH}/data/log/revoke-{service_name}.log'
        org['misc']['revoke_success_file'] = f'{SUBSTRA_PATH}/data/log/revoke-{service_name}.sum'
        org['misc']['revoke_fail_file'] = f'{SUBSTRA_PATH}/data/log/revoke-{service_name}.successful'

        with open(f'{SUBSTRA_PATH}/conf/config/conf-{service_name}.json', 'w+') as write_file:
            json.dump(org, write_file, indent=4)


if __name__ == '__main__':
    main()