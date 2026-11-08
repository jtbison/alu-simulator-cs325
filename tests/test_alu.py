from alu_simulator.alu import ALU, ALUResult


def test_add():
    alu = ALU(8)
    res = alu.add(12, 5)
    assert res == ALUResult(value=17, carry=False, overflow=False)


def test_add_carry():
    alu = ALU(8)
    # unsigned
    res = alu.add(255, 1)
    assert res == ALUResult(
        value=0,
        carry=True,
        overflow=False,
    )


def test_add_overflow():
    alu = ALU(8)
    # signed
    res = alu.add(127, 1)
    assert res == ALUResult(value=128, carry=False, overflow=True)


def test_add_both():
    alu = ALU(8)
    res = alu.add(128, 255)
    assert res == ALUResult(
        value=127,
        carry=True,
        overflow=True,
    )


def test_sub_normal():
    alu = ALU(8)
    assert alu.sub(12, 5) == ALUResult(
        value=7,
        carry=False,
        overflow=False,
    )


def test_sub_borrow():
    alu = ALU(8)
    assert alu.sub(0, 1) == ALUResult(
        value=255,
        carry=True,
        overflow=False,
    )


def test_sub_overflow():
    alu = ALU(8)
    assert alu.sub(127, 255) == ALUResult(
        value=128,
        carry=True,
        overflow=True,
    )


def test_sub_negative_overflow():
    alu = ALU(8)
    assert alu.sub(128, 1) == ALUResult(
        value=127,
        carry=False,
        overflow=True,
    )


def test_and_normal():
    alu = ALU(8)
    assert alu.bitwise_and(12, 5) == ALUResult(
        value=4,
        carry=False,
        overflow=False,
    )


def test_and_no_matching_bits():
    alu = ALU(8)
    assert alu.bitwise_and(10, 5) == ALUResult(
        value=0,
        carry=False,
        overflow=False,
    )


def test_and_all_bits():
    alu = ALU(8)
    assert alu.bitwise_and(255, 170) == ALUResult(
        value=170,
        carry=False,
        overflow=False,
    )


def test_or_normal():
    alu = ALU(8)
    assert alu.bitwise_or(12, 5) == ALUResult(
        value=13,
        carry=False,
        overflow=False,
    )


def test_or_zero():
    alu = ALU(8)
    assert alu.bitwise_or(12, 0) == ALUResult(
        value=12,
        carry=False,
        overflow=False,
    )


def test_xor_normal():
    alu = ALU(8)
    assert alu.bitwise_xor(12, 5) == ALUResult(
        value=9,
        carry=False,
        overflow=False,
    )


def test_xor_same_values():
    alu = ALU(8)
    assert alu.bitwise_xor(255, 255) == ALUResult(
        value=0,
        carry=False,
        overflow=False,
    )


def test_shift_left():
    alu = ALU(8)

    assert alu.shift_left(129, 1) == ALUResult(
        value=2,
        carry=True,
        overflow=False,
    )


def test_shift_right():
    alu = ALU(8)

    assert alu.shift_right(129, 1) == ALUResult(
        value=64,
        carry=True,
        overflow=False,
    )


def test_shift_left_no_carry():
    alu = ALU(8)

    assert alu.shift_left(12, 2) == ALUResult(
        value=48,
        carry=False,
        overflow=False,
    )


def test_shift_right_zero():
    alu = ALU(8)

    assert alu.shift_right(12, 0) == ALUResult(
        value=12,
        carry=False,
        overflow=False,
    )
