# Radial Basis Function Mesh Deformation

- [Radial Basis Function Mesh Deformation](#radial-basis-function-mesh-deformation)
    - [Project Objective](#project-objective)
    - [Development Environment & Library](#development-environment--library)
    - [Building Compilation Environment](#building-compilation-environment)
      - [Linux (Ubuntu 18.04 LTS)](#linux-ubuntu-1804-lts)
      - [Windows](#windows)
    - [Radial Basis Function Interpolation Algorithm](#radial-basis-function-interpolation-algorithm)
      - [Radial Basis Function:](#radial-basis-function)
      - [Interpolation:](#interpolation)
      - [Implementation of RBF on Mesh Deformation:](#implementation-of-rbf-on-mesh-deformation)
    - [Callable API](#callable-api)
      - [RBF](#rbf)
      - [RBF_Deformation](#rbfdeformation)
    - [Error Analysis](#error-analysis)
    - [Alternative Solution](#alternative-solution)

---
### Project Objective
**Radial basis functions** (“RBFs”) are the most versatile and commonly used scattered data interpolation techniques. In this project, we have two mesh objects: **source.obj** and **target.obj**. We need to use RBF interpolation algorithm to fit coordination of vertices in **source.obj**. Using the RBF class we gotten, we need to do mesh deformation on the **target.obj** to get **output.obj** which should have quite similar looking compared to the original source mesh.

### Development Environment & Library
* **Ubuntu 18.04 LTS** and above / **Windows 7** and above
* **Anaconda2** & **Spyder IDE** (Python 3.7)
* **Numpy** & **Scipy** & **PyMesh** and its dependency libraries (**nose, Eigen, PyBind11**)

### Building Compilation Environment
#### Linux (Ubuntu 18.04 LTS)
1. Open terminal and type in `bash Anaconda2-xxxx.xx-Linux-x86_64.sh` to Install **Anaconda2 for Linux** (Python 2.7)
2. `source ~/.bashrc`, `conda init` and `anaconda-navigator` to initialize conda and open anaconda GUI
3. `conda create -n <env_name> python=2.7` to create another conda environment
4. `conda activate <env_name>` to activate conda environment
5. install **Spyder** from anaconda navigator
6. uninstall **pip**, **setuptools**, **numpy**, **scipy** shown in the library list of **<env_name>** (because of version conflicts)
7. `conda install -c conda-forge pymesh2` to install pymesh and dependency libraries
8. run script under directory of scripts and obj files
9. `sudo apt-get install openctm-tools` and `ctmviewer output.obj` to install ctmviewer to view .obj files

#### Windows
1. Install **Python2** or **Python3**
2. Install **Numpy** and **Scipy**, you can follow this [document](https://mukai-lab.org/library/mayanumpy/)
3. Clone **Pymesh** from [GitHub](https://github.com/PyMesh/PyMesh.git), and follow its build & install instruction on [GitHub](https://github.com/PyMesh/PyMesh#build)
4. `python example.py` to run the example script under `\API` folder.
5. Double click `output.obj` to view .obj file.

### Radial Basis Function Interpolation Algorithm
#### Radial Basis Function:
A radial basis function is a real-valued function whose value depends only on the distance from the origin and the norm is usually Euclidean distance.
Commonly used types of radial basis functions include:  
Gaussians: ![equation](http://www.sciweavers.org/tex2img.php?eq=%24%5Cphi%5Cleft%28r%5Cright%29%3De%5E%7B%28-%5Cvarepsilon%20r%29%5E%7B2%7D%7D%24&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)  
Multiquadric: ![equation](http://www.sciweavers.org/tex2img.php?eq=%24%5Cphi%5Cleft%28r%5Cright%29%3D%5Csqrt%7B1%2B%28%5Cvarepsilon%20r%29%5E%7B2%7D%7D%24&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)  
Linear: ![equation](http://www.sciweavers.org/tex2img.php?eq=%24%5Cphi%5Cleft%28r%5Cright%29%3Dr%24&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)  
Cubic: ![equation](http://www.sciweavers.org/tex2img.php?eq=%24%5Cphi%5Cleft%28r%5Cright%29%3Dr%5E%7B3%7D%24&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)  
Thin plate spline: ![equation](http://www.sciweavers.org/tex2img.php?eq=%24%5Cphi%5Cleft%28r%5Cright%29%3Dr%5E%7B2%7D%5Cln%7Br%7D%24&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)  
Inverse quadratic: ![equation](http://www.sciweavers.org/tex2img.php?eq=%24%5Cphi%5Cleft%28r%5Cright%29%3D%5Cfrac%7B1%7D%7B1%2B%28%5Cvarepsilon%20r%29%5E%7B2%7D%7D%24&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)  
Inverse multiquadric: ![equation](http://www.sciweavers.org/tex2img.php?eq=%5Cphi%5Cleft%28r%5Cright%29%3D%5Cfrac%7B1%7D%7B%5Csqrt%7B1%2B%28%5Cvarepsilon%20r%29%5E%7B2%7D%7D%7D%24&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)  
In this script, we use **thin-plate spline function** as kernel function.

#### Interpolation:
Given a set of n distinct data points ![equation](http://www.sciweavers.org/tex2img.php?eq=%24%5C%7Bx_j%5C%7D_%7Bj%3D1%7D%5E%7Bn%7D%24&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) and corresponding data values ![equation](http://www.sciweavers.org/tex2img.php?eq=%24%5C%7Bf_j%5C%7D_%0A%7Bj%3D1%7D%5E%7Bn%7D%24&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0), RBF interpolant is given by ![equation](http://www.sciweavers.org/tex2img.php?eq=%24s%28x%29%20%3D%20%5Csum_%7Bi%3D1%7D%5E%7Bn%7D%20%5Clambda_i%5Cphi%28%5C%7C%5Cmathbf%7Bx%7D-%5Cmathbf%7Bx_i%7D%5C%7C%29%24&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0), where ![equation](http://www.sciweavers.org/tex2img.php?eq=%24x%5Cin%5Cmathbf%7BR%7D%24&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0), is some radial function. The expansion coefficients ![equation](http://www.sciweavers.org/tex2img.php?eq=%24%5Clambda%7B%CE%BB%7D_j%24&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) are determined from the interpolation conditions ![equation](http://www.sciweavers.org/tex2img.php?eq=%24s%28x_j%20%29%3Df_j%2C%20j%3D1%2C%5Cdots%20%2Cn%24&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0), which leads to the following symmetric linear system:
![equation](http://www.sciweavers.org/tex2img.php?eq=%24%5BA%5D%5B%5Clambda%5D%3D%5Bf%5D%24&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0).
For example, consider RBF estimation in two dimensions with an additional polynomial. A polynomial in one dimension is ![equation](http://www.sciweavers.org/tex2img.php?eq=%24a%2Bbx%2Bcx%5E2%2B%5Cdots%24&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) Truncating after the linear term gives a +bx. A similar polynomial in two dimensions is of the form ![equation](http://www.sciweavers.org/tex2img.php?eq=%24a%20%2B%20bx%20%2B%20cy%24&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0). Adding this to the RBF synthesis equation gives  
![equation](http://www.sciweavers.org/tex2img.php?eq=%24%24%5Chat%7Bf%7D%28%5Cmathbf%7Bp%7D%29%3D%5Csum_%7Bk%3D1%7D%5E%7Bn%7D%20c_k%5Cphi%28%5C%7C%5Cmathbf%7Bp%7D-%5Cmathbf%7Bp_k%7D%5C%7C%29%2Bc_%7Bn%2B1%7D.1%2Bc_%7Bn%2B2%7D.x%2Bc_%7Bn%2B3%7D.y%24%24%20&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)  
Here ![equation](http://www.sciweavers.org/tex2img.php?eq=%24p%20%3D%20%28x%2C%20y%29%24&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) is an arbitrary 2D point and P_k are the training points.

#### Implementation of RBF on Mesh Deformation:
Firstly, we call **pymesh.load_mesh()** to load source.obj and target_source.obj. We can get their vertices and faces in form of **<numpy.ndarray shape(vertices_num, 3)>** by calling **.vertices** and **.faces**. Then we choose small number of vertices as control points (50 vertices in the script). In source mesh, we calculate displacements between control points and rest points in x, y, x axis separately. For the two layers of loop 
```python
for i  in range(control_num, vertex_num): 
    for j in range(0, control_num):
```
in each subloop, we calculate distance between each points from one control points and add it into an 1-d array, after that, we form a 2d array 
![equation](http://www.sciweavers.org/tex2img.php?eq=%20%5Cbegin%7Bbmatrix%7D%5Bcp_x%5D%20%26%20%5Bcp_y%5D%20%26%20%5Bcp_z%5D%20%26%20%5Bdisp_i%5D%20%5Cend%7Bbmatrix%7D%20&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)  
and use it to initialize RBF class rbfX, rbfY and rbfZ for ![equation](http://www.sciweavers.org/tex2img.php?eq=%24displacement_X%2C%20displacement_Y%2C%20displacement_Z%24&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0). Then we can bring target vertices into ![equation](http://www.sciweavers.org/tex2img.php?eq=%24rbf_X%2C%20rbf_Y%2C%20rbf_Z%24&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) to calculate corresponding displacement. After that it is easy to get corresponding coordination of vertex. After all loops, we get a 3 1-d arrays of coordination.
Because faces arrays of two mesh are the same, the sequence of vertices are also the same. Then we can easily use the face array gotten from target or source mesh to form output mesh with **pymesh.save_mesh_raw(vertices, faces, voxel = None)**.

### Callable API
#### RBF
RBF class is implemented to fitting a 4 dimensions data [[para1],[para2],[para3],[para4]]and predict the column data with a 3 dimensions data.
sample code is provided below.
```python
from RBF import RBF
fitting_func = RBF(para1, para2, para3, para4)
result = fitting_func(para5, para6, para7)
# all parameters are <numpy.ndarray> and shape is (size,)
````
#### RBF_Deformation
RBF mesh deformation is written in callable class and provided in `/API/` folder. After import **RBF_Deformation** module, we need to use target mesh, source mesh and number of control points to initialize the class. Then, we can assign a name to the output mesh .obj file.
* `RBF_Deformation(directory_of_target_mesh, directory_of_source_mesh, num_control_points)`
* `Object(name_of_output_mesh)`

**example.py** is provided below.

```python
from RBF_Deformation import RBF_Deformation

Deformation = RBF_Deformation("target", "source", 50)
Deformation("output")
```

### Error Analysis
We calculate the error with a simple loop:
```python
percentage = 0
for i in rage(0, size):
	percentage += abs(source[i]-output[i])/source[i]
	percentage /= size
```
Based on the two example mesh file in the directory, the error we get is 0.04% on average. (on axis x, y and z)

### Alternative Solution
1. The solution shown above is calculating the coordination in three axes separately, we can also control coordination on x and y axis as independent variables and use RBF class to fitting the value of z coordination.
The problem of this solution is the error is larger than the previous one and the effect on the fringe is quite bad based on our first try deformation.py in our directory.
2. This problem can also be handled by **OpenMaya** api instead of **PyMesh** library and it can provide better visualization effect.
