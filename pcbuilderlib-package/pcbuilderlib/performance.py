class PerformanceEstimator:

    def estimate(self, cpu_name, gpu_name):

        if gpu_name is None:
            return "Unknown Performance"

        gpu_name = gpu_name.lower()

        if "4090" in gpu_name or "4080" in gpu_name:
            return "Ultra Gaming Performance"

        if "3070" in gpu_name or "3060" in gpu_name:
            return "High Gaming Performance"

        if "1660" in gpu_name or "1650" in gpu_name:
            return "Standard Gaming Performance"

        if "integrated" in gpu_name:
            return "Basic Office Performance"

        return "Standard Performance"


def estimate_performance(cpu_name, gpu_name):

    estimator = PerformanceEstimator()

    return estimator.estimate(cpu_name, gpu_name)