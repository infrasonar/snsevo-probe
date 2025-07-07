from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from ..snmpclient import get_snmp_client
from ..snmpquery import snmpquery

QUERIES = (
    (MIB_INDEX['EVO-MIB']['volumesTableEntry'], True),
)


async def check_volumes(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:

    snmp = get_snmp_client(asset, asset_config, check_config)
    state = await snmpquery(snmp, QUERIES)

    for item in state['volumesTableEntry']:
        item['volumesTableSize'] *= 1_000_000

    return {
        'volumes': state['volumesTableEntry']
    }
