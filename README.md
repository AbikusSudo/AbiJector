
# AbiJector DLL Injector for Windows (Python Library, CLI & GUI). 
----
## Make binary exetuable file
```bash
python setup.py --exe
```
 * Binary will save in **Python Scripts folder**! 
 > Usually it can be: **%localappdata%\Programs\Python\Python#\Scripts**  
Where `#` is your Python version (e.g., I have `310`). Other numbers depend on your Python installation.

----- 
## Usage

- **CLI**: `python AbiJector_CLI.py --process PID_HERE --dll DLL_PATH` 
- **GUI**: `python AbiJector_GUI.py`
- **Library (LIB)**: 
```Python
# This is LIB usage. Dont be scary.
from AbiJector import AbiJector_LIB

injector = AbiJector_LIB.AbiJector("PID", "DLL.dll")
injector.inject()
```
---

## FAQ

Q: How to get **PID (Process ID)**?
A: **Microsoft** already maked tutorial. Just click [here.](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/finding-the-process-id)
Q: How to use **LIB (Library)**?
A: **This already written on `USAGE.md`.** And here too!
Q: Cant start CLI/GUI version **(ImportError)**
A: Check, **are you have needed requirements?** Try to start `python setup.py --requirements`. If problem not fixed, **try reinstall python**.
Q: Can we **modify** this?
A: **Yes**, but please credit my GitHub.

---