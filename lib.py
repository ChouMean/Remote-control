import subprocess
import pkg_resources

libraries = ["Pillow", "pygetwindow", "mss", "psutil", "pynput"]
installed_libraries = [lib.project_name for lib in pkg_resources.working_set]

for lib in libraries:
    if lib not in installed_libraries:
        try:
            subprocess.run(f"pip install {lib}", shell=True, check=True)
            print(f"Thư viện {lib} đã được cài đặt thành công.")
        except subprocess.CalledProcessError:
            print(f"Cài đặt thư viện {lib} thất bại.")
    else:
        print(f"Thư viện {lib} đã có sẵn trên hệ thống.")