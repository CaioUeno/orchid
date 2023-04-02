import pytest
from orchid.decorators import exception_handler


class TestExceptionHandler:
    @staticmethod
    def write_file(tmp_path):
        d = tmp_path / "sub"
        d.mkdir()
        p = d / "tmp.txt"
        p.write_text("error handled!")

    def test_no_handlers(self):
        @exception_handler(
            exception=TypeError, callback=print, callback_args=["Type error detected!"]
        )
        def dummy():
            raise ValueError()

        with pytest.raises(ValueError):
            dummy()

    def test_simple_handler(self, tmp_path):
        @exception_handler(
            exception=TypeError,
            callback=self.write_file,
            callback_args=[tmp_path],
            exception_return="check!",
        )
        def dummy():
            raise TypeError()

        r = dummy()

        assert r == "check!"

        d = tmp_path / "sub"
        p = d / "tmp.txt"

        assert p.read_text() == "error handled!"
