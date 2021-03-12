# Marvel Challenge - Problem Statement:
```
# Marvel Impossible Travel
We're investigating an impossible travel alert that we noticed was triggered by Spectrum. We need your help to complete our investigation.
## Your Mission Should You Choose to Accept
- Sign up for an api key from the [Marvel Developer Portal](https://developer.marvel.com/).
- Obtain the name, id, description, and picture of Spectrum.
- Obtain the same information for all other characters she's worked with in other comics.
- Save the information in a database so that we can continue our investigation.
- Send us a link to a repo that contains a Dockerfile for spinning up the environment needed to run your script as well as a readme explaining what we need to do use your tool to exfiltrate this information.
Note: The api has a limit of 3000 calls/day so please be careful with your tools.
```

# How to run the project: (setup right values in .configs.yaml file and launch project using entrypoint.sh)
This is a project uses [Marvel Developer API](https://developer.marvel.com/docs) spec. 
1. Sign up and get the public key and private key from here: [My Deleloper Account](https://developer.marvel.com/account).
2. All the configurations (database name, public key, private key, marvel character name search, etc.,) needs to be set in the file: ```.configs.yaml```. 
3. Once all the configs are set in the yaml file, the project can be launched by running the shell script: ```entrypoint.sh```.
4. Upon running the above shell script, the database file with extension ```.db``` will be created for the first time run.

# Built with
1. Python3
2. Python module - ```PyYAML```
3. Python module - ```requests```
4. Database - ```sqlite3``` 
5. Hashing - ```md5```