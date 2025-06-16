# Never delete this comment. It reminds me of something important. Can't say that in a straightforward way because I'm planning to make this code publicly available.


from warnings import warn
from string   import whitespace
from random   import choice
from io       import TextIOWrapper


header_separator = ': '
header_lines_head = '#' # using Markdown flavor


def _parse_poem_header(content: str) -> dict[str, str | None]:
    header: dict[str, str | None] = {}
    for _line in content.split('\n'):
        line = _line.strip(whitespace)
        if line[0] == header_lines_head:
            line = line.lstrip(header_lines_head + whitespace)
            if header_separator in line:
                pair: tuple[str] | tuple[str, str | None] = tuple(line.split(header_separator, 1)) # type: ignore please. Note for mypy: BECUZ UR FOOLISH
                if len(pair) == 1:
                    pair += (None,)
                header[pair[0].lower()] = pair[1]
            else:
                header['name'] = line
    return header


def _parse_poem_text(content: str) -> str:
    lines: list[str] = []
    for line in content.split('\n'):
        if line.strip(whitespace)[0] == header_lines_head or not line.isprintable():
            continue
        lines.append(line)
    return '\n'.join(lines)


class Haiku:

    def __init__(
            self,
            text:                            str,
            name:                            str | None = None,
            author:                          str | None = None,
            language:                        str | None = None,
            name_fallback:                   str = 'Untitled Poem',
            author_fallback:                 str = 'Unknown Author',
            forgive_non_haikean_lines_count: bool = False
            ) -> None:
        self.language = language
        self.name = name_fallback if name is None else name
        self.author = author_fallback if author is None else author
        self.text = text.strip(whitespace)
        while '\n\n' in self.text:
            self.text = self.text.replace('\n\n', '\n')
        lf_count = self.text.count('\n')
        if lf_count != 2 and not forgive_non_haikean_lines_count:
            warn_text = f'Non-haikean lines count ({lf_count}) met in "{self.name}"'
            if name is None:
                warn_text += f' ({self.text.split("\n")[0]}\u2026)'
            warn(warn_text)

    def string(
            self,
            name_head: str = '',
            name_sep: str = ' by ',
            name_tail: str = '\n'
        ) -> str:
        return name_head + self.name + name_sep + self.author + name_tail + '\n' + self.text
    
    @property
    def dict(self) -> dict[str, str | None]:
        return {
            'name':     self.name,
            'author':   self.author,
            'language': self.language,
            'text':     self.text
        }

    def match(self, **rules: str) -> bool:
        '''
        Why da feck this function isn't implemented in pure vanilla-flavored Python?
        ...or it does and i'm just dense?
        '''
        for name, value in rules.items():
            if self.__getattribute__(name) != value:
                return False
        return True
    
    @classmethod
    def from_buffer(
            cls,
            buffer: TextIOWrapper,
            name_fallback:   str = 'Untitled Poem',
            author_fallback: str = 'Unknown Author',
            forgive_non_haikean_lines_count: bool = False,
            **override_properties: str | None
        ) -> 'Haiku':

        content = buffer.read()

        header = _parse_poem_header(content)
        for prop_name, prop_value in override_properties.items():
            header[prop_name] = prop_value

        return cls(
            _parse_poem_text(content),
            name_fallback = name_fallback,
            author_fallback = author_fallback,
            forgive_non_haikean_lines_count = forgive_non_haikean_lines_count,
            **header
        )


class HaikuList:

    def __init__(self, *poems: Haiku) -> None:
        self.poems = list(poems)
    
    def __getitem__(self, index: int) -> Haiku:
        return self.poems[index]
    
    def add(self, poem: Haiku) -> int:
        self.poems.append(poem)
        return len(self.poems)
    
    def filter(self, **rules: str) -> 'HaikuList':
        new_list = HaikuList()
        for poem in self.poems:
            if not poem.match(**rules):
                continue
            new_list.add(poem)
        return new_list
    
    def random(self) -> Haiku:
        return choice(self.poems)
    

__all__ = ['Haiku', 'HaikuList']