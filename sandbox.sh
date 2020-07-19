if [[ -z "`which pip3 2> /dev/null`" ]]; then
    echo "pip3 must be installed"
    echo "Aborting..."
    return
fi

# Set up a virtualenv if it doesn't already exist
if [[ ! -d $PWD/.venv ]]; then
    curl --silent --retry 3 --retry-delay 1 --head http://google.com > /dev/null
    if [[ "$?" -ne 0 ]]; then
        echo "No internet connection available"
        echo "Aborting..."
        return
    fi

    python3 -m venv $PWD/.venv
    $PWD/.venv/bin/pip install -U pip
    $PWD/.venv/bin/pip install -r $PWD/requirements.txt

    if [[ ! -d $PWD/tests ]]; then
        $PWD/.venv/bin/python $PWD/robot.py add-tests 2> /dev/null
    fi

    ln -sf $PWD/hooks/* $PWD/.git/hooks/
fi

export PATH=$PWD/.venv/bin:$PATH

# Upgrade any out-of-date pip packages
# HACK: It would be better to include the logic for updating pip packages right
# here, but direnv waits for all subshells and functions to finish before it
# initializes the environment, which causes a noticeable hang when cd-ing into
# the repository. Running a script in the background does not cause a delay.
(bash $PWD/hooks/post-merge envrc &)
