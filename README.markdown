lighty-thumbnailer
========================

lighty-thumbnailer is a simple image thumbnailer can be used for any bot web- 
and desktop-based application (or any another application type). It was 
inspired by sorl-thumbnail (popul thumbnail library for Django), but has some
additional 

Features:
---------

- Support cropping, resizing, different cropping and resizing strategies. It's 
  more customizable library than sorl-thumbnail.
- Different image libraries support.
  Now only PIL engine available.
- Data storage support.
  Now just a local filesystem storage implemented.
- Different datastores support.
  Not just a Redis support available.

TODO:
-----

- Django integration: django file storage, django templatetags, django field
  class.
- Clean up get_datastore, get_storage, etc. classmethods from Base* classes if
  it's possible. Use get_instance from lighty.thumbnailer.util.InstanceForClass
  instead.
- Add image filter's support.
- Add shortcuts.
- Add additional datastores.
- Add additional image libraries (pg_magick, ImageMagick, another one?)
- More tests.
- More documentation.
- May be some another clean-ups, refactoring, optimizations and laziness.
