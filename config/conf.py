APP_DESCRIPTION = "Simple application to monitor Ethereum on Raspberry Pi nodes"
APP_EPILOG = "Additional information regarding components configuration.\n\n"\
             "This application uses the following services:\n" \
             "  - InfluxDB\n" \
             "  - basic-system-monitor\n\n" \
             "Supported Ethereum clients:\n" \
             "  - execution: Geth\n" \
             "  - consensus: Lighthouse, Nimbus\n\n" \
             "Endpoint configuration details:\n" \
             "  - execution client (geth) is queried via a web socket, which requires proper client arguments, " \
             "at least --ws argument (and optionally: --ws.addr 0.0.0.0 --ws.origins '*')\n" \
             "  - consensus client is queried via HTTP, which requires at least --http argument (and optionally " \
             "--http-address 0.0.0.0)\n" \
             "  - basic-system-monitor must be running on each of the monitored devices\n" \
             "  - Default execution endpoint websocket listen port: 8546\n" \
             "  - Default consensus endpoint http listen port:      5052\n" \
             "  - Default basic-system-monitor http listen port:    7197\n\n" \
             "Custom consensus client sampling options\n" \
             "  - l flag forces sampler to use non-standard Lighthouse API to sample consensus client\n" \
             "  - d flag sets the default beacon API to in the sampler to query consensus client\n\n" \
             "InfluxDB:\n" \
             "  - InfluxDB is used to store data samples displayed by Grafana\n" \
             "  - Default InfluxDB http port: 8086\n" \
             "  - To interact with InfluxDB: a username, password, and an existing database name must be provided\n" \
             "  - Default values - user: geth, pass: geth, database: ethonrpi"

# Default configuration
LIGHTHOUSE_LETTER = 'l'
GENERIC_CONSENSUS_CLIENT_LETTER = 'd'

DEFAULT_GETH_WS_PORT = 8546
DEFAULT_GETH_SYSTEM_PORT = 7197

DEFAULT_CONSENSUS_CLI_HTTP_PORT = 5052
DEFAULT_SYSTEM_MONITOR_PORT = 7197

DEFAULT_INFLUX_DB_PORT = 8086

DEFAULT_INFLUX_USER = "geth"
DEFAULT_INFLUX_PASS = "geth"
DEFAULT_INFLUX_DATABASE = "ethonrpi"

DEFAULT_DELAY_BOTH_ACTIVE = 7.0
DEFAULT_DELAY_DEGRADED = 10.0

DEFAULT_INFLUXDB_FLUSH_INTERVAL = int(1000.0 * (DEFAULT_DELAY_BOTH_ACTIVE + 0.05))
DEFAULT_INFLUXDB_BATCH_SIZE = 75
