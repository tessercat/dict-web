import re
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from dictionary.models import Entry


ALPHA = re.compile(r'^[a-z]\.\s\S')
NUMER = re.compile(r'^\d+\.\s\S')


class Command(BaseCommand):
    help = "Import dictionary entries"

    def get_char(self, header):
        parts = header.split()
        if len(parts) == 4 and parts[2] == 'MC':
            return parts[0]
        else:
            raise CommandError(f'Bad header {header}')

    def get_lines(self, raw):
        lines = raw.split('\n')
        if raw.endswith('\n'):
            lines = lines[:-1]
        return lines

    def get_start_line(self, line):
        if re.search(NUMER, line):
            return line
        if re.search(ALPHA, line):
            return f'    1. {line[3:]}'
        return None

    def clean_definition(self, definition):
        return definition.replace('; ', ';  \n')

    def clean_line(self, line):
        if line.endswith('-'):
            return f'{line[:-1]}'
        if line.endswith('.'):
            return line
        return f'{line} '

    def get_entry(self, lines):

        # Char and pinyin from header.
        entry = ''
        pinyin = []
        header = lines[0]
        parts = header.split()
        if len(parts) == 4 and parts[2] == 'MC':
            pinyin.append(parts[1])
            entry += f'# *{parts[1]}*\n'
        else:
            raise CommandError(f'Bad header {header}')

        # Other data.
        definition = ''
        for line in lines[1:]:
            if line.startswith('#'):
                continue
            if "MC" in line:
                parts = line.split()
                if len(parts) == 3 and parts[1] == 'MC':
                    if definition:
                        definition = self.clean_definition(definition)
                        entry += f'\n{definition}\n'
                        definition = ''
                    pinyin.append(parts[0])
                    entry += f'\n# *{parts[0]}*\n'
                else:
                    raise CommandError(f'Bad line {line}')
            else:
                start_line = self.get_start_line(line)
                if start_line and definition:
                    definition = self.clean_definition(definition)
                    entry += f'\n{definition}\n'
                    definition = self.clean_line(start_line)
                else:
                    definition += self.clean_line(line)
        if definition:
            definition = self.clean_definition(definition)
            entry += f'\n{definition}\n'
        if entry.endswith('\n'):
            entry = entry[:-1]
        return entry, ', '.join(pinyin)

    def add_entry(self, raw):
        lines = self.get_lines(raw)
        char = self.get_char(lines[0])
        definitions, pinyin = self.get_entry(lines)
        try:
            entry = Entry.objects.get(pk=char)
            changed = False
            if entry.definitions != definitions:
                entry.definitions = definitions
                changed = True
            if entry.pinyin != pinyin:
                entry.pinyin = pinyin
                changed = True
            if changed:
                entry.save()
                print(f'Updated {char}')
        except Entry.DoesNotExist:
            Entry.objects.create(
                char=char,
                definitions=definitions,
                pinyin=pinyin
            )
            print(f'Added {char}')

    def handle(self, *args, **options):
        kroll_data = settings.BASE_DIR / 'var' / 'data' / 'kroll.txt'
        with open(kroll_data, encoding="utf-8") as datafd:
            raw = ''
            for line in datafd:
                if line == '\n':
                    if raw:
                        self.add_entry(raw)
                        raw = ''
                else:
                    raw += line
            if raw:
                self.add_entry(raw)
