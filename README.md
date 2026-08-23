A lightweight 2-way encryption program, made to avoid surveillance and ensure secure transmission of messages on apps like Discord.

Windows (x86 and x64) executables are now located on [the releases page](https://github.com/egnotech/Lightweight-2-way-message-encrypting-program/releases). No other distributions are currently available. Uncompiled source code can be found at `src/Main.py`.

Details:  
Uses X25519 encryption for key exchange, followed by AEAD (ChaCha20-Poly1305) symmetric encryption for message encrypting.
