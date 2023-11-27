class RESPEncoder:
    def encode_bulk_string( 
            string: str) -> str:
        """
        Encodes string data to a bulk string according to the Redis serialization 
        protocol (RESP).
        RESP encodes bulk strings in the following way: $<length>\r\n<data>\r\n

        :param str string: The string data to encode.

        :return: Encoded bulk string.
        :rtype: str
        """
        return f"${len(string)}\r\n{string}\r\n"
    
    def encode_error(
            error: str) -> str:
        """
        Encodes error message to a simple error according to the Redis serialization 
        protocol (RESP).
        RESP encodes simple errors in the following way: -Error message\r\n

        :param str error: The error message to encode.

        :return: Encoded simple error.
        :rtype: str
        """
        return f"-{error}\r\n"