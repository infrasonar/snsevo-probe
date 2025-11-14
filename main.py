from libprobe.probe import Probe
from lib.check.evo import CheckEvo
from lib.check.evo_int_disk_stats import CheckEvoIntDiskStats
from lib.check.per_drive_stats import CheckPerDriveStats
from lib.check.volumes import CheckVolumes
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = (
        CheckEvo,
        CheckEvoIntDiskStats,
        CheckPerDriveStats,
        CheckVolumes,
    )

    probe = Probe("snsevo", version, checks)

    probe.start()
