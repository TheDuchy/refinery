#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from refinery.units.blockwise import Arg, BlockTransformationBase


class terminate(BlockTransformationBase):
    """
    The unit reads data from the incoming chunk in blocks of any given size until the
    sentinel value is encountered. The output of the unit is all data that was read,
    excluding the sentinel. The default block size is one and the default sentinel value
    is zero, which corresponds to reading a null-terminated string from the input.
    If the sentinel value is not found anywhere in the incoming data, the complete input
    is returned as output.
    """
    def __init__(
        self,
        sentinel: Arg(help='sentinel value to look for; default is {default}') = B'\0',
        blocksize=1, bigendian=False
    ):
        super().__init__(blocksize=blocksize, bigendian=bigendian, sentinel=sentinel)

    def process(self, data: bytearray):
        sentinel = self.args.sentinel
        position = 0
        blocksize = self.args.blocksize

        while position >= 0:
            position = data.find(sentinel, position)
            if position < 0:
                self.log_info(F'The sentinel value {sentinel} was not found.')
                break
            if position % blocksize:
                position += 1
                continue
            else:
                data[position:] = []
                break

        return data
