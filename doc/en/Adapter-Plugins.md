# Developing Adapter Plug-ins for SQL Judge

SQL Judge can use Adapters that are registered as plug-ins. In order to do that, the installed module must have some conditions met:

### Using setuptools

in ```setup.py```, add the parameter ```entry_points``` argument in ```setup```, using the ```sql_judge.adapter``` entry point:

```python
setuptools.setup(
    ...
    install_requires=['sql_judge'],
    entry_points = {
        'sql_judge.adapter': ['[plugin_alias]=[plugin_module]']
    }
    ...
)
```

where ```[plugin_alias]``` is the name which SQL Judge will recognize the plug-in, and ```[plugin_module]``` is the module which contains the Custom Adapter implementation.

Inside the module where the plug-ins points, it has to follow some requirements:

 - The module must have an ```Adapter``` class
 - This class must be inherited from ```sql_judge.adapter:AbstractAdapter```

```python
from sql_judge.adapter import AbstractAdapter

class Adapter(AbstractAdapter):
    # Class implementation here
```

When using the plugin, the configuration file must have the "plugin" option inside "adapter", with the plugin alias in it:
```JSON
{
    "adapter": {
        "plugin": "[plugin_alias]"
    }
}
```