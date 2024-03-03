import speedtest
import __main__

def RunSpeedtest(command):
    if command[0] == "speedtest":
        st = speedtest.Speedtest()
        print(st.download())
        print(st.upload())


__main__.system_commands.append(RunSpeedtest)
print("SpeedTest module loaded")
