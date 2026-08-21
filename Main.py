import time
import os
import base64

def inp():
    print()
    while True:
        try:
            user_input = str(input("Do you have a shared secret key with the other person? (Y/N): "))
            if user_input in ['Y', 'N']:
                break
            else:
                raise ValueError("Invalid input.")
        except:
            print("Invalid input, please try again.")

    if user_input == 'Y':
        process_secret_key()
    else:
        print("Generating new secret key.")
        generate_new_secret_key()

def generate_new_secret_key():
    from cryptography.hazmat.primitives import hashes # type: ignore
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey # type: ignore
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF # type: ignore
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat # type: ignore

    private_key = X25519PrivateKey.generate()
    public_key = private_key.public_key()

    public_bytes = public_key.public_bytes(
        encoding=Encoding.Raw,
        format=PublicFormat.Raw
    )

    public_bytes_64 = base64.b64encode(public_bytes).decode('ascii')
    print(f"\nYour public key (send this to the other person): {public_bytes_64[:-1]}\n")

    while True:
        try:
            other_public_key_bytes = base64.b64decode(input("Paste the other person's public key here: ") + '=', validate=True)
            other_public_key = X25519PublicKey.from_public_bytes(other_public_key_bytes)
            shared_key = private_key.exchange(other_public_key)

            final_symmetric_key = HKDF(
                algorithm = hashes.SHA256(),
                length=32,
                salt=None,
                info=b"curve25519 handshake"
            ).derive(shared_key)
            final_symmetric_key_64 = base64.b64encode(final_symmetric_key).decode('ascii')

            break

        except Exception as e:
            print(f"\n\nError processing public key. Please try again. Error: {e}")

    print("\n\nSuccess! Shared secret key calculated. DO NOT SHARE THIS ANYWHERE, keep it in a secure place.")

    time.sleep(3)

    print(f"\nSecret key: {final_symmetric_key_64[:-1]}\n")

def helper_encrypt_or_decrypt():
    print()
    while True:
        try:
            user_input = str(input("Would you like to encrypt (send) or decrypt (receive) a message? (E/D): "))
            if user_input in ['E', 'D']:
                break
            else:
                raise ValueError("Invalid input.")
        except:
            print("Invalid input, please try again.")

    return user_input

def encrypt_message(cipher):
    while True:
        try:
            message = str(input("Type your message to be encrypted here: "))
            break
        except:
            print("Invalid input.")

    nonce = os.urandom(12)
    ciphertext = cipher.encrypt(nonce,
        message.encode('utf-8'),
        associated_data=None
    )

    message = base64.b64encode(nonce + ciphertext).decode('ascii').rstrip("=")

    return message

def decrypt_message(cipher):
    while True:
        try:
            message = str(input("Type your message to be decrypted here: "))
            break
        except:
            print("Invalid input.")

    data = base64.b64decode(message + "=" * (-len(message) % 4), validate=True)

    nonce = data[:12]
    ciphertext = data[12:]

    message = cipher.decrypt(nonce, ciphertext, associated_data=None).decode('utf-8')

    return message

def message_loop(cipher):
    while True:
        try:
            if helper_encrypt_or_decrypt() == 'E':
                message = encrypt_message(cipher)
                print(f"\nEncrypted message (send this to the other person): {message}")
            else:
                message = decrypt_message(cipher)

                print("\nSuccess! Secret message decrypted. DO NOT SHARE THIS ANYWHERE.")

                time.sleep(2)

                print(f"Secret message: {message}")
        except Exception as e:
            print(f"Error processing data. Please try again. Error: {e}")

def process_secret_key():
    from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305 # type: ignore
    print()
    while True:
        try:
            cipher = ChaCha20Poly1305(base64.b64decode(input("Paste your shared secret key here: ") + '=', validate=True))
            message_loop(cipher)
        except Exception as e:
            print(f"\n\nError processing data. Please try again. Error: {e}\n")

inp()
print("This dialog will automatically close in 8 seconds...")
time.sleep(8)