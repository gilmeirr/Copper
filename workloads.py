
from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import FunctionItem, SubmenuItem, CommandItem
import json


class Workload():
    
    def __init__(self) -> None:
        self.cmd = None
    def get_cmd(self):
        return self.cmd
    def menu(self):
        """
        Showing Workload menu to get all running parameters
        """
        raise NotImplementedError("Subclasses should implement this method")
    def post_process(self):
        raise NotImplementedError("Subclasses should implement this method")

class SpecWin(Workload):

    def __init__(self) -> None:
        super().__init__()
        self.subworkloads  = ["intrate","fprate","500.perlbench_r","502.gcc_r","505.mcf_r","520.omnetpp_r","523.xalancbmk_r","525.x264_r",
                         "531.deepsjeng_r","541.leela_r","548.exchange2_r","557.xz_r","503.bwaves_r","507.cactuBSSN_r","508.namd_r",
                         "510.parest_r","511.povray_r","519.lbm_r","521.wrf_r","526.blender_r","527.cam4_r","538.imagick_r","544.nab_r","549.fotonik3d_r","554.roms_r"]
        with open ('spec_compilers_conf.json') as file:
            self.compiler_conf = json.load(file)
        self.swl = self.subworkloads[2]
        comp = list(self.compiler_conf.keys())[0]
        self.spec_dir = f"C:\\Applications\\{self.compiler_conf[comp]['folder']}"
        st = True
        if st:
            self.config_file = self.compiler_conf[comp]["st"]
        else:
            self.config_file = self.compiler_conf[comp]["mt"]
        self.script = self.compiler_conf[comp]["script"]
        self.rep = "1"
        self.aff = "0x2"
        self.cmd = f"hopper multi_job add_job hopper.pnp.workloads.perf.spec17.spec17_rate -swl {self.swl} -spec_17_dir {self.spec_dir} -ncopy {'1' if st else 'ALL_LOGICAL'} -c {self.config_file} -script {self.script} -rep {self.rep} -aff {self.aff} --job hopper.pnp.workloads.perf.spec17.spec17_rate"
    def menu(self):
        spec_menu = ConsoleMenu("Spec Windows Menu", exit_option_text="Continue")
        swl_menu = SelectionMenu(self.subworkloads, title="Select subworkload",)
        swl_item = SubmenuItem("Select subworkload", swl_menu, menu=spec_menu)
        comp_menu = SelectionMenu(self.compiler_conf.keys(), title="Select Compiler")
        comp_item = SubmenuItem("Compiler", comp_menu, menu=spec_menu)
        stmt = ["st", "mt"]
        st_menu = SelectionMenu(stmt)
        st_item = SubmenuItem("Select ST or MT", st_menu, menu=spec_menu)
        rep_item = FunctionItem("Iterations", input, ["Enter Iterations number: "])
        aff_item = FunctionItem("Affinity", input, ["Enter affinity as hex mask: "])
        spec_menu.append_item(swl_item)
        spec_menu.append_item(comp_item)
        spec_menu.append_item(st_item)
        spec_menu.append_item(rep_item)
        spec_menu.append_item(aff_item)
        spec_menu.show()
        self.swl = self.subworkloads[swl_menu.selected_option]
        comp = list(self.compiler_conf.keys())[comp_menu.selected_option]
        self.spec_dir = f"C:\\Applications\\{self.compiler_conf[comp]['folder']}"
        st = True if st_menu.selected_option == 0 else False
        if st:
            self.config_file = self.compiler_conf[comp]["st"]
        else:
            self.config_file = self.compiler_conf[comp]["mt"]
        self.script = self.compiler_conf[comp]["script"]
        self.rep = rep_item.get_return()
        self.aff = aff_item.get_return()
        self.cmd = f"hopper multi_job add_job hopper.pnp.workloads.perf.spec17.spec17_rate -swl {self.swl} -spec_17_dir {self.spec_dir} -ncopy {'1' if st else 'ALL_LOGICAL'} -c {self.config_file} -script {self.script} -rep {self.rep}{' -aff ' if st else ''}{self.aff if st else ''} --job hopper.pnp.workloads.perf.spec17.spec17_rate"