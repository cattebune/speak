import time
import threading

from gtts.tokenizer import pre_processors
import gtts.tokenizer.symbols
from gtts import gTTS
import pyperclip
import pyglet
gtts.tokenizer.symbols.SUB_PAIRS.extend([
     ('tbh', 'to be honest'),
     ('wtf', 'what the fuck'),
     ('imo', 'in my opinion'),
     ('tbf', 'to be fair'),
]
)

def is_url_but_not_bitly(text):
    if text.startswith("$$talk$$"):
        return True
    return False

def print_to_stdout(clipboard_content):
    print("Found text: %s" % str(clipboard_content))
    text = str(clipboard_content.split("$$talk$$")[1])
    print("Stripped command: %s" % text)

    subbed = pre_processors.word_sub(text)

    print("Subbed: {}".format(subbed))
    tts = gTTS(subbed, 'en')
    tts.save("tts.mp3")

    explosion = pyglet.media.load("tts.mp3", streaming=False)
    explosion.play()


class ClipboardWatcher(threading.Thread):
    def __init__(self, predicate, callback, pause=5.):
        super(ClipboardWatcher, self).__init__()
        self._predicate = predicate
        self._callback = callback
        self._pause = pause
        self._stopping = False

    def run(self):
        recent_value = ""
        while not self._stopping:
            tmp_value = pyperclip.paste()
            if tmp_value != recent_value:
                recent_value = tmp_value
                if self._predicate(recent_value):
                    self._callback(recent_value)
            time.sleep(self._pause)

    def stop(self):
        self._stopping = True

def main():
    watcher = ClipboardWatcher(is_url_but_not_bitly,
                               print_to_stdout,
                               0.5)
    watcher.start()
    while True:
        try:
            print("Waiting for changed clipboard...")
            time.sleep(1)
        except KeyboardInterrupt:
            watcher.stop()
            break


if __name__ == "__main__":
    main()