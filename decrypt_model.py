import sys
import os
import argparse
import traceback
import pyAesCrypt
from loguru import logger

def log_handle(file = None):
    """
        returns a basic logger handle
    """
    logger.remove()
    logger.add(sys.stdout, format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <yellow>{process.name}:{thread.name}</yellow> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>')
    if file:
        logger.add(file, format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <yellow>{process.name}:{thread.name}</yellow> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>')

    return logger

logprint = log_handle('decryption_log.Log')

def decrypt_model( model_path, key, output_path=None, dest_extension = 'txt'):
    output_path = os.getcwd() if not output_path else output_path

    if not os.path.isfile(model_path):
        logprint.error(f"Encrypted model file does not exist at path {model_path}")
        return None
    
    if model_path and key:
        try:
            filename = os.path.basename(model_path).split('.')[0]
            if output_path:
                pyAesCrypt.decryptFile(model_path, output_path, key)
            else:
                pyAesCrypt.decryptFile(model_path, f"{filename}.{dest_extension}", key)
        except Exception as e:
            logprint.error(f'Exception while decrypting file -> {e}')
            logprint.debug(traceback.format_exc())

    else:
        logprint.error('Key missing.')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='decrypt model file')
    parser.add_argument('--model', dest='enc_model',
                        help='path to the encrypted model to be decrypted')
    parser.add_argument('--key', dest='dkey',
                        help='decryption key')
    parser.add_argument('--destination_path', dest='dest_path', default=None,
                        help='destination path to the decrypted model')
    
    args = parser.parse_args()
    print(args.enc_model, args.dkey, args.dest_path)
    decrypt_model(args.enc_model, args.dkey, args.dest_path)