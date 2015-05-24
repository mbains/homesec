
from emailer import Emailer
from twisted.internet import task
from protocols import FRAME_TYPES
from datetime import datetime



class Pkt_Processor(object):
	def __init__(self, name, emailer = None):
		self._online = False
		self.name = name
		self._connectionAge = 0
		self._short_source = None
		self.email = emailer
		self.loop = task.LoopingCall(self.everySecond)
		self.loop.start(1)

	def handle_message(self, frame):
		self.reset_age()
		if hasattr(frame, 'short_source'):
			self._short_source = frame.short_source;

		if frame.frame_type == FRAME_TYPES['ZigbeeRxPacket']:
			self.handle_motion(frame)



	def handle_error(self, frame):
		if frame.frame_type == FRAME_TYPES['ZigbeeTransmitStatus']:
			if frame.short_dest == self._short_source:
				self.handle_transmit_status(frame)

	def handle_transmit_status(self, frame):
		self.sendMessage("tx message sent", "%s" % frame.__dict__, True)

	def handle_motion(self, pkt):
		print self.name + " got motion"
		self.reset_age()
		self._short_source = pkt.short_source
		self.sendMessage("Motion ", pkt.load, False)

	def handle_undelivered(self, data):
		pass

	def everySecond(self):

		self._connectionAge+=1
		if self._online and self._connectionAge > 20:
			self._online = False
			self.sendMessage("offline", "went offline", True)


	def reset_age(self):
		if not self._online:
			print self.name + " came online"
		self._online = True
		self._connectionAge = 0

	def sendMessage(self, subject, message, critical):
		message = self.name + ": " + message
		now = datetime.now().strftime("%I:%M:%S %p")
		if self.email is not None:
			self.email.sendMail(now, subject, message, critical)
		else:
			print now, message

if __name__ == '__main__':
	from twisted.internet import reactor
	pkt = Pkt_Processor("test", Emailer());
	pkt._online=True
	reactor.run()