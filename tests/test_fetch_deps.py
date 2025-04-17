import unittest
from unittest.mock import patch, MagicMock
from bootstrap import fetch_deps

class TestFetchDeps(unittest.TestCase):

    @patch("subprocess.run")
    def test_use_efs_true(self, mock_subprocess):
        with patch("builtins.open", new_callable=unittest.mock.mock_open, read_data='{"use_efs": true}'):
            fetch_deps.EFS_DNS_NAME = "dummy"
            fetch_deps.main()
            self.assertTrue(mock_subprocess.called)

    @patch("subprocess.run")
    def test_use_efs_false(self, mock_subprocess):
        with patch("builtins.open", new_callable=unittest.mock.mock_open, read_data='{"use_efs": false}'):
            fetch_deps.main()
            self.assertTrue(mock_subprocess.called)
