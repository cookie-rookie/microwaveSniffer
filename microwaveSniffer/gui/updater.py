import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QLabel, QProgressBar, QWidget)
import requests

class UpdaterWindow(QMainWindow):
    def __init__(self, user, repo, current_version, token=None):
        super().__init__()
        self.user = user
        self.repo = repo
        self.current_version = current_version
        self.token = token
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Updater')
        self.setGeometry(100, 100, 300, 100)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel('Checking for updates...', self)
        layout.addWidget(self.status_label)

        # Start the update process
        self.check_for_updates()

    def download_file(self, url):
        headers = {"Authorization": f"token {self.token}"} if self.token else {}
        with requests.get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            total_length = int(r.headers.get('content-length'))
            dl = 0
            local_filename = url.split('/')[-1]
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        dl += len(chunk)
                        f.write(chunk)
                        done = int(100 * dl / total_length)
                        self.progress_bar.setValue(done)
        return local_filename

    def check_for_updates(self):
        url = f"https://api.github.com/repos/{self.user}/{self.repo}/releases/latest"
        headers = {"Authorization": f"token {self.token}"} if self.token else {}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        latest_version = data['tag_name']
        if latest_version != self.current_version:
            self.status_label.setText(f'New version available: {latest_version}')
            for asset in data['assets']:
                self.status_label.setText(f'Downloading {asset["name"]}...')
                self.download_file(asset['browser_download_url'])
                self.status_label.setText(f'Downloaded {asset["name"]}')
            self.status_label.setText('Update completed.')
        else:
            self.status_label.setText('You are up to date.')

def run_updater(user, repo, current_version, token=None):
    app = QApplication(sys.argv)
    updater_window = UpdaterWindow(user, repo, current_version, token)
    updater_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    # Example usage
    run_updater('cookie-rookie', 'microwaveSniffer', '1.0.0', 'your_token_here')
