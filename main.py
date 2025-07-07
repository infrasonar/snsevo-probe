from libprobe.probe import Probe
from lib.check.evo import check_evo
from lib.check.evo_int_disk_stats import check_evo_int_disk_stats
from lib.check.per_drive_stats import check_per_drive_stats
from lib.check.volumes import check_volumes
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'evo': check_evo,
        'evoIntDiskStats': check_evo_int_disk_stats,
        'perDriveStats': check_per_drive_stats,
        'volumes': check_volumes,
    }

    probe = Probe("snsevo", version, checks)

    probe.start()
