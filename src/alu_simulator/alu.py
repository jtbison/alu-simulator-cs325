from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ALUResult:
    value: int
    carry: bool = False
    overflow: bool = False


class ALU:
    __slots__ = (
        "bits",
        "mask",
        "sign_bit",
    )

    def __init__(self, bits: int = 8) -> None:
        self.bits = bits
        # Constrain binary number to just `bits` number of bits
        self.mask = (1 << bits) - 1
        self.sign_bit = 1 << (self.bits - 1)

    def add(self, a: int, b: int) -> ALUResult:
        carry = (a + b) > self.mask
        result = (a + b) & self.mask
        # ((A XNOR B) AND (A XOR result)) AND sign_bit
        # If A and B have the same sign AND if the result has
        # a different sign from A (scoped within only sign bits)
        overflow = bool((~(a ^ b) & (a ^ result) & self.sign_bit))
        return ALUResult(value=result, carry=carry, overflow=overflow)

    def sub(self, a: int, b: int) -> ALUResult:
        result = (a - b) & self.mask
        carry = a < b
        # ((A XOR B) AND (A XOR result)) AND sign_bit
        # If A and B have different signs AND if the result has
        # a different sign from A (scoped within only sign bits)
        overflow = bool(((a ^ b) & (a ^ result)) & self.sign_bit)
        return ALUResult(value=result, carry=carry, overflow=overflow)

    def bitwise_and(self, a: int, b: int) -> ALUResult:
        # A AND B within `mask` bits constrained
        result = (a & b) & self.mask
        return ALUResult(value=result)

    def bitwise_or(self, a: int, b: int) -> ALUResult:
        result = (a | b) & self.mask
        return ALUResult(value=result)

    def bitwise_xor(self, a: int, b: int) -> ALUResult:
        result = (a ^ b) & self.mask
        return ALUResult(
            value=result,
            carry=False,
            overflow=False,
        )

    def shift_left(self, a: int, amount: int) -> ALUResult:
        if not 0 <= amount < self.bits:
            raise ValueError(f"Invalid shift amount (0-${self.bits})")

        a &= self.mask
        result = (a << amount) & self.mask

        # False if no amount because no shifting obv
        carry = bool((a >> (self.bits - amount)) & 1) if amount else False

        return ALUResult(
            value=result,
            carry=carry,
            overflow=False,
        )

    def shift_right(self, a: int, amount: int) -> ALUResult:
        if not 0 <= amount < self.bits:
            raise ValueError("Invalid shift amount")

        a &= self.mask
        result = a >> amount

        carry = bool((a >> (amount - 1)) & 1) if amount else False

        return ALUResult(
            value=result,
            carry=carry,
            overflow=False,
        )
