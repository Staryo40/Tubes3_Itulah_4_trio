from .rsa_encryption import DatabaseEncryption, encrypt_applicant_data, decrypt_applicant_data
import functools
from typing import Dict, List, Any, Optional

class EncryptedDatabaseWrapper:
    def __init__(self):
        self.db_encryption = DatabaseEncryption()
        self._encryption_enabled = True
    
    def enable_encryption(self):
        self._encryption_enabled = True
    
    def disable_encryption(self):
        self._encryption_enabled = False
    
    def is_encryption_enabled(self) -> bool:
        return self._encryption_enabled
    
    def encrypt_before_save(self, applicant_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self._encryption_enabled:
            return applicant_data
        
        try:
            encrypted_data = self.db_encryption.encrypt_profile_data(applicant_data)
            return encrypted_data
        except Exception as e:
            print(f"Encryption error: {e}")
            return applicant_data
    
    def decrypt_after_load(self, encrypted_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self._encryption_enabled:
            return encrypted_data
        
        if not encrypted_data:
            return encrypted_data
        
        try:
            decrypted_data = self.db_encryption.decrypt_profile_data(encrypted_data)
            return decrypted_data
        except Exception as e:
            print(f"Decryption error: {e}")
            return encrypted_data
    
    def decrypt_list(self, encrypted_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not self._encryption_enabled:
            return encrypted_list
        
        if not encrypted_list:
            return encrypted_list
        
        decrypted_list = []
        successful_decryptions = 0
        
        for item in encrypted_list:
            decrypted_item = self.decrypt_after_load(item)
            decrypted_list.append(decrypted_item)
            
            # Check if decryption was successful
            sensitive_fields = ['first_name', 'last_name', 'address', 'phone_number']
            decrypted = False
            for field in sensitive_fields:
                if field in item and field in decrypted_item:
                    if str(item[field]) != str(decrypted_item[field]):
                        decrypted = True
                        break
            
            if decrypted:
                successful_decryptions += 1
        
        print(f"✓ Decrypted {successful_decryptions}/{len(encrypted_list)} records successfully")
        return decrypted_list

# Global instance
db_encryption_wrapper = EncryptedDatabaseWrapper()

def with_encryption(encrypt_input=False, decrypt_output=False, decrypt_list=False):
    """Decorator untuk otomatis encrypt/decrypt data"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Handle input encryption
            if encrypt_input and len(args) > 0 and isinstance(args[0], dict):
                encrypted_data = db_encryption_wrapper.encrypt_before_save(args[0])
                args = (encrypted_data,) + args[1:]
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Handle output decryption
            if result is not None:
                if decrypt_list and isinstance(result, list):
                    result = db_encryption_wrapper.decrypt_list(result)
                elif decrypt_output and isinstance(result, dict):
                    result = db_encryption_wrapper.decrypt_after_load(result)
            
            return result
        return wrapper
    return decorator

# Convenience functions
def encrypt_applicant_profile(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    return db_encryption_wrapper.encrypt_before_save(profile_data)

def decrypt_applicant_profile(encrypted_data: Dict[str, Any]) -> Dict[str, Any]:
    return db_encryption_wrapper.decrypt_after_load(encrypted_data)

def decrypt_applicant_list(encrypted_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return db_encryption_wrapper.decrypt_list(encrypted_list)

def enable_database_encryption():
    db_encryption_wrapper.enable_encryption()

def disable_database_encryption():
    db_encryption_wrapper.disable_encryption()

def is_database_encryption_enabled() -> bool:
    return db_encryption_wrapper.is_encryption_enabled()

def get_encryption_status() -> bool:
    return db_encryption_wrapper.is_encryption_enabled()