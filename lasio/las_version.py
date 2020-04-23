import subprocess, re
from pkg_resources import get_distribution, DistributionNotFound
from datetime import datetime

# d[year][month][day] example: 20200420
ver_date = datetime.now().strftime("d%Y%m%d")

def version():
    las_version = ''

    '''
    Look for distribution version

    This looks for a distribution in roughly the following order.
    - Local development install installed with 'pip install -e "."'
        Note:
            The '-e' puts the install in an editable-mode where it it looks at
            the source directory and reactes to changes in the code.
    - A lasio.egg-info dir in the current working directory.
        Note!:
            An existing lasio.egg-info dir can hide an offical release install
            for the case where an offical release is also installed.  The
            lasio.egg-info can be an artifact of running 'pip install -e "."',
            or of runnng 'bdist_wheel' to create a release package.
    - An official release installed with 'pip install lasio' or a development
    release installed with 'pip install "."'
    '''


    try:
        las_version = get_distribution(__package__).version
    except DistributionNotFound:
        # TODO: Add logger message
        pass

    '''
    If no distribution is found, check if the current working directory is in a
    version control system and attempt to derive a version string from the vsc.
    '''
    if not las_version.strip():
        las_version = _get_vcs_version()

    '''
    Else set a sensible default version
    0.25.0 was the most recent version before this change so it is being
    used as teh default basline.
    '''
    if not las_version.strip():
        las_version = (
            "0.25.0.dev0+unknown-post-dist-version.{}".format(ver_date)
        )

    return las_version


def _get_vcs_version():
    semver_regex = re.compile('^v\d+\.\d+\.\d+') # examples: 'v0.0.0', 'v0.25.0'
    split_regex = re.compile('-')
    local_las_version = ''
    tmpstr = ''
    tmpbytes = b''

    '''
    https://git-scm.com/docs/git-describe
    git describe --tags --match 'v*'
    This cmd will find the most recent tag starting with 'v' on the current
    branch.
    '''
    try:    
        tmpbytes = subprocess.check_output(
            ["git", "describe", "--tags", "--match", "v*"],
            stderr=subprocess.STDOUT,
        ).strip()

    except subprocess.CalledProcessError:
        pass

    # Convert byte string to text string
    try:
        tmpstr = "".join( chr(x) for x in tmpbytes)
    except TypeError as e:
        print("Error: {}\n".format(e))

    if semver_regex.match(tmpstr):
        tmpstr = tmpstr[1:]
        (rel_ver, commits_since_rel_ver, current_commit) = split_regex.split(tmpstr)
        local_las_version = "{}.dev{}+{}.{}".format(
            rel_ver, commits_since_rel_ver, current_commit, ver_date
        )

    return local_las_version
