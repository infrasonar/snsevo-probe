from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from libprobe.check import Check
from libprobe.exceptions import CheckException
from ..snmpclient import get_snmp_client
from ..snmpquery import snmpquery

QUERIES = (
    (MIB_INDEX['EVO-MIB']['evoIntDiskStats'], True),
)
# NOTE evoIntDiskStats is a single item, but we have to set is_table=True as
# oids in the result lack the 0 at the end.


class CheckEvoIntDiskStats(Check):
    key = 'evoIntDiskStats'
    unchanged_eol = 0

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        snmp = get_snmp_client(asset, local_config, config)
        state = await snmpquery(snmp, QUERIES)

        if not any(state.values()):
            raise CheckException('no data found')

        for item in state['evoIntDiskStats']:
            item['evoIntDiskStatsRead'] *= 1000
            item['evoIntDiskStatsWrite'] *= 1000

        return state
