### Декларируемые параметры

Функция, позволяющая описать вид передаваемых в executable или конфиг аргументов, валидировать и привести к нужному виду переданные параметры.

#### Способ описания

В Executable у каждого класса может быть метод declare(), возвращающий словарь с параметрами в формате приведённом ниже. При задании аргументов параметры рекурсивно складываются из этого метода вплоть до базового executable, образуя полный словарь со всеми параметрами.

#### Формат описания

Параметр должен быть классом, наследующим declarable.ArgumentsTypes.Argument. Для получения в коде можно прописать:

```
from declarable.ArgumentsTypes import {...нужные аргументы}
```

#### Создание своего аргумента

Создайте файл в папке `src/declarable/ArgumentsTypes`, с названием, оканчивающимся на "Argument.py".

```
from declarable.ArgumentsTypes.Argument import Argument

class [name]Argument(Argument):
    def value(self):
        return self.input_value

```

Его нужно добавить в `src/declarable/ArgumentsTypes/__init__.py`:

```
from declarable.ArgumentsTypes.[name]Argument import [name]Argument
```

#### Доступные типы

|Название|Описание|
|--|--|
|`BooleanArgument`|Принимается число 0 или 1, преобразуется соответственно в False или True|
|`CsvArgument`|Принимает строку на вход, разбивает её на массив через запятую|
|`FloatArgument`|Возвращает число с запятой|
|`IntArgument`|Возвращает целое число|
|`JsonArgument`|Сериализует переданную json-строку|
|`LimitedArgument`|Значение принимается только если есть в `values`|
|`ObjectArgument`|Словарь или массив, не может быть задан извне|
|`StorageUnitArgument`|Возвращает StorageUnit, беря id на входе|
|`StringArgument`|Принимается строка|

##### `values`

Тип значения: _list_
Только при: `type`=`LimitedArgument`

Список допустимых значений.

##### `default`

Тип значения: _зависит от `type`_

Значение, которое будет задано, если параметр не передан на вводе. Если не задан сам `default`, значение будет равно None либо произойдёт AssertionException.

##### `hidden`

Тип значения: _bool_

При `True` параметр всё ещё можно задать, но он не будет показан в интерфейсе.

##### `maxlength`

Тип значения: _int_
Только при: `type`=`StringArgument`

Длина, до которой будет обрезаться переданная строка.

##### `is_long`

Тип значения: _string_
Только при: `type`=`StringArgument`

Подразумевается ли что значение будет длинным.

##### `sensitive`

Тип значения: _bool_

Заменять ли значение `default` при показе документации. Рекомендуется ставить на True, если в `default` подставляется чувствительная информация вроде токена.

##### `save_none_values`

Тип значения: _bool_ (по умолчанию False)

При False не будут сохраняться ключи равные None.

##### `assertion`

Тип значения: _dict_

Словарь, отвечающий за дополнительные проверки на валидность. Каждый ключ отвечает за условие, если оно не выполнено то возвращается AssertionError.

Может содержать:

`not_null` _(bool)_: проверить, что значение не равно None

`assert_link` _(str)_: значение привязывается к указанному параметру, назовём X. Если текущий параметр равен None, будет проверятся параметр X, если он тоже равен None, будет возвращена AssertionError.

`only_when` _(list)_: массив проверки других параметров. Параметр активируется, если выполнено хоть одно условие из этого списка. Не влияет на выполнение скрипта, нужно лишь для интерфейса чтобы не показывать ненужные параметры. Каждый элемент задаётся в словаря с ключом с названием параметра и значением (тоже словарь):

`operator` — оператор сравнения

`value` — с каким значением сравнивать

Пример:

```
"path": {"operator": "!=", "value": None}
```

означает

значение аргумента `path` != None

##### `env_property`

Тип значения: _string_

Если `default` подставляется из `env`, то какой ключ за это отвечает.

##### `docs`

Документация к параметру. См. [documentation.md](documentation.md)

#### Вызов в коде

За сведение переданных аргументов и задокументированных отвечает класс DeclarableArgs, за дополнительное сравнение — ArgsValidator с методом validate(). В ArgsValidator так же может быть задействовать конфиг для проверки параметров[args_config.md](args_config.md)

#### Рекомендации

Лучше называть параметр кратко без дополнительных слов, например параметр с названием получаемого экстрактора лучше назвать просто `extractor` а не `extractor_name` или `name`. 

Лучше не называть параметр именами `i`, `name`
