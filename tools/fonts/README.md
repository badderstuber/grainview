# GRAINVIEW fonts

`gv_fonts.js` = candidate bitmap fonts for the 128×128 SSD1327, packed for the
browser by `bdf2js.py` (ASCII 32–126 + a few UI symbols). Used by
`../font_compare.html` (pick fonts by eye) and, once chosen, the emulator. The
same BDF files feed LVGL on the Pico, so emulator == module.

Source: u8g2 repo, `tools/font/bdf/` —
`https://raw.githubusercontent.com/olikraus/u8g2/master/tools/font/bdf/<name>.bdf`

Regenerate (download BDFs to a scratch dir first):

    python3 tools/fonts/bdf2js.py tools/fonts/gv_fonts.js <dir>/*.bdf

## Licences (from each BDF's COPYRIGHT line — check the full file before shipping)

| Fonts | Licence |
|---|---|
| 4x6, 5x7, 6x10, 6x12, 7x14B, micro (X11 misc-fixed) | public domain |
| u8glib_4, u8g2_squeezed_regular_6 | public domain |
| tom-thumb | MIT |
| spleen-5x8 / 6x12 / 8x16 | BSD-2-Clause (Frederic Cambus) |
| Tiny5 | SIL OFL (Tiny5 Project Authors) |
| t0-12 / 12b / 14b / 16b (Uwe Waldmann) | see BDF header comments |
| profont11/12/15/17 | ProFont distribution licence (MIT-style) |
| helvB08/B10/B12/R08, ncenB12 (Adobe X11 bitmaps) | Adobe X11 notice: free use + redistribution with notice |
| luBS10/12, lubB12 (Bigelow & Holmes X11 bitmaps) | B&H X11 notice — read before shipping (name restrictions) |
| ArtosSans-8, VictoriaMedium-8 | no COPYRIGHT field — check u8g2's font list before shipping |

Measured cap heights (lit rows of 'H'): tiny 4–6 px, medium 7–8 px, large 9–13 px.
