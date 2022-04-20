from drawille import Canvas
from sys import stdin


def get_wave_graph(wave):
    c = Canvas()

    wave_chars = []

    # remove last 2 ff
    if wave[-2:] != "ff":
        raise ValueError
    wave = wave[:-2]

    for i, s in enumerate(wave):
        n = int(s, 16)
        n = 16 - n
        c.set(i, n)

    wave_rows = 5
    canvas_rows = len(c.rows())

    for r in c.rows():
        yield "| " + r.ljust(16)

    for _ in range(wave_rows - canvas_rows):
        yield "| " + " " * 16


def main():
    line_cache = {}

    for line in stdin:
        k, _, v = line.partition(": ")

        if not v or len(k) > 4:
            print(line, end="")
            continue

        # store CH[1234], MISC, WAVE in cache
        v = v.strip()
        line_cache[k] = v

        if k == "WAVE":
            wave_chars = get_wave_graph(v)

            # output CH[1234], MISC, WAVE with chart
            for k, v in line_cache.items():
                wc = next(wave_chars, "")
                print(f"{(k + ':').ljust(5)} {v.ljust(14)} {wc}")


if __name__ == "__main__":

    try:
        print("\x1b[?25l")  # hide cursor
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print("\x1b[?25h")  # show cursor
