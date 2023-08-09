# data.json schema

- This README documents both [nimi Linku, the sheet](https://docs.google.com/spreadsheets/d/1xwgTAxwgn4ZAc4DBnHte0cqta1aaxe112Wh1rv9w5Yk/) and [jasima Linku, the database](https://linku.la/jasima/data.json), as jasima Linku is built from nimi Linku.
- Most fields are copied from [nimi Linku](https://docs.google.com/spreadsheets/d/1xwgTAxwgn4ZAc4DBnHte0cqta1aaxe112Wh1rv9w5Yk/) without change other than cleaned whitespace.

## Structure

- All fields are stored as strings, even if an integer or float representation would be appropriate.
- All immediate children of the top four keys (documented below) are stored alphabetically.
- If a key exists but has no value in nimi Linku, it will not be in jasima Linku. <!-- unless it is a parent to another field (see below) -->
- If a field's name contains a slash `/`, the word(s) before the slash is a parent key, and the word(s) after the slash is a child key. For example, the `Words` sheet or `data` parent key has `def/[language_code]` for all word definitions.
- It is not possible for a parent key to have the same name as a normal key; the updater script would fail, as it would attempt to insert to a string as though it were a dictionary.

## Reading the documentation

- A key is indicated with its name `key_name:`
- A variable key is indicated in brackets `[key_name]:`.
- If a bracketed key name has any formatting information, it will be documented in the first child key.
- Machine-reading instructions, if applicable, are indicated at the end of the description with \*\*surrounding asterisks\*\*.

## `languages`

Derived from the [Languages sheet](https://docs.google.com/spreadsheets/d/1xwgTAxwgn4ZAc4DBnHte0cqta1aaxe112Wh1rv9w5Yk/#gid=1133229503)

```yml
[language_code]:
  id_long: The full ID of the language according to ISO
  name_endonym: The name of the language according to its speakers.
  name_english: The name of the language in English.
  name_toki_pona: The name of the language in Toki Pona (generally derived from endonym).
  credits: List of those who contributed to this translation. **Split on `,` to get each name.**
  completeness_percent:
    [usage_category]:
      The integer percentage of words with definitions translated into this language in this usage category.
```

## `credits`

Derived from the [Credits sheet](https://docs.google.com/spreadsheets/d/1xwgTAxwgn4ZAc4DBnHte0cqta1aaxe112Wh1rv9w5Yk/#gid=1238936638)

```yml
[contributor]:
  description: A human-readable description of the contribution made.
```

## `data`

Derived from the [Words sheet](https://docs.google.com/spreadsheets/d/1xwgTAxwgn4ZAc4DBnHte0cqta1aaxe112Wh1rv9w5Yk/#gid=0).

Some static files are derived from [ijo Linku](https://github.com/lipu-linku/ijo), such as the luka pona and audio files.

All children of `etymology_data` have the same list length once split on `;`.

```yml
[word]: A unique identifier for the word which is often the word, but may have an integer suffix if the word has been coined multiple times.
  word: The word as it would be written in toki pona using sitelen Lasina.
  sitelen_pona: A list of latin character strings that convert to all alternates for a given word. Usually identical to [word]; see "akesi".
  ucsur: The unicode codepoint assigned to the word.
  sitelen_pona_etymology: Human-readable description of the origin of the sitelen pona.
  sitelen_sitelen: URL to an image of the sitelen sitelen for the word.
  sitelen_emosi: The emoji corresponding to the word in sitelen Emosi.
  luka_pona:
    [format]: URL to the luka pona sign being demonstrated in [format].
  audio:
    [author]: URL to the audio of the word being spoken by [author].
  coined_era: One of [pre-pu, post-pu, post-ku] indicating the "era" the word was created in, relative to the publishing of the Toki Pona books.
  book: One of [pu, ku suli, ku lili, none] indicating what Toki Pona book the word was first documented in.
  usage_category: One of [core, widespread, common, uncommon, rare, obscure] indicating the word's popularity.
  source_language: The language(s) the word derives from.
  etymology: A human-readable description of the word's etymology(ies), including the original word(s), definition(s), and other metadata.
  etymology_data:
    langs: List of languages the word derives from. **Split on `;`.**
    words: List of words the word derives from. **Split on `;`.**
    alts: List of alternate writings or indicated pronunciations for the words in `words`. **Split on `;`.**
    defs: List of definitions for the words in `words`. **Split on `;`.**
  creator: The name of the word's creator.
  ku_data: Usage data from Toki Pona Dictionary (ku), indicated with a superscript number. **Split on `,`.**
  recognition:
    [date]:
      Integer percentage of survey respondents who recognize and use the word as of [date]. [date] is YYYY-MM format.
  author_verbatim: Definition of the word as written by its original author. Defer to `pu_verbatim` if that is defined.
  pu_verbatim:
    [language_code]:
       Definition of the word in [language_code] as written in the corresponding translation of Toki Pona: The Language of Good.
  see_also: A list of words related to [word]. **Split on `,`.**
  commentary: Human-readable extra information about the word, such as historical usage, replacement, or clarifications.
  def:
    [language_code]:
      Definition of the word in [language_code]. [language_code] is an entry in the `language` key.
```

## `fonts`

Derived from the [Fonts sheet](https://docs.google.com/spreadsheets/d/1xwgTAxwgn4ZAc4DBnHte0cqta1aaxe112Wh1rv9w5Yk/#gid=1195574771).

Also used to fill out [nasin sitelen Linku](https://github.com/lipu-linku/nasin-sitelen).

Some fonts exist which are recorded here but are not distributed in nasin sitelen Linku or in ilo Linku; this is generally due to licensing conflicts, as we can only distribute fonts with licenses allowing us to do so. Commonly applicable fonts include OFL (Open Font License) and variations of CC (Creative Commons).

See also, [license IDs according to SPDX](https://spdx.org/licenses/)

```yml
[font_name]:
  name_short: The name of the font. Usually the same as [font_name], but not always.
  writing_system: The writing system of the font (alphabet, syllabary, sitelen pona, sitelen sitelen, ...)
  links:
    fontfile: A direct download link for the font. Usually downloadable without authentication.
    repo: The repository of the font on github or gitlab.
    webpage: The homepage of the font.
  creator: The name(s) of the font creator(s). TODO- Inconsistently split by `/` and `&`.
  license: The code of the license according to SPDX.
  version: Version number of the font as provided by the author(s). NOT GLOBALLY CONSISTENT.
  last_updated: The last time the font file was updated in nasin sitelen Linku. YYYY-MM format.
  filename: The name of the file in nasin sitelen Linku. Provided even if license is incompatible.
  style: One word description of font appearance.
  features: Human-readable list of capabilities of the font (supported glyphs, UCSUR support, combining glyphs, etc).
```
