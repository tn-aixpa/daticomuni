# Log Aziendale Artifact

To log the artifacts, it is possible to use ``convert_aziendali`` operation that performs conversion of dataset

1. Initialize the project

```python
import digitalhub as dh
PROJECT_NAME = "daticomuni" # here goes the project name that you are creating on the platform
project = dh.get_or_create_project(PROJECT_NAME)
```

2. Prepare dataset
Log the input dataset inside project using the zip file
```python
di = project.new_artifact(name="daticomuni",kind="artifact", path='csvs.zip')
```

3. Define the function

Register the ``convert_aziendali`` function in the project.

```python
func_az = project.new_function(name="convert_aziendali",
                         kind="python",
                         python_version="PYTHON3_10",
                         source={"source": "src/convert-aziendali.py", "handler": "convert_aziendali"})
```
The function represents a Python operation and may be invoked directly locally or on the cluster. 

4. Run the function
```python
run_convert_az = func_az.run(action="job", inputs={"source_artifact": di.key}, outputs={}, local_execution=False)
```
The dataset will be registered in side the project contexts as artifacts.
