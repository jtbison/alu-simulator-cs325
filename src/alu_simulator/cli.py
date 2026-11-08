import readchar

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from collections.abc import Callable
from .alu import ALU, ALUResult

console = Console()

OPERATIONS = {
    1: ("ADD", "add", "+"),
    2: ("SUB", "sub", "-"),
    3: ("AND", "bitwise_and", "&"),
    4: ("OR", "bitwise_or", "|"),
    5: ("XOR", "bitwise_xor", "^"),
    6: ("Shift Left", "shift_left", "<<"),
    7: ("Shift Right", "shift_right", ">>"),
}


def show_menu(compact: bool = False) -> Panel:
    if compact:
        return Panel.fit(
            "1 ADD  2 SUB  3 AND  4 OR\n5 XOR  6 SHL  7 SHR  0 Exit",
            title="[bold cyan]Mini ALU Simulator[/bold cyan]",
            border_style="blue",
        )

    table = Table(
        show_header=False,
        show_edge=False,
        box=None,
        padding=(0, 3),
    )

    table.add_column()
    table.add_column()

    table.add_row("1. ADD", "5. XOR")
    table.add_row("2. SUB", "6. Shift Left")
    table.add_row("3. AND", "7. Shift Right")
    table.add_row("4. OR", "0. Exit")

    return Panel.fit(
        table,
        title="[bold cyan]Mini ALU Simulator[/bold cyan]",
        border_style="blue",
    )


def create_layout() -> Layout:
    layout = Layout()

    layout.split_column(
        Layout(show_menu(), name="menu", size=6),
        Layout(" ", name="gap", size=1),
        Layout(" ", name="content", size=1),
        Layout(" ", name="spacer"),
    )

    return layout


def update_menu(layout: Layout) -> int:
    compact = console.height < 22

    layout["menu"].size = 4 if compact else 6
    layout["menu"].update(show_menu(compact))

    return layout["menu"].size + 1


def get_number(
    layout: Layout,
    live: Live,
    prompt: str,
    maximum: int,
) -> int:
    typed = ""
    error = ""

    while True:
        update_menu(layout)

        content = Text()
        content.append(f"==> {prompt}: ", style="cyan")
        content.append(typed + "_", style="bold white")

        if error:
            content.append(f"\n{error}", style="red")

        layout["content"].size = 2 if error else 1
        layout["content"].update(content)
        live.refresh()

        key = readchar.readkey()

        if key == "\x03":
            raise KeyboardInterrupt

        if key == readchar.key.ENTER:
            if typed and 0 <= int(typed) <= maximum:
                return int(typed)

            error = f"Value must be between 0 and {maximum}."

        elif key in (readchar.key.BACKSPACE, "\x7f"):
            typed = typed[:-1]
            error = ""

        elif len(key) == 1 and key in "0123456789":
            if len(typed) < len(str(maximum)) + 1:
                typed += key
                error = ""


def get_operation(layout: Layout, live: Live) -> int:
    return get_number(layout, live, "Enter operation (0-7)", 7)


def get_operands(
    alu: ALU,
    layout: Layout,
    live: Live,
    operation: int,
) -> tuple[int, int]:
    a = get_number(layout, live, "Enter operand A", alu.mask)

    if operation in (6, 7):
        b = get_number(layout, live, "Enter shift amount", alu.bits - 1)
    else:
        b = get_number(layout, live, "Enter operand B", alu.mask)

    return a, b


def build_result(
    alu: ALU,
    operation: int,
    a: int,
    b: int,
) -> tuple[str, Text]:
    name, _, symbol = OPERATIONS[operation]

    methods: dict[int, Callable[[int, int], ALUResult]] = {
        1: alu.add,
        2: alu.sub,
        3: alu.bitwise_and,
        4: alu.bitwise_or,
        5: alu.bitwise_xor,
        6: alu.shift_left,
        7: alu.shift_right,
    }

    result = methods[operation](a, b)
    title = f"{name} — {alu.bits}-bit ALU"
    width = alu.bits

    content = Text()

    content.append("A   ", style="cyan")
    content.append(f"{a:0{width}b}", style="white")
    content.append(f"  ({a})\n", style="dim")

    if operation in (6, 7):
        content.append(f"{symbol}  ", style="cyan")
        content.append(f"{b} positions\n", style="white")
    else:
        content.append(f"{symbol}   ", style="cyan")
        content.append(f"{b:0{width}b}", style="white")
        content.append(f"  ({b})\n", style="dim")

    content.append("    " + "─" * width + "\n", style="blue")

    content.append("=   ", style="bold cyan")
    content.append(
        f"{result.value:0{width}b}",
        style="bold green",
    )
    content.append(f"  ({result.value})\n", style="dim")

    if operation in (1, 2):
        label = "Carry" if operation == 1 else "Borrow"

        content.append(f"\n{label}: ", style="cyan")
        content.append(str(result.carry))

        content.append("\nSigned overflow: ", style="cyan")
        content.append(str(result.overflow))

    elif operation in (6, 7):
        content.append("\nLast shifted-out bit: ", style="cyan")
        content.append(str(int(result.carry)))

    sign_bit = 1 << (width - 1)

    if result.value & sign_bit:
        magnitude = ((~result.value) & alu.mask) + 1
        signed_value = -magnitude
    else:
        signed_value = result.value

    content.append("\n\nUnsigned result: ", style="cyan")
    content.append(str(result.value))

    content.append("\nSigned (2's complement): ", style="cyan")
    content.append(str(signed_value))

    content.append(
        "\n\nPress Enter to return to the menu.",
        style="dim",
    )

    return title, content


def draw_result(
    layout: Layout,
    live: Live,
    title: str,
    content: Text,
    offset: int = 0,
) -> int:
    menu_height = update_menu(layout)
    available = max(3, console.height - menu_height)

    lines = content.split("\n", allow_blank=True)
    scrolling = len(lines) + 2 > available

    capacity = (
        max(
            1,
            available - 2 - int(scrolling),
        )
        if scrolling
        else len(lines)
    )

    max_offset = max(0, len(lines) - capacity)
    offset = max(0, min(offset, max_offset))

    visible = Text("\n").join(lines[offset : offset + capacity])

    if scrolling:
        visible.append(
            f"\n↑/↓ Scroll ({offset + 1}-"
            f"{min(offset + capacity, len(lines))}"
            f"/{len(lines)})",
            style="dim",
        )

    layout["content"].size = min(
        available,
        capacity + 2 + int(scrolling),
    )

    layout["content"].update(
        Panel.fit(
            visible,
            title=f"[bold cyan]{title}[/bold cyan]",
            border_style="blue",
            padding=(0, 1),
        )
    )

    live.refresh()
    return offset


def wait_for_enter(
    layout: Layout,
    live: Live,
    title: str,
    content: Text,
) -> None:
    offset = 0

    while True:
        offset = draw_result(layout, live, title, content, offset)

        key = readchar.readkey()

        if key == "\x03":
            raise KeyboardInterrupt

        if key == readchar.key.ENTER:
            return

        if key in (readchar.key.UP, "k"):
            offset -= 1

        elif key in (readchar.key.DOWN, "j"):
            offset += 1


def main() -> None:
    alu = ALU(8)
    layout = create_layout()

    try:
        with Live(
            layout,
            console=console,
            screen=True,
            auto_refresh=False,
        ) as live:
            while True:
                operation = get_operation(layout, live)

                if operation == 0:
                    break

                a, b = get_operands(alu, layout, live, operation)

                title, content = build_result(alu, operation, a, b)

                wait_for_enter(layout, live, title, content)

    except KeyboardInterrupt, EOFError:
        pass
