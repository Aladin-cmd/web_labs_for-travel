import time
from abc import ABC, abstractmethod
from multiprocessing import Pipe, Process
from typing import Callable, Dict, List

from tqdm import tqdm


class TestUtility(ABC):
    stats_header_line = "Handled number of requests{n_requests} with following stats"

    @abstractmethod
    def run_utility(self, child_conn) -> None:
        pass

    @abstractmethod
    def validate_response(self, data: Dict) -> None:
        pass

    def print_results(self, final_result: List[float]) -> None:
        print("="*20)
        print(self.stats_header_line.format(n_requests=int(final_result[0])))
        print(f"total response time: {final_result[1]} ms\n"
              f"median resposne time: {final_result[2]} ms\n"
              f"average resposne time: {final_result[3]} ms\n"
              f"max response time: {final_result[4]} ms\n"
              f"min response time: {final_result[5]} ms")
        print("="*20)


class StressTest:
    def __init__(self, utility: TestUtility) -> None:
        self.utility = utility

    def send_parallel_requests(self, num_requests) -> List:
        parent_connections = list()
        processes = list()
        for _ in range(num_requests):
            parent_conn, child_conn = Pipe()
            parent_connections.append(parent_conn)
            process = Process(target=self.utility.run_utility,
                              args=(child_conn, ))
            processes.append(process)

        req_send_time_start = time.perf_counter() * 1000

        for process in processes:
            process.start()

        for process in processes:
            process.join()
        all_req_end = time.perf_counter() * 1000
        all_request_finish_time_ms = all_req_end - req_send_time_start

        all_response_times = list()
        for parent_conn in parent_connections:
            response_time, res_json = parent_conn.recv()
            self.utility.validate_response(res_json)
            all_response_times.append(response_time)
        all_response_times.sort()
        mid = num_requests // 2
        median_response_time = (all_response_times[mid] + all_response_times[-mid]) / 2
        total_response_time_ms = sum(all_response_times)
        average_response_time = total_response_time_ms / num_requests
        max_response_time_ms = max(all_response_times)
        min_response_time_ms = min(all_response_times)
        return [num_requests, all_request_finish_time_ms, median_response_time, average_response_time,
                max_response_time_ms, min_response_time_ms]

    def find_max_num_of_requests(self, start, end, within_ms) -> List:
        final_result = [0.] * 6
        while start < end:
            mid = (start+end)//2
            result = self.send_parallel_requests(mid)
            if result[0] <= within_ms:
                final_result = result
                start = mid + 1
            else:
                end = mid - 1
        return final_result

    def get_average_results(self, target: Callable, n_tests: int) -> List:
        test_results = [target() for _ in tqdm(range(n_tests))]
        final_result = [0.]*6
        for i in range(6):
            final_result[i] = sum([result[i] for result in test_results])/n_tests
        return final_result

    def find_best_results_within_some_duration(self, n_tests=50, start=100, end=500, within_ms=1000.):
        final_result = self.get_average_results(
            lambda: self.find_max_num_of_requests(start, end, within_ms), n_tests
        )
        print("="*20)
        print(f"Note: All stats are average of {n_tests} tests")
        self.utility.print_results(final_result)

    def stress_test_for_specific_number_of_reqeusts(self, num_reqeusts_to_check, n_tests=3):
        final_result = self.get_average_results(
            lambda: self.send_parallel_requests(num_reqeusts_to_check), n_tests
        )
        print("="*20)
        print(f"Note: All stats are average of {n_tests} tests")
        self.utility.print_results(final_result)
