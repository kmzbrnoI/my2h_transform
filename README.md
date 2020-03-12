# my2h_transform
MyJOP To hJOP Transform Utility

## Run

    python3 -m venv env
    source env/bin/activate
    pip3 install -r requirements.txt

    python my2h_transform


## Real usage

    # Load blocks & drive paths from myJOP and create blk.db file
    python my2h_transform load_blocks zadani/bloky.blk zadani/zaverova_tabulka.ztb blk.db

    # Create reid_map.csv for blk.db file.
    python my2h_transform reid blk.db reid_map.csv

    # Transfrom blk.db by reid_map.csv to new_blk.db
    python my2h_transform remap_by_reid blk.db reid_map.csv new_blk.db

    # Create IR table
    python my2h_transform create_ir new_blk.db

    # Create .ini file for hJOP from new_blk.db
    python my2h_transform create_ini new_blk.db blk.ini

    # Create .ini file for hJOP 'jizdni cesty' from new_blk.db
    python my2h_transform create_jc_ini new_blk.db JC.ini


## Development & Contributions

### Setup development environment on Linux

    # setup commit template
    git config commit.template .git-commit-template

    # git configuration
    git config user.name "your_name"
    git config user.email "your_email"

    # (optionally)
    git config user.signingkey your_gpg_key

### Local checks

    ./pep8-diff.sh
    pylint my2h_transform


## Resources

- [regular expression](https://regexr.com/)
- [sqlalchemy](https://docs.sqlalchemy.org/en/13/)
- [Vocabulary](https://www.fd.cvut.cz/personal/tyfal/str/slovnik/a-c-a.pdf)
