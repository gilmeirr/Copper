from utils import MultiJobWrapper
import workloads
from consolemenu import ConsoleMenu, Screen
from consolemenu import SelectionMenu
from consolemenu.items import FunctionItem, SubmenuItem, CommandItem
from consolemenu.prompt_utils import PromptUtils

# def get_spec_win_sub_menu():
#     spec_menu = 

workloads_str = ["Spec Win", "dscds1"]
# workloads_types = [workloads.SpecWin]

# print("Welcome to Copper - An interface for hopper MultiJob")
# name = input("Enter MultiJob name: ")
exit = False
entry_menu = ConsoleMenu(title="Welcome to Copper - An interactive menu for running hopper multijob")
multi_job_name = FunctionItem("Create new multi-job", input, ["Enter Multi-job name:"], should_exit=True)
entry_menu.append_item(multi_job_name)
entry_menu.show()
multi_job = MultiJobWrapper(multi_job_name.return_value)
multi_job_optios = ["Add Job", "Show Jobs", "Run multiJob"]
while not exit:
    jobs_menu = SelectionMenu(multi_job_optios, title=f"Select an option for multiJob {multi_job.name}")
    sel = jobs_menu.get_selection(multi_job_optios)
    if sel == 0:
        workload_menu = SelectionMenu(workloads_str, title="Select Workload",)
        workload = workload_menu.get_selection(workloads_str)
        if workload == 0: #spec win
            job = workloads.SpecWin()
        job.menu()
        multi_job.add_job(job)
    elif sel == 1:
        prompt = PromptUtils(Screen())
        for job in multi_job.get_jobs():
            print(job.get_cmd())
        prompt.enter_to_continue()
    elif sel == 2:
        multi_job.run()
        exit = True
    else:
        exit = True