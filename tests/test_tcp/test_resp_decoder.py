from src.resp.decoder import RESPDecoder

class TestRESPDecoder:
    def test_decode_array_one_bulk_string(self):
        encoding = "*1\r\n$5\r\nhello\r\n"
        decoded = RESPDecoder.decode_command(encoding)
        assert decoded == ["hello"]
    
    def test_decode_array_two_bulk_strings(self):
        encoding = "*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n"
        decoded = RESPDecoder.decode_command(encoding)
        assert decoded == ["hello", "world"]

    def test_decode_empty(self):
        encoding = ""
        decoded = RESPDecoder.decode_command(encoding)
        assert decoded == ["Invalid command"]

    def test_decode_invalid_command(self):
        encoding = "+OK\r\n"
        decoded = RESPDecoder.decode_command(encoding)
        assert decoded == ["Invalid command"]