# Usage
## Running the program
To run the program we first need to create the virtual environment (venv)
1. `CTRL + Shift + P`
2. Search `Run Task`
3. Now click on `Create venv`, then `Install requirements`
   
Then we activate it with in cmd (or any other terminal) using

4. `.venv\Scripts\activate`

Now, you should be able to run the application with

5. `python -m app.src.main `

If everything worked correctly, you should see this window:

![](media/Application-On-Startup.png)

## Settings
Now you can adjust the settings before starting. Most importantly the selection of the correct audio input device and threshold for audio detection.

## Result
Pressing `Start Listening` will start the application.

## Personalization (in work)
The project contains a [config](app/assets/configuration/config.json) json file, which determines which pictures to use. You can paste your own pictures in the (/media)[app/media] directory and replace mine with yours in the json file.
