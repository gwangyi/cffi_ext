# cffi\_ext

C Definition extractor for cffi

## Example

```python
from cffi import FFI
from cffi_ext import cdef_extract

ffi = FFI()
ffi.set_source("pypci._native", r"#include <pci/pci.h>", libraries=['pci'])

ffi.cdef(cdef_extract(r"""
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef uint64_t u64;

#define PCI_HAVE_Uxx_TYPES
#define PCI_U64_FMT ""
#include <pci/pci.h>
""", cpp_args=["-I/usr/include"]))

ffi.compile(verbose=True)
```
