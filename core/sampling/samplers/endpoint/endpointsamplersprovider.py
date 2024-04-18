from core.sampling.readers.readersprovider import ReadersProvider
from core.sampling.samplers.endpoint.endpointsamplers.batchsampler import BatchEndpointSampler
from core.sampling.samplers.endpoint.endpointsamplers.endpointsampler import EndpointSampler
from core.sampling.samplers.endpoint.transformers.gethdatatransformers import GethDataTransformerSyncing, \
    GethDataTransformerBlockNumber
from core.sampling.samplers.endpoint.transformers.lighthousedatatransformers import LighthouseDataTransformerSyncing,\
    LighthouseDataTransformerSyncingEth1
from core.sampling.samplers.endpoint.transformers.genericconsensusdatatransformers import \
    GenericConsensusDataTransformerHealth, GenericConsensusDataTransformerSyncing
from core.sampling.samplers.endpoint.transformers.systemdatatransformers import SystemStatusDataTransformer


class EndpointSamplersProvider:

    @classmethod
    def geth_endpoint_sampler(cls, endpoint_url: str) -> EndpointSampler:
        assert endpoint_url.startswith("ws://")

        queries = [
            '{"jsonrpc":"2.0","method":"eth_syncing","params":[],"id": 17}',
            '{"method":"eth_blockNumber","params":[],"id":1,"jsonrpc":"2.0"}'
        ]

        transformers = [
            GethDataTransformerSyncing(),
            GethDataTransformerBlockNumber()
        ]

        return BatchEndpointSampler(ReadersProvider.geth_websocket_reader(endpoint_url), queries, transformers)

    @classmethod
    def lighthouse_endpoint_sampler(cls, endpoint_url: str) -> EndpointSampler:
        queries = [
            '/lighthouse/eth1/syncing',
            '/lighthouse/syncing'
        ]

        transformers = [
            LighthouseDataTransformerSyncingEth1(),
            LighthouseDataTransformerSyncing()
        ]

        return BatchEndpointSampler(ReadersProvider.json_http_reader(endpoint_url), queries, transformers)

    @classmethod
    def generic_consensus_endpoint_sampler(cls, endpoint_url: str) -> EndpointSampler:
        queries = [
            '/eth/v1/node/health',
            '/eth/v1/node/syncing',
        ]

        transformers = [
            GenericConsensusDataTransformerHealth(),
            GenericConsensusDataTransformerSyncing()
        ]

        return BatchEndpointSampler(ReadersProvider.json_http_reader(endpoint_url), queries, transformers)

    @classmethod
    def system_endpoint_sampler(cls, endpoint_url: str) -> EndpointSampler:
        queries = [
            '/node/system/status'
        ]

        transformers = [
            SystemStatusDataTransformer()
        ]

        return BatchEndpointSampler(ReadersProvider.json_http_reader(endpoint_url), queries, transformers)
