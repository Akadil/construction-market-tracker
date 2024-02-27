## Parse text

```
class Parsetext:
    def __init__(self)

    def parse(self, text):
        characteristics: dict

        characteristics = someFunction(text)
        return (characteristisc)
```

- Input:      text - The text retrieved from the file
- Output:     characteristics - Full characteristics of the tender
- Exception:  If some problems occurs, just throw an exception

<details>
    <summary>Input example</summary>

```
№
п/п

Наименование предмета
закупаемых работ
(наименование лота)

1

Работы по капитальному
ремонту нежилых
зданий/сооружений/помещений

Вид
строительства
(новое
строительство,
расширение,
техническое
перевооружение,
модернизация,
реконструкция,
реставрация и
капитальный
ремонт
существующих
объектов)

реставрация и
капитальный
ремонт
существующих
объектов

Уровень
ответственности
зданий и
сооружений
(первый –
повышенный,
второй –
нормальный,
третий –
пониженный)

второй –
нормальный

Техническая
сложность
объектов
(здания и
сооружения,
относящиеся
к технически
сложным
объектам, и
здания и
сооружения,
не
относящиеся
к технически
сложным
объектам)

здания и
сооружения,
не
относящиеся
к технически
сложным
объектам

Подвид
лицензируемого вида
деятельности,
предусмотренного
разделами 5 и 6
Перечня разрешений
первой категории
(лицензий) Закона
Республики Казахстан
от «О разрешениях и
уведомлениях»,
соответствующий
предмету конкурса, за
исключением работ на
объектах
жилищногражданского
назначения

Функциональное
назначение
(промышленные
объекты,
производственные
здания, сооружения,
объекты жилищно-
гражданского
назначения, прочие
сооружения)

объекты жилищно-
гражданского назначения


```
</details>

---

### Job to do

The previous class will just retrieve the text, it won't analyze. So my job is to check the content of the text, and if everything is ok, then parse it

1. Check for properness of the text
2. Format the text
3. Analyze the text
4. Return the characteristics
