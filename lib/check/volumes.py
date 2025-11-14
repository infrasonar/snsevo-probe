from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from libprobe.check import Check
from ..snmpclient import get_snmp_client
from ..snmpquery import snmpquery

QUERIES = (
    (MIB_INDEX['EVO-MIB']['volumesTableEntry'], True),
)


class CheckVolumes(Check):
    key = 'volumes'

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        snmp = get_snmp_client(asset, local_config, config)
        state = await snmpquery(snmp, QUERIES)

        for item in state['volumesTableEntry']:
            item['volumesTableSize'] *= 1_000_000

        return {
            'volumes': state['volumesTableEntry']
        }
