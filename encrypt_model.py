import sys
import os
import pyAesCrypt
import argparse
import traceback
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

logprint = log_handle('encryption_log.Log')

def encrypt_model( model_path, key, output_path=None):
    output_path = os.getcwd() if not output_path else output_path

    if not os.path.isfile(model_path):
        logprint.error(f"Model file does not exist at path {model_path}")
        return None
    
    if model_path and key:
        try:
            filename = os.path.basename(model_path).split('.')[0]
            pyAesCrypt.encryptFile(model_path, f"{filename}.aes", key)
        except Exception as e:
            logprint.error(f'Exception while encrypting file -> {e}')
            logprint.debug(traceback.format_exc())

    else:
        logprint.error('Key missing.')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='encrypt model file')
    parser.add_argument('--model', dest='model',
                        help='path to the model to be encrypted')
    parser.add_argument('--key', dest='ekey',
                        help='encryption key')
    parser.add_argument('--destination_path', dest='dest_path', default=None,
                        help='destination path to the encrypted model')
    
    args = parser.parse_args()
    print(args.model, args.ekey, args.dest_path)
    encrypt_model(args.model, args.ekey, args.dest_path)