import threading
import time
from queue import Queue

from core.sampling.samplers.node.nodesampler import NodeSampler
from core.sampling.samplingunit.threading.waitpolicy import WaitPolicy


class NodeSamplingThread(threading.Thread):

    def __init__(self, sampler: NodeSampler, wait_policy: WaitPolicy, queue: Queue) -> None:
        super().__init__(daemon=True)

        self.sampler: NodeSampler = sampler

        self.wait_policy = wait_policy
        self.queue = queue

        self.quit = False

    def run(self) -> None:
        while not self.quit:
            st = time.time()
            sample = self.sampler.sample_node()
            self.queue.put(sample)
            time.sleep(max(0.0, self.wait_policy.get_current_delay(sample) - (time.time() - st)))

    def shutdown(self) -> None:
        self.quit = True
        self.join()
