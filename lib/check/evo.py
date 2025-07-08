from asyncsnmplib.mib.mib_index import MIB_INDEX
from asyncsnmplib.mib.syntax_funs import SYNTAX_FUNS
from libprobe.asset import Asset
from libprobe.exceptions import CheckException
from ..snmpclient import get_snmp_client
from ..snmpquery import snmpquery

QUERIES = (
    (MIB_INDEX['EVO-MIB']['evo'], True),
    (MIB_INDEX['EVO-MIB']['evoCpuDetails'], True),
    (MIB_INDEX['EVO-MIB']['evoUptime'], True),
    (MIB_INDEX['EVO-MIB']['evoUPS'], True),
)
# NOTE evo, evoCpuDetails, evoUptime, evoUPS are single item, but we have to
# set is_table=True as oids in the result lack the 0 at the end.


def as_int(val: bytes):
    try:
        return int(val)
    except Exception:
        return


SYNTAX_FUNS['as_int'] = as_int
SYNTAX_FUNS['as_none'] = lambda *_: None
AS_NONE = {
    'tp': 'CUSTOM', 'func': 'as_none',
}
AS_INT = {
    'tp': 'CUSTOM', 'func': 'as_int',
}
# use as custom syntax as it otherwise returns error for the evo query as
# there are 2 tables as direct child oids which we cannot parse
MIB_INDEX[MIB_INDEX['EVO-MIB']['volumesTable']]['syntax'] = AS_NONE
MIB_INDEX[MIB_INDEX['EVO-MIB']['realtimeVolumesTable']]['syntax'] = AS_NONE
MIB_INDEX[MIB_INDEX['EVO-MIB']['perDriveStatsTable']]['syntax'] = AS_NONE
# use as custom syntax to convert to float
MIB_INDEX[MIB_INDEX['EVO-MIB']['evoCpuLoadedUptime']]['syntax'] = AS_INT
MIB_INDEX[MIB_INDEX['EVO-MIB']['evoCpuDetailsUptime']]['syntax'] = AS_INT
MIB_INDEX[MIB_INDEX['EVO-MIB']['evoCpuDetailsIdleTime']]['syntax'] = AS_INT


async def check_evo(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:

    snmp = get_snmp_client(asset, asset_config, check_config)
    state = await snmpquery(snmp, QUERIES)

    if not state['evo'] or not not state['evoUPS'] or not any(state.values()):
        raise CheckException('no data found')

    ups = state['evoUPS']
    evoitem = state['evo'][0]
    cpu = state['evoCpuDetails']
    uptime = state['evoUptime']

    item = {
        'name': 'evo',
        'evoVersion': evoitem['evoVersion'],
        'evoLocalTime': evoitem['evoLocalTime'],
        'evoCpuLoadedUptime': evoitem['evoCpuLoadedUptime'],
    }

    if cpu:
        item.update(cpu[0])
    if uptime:
        item.update(uptime[0])

    return {
        'evo': [item],
        'ups': ups,
    }
