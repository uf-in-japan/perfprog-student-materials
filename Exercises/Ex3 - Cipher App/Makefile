RUSTC = rustc
RUST_FLAGS = --crate-type=dylib

SOURCE_FILES = xorcipher.rs
OUTPUT_FILE = libxorcipher.so

libxorcipher.so: ${SOURCE_FILES}
	${RUSTC} ${RUST_FLAGS} -o ${OUTPUT_FILE} ${SOURCE_FILES}

clean:
	rm ${OUTPUT_FILE}
