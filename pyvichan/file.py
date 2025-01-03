# brand new class to handle 8chan/vichan's multiple files per post
# supersedes py4chan's file generators in Thread and Post

from .url import Url
from base64 import b64decode
from binascii import hexlify

class File(object):
    """ Represents File objects and their thumbnails.
    
    Constructor:
        post (pyvichan.Post) - parent Post object.
        data (dict) - The post or extra_files dict from the 8chan API.
    
    Attributes:
        file_md5 (string): MD5 hash of the file attached to this post.
        file_md5_hex (string): Hex-encoded MD5 hash of the file attached to this post.
        filename (string): Original name of the file attached to this post.
        file_url (string): URL of the file attached to this post.
        file_extension (string): Extension of the file attached to this post. Eg: ``png``, ``webm``, etc.
        file_size (int): Size of the file attached to this post.
        file_width (int): Width of the file attached to this post.
        file_height (int): Height of the file attached to this post.
        thumbnail_width (int): Width of the thumbnail attached to this post.
        thumbnail_height (int): Height of the thumbnail attached to this post.
        thumbnail_fname (string): Filename of the thumbnail attached to this post.
        thumbnail_url (string): URL of the thumbnail attached to this post.
    """
    
    def __init__(self, post, data):
        self._post = post
        self._data = data
        self._url = Url(board=self._post._thread._board.name, https=self._post._thread._board.https, site_url=self._post._thread._board.site_url)       # vichan URL generator

    @property
    def file_md5(self):
        # Py 2/3 compatible equivalent of:
        #return self._data['md5'].decode('base64')
        # More info: http://stackoverflow.com/a/16033232
        # returns a bytestring
        return b64decode(self._data['md5'])
        
    @property
    def file_md5_hex(self):
        return hexlify(self.file_md5).decode('ascii')

    @property
    def filename(self):
        return '%s%s' % (
            self._data['tim'],
            self._data['ext']
        )

    @property
    def file_url(self):
        return self._url.file_url(
            self._data['tim'],
            self._data['ext']
        )

    @property
    def file_extension(self):
        return self._data.get('ext')

    @property
    def file_size(self):
        return self._data.get('fsize')

    @property
    def file_width(self):
        return self._data.get('w')

    @property
    def file_height(self):
        return self._data.get('h')

    # (May Change) 8chan/vichan does not inform you of deleted files
    @property
    def file_deleted(self):
        raise AttributeError("'pyvichan.File' object has no attribute 'file_deleted'")

    @property
    def thumbnail_width(self):
        return self._data.get('tn_w')

    @property
    def thumbnail_height(self):
        return self._data.get('tn_h')

    @property
    def thumbnail_fname(self):
        return '%ss.jpg' % (
            self._data['tim']
        )

    @property
    def thumbnail_url(self):
        board = self._post._thread._board
        return self._url.thumb_url(
            self._data['tim']
        )

    def file_request(self):
        return self._post._thread._board._requests_session.get(self.file_url)

    def thumbnail_request(self):
        return self._post._thread._board._requests_session.get(self.thumbnail_url)
        
    def __repr__(self):
        return '<File %s from Post /%s/%i#%i>' % (
            self.filename,
            self._post._thread._board.name,
            self._post._thread.id,
            self._post.post_number
        )
