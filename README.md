# Simple Ethereum Node Monitor
A simple tool to monitor ETH2 nodes based on [Ethereum on Raspberry Pi project](https://github.com/Web3-Pi/Ethereum-On-Raspberry-Pi). Monitor pushes data to the InfluxDB instance that, in turn, may be queried by Grafana to produce a visual representation of the node state. It works in parallel with [basic system monitor](https://github.com/Web3-Pi/basic-system-monitor) and allows monitoring of multiple nodes (both single and dual-device setups).

It was initially developed on **Windows 10 Pro** with **PyCharm 2022.3.1 (Community Edition)** and **Python 3.11**.

## Configuration and Running
This project requires:
- InfluxDB installed on either a local machine or on a machine available in a local subnet (some [installation instructions](https://geth.ethereum.org/docs/monitoring/dashboards))
- Optionally: local Grafana server (some [installation instructions](https://www.coincashew.com/coins/overview-eth/guide-or-how-to-setup-a-validator-on-eth2-mainnet/part-i-installation/monitoring-your-validator-with-grafana-and-prometheus)) to read data from InfluxDB and represent it in a neat, visual manner
- Working Ethereum node (preferably an Ethereum on Raspberry Pi node) available in a local subnet
  - node may be either a single-device setup or a dual-device setup

### Settings
InfluxDB and Grafana are installed and active on a machine **statsserver.local** (this name is just an example)
- InfluxDB uses the default port **8086** for queries
- Grafana uses the default port **3000** for queries

Dual-device nodes (one device hosting Geth and the second one hosting consensus client: either Nimbus or Lighthouse) are configured as follows
- Geth device
  - it has enabled web socket, which corresponds to setting at least `--ws` (and optionally: `--ws.addr 0.0.0.0 --ws.origins '*'`) geth flags
  - **basic system monitor** is running on the same device. For more information, refer to [README.md](https://github.com/Web3-Pi/basic-system-monitor/blob/main/README.md)
- Consensus device has enabled HTTP
  - in the case of Lighthouse, it corresponds to setting at least `--http` argument (optionally `--http-address 0.0.0.0`)
  - in the case of Nimbus, it corresponds to setting at least `--rest=true` argument (optionally `--rest-address=0.0.0.0 --rest-allow-origin='*'`)
  - **basic system monitor** is running on the same device. For more information, refer to [README.md](https://github.com/Web3-Pi/basic-system-monitor/blob/main/README.md)

The single-device setup (execution and consensus clients on one machine) looks as follows
- **basic system monitor** is running on the device. For more information, refer to [README.md](https://github.com/Web3-Pi/basic-system-monitor/blob/main/README.md)
- Geth is running with an enabled web socket, which corresponds to setting at least `--ws` (and optionally: `--ws.addr 0.0.0.0 --ws.origins '*'`) geth flags
- Consensus client is running with enabled HTTP
  - in the case of Lighthouse, it corresponds to setting at least the `--http` argument (optionally `--http-address 0.0.0.0`)
  - in the case of Nimbus, it corresponds to setting at least the `--rest=true` argument (optionally `--rest-address=0.0.0.0 --rest-allow-origin='*'`)

### Installation
Installation instruction (Ubuntu)
- Prerequisites
  - Configured and running [basic system monitor](https://github.com/Web3-Pi/basic-system-monitor/blob/main/README.md)
  - If necessary, configure a GitHub PAT - for details, refer to [README.md](https://github.com/Web3-Pi/web3-reverse-proxy/blob/main/README.md)
  - If necessary, install Python 3.11 and update the system configuration. More details are in [README.md](https://github.com/Web3-Pi/web3-reverse-proxy/blob/main/README.md)
- Node Monitor
```shell
cd APPROPRIATE_DIRECTORY
git clone https://github.com/jimmyisthis/simple-eth2-node-monitor.git
cd simple-eth2-node-monitor
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

After these steps, the node monitor is installed and configured.

### Usage
Two supported setups require many command line arguments for each specified node. Hence, most arguments can be skipped, and the application will use default values in such cases. Below is a complete list of default values:
- Database - InfluxDB:
  - listen port: 8086
  - user: geth
  - password: geth
  - database: ethonrpi
- Clients:
  - Geth Websocket listen port: 8546
  - Lighthouse HTTP listen port: 5052
  - Nimbus HTTP listen port: 5052
- System monitor:
  - listen port: 7197
- Sampling delays:
  - active node sampling delay: 7 seconds
  - degraded node sampling delay: 10 seconds

At least one Ethereum node and a database host must be specified to run the application.

#### Node specification
To add a single-device node, the `-sn` option must be used, followed by consensus client specifier (l|d), node_name/node_address, and optionally by geth WS port, consensus HTTP port, and system monitor HTTP port:
- `-sn NODE (l|d) [EXECUTION_WS_PORT CONSENSUS_HTTP_PORT SYSTEM_MONITOR_HTTP_PORT]`
  - **l** option corresponds to non-standard Lighthouse API
  - **d** option corresponds to to standard ETH Beacon Node API
  - optional ports are specified from left to right (i.e., if there is one port, it corresponds to **EXECUTION_WS_PORT**; if there are two, they correspond to **EXECUTION_WS_PORT** and **CONSENSUS_HTTP_PORT**)
  - example: 
    `-sn node0.local d 8546 5052 7197`

To add a dual-device node, the `-dn` option must be used, followed by node name, execution client device (and optional ports: WS port and system monitor port), consensus client device, consensus client specifier(l|d) (and options ports: consensus HTTP port and system monitor HTTP port):
- `-dn NODE_NAME EXECUTION_DEVICE [EXECUTION_WS_PORT SYSTEM_MONITOR_HTTP_PORT] CONSENSUS_DEVICE (l|d) [CONSENSUS_HTTP_PORT SYSTEM_MONITOR_HTTP_PORT]`
  - **l** option corresponds to non-standard Lighthouse API
  - **d** option corresponds to to standard ETH Beacon Node API
  - optional ports are specified from left to right for both devices (i.e., if there is one port in the execution device section, it corresponds to **EXECUTION_WS_PORT**; if there are two, they correspond to **EXECUTION_WS_PORT** and **SYSTEM_MONITOR_HTTP_PORT**)
  - example: 
    `-dn dual0 exec_device0.local 8546 7197 consensus_device0.local 5052 7197`

Each option (`-sn`, `-dn`) can be used multiple times to specify numerous nodes. A single-device node uses the provided host to get the node name. The node name must be provided explicitly in dual-device setups, as two devices have no preferred host name.

#### Examples

##### One single-device node
Example command with more and more optional arguments added explicitly:
- shortest command command (default consensus API used to query consensus client, node host, database host):
  ```shell
  python3 nodemonitor.py -sn node0.local d -db localhost
  ```
- Additionally, Geth port specified:
  ```shell
  python3 nodemonitor.py -sn node0.local d 8546 -db localhost
  ```
- Additionally, Geth port and consensus port specified:
  ```shell
  python3 nodemonitor.py -sn node0.local d 8546 5052 -db localhost
  ```
- Additionally, Geth port, consensus port, and system monitor port are specified:
  ```shell
  python3 nodemonitor.py -sn node0.local d 8546 5052 7197 -db localhost
  ```
- Additionally, Geth port, consensus port, system monitor port, and database port are specified:
  ```shell
  python3 nodemonitor.py -sn node0.local d 8546 5052 7197 -db localhost -dbp 8086
  ```
- Additionally, Geth port, consensus port, system monitor port, database port, and database credentials are specified:
  ```shell
  python3 nodemonitor.py -sn node0.local d 8546 7197 -db localhost -dbp 8086 -dbc geth geth ethonrpi
  ```
- Additionally, Geth port, consensus port, system monitor port, database port, database credentials, and active wait delay option are specified:
  ```shell
  python3 nodemonitor.py -sn node0.local d 8546 7197 -db localhost -dbp 8086 -dbc geth geth ethonrpi -wa 7
  ```

All the above commands correspond to the entire command below:
```shell
python3 nodemonitor.py -sn node0.local d 8546 5052 7197 -db localhost -dbp 8086 -dbc geth geth ethonrpi -wa 7 -wd 10
```

##### One dual-device node
Shortest command command (node name: dual0, default consensus API used to query consensus client, node host, database host):
```shell
python3 nodemonitor.py -dn dual0 exec_dev0.local consensus_dev0.local d -db localhost
```

The command above commands correspond to the entire command below:
```shell
python3 nodemonitor.py -dn dual0 exec_dev0.local 8546 7197 consensus_dev0.local d 5052 7197 -db localhost -dbp 8086 -dbc geth geth ethonrpi -wa 7 -wd 10
```

##### Multiple nodes with different-configurations
Shortest command command two single-device nodes and two dual-device nodes:
```shell
python3 nodemonitor.py -sn node0.local d -sn node1.local d -dn dual0 exec_dev0.local consensus_dev0.local d -dn dual1 exec_dev1.local consensus_dev1.local d -db localhost
```

The command above commands correspond to the entire command below:
```shell
python3 nodemonitor.py -sn node0.local d 8546 5052 7197 -sn node1.local d 8546 5052 7197 -dn dual0 exec_dev0.local 8546 7197 consensus_dev0.local d 5052 7197 -dn dual1 exec_dev1.local 8546 7197 consensus_dev1.local d 5052 7197 -db localhost -dbp 8086 -dbc geth geth ethonrpi -wa 7 -wd 10
```

#### Detailed configuration

##### General config
Running the app with `-h` or `--help` displays detailed usage instructions:
```shell
usage: nodemonitor.py [-h] [-sn endpoint consensus_type(l|d) [exec_port consensus_port sys_port ...]] [-dn node_name endpoint_exec [exec_port exec_sys_port] endpoint_consensus
                      endpoint consensus_type(l|d) [consensus_port consensus_sys_port] [...]] -db HOST [-dbp PORT] [-dbc USER PASS DATABASE] [-wa SECS] [-wd SECS]

Simple application to monitor Ethereum on Raspberry Pi nodes

options:
  -h, --help            show this help message and exit

Nodes:
  Ethereum nodes list

  -sn endpoint consensus_type(l|d) [exec_port consensus_port sys_port ...], --single_device_node endpoint consensus_type(l|d) [exec_port consensus_port sys_port ...]
                        Single-Device Ethereum node. Consensus clients: Lighthouse[l], GenericConsensusClient[d] (-sn can be used arbitrary number of times)
  -dn node_name endpoint_exec [exec_port exec_sys_port] endpoint_consensus endpoint consensus_type(l|d) [consensus_port consensus_sys_port] [ ...], --dual_device_node node_name endp
oint_exec [exec_port exec_sys_port] endpoint_consensus endpoint consensus_type(l|d) [consensus_port consensus_sys_port] [ ...]
                        Dual-Device Ethereum node Consensus clients: Lighthouse[l], GenericConsensusClient[d] (-dn can be used arbitrary number of times)

Database:
  Database parameters

  -db HOST, --database_host HOST
                        InfluxDB host
  -dbp PORT, --database_port PORT
                        InfluxDB port
  -dbc USER PASS DATABASE, --database_credentials USER PASS DATABASE
                        InfluxDB login credentials and a database name to use

Wait:
  Wait duration between samples

  -wa SECS, --wait_active SECS
                        Time between two samples when Ethereum node is active
  -wd SECS, --wait_degraded SECS
                        Time between two samples when not all clients are active (including inactive state)

Additional information regarding components configuration.

This application uses the following services:
  - InfluxDB
  - basic-system-monitor

Supported Ethereum clients:
  - execution: Geth
  - consensus: Lighthouse, Nimbus

Endpoint configuration details:
  - execution client (geth) is queried via a web socket, which requires proper client arguments, at least --ws argument (and optionally: --ws.addr 0.0.0.0 --ws.origins '*')
  - consensus client is queried via HTTP, which requires at least --http argument (and optionally --http-address 0.0.0.0)
  - basic-system-monitor must be running on each of the monitored devices
  - Default execution endpoint websocket listen port: 8546
  - Default consensus endpoint http listen port:      5052
  - Default basic-system-monitor http listen port:    7197

Custom consensus client sampling options
  - l flag forces sampler to use non-standard Lighthouse API to sample consensus client
  - d flag sets the default beacon API to in the sampler to query consensus client

InfluxDB:
  - InfluxDB is used to store data samples displayed by Grafana
  - Default InfluxDB http port: 8086
  - To interact with InfluxDB: a username, password, and an existing database name must be provided
  - Default values - user: geth, pass: geth, database: ethonrpi
```

#### Remarks
Configured names (node name, geth endpoint, and nimbus/lighthouse endpoint) are used both to connect to clients (geth and lighthouse) and to generate stats data pushed to InfluxDB (these names are used as tags, used in Grafana).

When the remote system monitor is not responding, it is treated as if the whole node is down.

#### Grafana
In order to use the data from this monitor in Grafana, InfluxDB has to be configured as a data source. Host names are used as tags in the database to retrieve required measurements (CPU load, DISK use, MEM and SWAP use, SYNC progress, including block number). Based on the names used in this document, Grafana is available via URL:
- `http://statsserver.local:3000`

An example Grafana dashboard prepared to work with this monitoring tool is available for [download or inspection](grafana/dashboard_v01.json).
