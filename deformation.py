import numpy as np
import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya
import rbf
import sys

dir  = "C:/Users/PC/Desktop/June26/RBF/"

def reset_scene():
	cmds.file(f=True, new=True)

def load_obj(file_name):

	cmds.file(file_name, i=True, type="OBJ")

def export_obj(obj, file_name):
    cmds.select(obj)
    cmds.file(file_name, force=True, options=
    	"groups=0;ptgroups=0;materials=0;smoothing=1;normals=1", 
    	typ="OBJexport", pr=True, es=True)

def deformation():
	#reset_scene()

	#vertexcount = self.newpoints.length()
	#inMeshFn.getVertices(mesh_counts, mesh_connect)
	#polycount = inMeshFn.numPolygons()
	#tempMeshData = OpenMaya.MFnMeshData()
	#tempObject = OpenMaya.MObject()
	#tempObject = tempMeshData.create()
	#newObject = OpenMaya.MObject()
	#MeshFs = OpenMaya.MFnMesh()

	# store vertex coordinations of source object in np.ndarray
	load_obj(dir+"source.obj")

	cmds.select("Mesh")
	vtxSourcePosition = []
	vtxSourceIndexList = cmds.getAttr("Mesh.vrts", multiIndices = True)
	for i in vtxSourceIndexList:
		curPointPosition = cmds.xform("Mesh.pnts["+str(i)+"]", query=True,
			translation=True, worldSpace=True)
		vtxSourcePosition.append(curPointPosition)
	# print type(vtxWorldPosition)
	source_vertices = np.array(vtxSourcePosition)


	# store vertex coordinations of target object in ndarray
	load_obj(dir+"target.obj")

	cmds.select("target_Mesh")
	vtxTargetPosition = []
	vtxTargetIndexList = cmds.getAttr("target_Mesh.vrts", multiIndices = True)
	for i in vtxTargetIndexList:
		curPointPosition = cmds.xform("target_Mesh.pnts["+str(i)+"]", query=True,
			translation=True, worldSpace=True)
		vtxTargetPosition.append(curPointPosition)
	# print type(vtxWorldPosition)
	target_vertices = np.array(vtxTargetPosition)	
	
	# get coordinations in x, y, z
	source_vertices_x = source_vertices[:,0]
	source_vertices_y = source_vertices[:,1]
	source_vertices_z = source_vertices[:,2]

	# sampling
	sample_vertices_x = np.array([])
	sample_vertices_y = np.array([])
	sample_vertices_z = np.array([])
	vertex_num = source_vertices_x.size
	for i in range(0,vertex_num):
		if i%10==0:
			sample_vertices_x = np.append(sample_vertices_x, source_vertices_x[i])
			sample_vertices_y = np.append(sample_vertices_y, source_vertices_y[i])
			sample_vertices_z = np.append(sample_vertices_z, source_vertices_z[i])

	target_vertices_x = target_vertices[:,0]
	target_vertices_y = target_vertices[:,1]
	target_vertices_z = target_vertices[:,2]

	fitting_func = rbf(sample_vertices_x, sample_vertices_y, sample_vertices_z)
	generate_z = fitting_func(target_vertices_x, target_vertices_y)
	result_vertices = np.dstack([target_vertices_x, target_vertices_y, generate_z])

	# mesh deformation on target.obj

	selection = OpenMaya.MSelectionList()
	OpenMaya.MGlobal.getActiveSelectionList( selection )
	iterSel = OpenMaya.MItSelectionList(selection, OpenMaya.MFn.kMesh)

	#while not iterSel.isDone():
		# get dagPath
		#dagPath = OpenMaya.MDagPath()
		#iterSel.getDagPath( dagPath )
		# create empty point array
		#inMeshMPointArray = OpenMaya.MPointArray()
		# create function set and get points in world space
		#currentInMeshMFnMesh = OpenMaya.MFnMesh(dagPath)
		#currentInMeshMFnMesh.getPoints(inMeshMPointArray, OpenMaya.MSpace.kWorld)
		# put each point to a list
		#pointList = []
		#for i in range( inMeshMPointArray.length() ) :
			#pointList.append( [inMeshMPointArray[i][0], inMeshMPointArray[i][1], inMeshMPointArray[i][2]] )


	selection = None		
	cmds.select("target_Mesh")
	selection_list = OpenMaya.MSelectionList()
	selection = cmds.duplicate(selection[0])[0]
	cmds.select(selection)
	selection_list.add(selection)
	dag_path = selection_list.getDagPath(0)

	mfn_set = OpenMaya.MFnMesh(dag_path)
	verts = mfn_set.getPoints(space=OpenMaya.MSpace.kObject)
	new_points = OpenMaya.MPointArray()

	i = 0

	for v in verts:
		v.x = v[i][0]
		v.y = v[i][1]
		v.z = v[i][2]
		new_points.append(v)
		i = i+1

	mfn_set.setPoints(new_points, space=OpenMaya.MSpace.kWorld)

	export_obj("mask_Mesh", dir+"output.obj")
	sys.exit()

def main():
	deformation()


if __name__ == "__main__":
	main()
