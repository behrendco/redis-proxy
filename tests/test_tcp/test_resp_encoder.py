from src.resp.encoder import RESPEncoder

class TestRESPEncoder:
    def test_encode_bulk_string(self):
        string = "hello"
        encoded = RESPEncoder.encode_bulk_string(string)
        assert encoded == "$5\r\nhello\r\n"

    def test_encode_empty_bulk_string(self):
        string = ""
        encoded = RESPEncoder.encode_bulk_string(string)
        assert encoded == "$0\r\n\r\n"

    def test_encode_error(self):
        string = "Error message"
        encoded = RESPEncoder.encode_error(string)
        assert encoded == "-Error message\r\n"
