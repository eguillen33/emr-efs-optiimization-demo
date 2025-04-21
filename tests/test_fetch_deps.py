from unittest.mock import patch, mock_open, call
from src import fetch_deps


@patch("src.fetch_deps.run_cmd")
@patch("src.fetch_deps.os.makedirs")
@patch("src.fetch_deps.is_efs_mounted", return_value=False)
def test_mount_efs_when_not_mounted(mock_is_mounted, mock_makedirs, mock_run_cmd):
    fetch_deps.mount_efs()
    mock_makedirs.assert_called_once_with(fetch_deps.EFS_MOUNT_PATH, exist_ok=True)
    mock_run_cmd.assert_called_once()


@patch("src.fetch_deps.is_efs_mounted", return_value=True)
@patch("src.fetch_deps.log")
def test_mount_efs_when_already_mounted(mock_log, mock_is_mounted):
    fetch_deps.mount_efs()
    mock_log.assert_called_with("EFS already mounted.")


@patch("src.fetch_deps.run_cmd")
def test_copy_from_efs(mock_run_cmd):
    fetch_deps.copy_from_efs()
    expected_path = [
        "cp", "-r", f"{fetch_deps.EFS_MOUNT_PATH}/dependencies", fetch_deps.LOCAL_DEPS_PATH
    ]
    mock_run_cmd.assert_called_with(expected_path, check=True)


@patch("src.fetch_deps.run_cmd")
def test_fetch_from_s3(mock_run_cmd):
    fetch_deps.fetch_from_s3()
    calls = [
        call([
            "aws", "s3", "cp", f"s3://{fetch_deps.S3_BUCKET}/dependencies.tar.gz", "/tmp/"
        ], check=True),
        call([
            "tar", "-xzf", "/tmp/dependencies.tar.gz", "-C", "/home/hadoop/"
        ], check=True)
    ]
    mock_run_cmd.assert_has_calls(calls)


@patch("builtins.open", new_callable=mock_open, read_data='{"use_efs": true}')
@patch("src.fetch_deps.mount_efs")
@patch("src.fetch_deps.copy_from_efs")
def test_main_use_efs(mock_copy, mock_mount, mock_open_file):
    fetch_deps.main()
    mock_mount.assert_called_once()
    mock_copy.assert_called_once()


@patch("builtins.open", new_callable=mock_open, read_data='{"use_efs": false}')
@patch("src.fetch_deps.fetch_from_s3")
def test_main_use_s3(mock_fetch, mock_open_file):
    fetch_deps.main()
    mock_fetch.assert_called_once()
