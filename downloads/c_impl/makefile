
## Copyright (c) 2006 Eli Gildish (netloc@gmail.com). All rights reserved.
##
## Redistribution  and  use in source  and  binary forms,  with or without
## modification,  are permitted provided that the following conditions and
## exceptions are met:
##
## - Redistribution of source code must retain the above copyright notice,
##   this list of conditions and the following disclaimer.
## - Redistributions  in  binary  form  must reproduce the above copyright
##   notice,  this list of conditions  and the following disclaimer in the
##   documentation  and/or other materials provided with the distribution.
## - The name of the author may not be used to endorse or promote products
##   derived from this software without specific prior written permission.
## - Any commercial distribution  or use whatsoever is not allowed without
##   a written permission from the author.
##
## THIS SOFTWARE IS PROVIDED AS IS, AND ANY EXPRESS OR IMPLIED WARRANTIES,
## INCLUDING, BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY
## AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL
## THE AUTHOR BE LIABLE FOR ANY  DIRECT,  INDIRECT,  INCIDENTAL,  SPECIAL,
## EXEMPLARY,  OR  CONSEQUENTIAL DAMAGES  (INCLUDING,  BUT NOT LIMITED TO,
## PROCUREMENT OF SUBSTITUTE  GOODS OR SERVICES;   LOSS OF USE,  DATA,  OR
## PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED  AND  ON  ANY THEORY
## OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
## NEGLIGENCE  OR  OTHERWISE)  ARISING IN  ANY  WAY OUT OF THE USE OF THIS
## SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


SRC_DIR	= ./src
SRC_OBJ	= constant particle formulae heimmass

FOLDERS = $(SRC_DIR)
SOURCES	= $(addsuffix .c, $(addprefix $(SRC_DIR)/,$(SRC_OBJ)))
OBJECTS	= $(addsuffix .o, $(SRC_OBJ))

COM_EXE	= gcc
COM_WAR	= -Wall -Wunused -Wuninitialized -Wparentheses -Wshadow -Winline -Wno-array-bounds
COM_INC	= $(addprefix -I, $(FOLDERS)) -I-
COM_DEF =
COM_OPT	= -ansi -O3 $(COM_WAR) $(COM_INC) $(COM_DEF)
COM_OUT	= heimmass


phoney    :
	    @make -s depend;
	    @make -s source;
	    @./$(COM_OUT);


source	  : $(OBJECTS)
	    @echo '# Producing file: $(COM_OUT)';
	    @$(COM_EXE) -o $(COM_OUT) $(OBJECTS) -lm;
	    @echo '# Executing file: $(COM_OUT)';


depend	  :
	    @echo '# Producing file: mkdepend';
	    @$(COM_EXE) -MM $(COM_INC) $(SOURCES) > mkdepend;


clean	  :
	    @echo '# Deleting files: $(OBJECTS) $(COM_OUT)';
	    @rm -f $(OBJECTS) $(COM_OUT).exe parser.output;

$(OBJECTS):
	    @echo '# Compiling file: $<';
	    @$(COM_EXE) -c $(COM_OPT) $<;

include	mkdepend
