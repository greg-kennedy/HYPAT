# 2600 ROM Audit
## Instructions

1. Get [ROM Hunter's Collection from AtariMania](https://www.atarimania.com/rom_collection_archive_atari_2600_roms.html) and unpack to ROMS subfolder
2. Run `romaudit.pl ROMS` to produce a `roms.tsv` file
3. Edit `roms.tsv` to correct parse errors
4. Get latest [Stella Properties file from GitHub](https://raw.githubusercontent.com/stella-emu/stella/refs/heads/master/src/emucore/stella.pro) and place in root dir
5. Run `proaudit.pl stella.pro` to produce a `pro.tsv` file
6. Edit `pro.tsv` to correct parse errors
7. Run `merge.pl roms.tsv pro.tsv` to create one `roms.json` file
