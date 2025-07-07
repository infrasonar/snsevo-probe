from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from ..snmpclient import get_snmp_client
from ..snmpquery import snmpquery

QUERIES = (
    (MIB_INDEX['EVO-MIB']['perDriveStatsTableEntry'], True),
)


async def check_per_drive_stats(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:

    snmp = get_snmp_client(asset, asset_config, check_config)
    state = await snmpquery(snmp, QUERIES)

    for item in state['perDriveStatsTableEntry']:
        in_kb = item.pop('perDriveStatsTableInputKbytes')
        out_kb = item.pop('perDriveStatsTableOutputKbytes')
        item['perDriveStatsTableInput'] = in_kb * 1000
        item['perDriveStatsTableOutput'] = out_kb * 1000

    return {
        'perDriveStats': state['perDriveStatsTableEntry']
    }
