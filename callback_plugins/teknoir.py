from ansible.plugins.callback import CallbackBase

class CallbackModule(CallbackBase):
    """This is an ansible callback plugin that save failed_devices to a file
    """
    def v2_playbook_on_stats(self, stats):
        """Display info about playbook statistics"""
        hosts = sorted(stats.processed.keys())

        failed_devices_file = 'failed_devices'
        successful_devices_file = 'successful_devices'
        failed_devices = []
        successful_devices = []

        for h in hosts:
            t = stats.summarize(h)
            if t['failures'] > 0 or t['unreachable'] > 0:
                failed_devices.append(h)
            else:
                successful_devices.append(h)

        with open(failed_devices_file, 'w') as outfile:
             outfile.write(' '.join(failed_devices))

        with open(successful_devices_file, 'w') as outfile:
            outfile.write(' '.join(successful_devices))
