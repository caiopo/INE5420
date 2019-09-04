class Matrix3:
    @classmethod
    def zeros(cls):
        return cls(
            [0] * 3 for _ in range(3)
        )

    @classmethod
    def identity(cls):
        return cls(
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        )

    def __init__(self, *rows):
        rows = list(rows)
        if len(rows) == 1:
            rows = rows[0]

        self.values = []

        for r in rows:
            self.values.extend(float(e) for e in r)

        assert len(self.values) == 9

    def __matmul__(self, other):
        assert isinstance(other, Matrix3)

        result = Matrix3.zeros()

        for i in range(3):
            for j in range(3):
                result[i, j] = sum(
                    self[i, k] * other[k, j]
                    for k in range(3)
                )

        return result

    def __getitem__(self, key):
        r, c = key

        return self.values[r * 3 + c]

    def __setitem__(self, key, value):
        r, c = key
        self.values[r * 3 + c] = float(value)

    def __str__(self):
        s = [
            self.values[0:3],
            self.values[3:6],
            self.values[6:9],
        ]
        return f'Matrix({s})'


m = Matrix3(
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
)

print(m @ m)
