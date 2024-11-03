# pythonOS / pyOS
an entire operating system (simulator) in python
## logging in
the default accounts are:
- `root` with the password `1234` (please change after logging in)
- `guest` with the password `guest`
## moving
pythonos is designed to be **extremely** portable.  
the entire os is just one file, the user accounts are in one file too. all your apps are in one folder.  
here is what a typical pythonos installation looks like:
```tree
./
    pythonos.py (os kernel and de)
    pythonos_config.json (all settings)
    pythonos_apps/ (all apps)
        program1.py (example program 1)
        program2.py (example program 2)
```
you can just grab the folder and **GO!!**

