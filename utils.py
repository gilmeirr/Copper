# Constants
from workloads import Workload
import subprocess

DEFAULT_DIR = "D:\\SVSHARE\\Results"

class MultiJobWrapper:
    """
    Wrapper for handling hopper multi job
    """
    def __init__(self, name, dir = DEFAULT_DIR ) -> None:
        """
        job_name : str
            The name of the job
        dir : str
            Oprtional directory, DEFAULT_DIR = "D:\\SVSHARE\\Results"
        """
        self.name = name
        self.dir = f"{dir}\\{name}"
        # self.__comm_cmd = "hopper multi_job add_inst -comm_type ps_exec"
        self.jobs = []
    
    def add_job(self, job:Workload):
        self.jobs.append(job)

    def run(self):
        proc = subprocess.Popen("hopper multi_job clear_all", shell=True)
        proc.communicate()
        proc = subprocess.Popen(f"hopper multi_job init {self.dir} -dbg", shell=True)
        proc.communicate()
        #SHOULD CHECK IF SUPPORT NOT ONLY PS_EXEC
        proc = subprocess.Popen("hopper multi_job add_inst -comm_type ps_exec", shell=True)
        proc.communicate()
        for job in self.jobs:
            proc = subprocess.Popen(job.get_cmd(), shell=True)
            proc.communicate()
        proc = subprocess.Popen("hopper multi_job run", shell=True)
        proc.communicate()

    def get_jobs(self):
        return self.jobs