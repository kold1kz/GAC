"""test"""
import asyncio
import os
import pytest
import with_async 


class Tests:
    """test class"""

    def test_check_list(self):
        """test check_list func"""
        assert with_async.check_list(
            ["ve/asd/123",
             "ve/asd/1234",
             "ve/asd/"],
            7) == ["ve/asd/123",
                   "ve/asd/1234"], "check_list error"

    def test_download_file(self):
        """test_download_file"""
        result = asyncio.run(with_async.download_file(5))
        assert result is None

    def test_main(self, monkeypatch):
        """test main"""
        monkeypatch.setattr(
            'builtins.input', lambda _: "https://gitea.radium.group/radium/project-configuration")
        assert with_async.main() is True

    def test_main_1(self, monkeypatch):
        """test main_1"""
        monkeypatch.setattr(
            'builtins.input', lambda _: "https://gitea.radium.group/radium/project-configuration")
        assert with_async.main() is False

    def test_main_3(self, monkeypatch):
        """test main_3"""
        monkeypatch.setattr(
            'builtins.input', lambda _: "http:///gitea.radium.group/radium/project-configuration/asdasda")
        assert with_async.main() is True

    def test_download_repo(self):
        """test download_repo"""
        assert asyncio.run(with_async.download_repo(url=0)) is None

    def test_get_urls(self):
        """test get_urls"""
        assert asyncio.run(with_async.get_urls(5)) is None

    def test_get_urls_2(self):
        """test get_urls_2"""
        assert asyncio.run(with_async.get_urls("\n")) is None

    def test_get_urls_3(self):
        """test get_urls_3"""
        assert asyncio.run(with_async.get_urls("\0")) is None

    # def test_main_name(self):
    #     """test_main_name"""
    #     assert runpy.run_path('src/with_async.py')[]  is True


if __name__ == "__main__":
    os.exit(pytest.main(["-qq"], plugins=[Tests()]))
