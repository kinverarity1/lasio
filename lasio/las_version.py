import subprocess, re
from pkg_resources import get_distribution, DistributionNotFound
from datetime import datetime

ver_date = datetime.now().strftime("d%Y%m%d")

def get_version():
    las_version = ''

    # Test for distribution version
    try:
        las_version = get_distribution(__name__).version
    except DistributionNotFound:
        pass

    # Test for version control system version
    if not las_version.strip():
        las_version = _get_vcs_version()

    # Else set a sensible default version
    if not las_version.strip():
        las_version = (
            "0.25.0.dev0+unknown-post-dist-version.{}".format(ver_date)
        )

    return las_version

def _get_vcs_version():
    semver_regex = re.compile('^v\d+\.\d+\.\d+')
    split_regex = re.compile('-')
    local_las_version = ''
    tmpstr = ''

    try:    
        # https://git-scm.com/docs/git-describe
        # git describe --tags --match 'v*'
        tmpstr = subprocess.check_output(
            # ["python", "setup.py", "--version"],
            ["git", "describe", "--tags", "--match", "v*"],
            stderr=subprocess.STDOUT,
            encoding='utf-8'
        ).strip()
    except subprocess.CalledProcessError:
        pass

    if semver_regex.match(tmpstr):
        tmpstr = tmpstr[1:]
        (rel_ver, commits_since_rel_ver, current_commit) = split_regex.split(tmpstr)
        local_las_version = "{}.dev{}+{}.{}".format(
            rel_ver, commits_since_rel_ver, current_commit, ver_date
        )

    return local_las_version

