from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import simplejson
import random
from os import curdir, sep
import os.path
from time import gmtime, strftime
from datetime import datetime, date, time
import json

def touchopen(filename, *args, **kwargs):
    # Open the file in R/W and create if it doesn't exist. *Don't* pass O_TRUNC
    fd = os.open(filename, os.O_RDWR | os.O_CREAT)

    # Encapsulate the low-level file descriptor in a python file object
    return os.fdopen(fd, *args, **kwargs)


class S(BaseHTTPRequestHandler):
    def _saveToFile(self, option):
        fileName = datetime.now().strftime("%Y-%m") + '/' + datetime.now().strftime("%Y-%m-%d") + '.json'
        fileNameLog = datetime.now().strftime("%Y-%m") + '/input.log'
        #isoDate = datetime.now().isocalendar()
        #fileName = str(isoDate[0]) + '_' + str(isoDate[1]) + '.json'
#        print(fileName)
        #print( datetime.now().isoformat(' ') )
        opt = option[8:]
        print ("Option sent is:", opt)
        
        os.makedirs(os.path.dirname(fileName), exist_ok=True)
#        with open(fileName, "r+") as f:

        # Open an existing file or create if it doesn't exist
        with touchopen(fileName, "r+") as f:

            # Acquire a non-blocking exclusive lock
            #fcntl.lockf(f, fcntl.LOCK_EX)

            # Read any previous value if present
            try:
                data = json.load(f)
                print(data)
            except ValueError as e:
                #print(e)
                print('No valid JSON found.')
                data = json.loads('{"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}')
           
            if(opt=='1'):
                car = data["1"]
                print(car)
                data["1"] = car+1
            if(opt=='2'):
                log = data["2"]
                print(log)
                data["2"] = log+1
            if(opt=='3'):
                log = data["3"]
                print(log)
                data["3"] = log+1
            if(opt=='4'):
                log = data["4"]
                print(log)
                data["4"] = log+1
            if(opt=='5'):
                log = data["5"]
                print(log)
                data["5"] = log+1

            # Write the new value and truncate
            f.seek(0)
            json.dump(data, f)
            f.truncate()

        # with open(fileName, 'a+') as f:
            # f.seek(0)
            # try:
                # data = json.load(f)
                # print(data)
            # except ValueError as e:
                # #print(e)
                # print('No valid JSON found.')
                # data = json.loads('{"Walk": 0, "Public transportation": 0, "Bike": 0, "E-car": 0, "Car": 0}')
           
            # if(opt=='car'):
                # car = data["Car"]
                # print(car)
                # data["Car"] = car+1
                
            # f.seek(0)
            # json.dump(data, f)
            # f.truncate()
            
        with open(fileNameLog, "a+") as outfile:
            outfile.write(datetime.now().isoformat(' ') + ';' + option[8:]+'\n')

            
    def _set_plain_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _set_json_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _set_js_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/javascript')
        self.end_headers()

    def _set_png_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()

    def _set_css_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/css')
        self.end_headers()

    def do_GET(self):
        #print ("in do_GET")
        option = self.path
#        print ("path: ", option)
        if 'option=' in option:
            self.send_error(404)
            self._saveToFile(option)
        elif 'opt=' in option:
            self.send_response(200)
            self.end_headers()
            self._saveToFile(option)
            self.flush_headers()
        elif option.startswith("/time"):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#            print(now)
            self._set_headers()
            self.wfile.write(now.encode())
#            self.wfile.close()
        else:
            try:
                with open(curdir + sep + self.path, 'rb') as f:
                    if option.endswith(".js"):
                        self._set_js_headers()
                    elif option.endswith(".css"):
                        self._set_css_headers()
                    elif option.endswith(".json"):
                        self._set_json_headers()
                    elif option.endswith(".html"):
                        self._set_headers()
                    elif option.endswith(".log"):
                        self._set_plain_headers()
                    elif option.endswith(".png"):
                        self._set_png_headers()
                    self.wfile.write(f.read())
            except IOError as e:
                self.send_error(404)
                
        return

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        print ("in post method")
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        self.send_response(200)
        self.end_headers()

        data = self.data_string
        with open("input.log", "ab") as outfile:
            outfile.write(data)
        outfile.close()
        #print ("{}".format(data))
        return
        

def run(server_class=HTTPServer, handler_class=S, port=8888):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    httpd.serve_forever()

run()