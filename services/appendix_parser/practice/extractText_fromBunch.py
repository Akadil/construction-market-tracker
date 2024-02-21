import re


def extract_text_blocks(text):
    # Split text into bunches based on double newline characters
    bunches = text.strip().split('\n\n')

    # Process each bunch
    blocks = []
    for bunch in bunches:
        # Split each bunch into lines
        lines = bunch.strip().split('\n')

        # Remove empty lines and any leading/trailing whitespace from each line
        lines = [line.strip() for line in lines if line.strip()]

        for i in range(len(lines)):
            # print(f"Character {lines[i][-1]} and the result is {is_minus_sign(lines[i][-1])}")
            if lines[i][-1] in {'-', '–', '—', '−', '‐', '‒'}:
                minus_sign = lines[i][-1]
                if (lines[i][-2] != ' '):
                    lines[i] = lines[i][:-1] + ' ' + minus_sign

        # Join the lines to form a single block of text
        block = ' '.join(lines)
        
        # Append the block to the list of blocks
        blocks.append(block)

    return blocks


def main():
    # Example usage
    text = """
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


    """
    blocks = extract_text_blocks(text)
    for block in blocks:
        print(block)
        print('---')


if __name__ == '__main__':
    main()