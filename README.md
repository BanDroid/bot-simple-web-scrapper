# Bot Simple Web Scrapper

Discord bot for simple web scrapping. Command prefix is `scrapper`.

Click image below to install for your discord server:

<a target="_blank" href="https://discord.com/oauth2/authorize?client_id=1325523244404445184"><img width="100" height="80" src="https://cdn.simpleicons.org/discord/5865F2" alt="discord.svg" /></a>

> **_NOTE:_** Unable to bypass captcha and executing javascript.

## Environment Variables

- BOT_TOKEN

## `get`

params:

````json
[
  {
    "name": "url",
    "description": "URL that will be fetched.",
    "required": true,
    "default": 0
  },
  {
    "name": "selector",
    "description": "CSS selector to determine the elements that will be taken.",
    "required": false,
    "default": "body"
  },
  {
    "name": "attributes",
    "description": "The attribute of the element from which data will be retrieved.",
    "required": false,
    "default": "innerHTML"
  },
  {
    "name": "template",
    "description": "The input that will be used as the output of the captured data, must be in the form of a code block.",
    "required": false,
    "default": "```html\n$1\n```"
  }
]
````

### example command:

    ````sh
    scrapper get https://anixverse.com/battle-through-the-heavens-season-5-episode-128-subtitle-indonesia/ .postbody>article>div.entry-content>div:nth-child(2)>div.mctnx>div>div:nth-child(2)>a "text,href"

    ```html
    Link $1: $2
    ```
    ````

> **_NOTE:_** $1 above is the value of the specified attribute, for example the attribute "text,href" (attributes separated by commas), then $1 is the value of `text` and $2 is the value of `href`, and so on if you add other attributes.

### example output:

    ```txt
    Link Mirrored: https://www.mirrored.to/files/8OLWY27C/[Anixverse]_BTTH_S5_-_128_[480p].mkv_links
    Link TeraBox: https://terabox.com/s/1x23JDohJ8LaXftPDHUOFwA
    ```
