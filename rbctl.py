from gi.repository import GObject, Peas
from gi.repository import RB

import gettext
gettext.install('rhythmbox', RB.locale_dir())

from concurrent import futures
import grpc
import rbctl_pb2, rbctl_pb2_grpc

class Service(rbctl_pb2_grpc.RBCtlServicer):
	def __init__(self, player):
		super(Service, self).__init__()
		self.shell_player = player

	# TODO: for all of these, return a result; return err in except
	def _next(self):
		self.shell_player.do_next()

	def _pause(self):
		self.shell_player.pause()

	def _play(self):
		self.shell_player.play()
		
	def _playpause(self):
		self.shell_player.playpause()
	
	def _previous(self):
		self.shell_player.do_previous()
	
	def _seek(self):
		# self.shell_player.set_playing_time(???int? str???)
		pass
	
	def _stop(self):
		self.shell_player.stop()
	
	def Control(self, command, context):
		resp = rbctl_pb2.ControlResponse(success=True)
		
		try:
			if command.type == rbctl_pb2.Command.PLAY:
				self._play()
			elif command.type == rbctl_pb2.Command.PAUSE:
				self._pause()
			elif command.type == rbctl_pb2.Command.PLAY_PAUSE:
				self._playpause()
			elif command.type == rbctl_pb2.Command.NEXT:
				self._next()
			elif command.type == rbctl_pb2.Command.PREVIOUS:
				self._previous()
			else:
				resp.success = False
				resp.message = "Unknown command {}".format(command.type)
		
		except Exception as e:
			resp.success = False
			resp.message = "An exception occurred: {}".format(e)
		
		return resp

class SamplePython(GObject.Object, Peas.Activatable):
	__gtype_name = 'SamplePythonPlugin'
	object = GObject.property(type=GObject.GObject)

	def __init__(self):
		GObject.Object.__init__(self)
			
	def do_activate(self):
		service = Service(self.object.props.shell_player)
		self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
		pt = self.server.add_insecure_port('0.0.0.0:12123')
		rbctl_pb2_grpc.add_RBCtlServicer_to_server(service, self.server)
		self.server.start()

		print("activating sample python plugin")

		shell = self.object
		db = shell.props.db
		model = RB.RhythmDBQueryModel.new_empty(db)
		self.source = GObject.new (PythonSource, shell=shell, name=_("Python Source"), query_model=model)
		self.source.setup()
		group = RB.DisplayPageGroup.get_by_id ("library")
		shell.append_display_page(self.source, group)
	
	def do_deactivate(self):
		print("deactivating sample python plugin")
		self.source.delete_thyself()
		self.source = None
		self.server.stop(0)

class PythonSource(RB.Source):
	def __init__(self, **kwargs):
		super(PythonSource, self).__init__(kwargs)

	def setup(self):
		shell = self.props.shell
		songs = RB.EntryView(db=shell.props.db, shell_player=shell.props.shell_player, is_drag_source=False, is_drag_dest=False)
		songs.append_column(RB.EntryViewColumn.TITLE, True)
		songs.set_model(self.props.query_model)
		songs.show_all()
		self.pack_start(songs, expand=True, fill=True, padding=0)

GObject.type_register(PythonSource)
