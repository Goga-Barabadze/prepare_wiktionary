"""
All the expressions used to parse information from the wiktionary dumps
"""


"""
- Description
    Find the language code for a wiktionary dump file
    They are usually written in the first line, as an attribute named xml:lang inside the mediawiki tag

- Example
    - Input
        <mediawiki ... xml:lang="it">
    - Output
        it
"""
FIND_LANGUAGE_CODE_FOR_DUMP_REGEX = \
    (r"(?<=xml:lang=\")"
     r"[a-z-]{2,10}"     # There is a '-' in there because the language code for e.g. Aramonian 'is roa-rup'
                         # Most languages have two character language codes, 
                         # except e.g. zh-min-nan (Min Nan) with ten chars
     r"(?=\")")

"""
- Description
    Find all the wiktionary pages
    They are typically enclosed with the page tag
    One page can contain one or multiple words

- Example
    - Input
        ...
        <page>
            Content
        </page>
        ...
    - Output
        <page>
            Content
        </page>
"""
FIND_ALL_PAGES_REGEX = \
    (r"<page>"
     r"[\s\S]+?"
     r"<\/page>")

"""
- Description
    The dump files have all a timestamp in their name. This regex parses it

- Example
    - Input
        amwiktionary-20220501-pages-articles-multistream
    - Output
        20220501
"""
FIND_DATE_FROM_DUMP_FILE_NAME_REGEX = \
    (r"(?<=-)"
     r"\d{8}"
     r"(?=-)")

"""
- Description
    Wiktionary assigns different namespaces to pages to identify their function
    Every language has their own variation but 0 means always a normal word page
    and not e.g. a template

- Example
    - Input
        ...
        <page>
            <title>MediaWiki:Blockedtext</title>
            <ns>8</ns>
            <id>156</id>
            <revision>
        ...
    - Output
        8
"""
FIND_NAMESPACE_REGEX = \
    (r"(?<=<ns>)"
     r"\d{1,5}"
     r"(?=</ns>)")

"""
- Description
    Every page has a title. When you search in the Wiktionary search-box, this is the main text it looks up
    
- Example
    - Input
        ...
        <page>
            <title>Hello</title>
            <ns>0</ns>
            <id>5062</id>
        ...
    - Output
        Hello
"""
FIND_PAGE_TITLE_REGEX = \
    (r"(?<=<title>)"
     r".+"
     r"(?=</title>)")

"""
- Description
    Find the id of the page. Enclosed with the id tag
    
- Example
    - Input
        ...
        <page>
            <title>Hello</title>
            <ns>0</ns>
            <id>5062</id>
        ...
    - Output
        5062
"""
FIND_PAGE_ID_REGEX = \
    (r"(?<=</ns>\n    <id>)"
     r"\d{1,15}"
     r"(?=</id>)")

"""
- Description
    The page might just be redirecting to another and has itself no real content.
    Such pages have the <redirect title="..."> tag
    
- Example
    - Input
        ...
        <page>
            <title>??????</title>
            <ns>0</ns>
            <id>605022</id>
            <redirect title="??????" />
            <revision>
        ...
    - Output
        ??????
"""
FIND_PAGE_REDIRECT_REGEX = \
    (r"(?<=</id>\n    <redirect title=\")"
     r".*"
     r"(?=\" />)")

"""
- Description
    Pages can have 0, 1 or more pages
    They have 0 when they are only redirects
    The content is inside the text tag

- Example
    - Input
        <page>
            ...
              <text bytes="510" xml:space="preserve">== Urheberrechtsversto??es ({{Sprache|Deutsch}}) ==
        === {{Wortart|Deklinierte Form|Deutsch}} ===
        ...
        {{Grundformverweis Dekl|Urheberrechtsversto??}}</text>
              <sha1>i5lb30gzvcizi5bxopvwmxflmd968qz</sha1>
            </revision>
          </page>
          
    - Output
        == Urheberrechtsversto??es ({{Sprache|Deutsch}}) ==
        === {{Wortart|Deklinierte Form|Deutsch}} ===
        ...
        {{Grundformverweis Dekl|Urheberrechtsversto??}}
"""
FIND_PAGE_CONTENT_REGEX = \
    (r"(?<= xml:space=\"preserve\">)"
     r"[\s\S]*?"
     r"(?=</text>)")
