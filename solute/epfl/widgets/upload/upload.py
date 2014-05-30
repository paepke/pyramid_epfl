# -*- coding: utf-8 -*-

import os
import string
import uuid

import magic

from pyramid.view import view_config
from pyramid.response import Response

from solute.epfl import json

from solute.epfl.core import epflwidgetbase, epflfieldbase

class UploadWidget(epflwidgetbase.WidgetBase):

    """ A powerfull upload widget to upload multiple or single files.

    """

    name = "upload"
    template_name = "upload/upload.html"
    asset_spec = "solute.epfl.widgets:upload/static"

    js_name = ["jquery.iframe-transport.js", "jquery.fileupload.js", "upload.js"]
    css_name = ""

    param_def = {"multiple": (bool, False),                                         # multiple = true, you can upload multiple files at once
                 "preview_width": (epflwidgetbase.OptionalIntType, 300),            # width of the preview, if file is an image
                 "preview_height": (epflwidgetbase.OptionalIntType, None)}          # height of preview, if file is an image

    @classmethod
    def add_pyramid_routes(cls, config):
        super(UploadWidget, cls).add_pyramid_routes(config)

        def upload_preview(request):
            persisted_id = request.matchdict["id"]
            fuob = FileUploadObject().from_persisted_id(request, persisted_id)
            data = fuob.get_data(request)
            if data:
                return Response(status = "200 OK", 
                                body = data, 
                                content_type = str(fuob.mime_type))
            else:
                return Response(status = "404 NOT FOUND", 
                                body = "Preview not found.")


        config.add_route(name = 'epfl/widgets/upload/preview', pattern = '/epfl/upload/preview/{id}') 
        config.add_view(upload_preview, route_name = "epfl/widgets/upload/preview")


    def update_data_source(self, data_source):

        if self.field.data:
            fuob = self.field.data
            data_source.preview_url = fuob.get_preview_url(self.request)
        else:
            data_source.preview_url = None

    def handle_UploadFile(self):
        """ This is called whenever a user uploads a file. """

        fuob = FileUploadObject().from_upload(self.request, self.field)
        self.field.data = fuob

        upload_info = {"preview_url": fuob.get_preview_url(self.request),
                       "preview_height": self.params["preview_height"],
                       "preview_width": self.params["preview_width"],
                       }

        self.form.return_ajax_response(upload_info)




class FileUploadObject(object):
    """ A smart object, that is the value of this upload-field.
    It has a "state" which can be:
    - as file: when the client uploads the file to the server a file-object is stored in this FileUploadObject
    - in data: when the framework needs the data of this file
    - persisted: when the framework needs to pickle the session/transaction/server-side-state only a uuid
                 pointing to the data is stored here
    The states are managed transparently. So you can call "get_data()" to get the data and the object is
    transfered in the needed state.
    When pickling the object it is transfered to "persisted" by the __getstate__-method.
    """

    def __init__(self):
        self.request = None
        self.persisted_id = None
        self.file_obj = None
        self.data = None
        self.file_name = None
        self.file_extension = None
        self.mime_type = None

    def __repr__(self):
        state = "empty"
        if self.persisted_id is not None:
            state = "persisted"
        elif self.data is not None:
            state = "in data"
        elif self.file_obj is not None:
            state = "as file"
        return "<FileUploadObject {name} ({mime_type}) at {id} {state}>".format(id = id(self), 
                                                                                state = state, 
                                                                                name = self.file_name,
                                                                                mime_type = self.mime_type)
    def from_upload(self, request, field_obj):
        """ called when uploaded file arrives at server """

        self.request = request
        page_request = field_obj.form.page_request

        if field_obj.name not in page_request.get_uploads():
            return self

        upload = page_request.get_uploads()[field_obj.name]

        filename = upload.filename.replace("\\", "/")

        self.file_obj = upload.file
        self.mime_type = upload.type
        self.file_extension = os.path.splitext(filename)[-1]
        self.file_name = filename.split("/")[-1]

        return self

    def from_persisted_id(self, request, persisted_id):
        """ called e.g. at preview time. """

        self.request = request
        self.persisted_id = persisted_id

        try:
            meta = json.loads(request.get_epfl_temp_blob(self.persisted_id + "_meta"))
            self.mime_type = meta["mime_type"]
            self.file_extension = meta["ext"]
            self.file_name = meta["name"]
        except:
            self.persisted_id = None

        return self

    def from_file(self, request, file_name):
        """ called e.g. to set the data of an upload-field at form-data-filling-time """

        f = open(file_name, "rb")
        data = f.read()
        f.close()

        return self.from_data(request, data, file_name)

    def from_data(self, request, data, file_name):
        """ called e.g. to set the data of an upload-field at form-data-filling-time """

        mime_guesser = magic.Magic(mime = True)
        file_name = file_name.replace("\\", "/")
        self.data = data
        self.mime_type = mime_guesser.from_buffer(data)
        self.file_extension = os.path.splitext(file_name)[-1]
        self.file_name = file_name.split("/")[-1]

        return self


    def to_data(self, request):
        """ called whenever the data of the file is needed.
        It grabs it from wherever the data currently is.
        """

        if self.data is not None:
            # data already here
            return

        if self.file_obj:
            # it's still a file, go and read it
            self.data = self.file_obj.read()
            self.file_obj.close()
            self.file_obj = None
            return

        if self.persisted_id is not None:
            # it's already temp-blob, fetch it
            try:
                self.data = request.get_epfl_temp_blob(self.persisted_id)
                meta = json.loads(request.get_epfl_temp_blob(self.persisted_id + "_meta"))
                self.mime_type = meta["mime_type"]
                self.file_extension = meta["ext"]
                self.file_name = meta["name"]
            except:
                raise
                self.persisted_id = None
                self.data = None
            return

    def to_temp_blob(self, request):
        if self.persisted_id is not None:
            # already blobbed
            return

        self.to_data(request)

        self.persisted_id = str(uuid.uuid4())

        meta_data = {"mime_type": self.mime_type,
                     "ext": self.file_extension,
                     "name": self.file_name}

        request.set_epfl_temp_blob(self.persisted_id, self.data)
        request.set_epfl_temp_blob(self.persisted_id + "_meta", json.dumps(meta_data))

    def get_data(self, request):
        self.to_data(request)
        return self.data

    def get_preview_url(self, request):
        self.to_temp_blob(request)
        return request.route_url("epfl/widgets/upload/preview", id = self.persisted_id)


    def __getstate__(self):
        """ called before pickeling """
        if self.persisted_id is None:
            self.to_data(self.request)
            self.to_temp_blob(self.request)

        self.request = None
        self.file_obj = None
        self.data = None

        return self.__dict__


class Upload(epflfieldbase.FieldBase): 
    widget_class = UploadWidget

    FileUploadObject = FileUploadObject # to access the this class from a component

    def setup_type(self):
        # do not touch coerce_func here

        self.coerce_error_msg = "txt_value_must_be_file_upload_object"
        self.coerce_func = self._coerce_func


    def _coerce_func(self, value):
        # we have "real" FileUploadObject here
        if not isinstance(value, FileUploadObject):
            raise TypeError, "FileUploadObject needed as value of Upload-Field, got " + repr(type(value))            
        return value


