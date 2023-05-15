def cipher(message, key):
     return bytes([message[i] ^ key[i % len(key)] for i in range(0, len(message))])


 ctrl_translation = str.maketrans(bytes(range(0,32)).decode("cp437"), "�☺☻♥♦♣♠•◘○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼")
 display_text = text.translate(ctrl_translation)