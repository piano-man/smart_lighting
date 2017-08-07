def read_from_arduino():
	from urllib.parse import urlencode
	from urllib.request import Request, urlopen
	from serial import Serial
	import requests, time
	serial_port = Serial('/dev/ttyACM0', 9600,timeout=2)
	time.sleep(1)
	counter = 0
	while True:
		try:
			received = (str(serial_port.readline())[2:-5]).split()
			if len(received) < 2:
				continue
			try:
				id, intensity = map(int, received)
				print('id = %d intensity = %d' % (id, intensity))
				if counter == 0:
					url = 'http://172.20.43.63:5000/intensity'
					post_fields = {'intensity': str(intensity), 'module_no': str(id), 'pi_token': "test12345"}
					request = Request(url, urlencode(post_fields).encode())
					r= requests.post(url,json=post_fields)
					print(r)
				counter = (counter + 1) % 20
			except ValueError:
				continue
		except BlockingIOError:
			print('NO DATA RECEIVED')

def main():
	read_from_arduino()

if __name__ == '__main__':
	main()
	
