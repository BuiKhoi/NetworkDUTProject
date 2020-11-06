from ftplib import FTP

class FTPHandler:
    def __init__(self, ip, user, password):
        self.ip = ip
        self.user = user
        self.password = password
        self.init_fpt_connection()
        self.current_folder = self.get_current_folder()
        self.start_folder = self.current_folder
        
    def init_fpt_connection(self):
        self.ftp_client = FTP(self.ip)
        self.ftp_client.login(user=self.user, passwd = self.password)
        
    def get_current_folder(self):
        return self.ftp_client.pwd()
    
    def open_folder(self, folder):
        self.ftp_client.cwd(folder)
        self.current_folder = self.get_current_folder()
        return self.current_folder
    
    def create_folder(self, folder_name):
        self.ftp_client.mkd(folder_name)
        
    def delete_folder(self, folder_name):
        self.ftp_client.rmd(folder_name)
        
    def delelte_file(self, file_name):
        self.ftp_client.delete(file_name)
        
    def files_list_handler(self, text):
        self.files.append(text)
        
    def get_folder_items(self):
        self.files = []
        self.ftp_client.retrlines('NLST', self.files_list_handler)
        return self.files
        
    def upload_file(self, file_path):
        file_stream = open(file_path, 'rb')
        self.ftp_client.storbinary("{CMD} {FileName}".
               format(CMD="STOR", FileName=file_path.split('/')[-1]),
               file_stream)
        file_stream.close()
    
    def download_file(self, file_name, save_path):
        file_path = save_path + file_name
        file_stream = open(file_path, "wb")
        self.ftp_client.retrbinary('RETR {}'.format(file_name), file_stream.write, 1024)
        file_stream.close()
        
    def reconnect(self):
        self.init_fpt_connection()
        self.open_folder(self.current_folder)

    def close_connection(self):
        self.ftp_client.close()

    def check_root(self):
        return self.get_current_folder() == self.start_folder