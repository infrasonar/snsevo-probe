from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from libprobe.check import Check
from ..snmpclient import get_snmp_client
from ..snmpquery import snmpquery

QUERIES = (
    (MIB_INDEX['EVO-MIB']['perDriveStatsTableEntry'], True),
)


class CheckPerDriveStats(Check):
    key = 'perDriveStats'
    unchanged_eol = 0

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        snmp = get_snmp_client(asset, local_config, config)
        state = await snmpquery(snmp, QUERIES)

        for item in state['perDriveStatsTableEntry']:
            in_kb = item.pop('perDriveStatsTableInputKbytes')
            out_kb = item.pop('perDriveStatsTableOutputKbytes')
            item['perDriveStatsTableInputBytes'] = in_kb * 1000
            item['perDriveStatsTableOutputBytes'] = out_kb * 1000

        return {
            'perDriveStats': state['perDriveStatsTableEntry']
        }
