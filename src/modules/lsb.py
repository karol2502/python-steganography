from pydub import AudioSegment
import wave
import os


def lsb_encode(frame_bytes: bytearray, message: str, bytes_cycle: int, number_of_bits: int, shift: int = 0) -> bytes:
    # Append hashes to fill out rest of the bytes
    message = message + int((len(frame_bytes)/bytes_cycle-(len(message) * number_of_bits * 2))/number_of_bits) *'#'

    # Convert text to bit array
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(number_of_bits,'0') for i in message])))

    # Replace LSB of each byte of the audio data by one bit from the text bit array
    for i, bit in enumerate(bits):
        frame_bytes[bytes_cycle * i + shift] = (frame_bytes[bytes_cycle * i + shift] & 254) | bit

    # Get the modified bytes
    return bytes(frame_bytes)

def lsb_decode(frame_bytes: bytearray, bytes_cycle: int, number_of_bits: int, shift: int = 0) -> str:
    extracted = [frame_bytes[bytes_cycle * i + shift] & 1 for i in range(int(len(frame_bytes)/bytes_cycle))]
    # Convert byte array back to string
    message = "".join(chr(int("".join(map(str,extracted[i:i+number_of_bits])),2)) for i in range(0,len(extracted),number_of_bits))

    return message.split("###")[0]



def message_encode(path_to_audio: str, path_to_message: str, path_to_save: str, bytes_cycle: int, bits_per_char: int):
    temp_audio = AudioSegment.from_file(path_to_audio, path_to_audio.split('.')[-1])
    temp_audio.export('temp.wav', format='wav')

    audio = wave.open('temp.wav', mode='rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

    message_max_length = len(frame_bytes) // (bytes_cycle * bits_per_char)

    with open(path_to_message, 'r') as message_file:
        message = message_file.read()

        if(len(message) > message_max_length):
            raise Exception("Message to long!")

        encoded_bytes = lsb_encode(frame_bytes, message, bytes_cycle, bits_per_char)

        with wave.open(path_to_save, 'wb') as fd:
            fd.setparams(audio.getparams())
            fd.writeframes(encoded_bytes)
        audio.close()

        os.remove('temp.wav')
    print("ENCODED!")

def message_decode(path_to_audio: str, path_to_save: str, bytes_cycle: int, bits_per_char: int):
    song = wave.open(path_to_audio, mode='rb')

    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    decoded_message = lsb_decode(frame_bytes, bytes_cycle, bits_per_char)

    with open(path_to_save, 'w') as message_file:
        message_file.write(decoded_message)
    song.close()
    print("DECODED!")
