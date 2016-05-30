# Unsplash OSX dynamic wallpaper

Change every x minutes the wallpaper with a random high quality picture from [unsplash](unsplash.com)

## Steps

1. Register as a developer in https://unsplash.com/developers and create a new app
2. Setup credentials in `app.py`
3. Install requirements `pip install -r requirements.txt`
4. Run `python app.py authorize` and follow the process
5. Run `python app.py` to get a random picture as a wallpaper, just to see it works :)
6. Setup crontab `EDITOR=nano crontab -e`
7. Add a new rule `*/20 * * * * {python_path} {app.py}`
8. Enjoy

## Notes
* Swift must be installed
* Use absolute paths in the crontab rule
* You can change the query value for whatever you want
* You can setup the interval you want
* The images will be downloaded to `images` folder
