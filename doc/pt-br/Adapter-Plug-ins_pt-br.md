# Desenvolvendo Plug-ins de Adaptador para SQL Judge

SQL Jusge pode usar Adaptadores instalados em plug-ins. Para que isso ocoraa, o módulo instalado deve cumprir certas condições:

### Usando setuptools

Em ```setup.py```, adicione o parâmetro ```entry_points``` em ```setup```, com o _entry point_ ```sql_judge.adapter```:

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

Onde ```[plugin_alias]``` é o nome pelo qual SQL Judge irá identificar o plug-in, e ```[plugin_module]``` é o módulo no pacote em que a implementação do adaptador está.

O módulo que o plug-in aponta também precisa cumprir alguns requerimentos:
 - O módulo deve possuir uma class ```Adapter```
 - Essa classe deve ser filha de ```sql_judge.adapter:AbstractAdapter```

```python
from sql_judge.adapter import AbstractAdapter

class Adapter(AbstractAdapter):
    # Implementação da Classe aqui
```

Quando for usar na validação, o arquivo de configuração deve a opção "plugin" dentro de "adapter", com o alias do plugin nele:
```JSON
{
    "adapter": {
        "plugin": "[plugin_alias]"
    }
}
```
