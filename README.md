# Bot Simple Web Scrapper

Bot discord untuk web scrapping sederhana.

> **_NOTE:_** Tidak dapat bypass captcha atau eksekusi javascript.

## Environment Variables

- BOT_TOKEN

> Command Name (prefix: "scrapper")

## `get`

params:

````json
[
  {
    "name": "url",
    "description": "URL yang akan di fetch",
    "required": true,
    "default": 0
  },
  {
    "name": "selector",
    "description": "CSS selector untuk menentukan element yang akan di ambil.",
    "required": false,
    "default": "body"
  },
  {
    "name": "attributes",
    "description": "Atribut element yang akan di ambil.",
    "required": false,
    "default": "innerHTML"
  },
  {
    "name": "template",
    "description": "Input yang akan digunakan sebagai output dari data yang diambil, wajib dalam bentuk blok kode.",
    "required": false,
    "default": "```html\n$1\n```"
  }
]
````

> **_NOTE:_** $1 diatas adalah value dari atribut yang ditentukan, misal atribut "src,alt" (attributes dipisah dengan koma), maka $1 adalah value dari `src` dan $2 adalah value dari `alt`, dan seterusnya jika anda menambahkan atribut lain.

### example command:

    ````bash
    scrapper get https://anixverse.com/battle-through-the-heavens-season-5-episode-128-subtitle-indonesia/ .postbody>article>div.entry-content>div:nth-child(2)>div.mctnx>div>div:nth-child(2)>a "text,href"

    ```html
    Link $1: $2
    ```
    ````

### example output:

    ```txt
    Link Mirrored: https://www.mirrored.to/files/8OLWY27C/[Anixverse]_BTTH_S5_-_128_[480p].mkv_links
    Link TeraBox: https://terabox.com/s/1x23JDohJ8LaXftPDHUOFwA
    ```
