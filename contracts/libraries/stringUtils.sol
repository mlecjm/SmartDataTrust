// SPDX-License-Identifier: MIT
pragma solidity >0.6.1 <0.9.0;

library StringUtils {
  
  function uint2str(uint256 _i) internal pure returns (string memory str) {
    if (_i == 0) {
      return "0";
    }
    uint256 j = _i;
    uint256 length;
    while (j != 0) {
      length++;
      j /= 10;
    }
    bytes memory bstr = new bytes(length);
    uint256 k = length;
    j = _i;
    while (j != 0) {
      bstr[--k] = bytes1(uint8(48 + (j % 10)));
      j /= 10;
    }
    str = string(bstr);
  }

  function toString(address account) public pure returns(string memory) {
    return toString(abi.encodePacked(account));
  }

  function toString(uint256 value) public pure returns(string memory) {
    return toString(abi.encodePacked(value));
  }

  function toString(bytes32 value) public pure returns(string memory) {
    return toString(abi.encodePacked(value));
  }

  function toString(bytes memory data) public pure returns(string memory) {
    bytes memory alphabet = "0123456789abcdef";
    bytes memory str = new bytes(2 + data.length * 2);
    str[0] = "0";
    str[1] = "x";
    for (uint i = 0; i < data.length; i++) {
      str[2+i*2] = alphabet[uint(uint8(data[i] >> 4))];
      str[3+i*2] = alphabet[uint(uint8(data[i] & 0x0f))];
    }
    return string(str);
  }
}
