"""
Authentication utilities for password hashing and verification
"""
import base64
import traceback
import warnings
import logging
from contextlib import redirect_stderr
import io
from passlib.context import CryptContext

# Try to import scrypt for manual verification
try:
    import scrypt
    _scrypt_lib_available = True
except ImportError:
    _scrypt_lib_available = False
    scrypt = None

# Suppress bcrypt version warning and passlib warnings
warnings.filterwarnings("ignore", category=UserWarning, module="passlib")
warnings.filterwarnings("ignore", message=".*bcrypt.*")
logging.getLogger("passlib").setLevel(logging.ERROR)

# Suppress the trapped bcrypt error by temporarily redirecting stderr during initialization
_stderr_buffer = io.StringIO()
with redirect_stderr(_stderr_buffer):
    try:
        # Try to support both bcrypt and scrypt for password verification
        # If scrypt is not available, fall back to bcrypt only
        try:
            pwd_context = CryptContext(schemes=["bcrypt", "scrypt"], deprecated="auto")
            _scrypt_available = True
        except (ValueError, AttributeError) as e:
            # scrypt not available, use bcrypt only
            print(f"Note: scrypt not available, using bcrypt only: {str(e)}")
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            _scrypt_available = False
    except Exception as e:
        # Final fallback
        print(f"Warning: Error initializing CryptContext: {str(e)}")
        try:
            pwd_context = CryptContext(schemes=["bcrypt", "scrypt"])
            _scrypt_available = True
        except Exception:
            pwd_context = CryptContext(schemes=["bcrypt"])
            _scrypt_available = False


def verify_scrypt_hash_manual(password: str, hash_string: str) -> bool:
    """Manually verify a scrypt hash using the scrypt library"""
    if not _scrypt_lib_available:
        return False
    
    try:
        # Parse custom scrypt format: scrypt:N:r:p$salt$hash
        # Example: scrypt:32768:8:1$5cgokKpgfRsnx5Gb$9f32d1abe6ce3ba3df9e62149c58e643dd4667b6179cccf5284ea6c56892ead188aa28371bfa309ba268fa4a2a437192d2e8b7a2bf7059fad8c0824e6cab4ea5
        if not hash_string.startswith('scrypt:'):
            return False
        
        # Remove 'scrypt:' prefix
        hash_part = hash_string[7:]
        
        # Split by $ to get params and salt+hash
        parts = hash_part.split('$')
        if len(parts) != 3:
            return False
        
        # Parse N:r:p parameters
        params = parts[0].split(':')
        if len(params) != 3:
            return False
        
        N = int(params[0])  # CPU/memory cost parameter
        r = int(params[1])  # Block size parameter
        p = int(params[2])  # Parallelization parameter
        
        # Salt might be base64 or raw string - try both
        salt_str = parts[1]
        stored_hash = parts[2]
        
        # Try different salt decoding methods
        salt = None
        # Method 1: Try base64 decode (with and without padding)
        try:
            # Add padding if needed for base64
            salt_str_padded = salt_str
            missing_padding = len(salt_str) % 4
            if missing_padding:
                salt_str_padded += '=' * (4 - missing_padding)
            salt = base64.b64decode(salt_str_padded)
        except Exception:
            pass
        
        # Method 2: If base64 failed, try as raw UTF-8 string
        if salt is None:
            try:
                salt = salt_str.encode('utf-8')
            except Exception:
                pass
        
        # Method 3: If still None, try as hex
        if salt is None:
            try:
                salt = bytes.fromhex(salt_str)
            except Exception:
                pass
        
        if salt is None:
            print(f"Error: Could not decode salt: {salt_str}")
            return False
        
        # Compute hash using scrypt
        password_bytes = password.encode('utf-8')
        computed_hash = scrypt.hash(password_bytes, salt, N=N, r=r, p=p)
        
        # Convert to hex for comparison
        computed_hash_hex = computed_hash.hex()
        
        # Compare hashes (stored hash is already hex)
        return computed_hash_hex == stored_hash
    except Exception as e:
        print(f"Error in manual scrypt verification: {str(e)}")
        traceback.print_exc()
        return False


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    try:
        # Reject empty or missing plain password
        if not plain_password or not isinstance(plain_password, str):
            return False
        plain_password = plain_password.strip()
        if not plain_password:
            return False
        # Check if hash is valid before attempting verification
        if not hashed_password or not isinstance(hashed_password, str):
            print(f"Error: Invalid hash format - hash is empty or not a string")
            return False
        
        # Check if hash looks valid (should start with $2b$, $2a$, $2y$ for bcrypt or scrypt: for scrypt)
        if not (hashed_password.startswith('$2') or hashed_password.startswith('scrypt:')):
            print(f"Error: Hash format not recognized - hash starts with: {hashed_password[:20] if len(hashed_password) > 20 else hashed_password}")
            return False
        
        # Try passlib verification first
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception as passlib_error:
            error_msg = str(passlib_error).lower()
            
            # If passlib can't identify scrypt hash, try manual verification
            if hashed_password.startswith('scrypt:'):
                if "hash could not be identified" in error_msg or "unknown hash algorithm" in error_msg:
                    print(f"Passlib couldn't verify scrypt hash, trying manual verification...")
                    if _scrypt_lib_available:
                        result = verify_scrypt_hash_manual(plain_password, hashed_password)
                        if result:
                            print(f"Manual scrypt verification succeeded")
                            return True
                        else:
                            print(f"Manual scrypt verification failed")
                    else:
                        raise ValueError("Password hash uses scrypt format, but scrypt library is not available. Please install scrypt package or re-hash the password using bcrypt.")
                else:
                    # Some other error with passlib, try manual verification as fallback
                    if _scrypt_lib_available:
                        print(f"Passlib error with scrypt, trying manual verification: {error_msg}")
                        result = verify_scrypt_hash_manual(plain_password, hashed_password)
                        if result:
                            return True
            
            # Re-raise if we can't handle it
            raise passlib_error
            
    except ValueError as e:
        # Re-raise ValueError (our custom error for missing scrypt)
        raise
    except Exception as e:
        error_msg = str(e).lower()
        if "hash could not be identified" in error_msg or "unknown hash algorithm" in error_msg:
            # Hash format not supported
            if hashed_password.startswith('scrypt:'):
                if _scrypt_lib_available:
                    # Last attempt with manual verification
                    result = verify_scrypt_hash_manual(plain_password, hashed_password)
                    if result:
                        return True
                raise ValueError("Password hash uses scrypt format, but scrypt support is not available. Please install scrypt package or re-hash the password using bcrypt.")
            else:
                raise ValueError(f"Password hash format not recognized: {hashed_password[:30]}...")
        print(f"Error verifying password: {str(e)}")
        print(f"Hash format: {hashed_password[:50] if hashed_password and len(hashed_password) > 50 else hashed_password}")
        raise


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)
