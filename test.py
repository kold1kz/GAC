"""test"""
import pytest
import src.with_async as with_async


class Tests:
    """test class"""

    def test_dowload_repo(self):
        """download_repo test"""
        assert with_async.download_repo(
            'https://gitea.radium.group/radium/project-configuration') is True

    def test_dowload_repo_2(self):
        """download_repo test"""
        assert with_async.download_repo(
            'https://gitea.radium.group/radium/project-configuration') is False

    def test_dowload_repo_3(self):
        """download_repo test"""
        assert with_async.download_repo('') is False

    def test_dowload_repo_4(self):
        """download_repo test"""
        assert with_async.download_repo(
            'htps://gite.radium.group/radium/project-configuration') is False

    def test_check_list(self):
        """test check_list func"""
        assert with_async.check_list(
            ["ve/asd/123",
             "ve/asd/1234",
             "ve/asd/"],
            7) == ["ve/asd/123",
                   "ve/asd/1234"], "check_list error"

    def test_main(self):
        """test main"""
        assert with_async.main()
