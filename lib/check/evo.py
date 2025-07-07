from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from libprobe.exceptions import CheckException
from ..snmpclient import get_snmp_client
from ..snmpquery import snmpquery

QUERIES = (
    (MIB_INDEX['EVO-MIB']['evo'], False),
    (MIB_INDEX['EVO-MIB']['evoCpuDetails'], False),
    (MIB_INDEX['EVO-MIB']['evoUptime'], False),
    (MIB_INDEX['EVO-MIB']['evoUPS'], False),
)


async def check_evo(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:

    snmp = get_snmp_client(asset, asset_config, check_config)
    state = await snmpquery(snmp, QUERIES)

    if not state['evo'] or not not state['ups'] or not any(state.values()):
        raise CheckException('no data found')

    ups = state['ups']
    evo = state['evo']
    cpu = state['evoCpuDetails']
    uptime = state['evoUptime']

    return {
        'evo': [{
            **evo[0],
            **(cpu and cpu[0] or {}),
            **(uptime and uptime[0] or {}),
            'name': 'evo',
        }],
        'ups': ups,
    }
