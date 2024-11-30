# mappilary_gopro_tools

Tools for gopro or other action cams for preparing upload to mapillary, kartaview, panoramx or other street image sites.

- remove_stopping.py - Move images without GPS position in file and nearby photos (duplicated position)
- copy_from_gopro.py - Copy or move images from action cam to a folder with subfolder each date

## Standalone

To run the Python script inside docker from the command line, you can [use Bun](https://bun.sh/docs/installation) like this:

```sh
chmod +x remove_stopping_executable.ts
./remove_stopping_executable.ts PATH/TO/YOUR/FILES
```
