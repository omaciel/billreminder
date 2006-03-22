LIBS=-pkg:glade-sharp-2.0 -pkg:gtk-sharp-2.0

EXAMPLES=			\
	billreminder.exe

all: $(EXAMPLES)

billreminder.exe: BillReminder.cs
	mcs -warn:4 -out:$@ $< $(LIBS)

.PHONY: all
