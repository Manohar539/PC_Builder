class CompatibilityChecker:

    @staticmethod
    def check_cpu_motherboard(cpu_socket, motherboard_socket):

    
        if not cpu_socket or not motherboard_socket:
            return True

    
        return cpu_socket == motherboard_socket


def check_cpu_motherboard(cpu_socket, motherboard_socket):

    checker = CompatibilityChecker()

    return checker.check_cpu_motherboard(cpu_socket, motherboard_socket)