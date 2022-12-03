import mytelebot_with_not_back
import threading
import update_data
import time
import logging

def main():
    mytelebot_with_not_back.tbot()
    #thr2 = threading.Thread(target = mytelebot_with_not_back.tbot, args = ())
    #tbt = threading.Thread(target = update_data.main, args = ())
    #thr2.start()
#mytelebot_with_not_back.tbot()
    #tbt.start()

if __name__ == "__main__":
    main()
