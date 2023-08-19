# Test Files Explained

### SS & MS
SS - Single Section LAS 3 file  
MS - Multi-Section LAS 3 file

### Good File
This file opens and reads as expected. It has essentially the same structure as a LAS 2 file.

### 0-d Array
These files throw the error 'iteration over a 0-d array' upon opening.

### Reshape Error
These file open but, throw the error 'Cannot reshape ~A data size (X,) into Y columns'. As a result there are errors with the rest of the file.

### Curve-Param Error
These are LAS 3 files with multiple 'Data Section Sets'. It has an empty 'curves' section, although the 'Data Section Sets' are parsed correctly, there needs to be a more generic way of parsing them.

### Curve-Param Unknown
These are LAS 3 files with multiple 'Data Section Sets'. The 'curves' section when parsed produces 'UNKNOWN' mnemonics instead of a blank section.