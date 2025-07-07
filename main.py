from libprobe.probe import Probe
from lib.check.evo import check_evo
from lib.check.evo_cpu_details import check_evo_cpu_details
from lib.check.evo_int_disk_stats import check_evo_int_disk_stats
from lib.check.fc_sessions import check_fc_sessions
from lib.check.iscsi_sessions import check_iscsi_sessions
from lib.check.nas_sessions import check_nas_sessions
from lib.check.per_drive_stats import check_per_drive_stats
from lib.check.realtime_volumes import check_realtime_volumes
from lib.check.volumes import check_volumes
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'evo': check_evo,
        'evoCpuDetails': check_evo_cpu_details,
        'evoIntDiskStats': check_evo_int_disk_stats,
        'fcSessions': check_fc_sessions,
        'iscsiSessions': check_iscsi_sessions,
        'nasSessions': check_nas_sessions,
        'perDriveStats': check_per_drive_stats,
        'realtimeVolumes': check_realtime_volumes,
        'volumes': check_volumes,
    }

    probe = Probe("snsevo", version, checks)

    probe.start()
