## Installation of deployers/agents

### Prerequisites

- node.js
- npm
- shellinabox

### OSHI Agent

Let us deploy the OSHI agent (see http://netgroup.uniroma2.it/OSHI/)

A specific prerequisite for this Agent is to have the mininet emulation tool installed.

Clone the project from repository with ssh:
    
    $ git clone git@bitbucket.org:ssalsano/rdcl-agent.git
    
or https:

    $ git clone https://ssalsano@bitbucket.org/ssalsano/rdcl-agent.git
	
(NB: It will moved to a public git repository ASAP)

Install all node.js dependencies:

    $ npm install

Check the paths in the configuration file config/config.js :
- shellinabox.script_path
- config.mininet.mininet_extension_path

Start node:

    $ npm start



