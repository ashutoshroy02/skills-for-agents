#!/usr/bin/env python3
"""vk: video-editor toolkit. Every command works inside a video folder created by `vk new`.

  vk new "title" --from file   create videos/<date>-<slug>/ {source,work,assets,exports}
  vk probe | sheet | frames    look at media (sheet/frames write PNGs to Read)
  vk transcribe | words        word-level transcript (faster-whisper, cached)
  vk silence | edl | cut       edit decisions as EDL json -> frame-accurate cut + map
  vk captions                  word-highlight .ass/.srt on the cut timeline
  vk track | render | verify   face reframe, one-pass final encode, platform checks
  vk status | clean | doctor   housekeeping
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from vk_common import VkError, utf8_stdio  # noqa: E402


def main(argv=None) -> int:
    utf8_stdio()
    import vk_captions
    import vk_cut
    import vk_media
    import vk_project
    import vk_reframe
    import vk_render
    import vk_transcribe

    parser = argparse.ArgumentParser(prog="vk", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True, metavar="<command>")
    for mod in (vk_project, vk_media, vk_transcribe, vk_cut, vk_captions, vk_reframe, vk_render):
        mod.register(sub)
    args = parser.parse_args(argv)
    try:
        return args.func(args) or 0
    except VkError as e:
        print(f"vk {args.cmd}: error: {e}", file=sys.stderr, flush=True)
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
