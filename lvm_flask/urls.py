from flask import views,render_template,url_for,request,jsonify
from lvm_flask import models

class lvmHome(views.View):
    def __init__(self):
        self.i = models.get_disk_partition_name(1)
        self.PVName = models.get_PV_name()
        self.VGName = models.get_VG_name()
        self.LVName = models.get_LV_name()

    def dispatch_request(self):
        context={
            'allDiskData' : self.i,
            'allPVName' : self.PVName,
            'lenPVName' : len(self.PVName),
            'allVGName' : self.VGName,
            'lenVGName': len(self.VGName),
            'allLVName' : self.LVName,
            'lenLVName': len(self.LVName)
        }
        return render_template('lvmStart.html',**context)


class lvmInstall(views.View):
    def dispatch_request(self):
        return render_template('lvmInstall.html')


class lvmfunc(views.MethodView):
    def get(self):
        global pvcreateResult
        global pvremoveResult
        global vgcreateResult
        global vgremoveResult
        global vgAllPVName
        global lvcreateResult
        pvcreateResult=''
        pvremoveResult=''
        vgcreateResult=''
        vgremoveResult=''
        vgAllPVName=''
        lvcreateResult=''
        if request.args.get('pvcreatedata'):
            pvcreateResult = models.export_pvcreate_result(request.args.get('pvcreatedata'))
        if request.args.get('pvremovedata'):
            pvremoveResult = models.export_pvremove_result(request.args.get('pvremovedata'))
        if request.args.get('vgcreatedata') and request.values.get('vgCreateName'):
            vgcreateResult = models.export_vgcreate_result(request.values.get('vgCreateName'),request.args.get('vgcreatedata'))
        if request.args.get('vgremovedata'):
            vgremoveResult = models.export_vgremove_result(request.args.get('vgremovedata'))
        if request.args.get('vgextenddata'):
            vgAllPVName = models.get_VG_PV(request.args.get('vgextenddata'))
        if request.args.get('lvcreateName') and request.args.get('lvcreateSize') and request.args.get('lvcreatedata'):
            lvcreateResult = '%s successfully created' % request.args.get('lvcreateName')
        return 'test'

    def post(self):
        return 'post'


class lvmexport(views.MethodView):
    def get(self):
        global pvcreateResult
        global pvremoveResult
        global vgcreateResult
        global vgremoveResult
        global vgAllPVName
        global lvcreateResult
        #print ('pvremoveResult:',pvremoveResult)
        message_json = {
            "pvcreateResult": pvcreateResult,
            "pvremoveResult": pvremoveResult,
            "vgcreateResult": vgcreateResult,
            "vgremoveResult": vgremoveResult,
            "vgAllPVName" : vgAllPVName,
            "lvcreateResult" : lvcreateResult,
        }
        return jsonify(message_json)


class lvmShow(views.View):
    def __init__(self):
        self.i = models.get_disk_partition_name(1)
        self.allPVName = models.get_PV_name()
        self.allVGName = models.get_VG_name()
        self.allLVName = models.get_LV_name()

    def dispatch_request(self):
        context={
            'allDiskData': self.i,
            'allPVName' : self.allPVName,
            'allVGName': self.allVGName,
            'allLVName' : self.allLVName

        }
        return render_template('lvmChild.html',**context)


class PhysicalVolume(views.View):
    pass