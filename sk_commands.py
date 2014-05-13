# sk_scriptCollection
import math
from win32com.client import constants as c
from win32com.client.dynamic import Dispatch

XSIFactory = Dispatch("XSI.Factory")

null = None
false = 0
true = 1

app = Application
log = app.Logmessage
oSel = app.Selection
oRoot = app.ActiveSceneRoot
oScene = app.ActiveProject.ActiveScene
oPass = oScene.ActivePass

def XSILoadPlugin( in_reg ):
	in_reg.Author = "sekow"
	in_reg.Name = "sk_commands"
	in_reg.Email = ""
	in_reg.URL = ""
	in_reg.Major = 1
	in_reg.Minor = 0

	in_reg.RegisterCommand("sk_parentUnderNull","sk_parentUnderNull")
	# in_reg.RegisterCommand("sk_addToPartition","sk_addToPartition")
	#in_reg.RegisterCommand("sk_groupToPartition","sk_groupToPartition")
	#in_reg.RegisterCommand("sk_assignOwnersToMat","sk_assignOwnersToMat")
	in_reg.RegisterCommand("sk_setSceneCamera","sk_setSceneCamera")
	#in_reg.RegisterCommand("sk_membersSorting","sk_membersSorting")
	#in_reg.RegisterCommand("sk_inspectActivePass","sk_inspectActivePass")
	in_reg.RegisterCommand("sk_renamer","sk_renamer")
	in_reg.RegisterCommand("sk_startup","sk_startup")
	in_reg.RegisterCommand("sk_setStaticKine","sk_setStaticKine")
	in_reg.RegisterCommand("sk_pointCloud","sk_pointCloud")
	#in_reg.RegisterCommand("sk_camRig","sk_camRig")
	#in_reg.RegisterCommand("sk_cachePath","sk_cachePath")
	in_reg.RegisterCommand("sk_timewarpProp","sk_timewarpProp")
	#in_reg.RegisterCommand("sk_setRenderPaths", "sk_setRenderPaths")
	#in_reg.RegisterCommand("lao_buffer", "lao_buffer")
	# in_reg.RegisterCommand("sk_freeze", "sk_freeze")
	in_reg.RegisterCommand("sk_freezeModeling", "sk_freezeModeling")
	#in_reg.RegisterCommand("sk_gridSort", "sk_gridSort")
	# in_reg.RegisterCommand("sk_addChild", "sk_addChild")
	in_reg.RegisterCommand('sk_selectInstanceMaster', 'sk_selectInstanceMaster')
	#in_reg.RegisterCommand('sk_get_selectedIceNodes', 'sk_get_selectedIceNodes')
	in_reg.RegisterCommand("sk_layout_MCP", "sk_layout_MCP")
	in_reg.RegisterCommand("sk_layout_PLAYBACK", "sk_layout_PLAYBACK")
	in_reg.RegisterCommand("sk_layout_MODULES", "sk_layout_MODULES")


	#RegistrationInsertionPoint - do not remove this line

	return true

def XSIUnloadPlugin( in_reg ):
	strPluginName = in_reg.Name
	log(strPluginName + str(" has been unloaded."),c.siVerbose)
	return true

def sk_parentUnderNull_Execute(  ):

	log("parentUnderNull_Execute called",c.siVerbose)
	oNull = app.ActiveSceneRoot.AddNull()
	for i in app.Selection:
		oNull.AddChild(i)
	
	log("done")
		
	return true

# def sk_addToPartition_Execute(  ):

	# log("sk_addToPartition_Execute called",c.siVerbose)

	# oPicked = app.PickElement(c.siObjectPartitionFilter)
	# oPartition = oPicked(2)
	# log(oPartition.Name)

	# for item in app.Selection:
		# oPartition.AddMember(item)
	
	# log("done")
	
	# return true
	
def sk_groupToPartition_Execute(  ):
	
	oGroups = XSIFactory.CreateObject("XSI.Collection")

	pickEnd = 1
	while pickEnd != 0:
		oPicked = app.PickElement(c.siGroupFilter)
		if oPicked(1) == 1:
			oGroups.Add(oPicked(2))
		else:
			pickEnd = 0

	for oGroup in oGroups:
		oPartition = oPass.CreatePartition(oGroup.Name[:-1]+"p",1)
		for oMember in oGroup.Members:
			oPartition.AddMember(oMember)

	log("done")
	
	return true

def sk_assignOwnersToMat_Execute():
	
	oColl = XSIFactory.CreateObject('XSI.Collection')

	for i in oSel:
		for o in i.Owners:
			log(o.Type)
			if o.Type == 'polymsh' or o.Type == 'poly':
				oColl.Add(o)
				
	oPicked = app.PickElement()
	oMat = oPicked[2]

	for item in oColl:
		item.SetMaterial(oMat)

	log('done')
	
	return true
	
	
def sk_setSceneCamera_Execute():
	
	oCam = app.PickElement(c.siCameraFilter)[2]

	for oPass in oScene.Passes:
		
		oPass.Camera.Value = oCam
		log(oCam.Name + ' set in ' + oPass.Name)
# --- setting mental ray properties ---		
#		for oProp in oPass.Properties:
#			if oProp.Type == "mentalray":
#				oProp.Parameters("SamplesMin").Value = 1
#				oProp.Parameters("SamplesMax").Value = 3
#				oProp.Parameters("SamplesContrastRed").Value = 0.05
#				oProp.Parameters("SamplesContrastGreen").Value = 0.05		
#				oProp.Parameters("SamplesContrastBlue").Value = 0.05
#				oProp.Parameters("SamplesContrastAlpha").Value = 0.05	
#				oProp.Parameters("TraceDepthReflection").Value = 2
#				oProp.Parameters("TraceDepthRefraction").Value = 2		
#				oProp.Parameters("TraceDepthCombined").Value = 4		
#				oProp.Parameters("VisibleGeometryFace").Value = 0
		
	log('done')
	
	return true

def sk_membersSorting_Execute():

	oColl = XSIFactory.CreateObject('XSI.Collection')

	pickEnd = 1
	while pickEnd != 0:
		oPicked = app.PickElement(c.siGroupFilter)
		log(oPicked[2].Name)
		if oPicked[1] == 1:
			for oMember in oPicked[2].Members:
				log(oMember.Name)
				oColl.Add(oMember)
		else:
			for oMember in oPicked[2].Members:
				log(oMember.Name)
				oColl.Add(oMember)
			pickEnd = 0

#	sourcePicked = app.PickElement(c.siGroupFilter)
#

	log(oColl.Count)
	targetPicked = app.PickElement(c.siGroupFilter)

	for item in oColl:
		#log(item.Name)
		targetPicked[2].AddMember(item)

	log('done')
	
	return true
	
def sk_inspectActivePass_Execute():
	
	oPass = app.ActiveProject.ActiveScene.ActivePass
	app.InspectObj(oPass)
	log(oPass.Name)
	
	return true

def sk_renamer_Execute():
	
	renameProp = XSIFactory.CreateObject("CustomProperty")
	renameProp.name = 'sk_renamer'
	renameProp.AddParameter2("search",c.siString)
	renameProp.AddParameter2("write",c.siString)
	layout = renameProp.PPGLayout
	layout.Language = "Python"
	layout.AddItem('search')
	#layout.AddStaticText('leave empty for pre or sufix')
	layout.AddItem('write')
	layout.AddStaticText('''leave search field empty for pre or suffix naming. 
example: prefix_ or _suffix''')
	layout.AddButton('rename')

	sLogic = '''

app = Application
log = app.Logmessage
sel = app.Selection

def rename_OnClicked():
	
	oPPG = PPG.Inspected[0]
	oSearch = oPPG.search.Value
	oWrite = oPPG.write.Value

	if len(oSearch):
	
		for item in sel:
			oName = item.Name
			item.Name = oName.replace(oSearch,oWrite)
	else:
		if oWrite[0] == '_':
		
			for item in sel:
				oName = item.Name
				item.Name = oName + oWrite
		elif oWrite[-1] == '_':
			
			for item in sel:
				oName = item.Name
				item.Name = oWrite + oName
		else:
			
			for item in sel:
				item.Name = oWrite

	'''

	layout.Logic = sLogic	
	app.InspectObj(renameProp)
	
	
def sk_startup_Execute():

	viewports = Application.Desktop.ActiveLayout.Views('vm')
	viewports.setattributevalue('layout','default')
	viewports.setattributevalue('activecamera:b','User')
	viewports.setattributevalue('viewport:a','ICE Tree')
	viewports.setattributevalue('viewport:d','Explorer')
	viewports.setattributevalue('layout','vertical:ac')

def sk_setStaticKine_Execute():

	for item in oSel:
		if item.Properties('Static_KineState') == None:
			item.AddProperty('Static Kinematic State Property')

		app.SetEnvelopeRefPoses(item)
		
def sk_pointCloud_Execute():
	cloudName  = app.XSIInputBox('cloud Name','','cache')
	if not oSel(0):
		oCloud = oRoot.AddGeometry('Pointcloud','',cloudName)
		app.ApplyOp('ICETree',oCloud)
	else:
		if oSel(0).Type == '#model':
			oCloud = oSel(0).AddGeometry('Pointcloud','',cloudName)
			app.ApplyOp('ICETree',oCloud)
		else:
			oCloud = oRoot.AddGeometry('Pointcloud','',cloudName)
			app.ApplyOp('ICETree',oCloud)
	
def sk_camRig_Execute():

	oShot = app.XSIInputBox('shot','','F01S010') # prompt user, or automatic from scene info

	# check if selection is a camera and set proper settings
	# cam gate x = 0.945
	# cam focal lenght = 24

	if oSel[0].Type == 'camera':

		oCam = oSel[0]
		tCam = oCam.Kinematics.Global.Transform
		
		oCam.projplanewidth = 0.945
		oCam.projplanedist = 24
		oCam.projplane = 1
		oCam.Name = '_'.join([oShot, oCam.Name])

		oCns = oCam.Kinematics.Constraints
		for i in oCns:
			app.DeleteObj(i)
		
		oCamRT = oCam.Parent
		if oCamRT.Type == 'CameraRoot':
			
			t1 = XSIMath.CreateTransform()
			oCamRT.Kinematics.Global.Transform = t1
			oCamRT.Name = 'Cam_SRT'
		
		# reset cam transform
		
		oCam.Kinematics.Global.Transform = tCam
		
		# rig
		
		rotNull = oCamRT.AddNull()
		rotNull.Name = 'camRot'
		rotNull.primary_icon = 2
		rotNull.Kinematics.Global.Transform = tCam
		tCam.RotX = 0
		tCam.RotY = 0
		tCam.RotZ = 0
		posNull = oCamRT.AddNull()
		posNull.Name = 'camPos'
		posNull.primary_icon = 4
		posNull.Kinematics.Global.Transform = tCam
		
		app.ParentObj(rotNull,oCam)
		app.ParentObj(posNull, rotNull)
		
		oCamMdl = app.ActiveSceneRoot.AddModel()
		oCamMdl.Name = '_'.join(['mdl', oShot, 'camera'])
		
		app.ParentObj(oCamMdl, oCamRT)
		
	else:
		log('thats something, but not a camera')
	
	log('done')

def sk_cachePath_Execute():
	
	oProject = app.ActiveProject2
	lNodes = []
	vm = app.Desktop.ActiveLayout.Views.Find( "View Manager" )
	fc = vm.GetAttributeValue("focusedviewport")
	activeView = vm.Views(fc)
	oNodes = activeView.GetAttributeValue('selection')
	lNodes = oNodes.split(',')
	oPathDir = ''
	for item in lNodes:

		oNode = app.Dictionary.GetObject(item)
		log(oNode.Name)
		if oNode.Name == 'Cache on File':
			oNode.templatepath.Value = 5
			oFileBrowser = XSIUIToolkit.FileBrowser
			if len(oPathDir) == 0:
				oFileBrowser.InitialDirectory = oProject.Path + '\Simulation'
				log(oFileBrowser.InitialDirectory)
			else:
				oFileBrowser.InitialDirectory = oPathDir
				log(oFileBrowser.InitialDirectory)
			oFileBrowser.DialogTitle = 'select a cache file'
			oFileBrowser.ShowOpen()
			oPathDir = oFileBrowser.FilePath
			log('PathDir: ' + oPathDir)
			oPath = oFileBrowser.FilePathName
			oPath = oPath.split('Simulation')
			oPath = oPath[1].split('[')
			oPath = '[project path]\Simulation'+oPath[0]+'[frame].icecache'
			log(oPath)
			oNode.alternativepath.Value = oPath
		else:
			log('no cache node selected' )

def sk_timewarpProp_Execute():
	dParams = {}
	propName  =app.XSIInputBox('Property Name','','timewrap')
	minValue = app.XSIInputBox('first Frame of Cache','',1)
	maxValue = app.XSIInputBox('last Frame of Cache','',150)
	dParams['name'] = propName
	dParams['min'] = int(minValue)
	dParams['max'] = int(maxValue)

	for item in oSel:
		if item.Type == 'pointcloud':
			oTrees = item.ActivePrimitive.ICETrees
			oProp = item.AddCustomProperty(dParams['name'], False)
			oProp.AddParameter3('speedramp', c.siFloat, dParams['min'], dParams['min'], dParams['max'], True, False)
			app.AddICECompoundNode("cache retime", oTrees(0))
		
	
	return True

def sk_setRenderPaths_Execute():
	cpNode = app.ActiveSceneRoot.FindChild('_CP_Data_Node', c.siModelNullPrimType)
	if cpNode:
		
		oProp = [prop for prop in cpNode.Properties if prop.Type == 'CP_RenderSettings'][0]
		sFilm = oProp.Parameters('Film').Value
		sShot = 'S' + oProp.Parameters('Shot').Value
		sVersion = 'V' + oProp.Parameters('Version').Value
		sRenderPath = '\\'.join([oProp.Parameters('Jobpath').Value, 'render', '3D', sFilm, sShot, sVersion])  
		oPath = '[Pass]\[Framebuffer]\%s%s_%s_[Pass]_[Framebuffer]' % (sFilm, sShot, sVersion)
		print sRenderPath + oPath

		buttonPressed = XSIUIToolkit.Msgbox('are you sure?', c.siMsgYesNo)
		if buttonPressed == 6:
			print 'yay'
			oScene = app.ActiveProject2.ActiveScene
			oSceneProp = oScene.PassContainer.Properties( "Scene Render Options" )
			oSceneProp.Parameters('OutputDir').Value = sRenderPath

			for oPass in oScene.Passes:
				for buffer in oPass.Framebuffers:
					buffer.Filename.Value = oPath
		elif buttonPressed == 7:
			print 'nay'
		else:
			print 'error'
		
	else:
		print 'no cp node found!!!'
		
def lao_buffer_Execute():
	for oMat in oSel:
		oShaders = oMat.GetAllShaders()
		oNodes = [item for item in oShaders if item.ProgID == 'Softimage.standard.1.0']
		for oNode in oNodes:
			if oNode:
				oNode.Parameters('aov_direct_diffuse').Value = 'lao_diffD'
				oNode.Parameters('aov_indirect_diffuse').Value = 'lao_diffI'
				oNode.Parameters('aov_direct_specular').Value = 'lao_specD'
				oNode.Parameters('aov_indirect_specular').Value = 'lao_specI'
				oNode.Parameters('aov_refraction').Value = 'lao_refr'
				oNode.Parameters('aov_reflection').Value = 'lao_refl'
			else:
				print 'no shader found'
				pass
# def sk_freeze_Execute():
	# for eachItem in Application.Selection:
		# Application.FreezeObj(eachItem)
		# print 'freeze of %s done' % eachItem.Name
		
def sk_freezeModeling_Execute():
	for eachItem in Application.Selection:
		Application.FreezeModeling(eachItem)
		print 'freeze modeling stack of %s done' % eachItem.Name

def sk_gridSort_Execute():
	spacing = int(app.XSIInputBox('spacing?','','25'))
	d1 = math.floor(math.sqrt(oSel.Count))
	t1 = XSIMath.CreateTransform()
	for i, eachItem in enumerate(oSel):
		t1.PosX = (i % d1) * spacing		
		t1.PosZ = (math.floor(i/d1)) * spacing
		eachItem.Kinematics.Global.Transform = t1
		
# def sk_addChild_Execute():
	# oObj = Application.PickElement(c.siGenericObjectFilter, 'select Parent')[2]
	# map(oObj.AddChild, Application.Selection)
	# for eItem in Application.Selection:
		# oObj.AddChild(eItem)
	# print 'done'

def sk_selectInstanceMaster_Execute():
	oInst = Application.Selection(0)
	if oInst.Type =='#model' and oInst.ModelKind == 2:
		Application.SelectObj(oInst.InstanceMaster)
	else:
		print '%s is not an Instance' % oInst.FullName
		
def sk_layout_MCP_Execute():
	Application.ToggleOptionalPanel("mcp", "")
	return True
	
def sk_layout_PLAYBACK_Execute():
	Application.ToggleOptionalPanel("playback", "")
	return True

def sk_layout_MODULES_Execute():
	Application.ToggleOptionalPanel("module_menu", "")
	return True
	
