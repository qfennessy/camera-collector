import pytest

from camera_collector.models.token import Token, TokenPayload


class TestTokenModel:
    """Test Token model."""
    
    def test_token_model(self):
        """Test creating a Token model."""
        token = Token(
            access_token="access_token_value", 
            refresh_token="refresh_token_value", 
            token_type="bearer"
        )
        
        assert token.access_token == "access_token_value"
        assert token.refresh_token == "refresh_token_value"
        assert token.token_type == "bearer"
    
    def test_token_payload_model(self):
        """Test creating a TokenPayload model."""
        payload = TokenPayload(sub="user_123")
        
        assert payload.sub == "user_123"