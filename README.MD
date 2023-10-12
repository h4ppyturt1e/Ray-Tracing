
# Ray Tracing

## Dependencies
All dependencies are listed in the `requirements.txt` file. To install them, run `pip install -r requirements.txt` in the project directory.

## Running the Program
To run the program, run `python main.py {input_file.txt}` in the project directory. Alternatively, by running `python main.py TEST` instead, all files within a subdirectory named `tests` that has a `.txt` filetype will be ran as test files.

## Files
- `main.py`: Runs the program and renders the scene.
- `Objects.py`: Contains all the object classes.
    - `Color`: contains rgb values
    - `Ray`: a ray with origin and direction
    - `Setup`: containing scene and screen variables and output file
    - `Sphere`: containing sphere parameters
    - `Light`: containing light parameters
- `Parser.py`: Parses the input file data into respective classes.
- `ppm.py`: Take in the screen pixel array and saves it into a `.ppm` file.
- `RayTracer.py`: Contains RayTracer class, responsible for tracing rays through the scene and computing resulting color values.
- `Vector.py`: Contains the `vec3` class, complete with vector methods such as dot product, magnitude, normalize etc.
