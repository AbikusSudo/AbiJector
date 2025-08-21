import ctypes
import os
import psutil
import logging
import time

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

class AbiJector:
    def __init__(self, target_process: str, dll_path: str):
        self.target_process = target_process
        self.dll_path = os.path.abspath(dll_path)
        self.process_handle = None
        self.pid = None
        self.thread_id = None
        logging.info(f"Initialized injector for {self.target_process} with DLL {self.dll_path}")

    def _get_pid(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == self.target_process.lower():
                self.pid = proc.info['pid']
                logging.info(f"Found process {self.target_process} (PID: {self.pid})")
                return self.pid
        raise Exception(f"Process {self.target_process} not found")

    def _open_process(self):
        PROCESS_ALL_ACCESS = 0x1F0FFF
        self.process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, self.pid)
        if not self.process_handle:
            raise Exception("Failed to obtain process handle")
        logging.info(f"Process handle opened (PID: {self.pid})")

    def _allocate_memory(self):
        dll_bytes = self.dll_path.encode('utf-8')
        arg_address = ctypes.windll.kernel32.VirtualAllocEx(
            self.process_handle, None, len(dll_bytes), 0x3000, 0x40
        )
        if not arg_address:
            raise Exception("Failed to allocate memory in target process")
        ctypes.windll.kernel32.WriteProcessMemory(
            self.process_handle, arg_address, dll_bytes, len(dll_bytes), None
        )
        logging.info(f"Allocated memory and wrote DLL path at {hex(arg_address)}")
        return arg_address

    def _create_remote_thread(self, arg_address):
        h_kernel32 = ctypes.windll.kernel32.GetModuleHandleW("kernel32.dll")
        h_loadlib = ctypes.windll.kernel32.GetProcAddress(h_kernel32, b"LoadLibraryA")
        self.thread_id = ctypes.c_ulong(0)
        if not ctypes.windll.kernel32.CreateRemoteThread(
            self.process_handle, None, 0, h_loadlib, arg_address, 0, ctypes.byref(self.thread_id)
        ):
            raise Exception("Failed to create remote thread")
        logging.info(f"Remote thread created (TID: {self.thread_id.value})")

    def inject(self):
        self._get_pid()
        self._open_process()
        arg_address = self._allocate_memory()
        self._create_remote_thread(arg_address)
        ctypes.windll.kernel32.CloseHandle(self.process_handle)
        logging.info(f"[+] DLL injected into {self.target_process} (PID: {self.pid})")

    def is_process_running(self):
        return psutil.pid_exists(self.pid)

    def wait_for_process(self, timeout=30):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                self._get_pid()
                logging.info(f"Process {self.target_process} started (PID: {self.pid})")
                return True
            except Exception:
                time.sleep(0.5)
        raise TimeoutError(f"Process {self.target_process} did not start within {timeout} seconds")

    def inject_when_ready(self, timeout=30):
        self.wait_for_process(timeout)
        self.inject()