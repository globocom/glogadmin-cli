===============================
Glogadmin-CLI
===============================

* Free software: Apache Software License 2.0

Glogadmin-CLI is an opensource command line interface for Graylog2.

Instalation
--------

	git clone https://github.com/globocom/glogadmin-cli
	cd glogadmin-cli/
	pip install .

Usage
--------



Configuration
--------

Glogadmin-CLI can reuse some common configurations like address of your Graylog server and your credentials, it will look for a
*~/.glogcli.cfg* or a *glogcli.cfg* (in your current directory). Glogadmin-CLI will use default environment and format
whenever an environment or format is omitted.

Here is a template for your glogcli.cfg file:

    [environment:default]
    host=mygraylogserver.com
    port=80
    username=john.doe
    default_stream=*

    [environment:dev]
    host=mygraylogserver.dev.com
    port=80
    tls=true
    username=john.doe

    [environment:qa]
    host=mygraylogserver.qa.com
    port=80
    tls=true
    username=john.doe

Please run the *help* command for more detailed information about all the client features.

Options:
  -se, --source-environment TEXT  The Graylog source environment
  -te, --target-environment TEXT  The Graylog target environment
  -sh, --source-host TEXT         The Graylog node's source host
  -th, --target-host TEXT         The Graylog node's target host
  -su, --source-username TEXT     The source Graylog username
  -tu, --target-username TEXT     The target Graylog username
  -sp, --source-password TEXT     The source Graylog user password
  -tp, --target-password TEXT     The target Graylog user password
  --source-port INTEGER           The source Graylog port (default: 80)
  --target-port INTEGER           The target Graylog port (default: 80)
  --import-roles                  Imports the Roles and its Streams from the
                                  source to the target
  --import-inputs                 Imports the Inputs and its Extractors from
                                  the source to the target
  --update                        Force update of resources like Roles,
                                  Streams, Inputs and Extractors
  --help                          Show this message and exit.



