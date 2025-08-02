# 代码生成时间: 2025-08-02 13:32:36
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid import security
from pyramid.httpexceptions import HTTPBadRequest
from cryptography.fernet import Fernet

# 密码加密解密工具
class PasswordEncryptionDecryptionTool:
    def __init__(self, secret_key):
        self.fernet = Fernet(secret_key)

    def encrypt(self, password):
        """
        加密密码
        :param password: 待加密的密码
        :return: 加密后的密码
        """
        try:
            encrypted_password = self.fernet.encrypt(password.encode())
            return encrypted_password.decode()
        except Exception as e:
            raise security.Forbidden('Password encryption failed: ' + str(e))

    def decrypt(self, encrypted_password):
        """
        解密密码
        :param encrypted_password: 待解密的密码
        :return: 解密后的密码
        """
        try:
            decrypted_password = self.fernet.decrypt(encrypted_password.encode())
            return decrypted_password.decode()
        except Exception as e:
            raise security.Forbidden('Password decryption failed: ' + str(e))

# Pyramid视图函数
@view_config(route_name='encrypt_password', request_method='POST')
def encrypt_password(request):
    secret_key = 'your_secret_key_here'  # 使用自己的密钥
    password_encryption_decryption_tool = PasswordEncryptionDecryptionTool(secret_key)

    password = request.json.get('password')
    if not password:
        raise HTTPBadRequest('Password is required')

    encrypted_password = password_encryption_decryption_tool.encrypt(password)
    return Response(json={'encrypted_password': encrypted_password})

@view_config(route_name='decrypt_password', request_method='POST')
def decrypt_password(request):
    secret_key = 'your_secret_key_here'  # 使用自己的密钥
    password_encryption_decryption_tool = PasswordEncryptionDecryptionTool(secret_key)

    encrypted_password = request.json.get('encrypted_password')
    if not encrypted_password:
        raise HTTPBadRequest('Encrypted password is required')

    decrypted_password = password_encryption_decryption_tool.decrypt(encrypted_password)
    return Response(json={'decrypted_password': decrypted_password})

# Pyramid配置
def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.add_route('encrypt_password', '/encrypt_password')
        config.add_route('decrypt_password', '/decrypt_password')
        config.scan()

def run():
    main({}, 
        password_encrypt_decrypt.secret_key='your_secret_key_here')

if __name__ == '__main__':
    run()