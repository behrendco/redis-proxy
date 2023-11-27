class RESPDecoder:
    def decode_command(
            command: str) -> list:
        """
        Decodes string data to a Redis command according to the Redis serialization 
        protocol (RESP).
        Clients send commands to a Redis server as an array of bulk strings.
        The first (and sometimes second) bulk string in the array is the command's name. 
        Subsequent elements of the array are the arguments for the command.
        If the encoded command is not an array of bulk strings, returns a list 
        consisting of a single error message to indicate that.

        :param str string: The string data to encode.

        :return: Encoded bulk string.
        :rtype: str
        """
        if not command:
            return ["Invalid command"]
        
        data_type = command[0]
        if data_type != "*":
            return ["Invalid command"]
        
        return RESPDecoder.decode_array(command)

    def decode_array(
            array: str) -> list:
        """
        Decodes the array string consisting of bulk strings.
        Calls the decode_bulk_string class method on each bulk string in the array.

        :param str array: The string representing an array of bulk strings.

        :return: Returns a list of decoded bulk string elements consisting of the command.
        :rtype: list
        """
        decoded = []
        delim_index = array.find("\r\n")
        if delim_index == -1:
            return ["Invalid command"]
        
        elements = int(array[1:delim_index])
        start_index = delim_index + 2

        for _ in range(elements):
            string, new_start = RESPDecoder.decode_bulk_string(array, start_index)
            decoded.append(string)
            start_index = new_start

        return decoded

    def decode_bulk_string(
            string: str, 
            start_index: int) -> tuple:
        """
        Decodes each bulk string in the encoded command array and sends a 
        response back to the decode_array class method.

        :param str string: Data to decode.
        :param int start_index: Index representing the point of the string not yet decoded.

        :return: Returns a pair consisting of a single decoded bulk string in the array, 
        and the index to start at in the next pass.
        :rtype: tuple
        """
        delim_index = string.find("\r\n", start_index)
        string_len = int(string[start_index + 1:delim_index])
        string_start = delim_index + 2
        return (string[string_start:string_start + string_len], 
                string_start + string_len + 2)