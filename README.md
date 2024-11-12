# TAPESTRY - Temporal Analytics Platform for Exploratory Scientific and Translational Research inquirY

For docuementation please see [TAPESTRY documentation home](docs/index.md)

## Repo Manifest

- .devcontainer/ - folder containing vs code specific instructions to run a 'devcontainer' for this project
- docs/ - documentation in .md files
- legacy/ - holdover from poor organization during project maturation process.  May include some helpful nuggets but, will eventually be eliminated after contents are reivewed and moved to appropriate places
- resources/ - directory containing helpful sql, data, and/or python code
- tapestry/ - tapestry source code
- .gitignore - git specific file used to ignore artifacts from git tracking
- Dockerfile - docker config file defining the environment for this project
- example_tapestry_config.py - template you can use to build your own tapestry config files
- example_my_secrets.py - One of the two mechanisms for secrets distribution to the codebase, provided as example you can copy
- README.md - this file.  How meta?
- requirements.txt - python requirements file
- setup.py - Python packaging file used to build the pip distributable
- tnsnames.ora - Oracle specific file used to define TNS endpoints used in the packaged example
