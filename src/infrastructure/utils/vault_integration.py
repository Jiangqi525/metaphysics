import os
import hvac
import logging
from hvac.exceptions import VaultError

logger = logging.getLogger(__name__)


class VaultSecretManager:
    _instance = None  # 单例模式

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VaultSecretManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.vault_addr = os.getenv("VAULT_ADDR")
        self.vault_token = os.getenv("VAULT_TOKEN")  # 生产环境应使用K8s Service Account Token或AppRole
        self.vault_role_id = os.getenv("VAULT_ROLE_ID")
        self.vault_secret_id = os.getenv("VAULT_SECRET_ID")

        if not self.vault_addr:
            logger.critical("VAULT_ADDR environment variable not set. Vault integration will not function.")
            raise ValueError("VAULT_ADDR is required for Vault integration.")

        self.client = hvac.Client(url=self.vault_addr)
        self._authenticate()
        self._initialized = True

    def _authenticate(self):
        """根据配置进行认证，优先使用AppRole"""
        try:
            if self.vault_role_id and self.vault_secret_id:
                # AppRole 认证
                response = self.client.auth.approle.login(
                    role_id=self.vault_role_id,
                    secret_id=self.vault_secret_id
                )
                self.client.token = response['auth']['client_token']
                logger.info("Authenticated with Vault using AppRole.")
            elif self.vault_token:
                # Token 认证 (开发/测试环境或K8s Service Account Token)
                self.client.token = self.vault_token
                logger.info("Authenticated with Vault using token.")
            else:
                raise VaultError(
                    "No valid Vault authentication method configured (VAULT_TOKEN or VAULT_ROLE_ID/VAULT_SECRET_ID).")

            if not self.client.is_authenticated():
                raise VaultError("Failed to authenticate with Vault.")
        except VaultError as e:
            logger.critical(f"Vault authentication failed: {e}")
            raise

    def get_secret(self, path: str, mount_point: str = 'secret'):
        """从Vault KV secret engine获取秘密"""
        try:
            response = self.client.secrets.kv.read_secret_version(
                path=path,
                mount_point=mount_point
            )
            return response['data']['data']
        except VaultError as e:
            logger.error(f"Failed to retrieve secret from Vault at path {path}: {e}")
            raise

    def get_database_creds(self):
        """获取数据库凭证"""
        # 假设数据库凭证存储在 secret/database/creds/app-role
        return self.get_secret("database/creds/app-role")

    def get_encryption_key(self):
        """获取加密密钥"""
        # 假设加密密钥存储在 secret/encryption/main
        return self.get_secret("encryption/main")['key']

# 在应用启动时初始化VaultSecretManager
# 例如在 app_factory.py 中
# vault_manager = VaultSecretManager()
# db_creds = vault_manager.get_database_creds()
# encryption_key = vault_manager.get_encryption_key()
