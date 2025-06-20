# dccpath

Small utility library for locating common DCC (Digital Content Creation) software executables

Currently supported DCCs:

- Autodesk Maya
- Autodesk MotionBuilder
- Blender

```python
from dccpath import get_blender, get_mayapy

blender = get_blender(version="4.4")
mayapy = get_mayapy(version="2025")
```
