"""Provides prototypes for each function and data structure defined in
libpndman.h."""

import ctypes as c
from ctypes.util import find_library
time_t = c.c_long # FIXME: System dependent, but I don't know what it is where.

# Preload necessary libraries.
c.CDLL(find_library('expat'), mode=c.RTLD_GLOBAL)
c.CDLL(find_library('curl'), mode=c.RTLD_GLOBAL)
c.CDLL(find_library('jansson'), mode=c.RTLD_GLOBAL)

# FIXME: Replace with find_library to be more cross-platform.
p = c.CDLL('libpndman.so')


# Defined string lengths.
# FIXME: These two are system dependent.  Values here are for my Linux desktop.
s_PATH_MAX = c.c_char * 4096
s_LINE_MAX = c.c_char * 2048

s_PND_ID = c.c_char * 256
s_PND_NAME = c.c_char * 24
s_PND_VER = c.c_char * 8
s_PND_STR = s_LINE_MAX
s_PND_SHRT_STR = c.c_char * 24
s_PND_MD5 = c.c_char * 33
s_PND_INFO = s_LINE_MAX
s_PND_PATH = s_PATH_MAX
s_REPO_URL = s_LINE_MAX
s_REPO_NAME = c.c_char * 24
s_REPO_VERSION = c.c_char * 8
s_HANDLE_NAME = s_PND_ID


# Enums.

sync_flags = c.c_int
SYNC_FULL = 0x001

handle_flags = c.c_int
HANDLE_INSTALL = 0x001
HANDLE_REMOVE = 0x002
HANDLE_FORCE = 0x004
HANDLE_INSTALL_DESKTOP = 0x008
HANDLE_INSTALL_MENU = 0x010
HANDLE_INSTALL_APPS = 0x020

version_type = c.c_int
PND_VERSION_RELEASE = 0
PND_VERSION_BETA = 1
PND_VERSION_ALPHA = 2

exec_x11 = c.c_int
PND_EXEC_REQ = 0
PND_EXEC_STOP = 1
PND_EXEC_IGNORE = 2


# Structs.
class version(c.Structure):
    _fields_ = [
        ('major', s_PND_VER),
        ('minor', s_PND_VER),
        ('release', s_PND_VER),
        ('build', s_PND_VER),
        ('type', version_type),
    ]

class exec_(c.Structure): # exec is a Python keyword; therefore, exec_.
    _fields_ = [
        ('background', c.c_int),
        ('startdir', s_PND_PATH),
        ('standalone', c.c_int),
        ('command', s_PND_PATH),
        ('arguments', s_PND_PATH),
        ('x11', exec_x11),
    ]

class author(c.Structure):
    _fields_ = [
        ('name', s_PND_NAME),
        ('website', s_PND_STR),
        ('email', s_PND_STR),
    ]

class info(c.Structure):
    _fields_ = [
        ('name', s_PND_NAME),
        ('type', s_PND_SHRT_STR),
        ('src', s_PND_STR),
    ]

class translated(c.Structure): pass
translated_p = c.POINTER(translated)
translated._fields = [
    ('lang', s_PND_SHRT_STR),
    ('string', s_PND_STR),
    ('next', translated_p),
]

class license(c.Structure): pass
license_p = c.POINTER(license)
license._fields = [
    ('name', s_PND_STR),
    ('url', s_PND_STR),
    ('sourcecodeurl', s_PND_STR),
    ('next', license_p),
]

class previewpic(c.Structure): pass
previewpic_p = c.POINTER(previewpic)
previewpic._fields_ = [
    ('src', s_PND_PATH),
    ('next', previewpic_p),
]

class association(c.Structure): pass
association_p = c.POINTER(association)
association._fields_ = [
    ('name', s_PND_STR),
    ('filetype', s_PND_SHRT_STR),
    ('exec', s_PND_PATH),
    ('next', association_p),
]

class category(c.Structure): pass
category_p = c.POINTER(category)
category._fields_ = [
    ('main', s_PND_SHRT_STR),
    ('sub', s_PND_SHRT_STR),
    ('next', category_p),
]

class application(c.Structure): pass
application_p = c.POINTER(application)
application._fields_ = [
    ('id', s_PND_ID),
    ('appdata', s_PND_PATH),
    ('icon', s_PND_PATH),
    ('frequency', c.c_int),

    ('author', author),
    ('osversion', version),
    ('version', version),
    ('exec', exec_),
    ('info', info),

    ('title', translated_p),
    ('description', translated_p),
    ('license', license_p),
    ('previewpic', previewpic_p),
    ('category', category_p),
    ('association', association_p),

    ('next', application_p),
]

class package(c.Structure): pass
package_p = c.POINTER(package)
package._fields_ = [
    ('path', s_PND_PATH),
    ('id', s_PND_ID),
    ('icon', s_PND_PATH),
    ('info', s_PND_INFO),
    ('md5', s_PND_MD5),
    ('url', s_PND_STR),
    ('vendor', s_PND_NAME),
    ('size', c.c_size_t),
    ('modified_time', time_t),
    ('rating', c.c_int),

    ('author', author),
    ('version', version),
    ('app', application_p),

    ('title', translated_p),
    ('description', translated_p),
    ('license', license_p),
    ('previewpic', previewpic_p),
    ('category', category_p),

    ('repository', s_PND_STR),
    ('mount', s_PND_PATH),
    ('update', package_p),
    ('next_installed', package_p),
    ('next', package_p),
]

class repository(c.Structure): pass
repository_p = c.POINTER(repository)
repository._fields_ = [
    ('url', s_REPO_URL),
    ('name', s_REPO_NAME),
    ('updates', s_REPO_URL),
    ('version', s_REPO_VERSION),
    ('timestamp', time_t),

    ('pnd', package_p),
    ('next', repository_p), ('prev', repository_p),
]

class device(c.Structure): pass
device_p = c.POINTER(device)
device._fields_ = [
    ('mount', s_PATH_MAX),
    ('device', s_PATH_MAX),
    ('size', c.c_size_t), ('free', c.c_size_t), ('available', c.c_size_t),

    ('appdata', s_PATH_MAX),
    ('next', device_p), ('prev', device_p),
]

class curl_write_result(c.Structure):
    _fields_ = [
        ('data', c.c_void_p),
        ('pos', c.c_int),
    ]

class curl_request(c.Structure):
    _fields_ = [
        ('result', curl_write_result),
        ('curl', c.c_void_p),
    ]

class curl_progress(c.Structure):
    _fields_ = [
        ('download', c.c_double),
        ('total_to_download', c.c_double),
        ('done', c.c_char),
    ]

class handle(c.Structure):
    _fields_ = [
        ('name', s_HANDLE_NAME),
        ('error', s_LINE_MAX),
        ('pnd', package_p),
        ('device', device_p),
        ('flags', c.c_uint),

        ('progress', curl_progress),

        ('request', curl_request),
        ('file', c.c_void_p),
    ]
handle_p = c.POINTER(handle)

class sync_handle(c.Structure):
    _fields_ = [
        ('error', s_LINE_MAX),
        ('repository', repository_p),

        ('flags', c.c_uint),

        ('progress', curl_progress),

        ('file', c.c_void_p),
        ('curl', c.c_void_p),
    ]
sync_handle_p = c.POINTER(sync_handle)


# Functions.

def proto(f, args, res):
    "Helper function to shorten function prototyping to one line."
    f.argtypes = args
    f.restype = res
    return f

git_head = proto(p.pndman_git_head, [], c.c_char_p)
git_commit = proto(p.pndman_git_commit, [], c.c_char_p)
get_md5 = proto(p.pndman_get_md5, [package_p], c.c_char_p)
set_verbose = proto(p.pndman_set_verbose, [c.c_int], None)
get_verbose = proto(p.pndman_get_verbose, [], c.c_int)
get_error = proto(p.pndman_get_error, [], c.c_char_p)

repository_init = proto(p.pndman_repository_init, [], repository_p)
repository_add = proto(p.pndman_repository_add,
                       [c.c_char_p, repository_p], repository_p)
repository_clear = proto(p.pndman_repository_clear, [repository_p], None)
repository_check_local = proto(p.pndman_repository_check_local,
                               [repository_p], None)
repository_free = proto(p.pndman_repository_free, [repository_p], repository_p)
repository_free_all = proto(p.pndman_repository_free_all,
                            [repository_p], c.c_int)

device_add = proto(p.pndman_device_add, [c.c_char_p, device_p], device_p)
device_detect = proto(p.pndman_device_detect, [device_p], device_p)
device_free = proto(p.pndman_device_free, [device_p], device_p)
device_free_all = proto(p.pndman_device_free_all, [device_p], c.c_int)

handle_init = proto(p.pndman_handle_init, [c.c_char_p, handle_p], c.c_int)
handle_perform = proto(p.pndman_handle_perform, [handle_p], c.c_int)
handle_commit = proto(p.pndman_handle_commit,
                      [handle_p, repository_p], c.c_int)
handle_free = proto(p.pndman_handle_free, [handle_p], c.c_int)

download = proto(p.pndman_download, [], c.c_int)
read_from_device = proto(p.pndman_read_from_device,
                         [repository_p, device_p], c.c_int)

sync = proto(p.pndman_sync, [], c.c_int)
sync_request = proto(p.pndman_sync_request,
                     [sync_handle_p, c.c_uint, repository_p], c.c_int)
sync_request = proto(p.pndman_sync_request_free, [sync_handle_p], c.c_int)
commit_all = proto(p.pndman_commit_all, [repository_p, device_p], c.c_int)

crawl = proto(p.pndman_crawl, [c.c_int, device_p, repository_p], c.c_int)
crawl_pnd = proto(p.pndman_crawl_pnd, [c.c_int, package_p], c.c_int)
check_updates = proto(p.pndman_check_updates, [repository_p], c.c_int)
