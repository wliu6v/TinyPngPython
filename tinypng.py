import tinify
import sys
import os
import threading
import threadpool
import configparser

keys = []
key_index = 0

lock = threading.Lock()
index = 0
count = 0


def main():
    # check config file
    config = configparser.ConfigParser()
    current_path = os.path.abspath(os.path.dirname(__file__))
    config_file_path = os.path.join(current_path, 'tinypng.ini')
    if not os.path.exists(config_file_path):
        cfgfile = open(config_file_path, 'w')
        config['TinyPngKey'] = {'key': 'YOUR_DEVELOPER_KEY'}
        config.write(cfgfile)
        cfgfile.close()

    config.read(config_file_path)
    key = config['TinyPngKey']['key']

    if key == 'YOUR_DEVELOPER_KEY':
        print('Please write your tinypng api key into tinypng.ini file')
        print('Api key can be created on https://tinypng.com/developers')
        return

    global keys
    keys = key.split(',')

    global count
    if len(sys.argv) == 1:
        print("No input file")
        os.system("pause")
        return

    result_folder = "tinify"
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)

    count = 0
    for i in range(1, len(sys.argv)):
        param = sys.argv[i]
        if os.path.isdir(param):
            for __, __, files in os.walk(param):
                for name in files:
                    if isImage(name):
                        count += 1
        else:
            count += 1
    pool = threadpool.ThreadPool(16)
    print("---- %i images need to compress ----" % count)
    for i in range(1, len(sys.argv)):
        param = sys.argv[i]
        if os.path.isdir(param):
            current_result_folder = os.path.join(os.getcwd(), result_folder, os.path.basename(param))
            if not os.path.exists(current_result_folder):
                os.mkdir(current_result_folder)
            for file in os.listdir(param):
                if isImage(file):
                    file_path = os.path.join(param, file)
                    result = os.path.join(current_result_folder, file)
                    params = [{'file_path': file_path, 'result_path': result, 'file': file}]
                    t = threadpool.makeRequests(compress, params)
                    [pool.putRequest(r) for r in t]
        else:
            result = os.path.join(os.getcwd(), result_folder, os.path.basename(param))
            params = {'file_path': param, 'result_path': result, 'file': os.path.basename(param)}
            compress(params)
    pool.wait()
    print("\n---- Complete ----")
    os.system("pause")


def compress(params):
    global keys, key_index
    file_path = params['file_path']
    result_path = params['result_path']
    tinify.key = keys[key_index]
    source = tinify.from_file(file_path)
    source.to_file(result_path)
    global index, count
    lock.acquire()
    try:
        index += 1
        current = index
        print(">{:3}/{}: {:50s}".format(current, count, params['file']))
    finally:
        lock.release()


def isImage(file_name):
    __, fileSuffix = os.path.splitext(file_name)
    return fileSuffix == '.png' or fileSuffix == '.jpg' or fileSuffix == '.jpeg'


if __name__ == '__main__':
    main()
