from source import lvmShell as ls

DS_C=ls.DiskStatus()
PV_C=ls.PhysicalVolume()
VG_C = ls.VolumeGroup()
LV_C = ls.LogicalVolume()


def get_disk_partition_name(status):
    lis_disk_and_partition_status,lis_disk_and_partition=DS_C.data_to_json()
    if status==0:
        return lis_disk_and_partition_status
    elif status==1:
        return lis_disk_and_partition
    elif status==2:
        return lis_disk_and_partition_status,lis_disk_and_partition

def get_PV_name():
    lis_PV_name=PV_C.shell_pvs()
    return lis_PV_name

def get_VG_name():
    lis_VG_name=VG_C.shell_vgdisplay_vgname()
    return lis_VG_name

def get_LV_name():
    lis_LV_name=LV_C.shell_lvdisplay()
    return lis_LV_name

def export_pvcreate_result(str_name):
    if PV_C.shell_pvcreate(str_name):
        return '%s successfully created' % str_name
    else:
        return '%s fail created' % str_name

def export_pvremove_result(str_name):
    if PV_C.shell_pvremove(str_name):
        return '%s successfully removed' % str_name
    else:
        return '%s fail removed' % str_name

def export_vgcreate_result(str_name,lis_pv):
    lis_pv=[lis_pv]
    if VG_C.shell_vgcreate(str_name,lis_pv):
        return '%s successfully created' % str_name
    else:
        return '%s fail created' % str_name

def export_vgremove_result(str_name):
    if VG_C.shell_vgremove(str_name):
        return '%s successfully removed' % str_name
    else:
        return '%s fail removed' % str_name

def get_VG_PV(str_name):
    return VG_C.shell_vgdisplay_pv(str_name)