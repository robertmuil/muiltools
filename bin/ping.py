import subprocess

def do_ping(host, num=4):
	ping = subprocess.Popen(
			["ping", "-c", "%d"%(num), host],
			stdout = subprocess.PIPE,
			stderr = subprocess.PIPE
	)

	out, error = ping.communicate()
	return out, error

if __name__ == '__main__':
	out,err = do_ping('www.google.com')
	print out
