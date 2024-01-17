from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    """
    Helper class for password hashing and verification.

    Uses the `passlib.context.CryptContext` to securely hash passwords
    using the `bcrypt` algorithm. Passwords are automatically salted during
    the hashing process to enhance security.
    """

    @staticmethod
    def verify_password(*, plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a provided plain-text password against a hashed password.

        Args:
            plain_password (str): The plain-text password to be verified.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the passwords match, False otherwise.
        """

        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(*, password: str) -> str:
        """
        Generates a secure hash for a given plain-text password.

        Args:
            password (str): The plain-text password to be hashed.

        Returns:
            str: The generated hashed password.
        """

        return pwd_context.hash(password)