import os
import json
from typing import Tuple, Optional, Dict, Any
import base64
import string

# Global mapping file untuk persistent storage
MAPPING_FILE = "encryption_mapping.json"

def load_mapping():
    """Load encryption mapping dari file"""
    if os.path.exists(MAPPING_FILE):
        try:
            with open(MAPPING_FILE, 'r') as f:
                data = json.load(f)
                return data.get('encrypt_map', {}), data.get('decrypt_map', {})
        except:
            pass
    return {}, {}

def save_mapping(encrypt_map, decrypt_map):
    """Save encryption mapping ke file"""
    try:
        with open(MAPPING_FILE, 'w') as f:
            json.dump({
                'encrypt_map': encrypt_map,
                'decrypt_map': decrypt_map
            }, f, ensure_ascii=False, indent=2)
    except:
        pass

class SimpleEncryption:
    """Simple but safe encryption menggunakan Caesar Cipher + Base64"""
    
    def __init__(self):
        self.shift = 13  # ROT13 style
        # Definisikan character set yang akan digunakan
        self.charset = string.ascii_letters + string.digits + " .,'-"
    
    def encrypt(self, message: str) -> str:
        """Encrypt message dengan Caesar cipher + base64"""
        if not message:
            return message
        
        # Encode ke bytes dulu, lalu base64
        message_bytes = message.encode('utf-8')
        base64_encoded = base64.b64encode(message_bytes).decode('ascii')
        
        # Apply Caesar cipher ke base64 string
        result = []
        for char in base64_encoded:
            if char.isalnum():
                if char.isdigit():
                    # Shift angka 0-9
                    shifted = str((int(char) + self.shift) % 10)
                elif char.isupper():
                    # Shift huruf besar A-Z
                    shifted = chr((ord(char) - ord('A') + self.shift) % 26 + ord('A'))
                elif char.islower():
                    # Shift huruf kecil a-z
                    shifted = chr((ord(char) - ord('a') + self.shift) % 26 + ord('a'))
                else:
                    shifted = char
                result.append(shifted)
            else:
                result.append(char)  # Karakter khusus tidak diubah
        
        return ''.join(result)
    
    def decrypt(self, encrypted_message: str) -> str:
        """Decrypt message"""
        if not encrypted_message:
            return encrypted_message
        
        try:
            # Reverse Caesar cipher dulu
            result = []
            for char in encrypted_message:
                if char.isalnum():
                    if char.isdigit():
                        # Reverse shift angka
                        shifted = str((int(char) - self.shift) % 10)
                    elif char.isupper():
                        # Reverse shift huruf besar
                        shifted = chr((ord(char) - ord('A') - self.shift) % 26 + ord('A'))
                    elif char.islower():
                        # Reverse shift huruf kecil
                        shifted = chr((ord(char) - ord('a') - self.shift) % 26 + ord('a'))
                    else:
                        shifted = char
                    result.append(shifted)
                else:
                    result.append(char)
            
            base64_decoded_str = ''.join(result)
            
            # Decode dari base64 ke bytes, lalu ke string
            decoded_bytes = base64.b64decode(base64_decoded_str.encode('ascii'))
            original_message = decoded_bytes.decode('utf-8')
            
            return original_message
            
        except Exception as e:
            print(f"Decryption error for '{encrypted_message}': {e}")
            return encrypted_message

class DatabaseEncryption:
    def __init__(self):
        self.encryption = SimpleEncryption()
        self.encrypt_map, self.decrypt_map = load_mapping()
    
    def encrypt_profile_data(self, profile_data: dict) -> dict:
        """Encrypt sensitive fields dalam profile data"""
        sensitive_fields = [
            'first_name', 'last_name', 'address', 'phone_number'
        ]
        
        encrypted_data = profile_data.copy()
        
        for field in sensitive_fields:
            if field in profile_data and profile_data[field]:
                original_value = str(profile_data[field])
                
                # Skip jika sudah encrypted (ada di encrypt_map)
                if original_value in self.encrypt_map:
                    encrypted_value = self.encrypt_map[original_value]
                else:
                    # Encrypt value
                    encrypted_value = self.encryption.encrypt(original_value)
                    
                    # Store dalam mapping
                    self.encrypt_map[original_value] = encrypted_value
                    self.decrypt_map[encrypted_value] = original_value
                    
                    # Save mapping
                    save_mapping(self.encrypt_map, self.decrypt_map)
                
                encrypted_data[field] = encrypted_value
        
        return encrypted_data
    
    def decrypt_profile_data(self, encrypted_data: dict) -> dict:
        """Decrypt profile data"""
        if not encrypted_data:
            return encrypted_data
            
        decrypted_data = encrypted_data.copy()
        
        sensitive_fields = ['first_name', 'last_name', 'address', 'phone_number']
        
        for field in sensitive_fields:
            if field in encrypted_data and encrypted_data[field]:
                encrypted_value = str(encrypted_data[field])
                
                # Try mapping first
                if encrypted_value in self.decrypt_map:
                    decrypted_value = self.decrypt_map[encrypted_value]
                    decrypted_data[field] = decrypted_value
                else:
                    # Try direct decryption
                    decrypted_value = self.encryption.decrypt(encrypted_value)
                    if decrypted_value != encrypted_value:  # Berhasil decrypt
                        decrypted_data[field] = decrypted_value
                        # Update mapping
                        self.decrypt_map[encrypted_value] = decrypted_value
                        self.encrypt_map[decrypted_value] = encrypted_value
                        save_mapping(self.encrypt_map, self.decrypt_map)
        
        return decrypted_data

def encrypt_applicant_data(applicant_data: dict) -> dict:
    """Wrapper function untuk encrypt applicant data"""
    db_encryption = DatabaseEncryption()
    return db_encryption.encrypt_profile_data(applicant_data)

def decrypt_applicant_data(encrypted_data: dict) -> dict:
    """Wrapper function untuk decrypt applicant data"""
    db_encryption = DatabaseEncryption()
    return db_encryption.decrypt_profile_data(encrypted_data)

if __name__ == "__main__":
    # Test encryption dengan data Indonesia
    test_data = {
        'applicant_id': 1,
        'first_name': 'Mohammad',
        'last_name': 'Nugraha',
        'address': 'Jl. Kenanga No. 12, Jakarta',
        'phone_number': '+62-812-3456-7890',
        'date_of_birth': '2003-06-14'
    }
    
    print("=== TEST ENCRYPTION ===")
    print("Original data:")
    for k, v in test_data.items():
        print(f"  {k}: {v}")
    
    # Test simple encryption
    enc = SimpleEncryption()
    
    print("\n=== SIMPLE ENCRYPTION TEST ===")
    test_strings = ['Mohammad', 'Nugraha', 'Jl. Kenanga No. 12, Jakarta', '+62-812-3456-7890']
    
    for test_str in test_strings:
        encrypted = enc.encrypt(test_str)
        decrypted = enc.decrypt(encrypted)
        success = test_str == decrypted
    
    print("\n=== DATABASE ENCRYPTION TEST ===")
    # Database encryption test
    db_enc = DatabaseEncryption()
    encrypted = db_enc.encrypt_profile_data(test_data)
    
    print("Encrypted data:")
    for k, v in encrypted.items():
        print(f"  {k}: {v}")
    
    # Decrypt
    decrypted = db_enc.decrypt_profile_data(encrypted)
    
    print("\nDecrypted data:")
    for k, v in decrypted.items():
        print(f"  {k}: {v}")
    
    # Verify
    sensitive_fields = ['first_name', 'last_name', 'address', 'phone_number']
    success = all(test_data[k] == decrypted[k] for k in sensitive_fields if k in test_data)
    print(f"\n🎯 Overall decryption successful: {success}")
    
    if not success:
        print("Failed fields:")
        for field in sensitive_fields:
            if field in test_data and field in decrypted:
                if test_data[field] != decrypted[field]:
                    print(f"  {field}: '{test_data[field]}' ≠ '{decrypted[field]}'")