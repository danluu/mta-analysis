Warning: performnance is very bad without the cpp protobuf implementation.

To get the cpp implementation on Mac, first install the C++ protobuf runtime:

https://github.com/google/protobuf/tree/master/src

~~~
brew install autoconf automake libtool
./autogen.sh
./configure
make
make check
sudo make install
sudo ldconfig
~~~

Then follow the python protobuf instructions. Note that, on Mac, this appears to have at least one bug: https://github.com/google/protobuf/issues/539.

