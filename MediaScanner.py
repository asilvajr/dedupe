



class MediaScanner:
    def __init__(self, media_type, accepted_types):
        self.media_type = media_type
        self.accepted_types = accepted_types


class VideoScanner(MediaScanner):
    def __init__(self):
        MediaScanner.__init__(self,"Video",)
        self.media_type = "Video"
        self.accepted_types = ['ts','mp4','flv','avc','wmv','av1','h.265','mpg','mpeg']


class PhotoScanner(MediaScanner):
    def __init__(self):
        MediaScanner.__init__(self,"Photo")
        self.accepted_types = ['jpg','png','gif','tiff','RAW']

